# Term extraction/translation subcommand (term extract / term translate)

import csv
import json
import os
import sys
from pathlib import Path
from pydantic import BaseModel, Field
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .language import resolve_lang, resolve_langs


class TermList(BaseModel):
    terms: list[str] = Field(
        description="Proper nouns and domain-specific technical terms in the original source language"
    )


class TermPair(BaseModel):
    original: str = Field(description="The term in the source language")
    translation: str = Field(description="The translated term in the target language")


class Glossary(BaseModel):
    glossary: list[TermPair]


# ---------------------------------------------------------------------------
# add_parser
# ---------------------------------------------------------------------------

def add_parser(subparsers):
    term_parser = subparsers.add_parser("term", help="Extract/translate terms")
    term_sub = term_parser.add_subparsers(dest="term_command", metavar="<command>")
    term_sub.required = True
    _add_extract_parser(term_sub)
    _add_translate_parser(term_sub)
    _add_show_parser(term_sub)
    _add_set_parser(term_sub)
    _add_reorder_parser(term_sub)
    _add_merge_parser(term_sub)


def _add_show_parser(subparsers):
    parser = subparsers.add_parser("show", help="Show a TSV filtered by columns/rows")
    parser.add_argument("input_file", metavar="FILE", help="Target TSV file")
    parser.add_argument("-l", "--lang", action="append", metavar="LANG",
                        help="Language column(s) to show (multiple allowed; all columns if omitted)")
    parser.add_argument("-k", "--key", action="append", metavar="KEY",
                        help="Key(s) to show, i.e. values in the first column (multiple allowed; all rows if omitted)")
    parser.set_defaults(func=run_show)


def _add_reorder_parser(subparsers):
    parser = subparsers.add_parser("reorder", help="Reorder TSV columns into the given order")
    parser.add_argument("input_file", metavar="FILE", help="Target TSV file")
    parser.add_argument("-c", "--col", action="append", required=True, metavar="LANG",
                        help="Column name(s) to output (multiple; language name or code)")
    parser.add_argument("-o", "--output", required=True, help="Output TSV file")
    parser.set_defaults(func=run_reorder)


def _add_set_parser(subparsers):
    parser = subparsers.add_parser("set", help="Update a specific TSV cell")
    parser.add_argument("input_file", metavar="FILE", help="Target TSV file")
    parser.add_argument("-k", "--key", required=True, help="Key to change (value in the first column)")
    parser.add_argument("-l", "--lang", required=True, help="Language column name to change")
    parser.add_argument("-v", "--value", required=True, help="New value")
    parser.set_defaults(func=run_set)


def _add_extract_parser(subparsers):
    parser = subparsers.add_parser("extract", help="Extract terms from text and save as JSON")
    parser.add_argument("input_file", help="Text file to translate")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="Source language (e.g. French, English, Japanese)")
    parser.add_argument("-m", "--model", required=True, help="Model to use")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="Term extraction file (JSON)")
    parser.add_argument("--keep", type=int, default=5,
                        help="Chunk size (default: 5)")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"Wait time on retry, in seconds (default: {DEFAULT_RETRY_WAIT_SECONDS}s)")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking (for Qwen3 models)")
    parser.set_defaults(func=run_extract)


def _add_translate_parser(subparsers):
    parser = subparsers.add_parser("translate", help="Translate a term JSON into a TSV (fill-in-the-blanks)")
    parser.add_argument("extract_file", help="Term extraction file (JSON)")
    parser.add_argument("-t", "--to", dest="to_langs", action="append", required=True,
                        metavar="LANG", help="Target language(s) (multiple allowed)")
    parser.add_argument("-m", "--model", required=True, help="Model to use")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="Output TSV file")
    parser.add_argument("-c", "--common", dest="common_file", default=None,
                        help="Common glossary TSV file (matching terms are taken from it, skipping the LLM)")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"Wait time on retry, in seconds (default: {DEFAULT_RETRY_WAIT_SECONDS}s)")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking (for Qwen3 models)")
    parser.set_defaults(func=run_translate)


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def load_entries(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    entries = []
    for line in lines:
        line = line.strip()
        if not line or ":" not in line:
            continue
        speaker, text = line.split(":", 1)
        entries.append((speaker.strip(), text.strip()))
    return entries


def chunk_ranges(total, keep):
    """Return (chunk_index, start, end) for every chunk (1-indexed inclusive)."""
    num = (total + keep - 1) // keep
    for cidx in range(1, num + 1):
        start = (cidx - 1) * keep + 1
        end = min(cidx * keep, total)
        yield cidx, start, end


def _call_translate(client, from_lang, to_lang, terms):
    listing = "\n".join(f"- {t}" for t in terms)
    prompt = (
        f"Translate the following {from_lang} terms into {to_lang}. "
        f"Provide a translation for every term. If a term is a proper noun "
        f"(e.g., person name) that should remain unchanged, output it as-is.\n\n"
        f"Terms:\n{listing}"
    )
    data = client.call_json([prompt], schema=Glossary)
    pairs = data.get("glossary", [])
    original_set = set(terms)
    mapping = {}
    for p in pairs:
        orig = p["original"]
        if orig not in original_set:
            print(f"  WARNING: unexpected term in glossary response '{orig}', ignoring.")
            continue
        mapping[orig] = p["translation"]
    return mapping


def translate_glossary(client, from_lang, to_lang, originals, max_retries=5):
    if not originals:
        return {}
    mapping = _call_translate(client, from_lang, to_lang, originals)
    missing = [t for t in originals if t not in mapping]
    for attempt in range(max_retries):
        if not missing:
            break
        print(f"  Retrying {len(missing)} missing term(s) (attempt {attempt + 1}/{max_retries})...")
        retry_mapping = _call_translate(client, from_lang, to_lang, missing)
        mapping.update(retry_mapping)
        missing = [t for t in missing if t not in mapping]
    for term in missing:
        print(f"  WARNING: no translation for '{term}' after {max_retries} retries, using empty string.")
        mapping[term] = ""
    return mapping


# ---------------------------------------------------------------------------
# term extract
# ---------------------------------------------------------------------------

def extract_terms(client, from_lang, chunk_text):
    prompt = (
        f"Extract proper nouns and domain-specific technical terms from the following "
        f"{from_lang} text. Return them in the original {from_lang} form (do NOT translate).\n\n"
        f"Include:\n"
        f"- Person names, place names, organization names\n"
        f"- Work titles, product names, brand names\n"
        f"- Domain-specific technical terms and jargon\n\n"
        f"Exclude:\n"
        f"- Common everyday words and general vocabulary\n"
        f"- Pronouns, articles, conjunctions, prepositions\n"
        f"- Speaking styles or expressions\n\n"
        f"Output each term in its base form WITHOUT leading articles "
        f"(e.g., output 'affinage', not 'l'affinage' or 'le affinage').\n\n"
        f"Text:\n{chunk_text}"
    )
    data = client.call_json([prompt], schema=TermList)
    return data.get("terms", [])


def run_extract(args):
    args.from_lang = resolve_lang(args.from_lang)
    if os.path.exists(args.output_file):
        print(f"Term extraction file already exists (skipping): {args.output_file}")
        return

    entries = load_entries(args.input_file)
    total = len(entries)
    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )
    chunks = list(chunk_ranges(total, args.keep))
    print(f"Starting term extraction: {len(chunks)} chunk(s) (keep={args.keep})")
    chunk_terms_map = {}
    for cidx, start, end in chunks:
        chunk_text = "\n".join(f"{sp}: {tx}" for sp, tx in entries[start - 1:end])
        print(f"[Extract chunk {cidx}: lines {start}-{end}]")
        terms = extract_terms(client, args.from_lang, chunk_text)
        chunk_terms_map[cidx] = {"start": start, "end": end, "terms": terms}

    data = {
        "from": args.from_lang,
        "chunks": [
            {"index": cidx, "start": info["start"], "end": info["end"],
             "terms": info["terms"]}
            for cidx, info in sorted(chunk_terms_map.items())
        ],
    }
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved term extraction file: {args.output_file}")


# ---------------------------------------------------------------------------
# term translate
# ---------------------------------------------------------------------------

def load_tsv(path):
    """Load a TSV and return (header, rows). rows is a list of {lang: value} dicts."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        rows = [dict(zip(header, row)) for row in reader]
    return header, rows


def save_tsv(path, header, rows):
    """Save (header, rows) as a TSV."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        for row in rows:
            writer.writerow([row.get(col, "") for col in header])


def run_translate(args):
    args.to_langs = resolve_langs(args.to_langs)
    # Load from.json
    with open(args.extract_file, "r", encoding="utf-8") as f:
        extract_data = json.load(f)
    from_lang = extract_data["from"]

    # Build the unique term list, preserving order
    seen = set()
    unique_terms = []
    for chunk in extract_data.get("chunks", []):
        for t in chunk["terms"]:
            if t not in seen:
                seen.add(t)
                unique_terms.append(t)

    # Open the TSV, or create a new one
    if os.path.exists(args.output_file):
        header, rows = load_tsv(args.output_file)
        # Check that from_lang matches
        if header[0] != from_lang:
            print(f"WARNING: TSV source column '{header[0]}' differs from from.json's '{from_lang}'.")
        # Keep rows not present in unique_terms while appending new terms at the end
        existing = {row[from_lang]: row for row in rows if from_lang in row}
        rows = []
        for t in unique_terms:
            rows.append(existing.get(t, {from_lang: t}))
    else:
        header = [from_lang]
        rows = [{from_lang: t} for t in unique_terms]

    # Add the new to_lang column(s) to the header
    for to_lang in args.to_langs:
        if to_lang not in header:
            header.append(to_lang)

    # Load the common glossary: {term: {lang: translation}}
    common = {}
    if args.common_file and os.path.exists(args.common_file):
        common_header, common_rows = load_tsv(args.common_file)
        if from_lang not in common_header:
            print(f"WARNING: common glossary has no '{from_lang}' column. Skipping.")
        else:
            for row in common_rows:
                term = row.get(from_lang, "")
                if term:
                    common[term] = row

    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    # Fill in the blanks per language
    for to_lang in args.to_langs:
        missing_terms = [row[from_lang] for row in rows if not row.get(to_lang)]
        if not missing_terms:
            print(f"[{to_lang}] All terms already translated (skipping)")
            continue

        # Fill in from the common glossary first
        from_common = []
        need_llm = []
        for term in missing_terms:
            if term in common and common[term].get(to_lang):
                from_common.append(term)
            else:
                need_llm.append(term)
        if from_common:
            print(f"  Taken from common glossary: {len(from_common)}")
            for row in rows:
                if not row.get(to_lang) and row[from_lang] in common:
                    val = common[row[from_lang]].get(to_lang, "")
                    if val:
                        row[to_lang] = val

        if not need_llm:
            save_tsv(args.output_file, header, rows)
            print(f"  Saved: {args.output_file}")
            continue

        print(f"[Translating {len(need_llm)} term(s) → {to_lang}]")
        mapping = translate_glossary(client, from_lang, to_lang, need_llm)
        for row in rows:
            if not row.get(to_lang):
                term = row[from_lang]
                if term in mapping:
                    row[to_lang] = mapping[term]
        # Save per language (resumable if interrupted)
        save_tsv(args.output_file, header, rows)
        print(f"  Saved: {args.output_file}")


# ---------------------------------------------------------------------------
# term show / term set
# ---------------------------------------------------------------------------

def run_show(args):
    if args.lang:
        args.lang = resolve_langs(args.lang)
    header, rows = load_tsv(args.input_file)
    key_col = header[0]

    if args.lang:
        cols = [key_col]
        for lang in args.lang:
            if lang not in header:
                print(f"Warning: column '{lang}' not found", file=sys.stderr)
            else:
                cols.append(lang)
    else:
        cols = header

    if args.key:
        key_set = set(args.key)
        rows = [r for r in rows if r.get(key_col) in key_set]

    writer = csv.writer(sys.stdout, delimiter="\t")
    writer.writerow(cols)
    for row in rows:
        writer.writerow([row.get(c, "") for c in cols])


def run_set(args):
    args.lang = resolve_lang(args.lang)
    header, rows = load_tsv(args.input_file)
    key_col = header[0]

    if args.lang not in header:
        print(f"Error: column '{args.lang}' not found", file=sys.stderr)
        sys.exit(1)

    updated = False
    for row in rows:
        if row.get(key_col) == args.key:
            row[args.lang] = args.value
            updated = True
            break

    if not updated:
        print(f"Error: key '{args.key}' not found", file=sys.stderr)
        sys.exit(1)

    save_tsv(args.input_file, header, rows)
    print(f"Updated: {args.key!r} [{args.lang}] = {args.value!r}")


def _add_merge_parser(subparsers):
    parser = subparsers.add_parser("merge", help="Merge multiple TSVs by column (later files overwrite cell by cell)")
    parser.add_argument("input_files", metavar="FILE", nargs="+", help="Input TSV files (multiple)")
    parser.add_argument("-o", "--output", required=True, help="Output TSV file")
    parser.set_defaults(func=run_merge)


def run_merge(args):
    header = []
    rows = {}  # key -> {col: value}
    key_order = []

    for path in args.input_files:
        file_header, file_rows = load_tsv(path)
        if not file_header:
            continue
        key_col = file_header[0]
        for col in file_header:
            if col not in header:
                header.append(col)
        for row in file_rows:
            key = row.get(key_col, "")
            if key not in rows:
                rows[key] = {}
                key_order.append(key)
            for col, val in row.items():
                if val:
                    rows[key][col] = val

    merged_rows = [rows[k] for k in key_order]
    save_tsv(args.output, header, merged_rows)
    print(f"Saved: {args.output} ({len(merged_rows)} rows, {len(header)} columns)")


def run_reorder(args):
    args.col = resolve_langs(args.col)
    header, rows = load_tsv(args.input_file)
    for col in args.col:
        if col not in header:
            print(f"Warning: column '{col}' not present in the input file (added as an empty column)", file=sys.stderr)
    save_tsv(args.output, args.col, rows)
    print(f"Saved: {args.output}")
