# Subcommand that summarizes per-language trends from evaluation logs
# Merges 3 evaluation results and passes them to the LLM to generate a sentence
# that can be pasted into the README's "Trend Analysis" column.
# Intermediate results are appended to a JSONL, so only unprocessed languages
# need to be redone if interrupted.

import json
from pathlib import Path
from .aggregate import find_evaluation_groups, load_evaluation_data, calculate_statistics
from .language import LANGUAGES, LANG_NAMES
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .statusline import StatusLine

CRITERIA = [
    "readability",
    "fluency",
    "terminology",
    "contextual_adaptation",
    "information_completeness",
]

# Header row identifying the target table to sync (per language)
TABLE_HEADERS = {
    "en": "| Language | Score | Trend Analysis |",
    "ja": "| 言語 | スコア | 傾向の分析 |",
}
TABLE_SEPARATOR = "| --- | ---: | --- |"


def add_parser(subparsers):
    parser = subparsers.add_parser("trend", help="Summarize per-language trends from evaluation logs")
    parser.add_argument("files", nargs="*", help="Evaluation result JSON files (multiple allowed)")
    parser.add_argument("-m", "--model", default=None,
                        help="Model used for summarization (not needed with --render-only)")
    parser.add_argument("-o", "--output", dest="output_file", default="TRENDS.jsonl",
                        help="Intermediate result JSONL (default: TRENDS.jsonl)")
    parser.add_argument("--sync", default=None,
                        help="Path of the README.md to write the table back into after generation")
    parser.add_argument("--render-only", action="store_true",
                        help="Only output/sync the table from the JSONL, without generating")
    parser.add_argument("--no-think", action="store_true", help="Disable thinking")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"Wait time on retry, in seconds (default: {DEFAULT_RETRY_WAIT_SECONDS}s)")
    parser.add_argument("-l", "--lang", choices=["en", "ja"], default="en",
                        help="Output language of the summary (default: en)")
    parser.set_defaults(func=run)
    return parser


def _lang_code(base_name):
    """Extract the language code from base_name (e.g. onde-ja, onde-ja-1)."""
    parts = base_name.split("-")
    if len(parts) >= 3 and parts[-1].isdigit():
        return parts[-2]
    return parts[-1]


def _is_japanese(text):
    """Whether the text contains kana/kanji. Used to detect when plain-text output comes back in English."""
    return any(
        "぀" <= ch <= "ヿ" or "一" <= ch <= "鿿"
        for ch in text
    )


def _clean(text):
    """Trim the LLM's plain-text output down to a single line that fits in a table cell."""
    s = " ".join(text.split())
    # Strip quotes only if they wrap the whole string (keep quotes used within a quoted term)
    for lq, rq in (("「", "」"), ('"', '"'), ("'", "'"), ("“", "”")):
        if len(s) > 1 and s.startswith(lq) and s.endswith(rq) and lq not in s[1:-1]:
            s = s[1:-1].strip()
    s = s.rstrip("。.")
    # Escape since it clashes with the cell separator
    return s.replace("|", "\\|")


def load_jsonl(path):
    """Load a JSONL as {lang: record}. Returns empty if it doesn't exist."""
    records = {}
    p = Path(path)
    if not p.exists():
        return records
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            records[rec["lang"]] = rec
    return records


def append_jsonl(path, record):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _build_input(data_list):
    """Convert 3 evaluation logs into plain-text Evaluation blocks.
    Per-criterion scores/reasoning are omitted since they would confuse the
    summary; only the total score and overall_comment are passed.
    """
    blocks = []
    for i, d in enumerate(data_list, 1):
        if not d or "evaluation" not in d:
            continue
        ev = d["evaluation"]
        total = sum(ev[c]["score"] for c in CRITERIA if c in ev)
        comment = ev.get("overall_comment", "")
        blocks.append(f"# Evaluation {i} (Score {total})\n\n{comment}")
    return "\n\n".join(blocks)


def _matches_lang(text, lang):
    """Whether the text is written in the given language (en/ja)."""
    return _is_japanese(text) if lang == "ja" else not _is_japanese(text)


def render_table(records, lang):
    """Build a Markdown table from JSONL records. Sorted by score descending, then language code ascending."""
    rows = sorted(records.values(), key=lambda r: (-r["score"], r["lang"]))
    lines = [TABLE_HEADERS[lang], TABLE_SEPARATOR]
    for r in rows:
        name = LANGUAGES.get(r["lang"], {}).get(lang, r["lang"])
        lines.append(f"| {name} | {r['score']} | {r['analysis']} |")
    return lines


def sync_readme(path, table_lines):
    """Replace the table in the README whose header matches one of TABLE_HEADERS."""
    p = Path(path)
    lines = p.read_text(encoding="utf-8").split("\n")
    result = []
    i = 0
    replaced = False
    while i < len(lines):
        if lines[i].strip() in TABLE_HEADERS.values():
            result.extend(table_lines)
            replaced = True
            i += 1
            # Skip past the existing table body
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
        else:
            result.append(lines[i])
            i += 1
    if not replaced:
        headers = " / ".join(TABLE_HEADERS.values())
        print(f"Warning: no matching table found in {path}: {headers}")
        return False
    p.write_text("\n".join(result), encoding="utf-8")
    print(f"Updated table: {path}")
    return True


def run(args):
    records = load_jsonl(args.output_file)

    if not args.render_only:
        if not args.files:
            print("Error: specify evaluation JSON files (not needed with --render-only)")
            return
        if not args.model:
            print("Error: -m/--model is required")
            return

        groups = find_evaluation_groups(args.files)
        if not groups:
            print("No evaluation file groups found.")
            return

        # Target only unprocessed languages
        pending = []
        for base_name, runs in sorted(groups.items()):
            code = _lang_code(base_name)
            if code in records:
                continue
            pending.append((base_name, code, runs))

        skipped = len(groups) - len(pending)
        if skipped:
            print(f"Skipping {skipped} language(s) already present in the JSONL.")

        output_lang_name = "Japanese" if args.lang == "ja" else "English"

        if pending:
            client = LLMClient(
                model=args.model,
                think=(not args.no_think),
                retry_wait=args.retry_wait,
            )
            # Each language is processed only once, so show a single bar across all languages
            # The denominator stays the total across all languages on resume too, treating skipped ones as complete
            total = len(groups)
            ui = StatusLine(label=pending[0][1], left_count=True)
            with ui.progress(total, start=skipped) as prog:
                for offset, (base_name, code, runs) in enumerate(pending, skipped + 1):
                    prog.update(offset - 1, label=code)
                    data_list = [load_evaluation_data(runs[i]) for i in [1, 2, 3]]
                    _, total_scores = calculate_statistics(data_list)
                    lang_name = LANG_NAMES.get(code, code.capitalize())

                    evaluations = _build_input(data_list)
                    prompts = [
                        f"<evaluations lang=\"{lang_name}\">\n"
                        f"{evaluations}\n"
                        f"</evaluations>",
                        f"The block above contains three independent evaluations of one translation "
                        f"whose target language is {lang_name}. Trust these evaluations as given; "
                        f"do not re-evaluate the translation yourself. Summarize the single most "
                        f"notable characteristic in one short phrase. "
                        f"An issue mentioned in multiple runs is more reliable than one mentioned "
                        f"only once.\n"
                        f"IMPORTANT: The summary must be written in {output_lang_name}, but it "
                        f"describes a translation into {lang_name}. Never confuse the language you "
                        f"write in with the language being evaluated.\n"
                        f"IMPORTANT: State only what the evaluations actually say. Do not add "
                        f"details they do not mention. For example, if they report a mixed-language "
                        f"defect without naming the intruding language, describe it generically "
                        f"rather than guessing which language it was.\n"
                        f"OUTPUT FORMAT: Reply with the summary phrase itself and nothing else. "
                        f"It goes directly into a Markdown table cell, so no labels, no quotation "
                        f"marks around the whole phrase, no bullet points, no line breaks, no "
                        f"trailing period, and no explanation before or after. "
                        f"If defects exist, state the most prominent one concretely. If the "
                        f"translation is sound, state that briefly. "
                        f"Keep it within 40 characters if written in Japanese, or a short phrase of "
                        f"about 8 words or fewer if written in English. "
                        f"Write it in {output_lang_name} — not in {lang_name}.",
                    ]

                    print(f"\nAnalyzing {base_name} ...")
                    for attempt in range(3):
                        p = prompts if attempt == 0 else prompts + [
                            f"The previous reply was not in {output_lang_name}. "
                            f"Reply again with the same summary written in {output_lang_name}, "
                            f"and output nothing but the phrase itself."
                        ]
                        text = client.call(p, file=ui.stream)
                        ui.stream.end()
                        if _matches_lang(text, args.lang):
                            break
                        print(f"Retrying since the reply was not in {output_lang_name} ({attempt + 1}/3)")

                    median = total_scores["median"]
                    record = {
                        "lang": code,
                        "score": int(median) if median is not None else 0,
                        "analysis": _clean(text),
                    }
                    # Append after each language so an interruption loses at most one
                    append_jsonl(args.output_file, record)
                    records[code] = record
                    prog.update(offset, label=code)

    if not records:
        print(f"No records in {args.output_file}.")
        return

    table = render_table(records, args.lang)
    print()
    for line in table:
        print(line)

    if args.sync:
        sync_readme(args.sync, table)
