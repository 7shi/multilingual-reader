# Line-by-line translation subcommand (term injection / summary compression)
# Based on experimental4/translate.py, but drops speaker separation and translates
# line by line while preserving empty lines.
# Term extraction is done beforehand with trtools term extract/translate, and the
# resulting JSON and TSV are loaded and injected here.

import csv
import json
import os
import time
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .statusline import StatusLine
from .summary import load_summaries

LINE_RETRY_COUNT = 3


def add_parser(subparsers):
    parser = subparsers.add_parser("translate", help="Translate text line by line (preserving empty lines)")
    parser.add_argument("input_file", help="Text file to translate")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="Source language (e.g. French, English, Japanese)")
    parser.add_argument("-t", "--to", dest="to_lang", required=True,
                        help="Target language (e.g. Spanish, Japanese)")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="Output filename")
    parser.add_argument("-m", "--model", required=True, help="Translation model")
    parser.add_argument("--threshold", type=int, default=10,
                        help="Interval for summary generation, in lines (default: 10)")
    parser.add_argument("--keep", type=int, default=5,
                        help="Number of translation pairs to keep after compression (default: 5)")
    parser.add_argument("--terms-json", default=None,
                        help="Output JSON file from trtools term extract")
    parser.add_argument("--terms-tsv", default=None,
                        help="Output TSV file from trtools term translate")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking (for Qwen3 models)")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"Wait time on retry, in seconds (default: {DEFAULT_RETRY_WAIT_SECONDS}s)")
    parser.add_argument("--fix", action="store_true",
                        help="Retranslate only the empty lines in the existing output and rewrite the whole file (normal mode determines resume position from line count alone)")
    parser.set_defaults(func=run)


def _load_terms(terms_json, terms_tsv, from_lang, to_lang, write=None):
    """Build chunk_data and glossary from the JSON and TSV."""
    if write is None:
        write = lambda text: print(text, end="")

    with open(terms_json, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    if json_data.get("from") != from_lang:
        write(f"WARNING: term JSON's source language '{json_data.get('from')}' differs from the specified '{from_lang}'.\n")

    chunk_data = json_data.get("chunks", [])

    glossary = {}
    with open(terms_tsv, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        if from_lang not in header:
            write(f"WARNING: TSV has no '{from_lang}' column. Skipping term injection.\n")
            return chunk_data, glossary
        if to_lang not in header:
            write(f"WARNING: TSV has no '{to_lang}' column. Skipping term injection.\n")
            return chunk_data, glossary
        from_idx = header.index(from_lang)
        to_idx = header.index(to_lang)
        for row in reader:
            if len(row) > max(from_idx, to_idx):
                term = row[from_idx]
                translation = row[to_idx]
                if term and translation:
                    glossary[term] = translation

    return chunk_data, glossary


def _build_terms_messages(start_line, end_line, chunk_data, glossary, from_lang, to_lang):
    """Return message pairs for terms appearing in the given line range (1-indexed inclusive)."""
    seen = set()
    relevant = []
    for chunk in chunk_data:
        cstart, cend = chunk["start"], chunk["end"]
        if cstart <= end_line and cend >= start_line:
            for t in chunk["terms"]:
                if t not in seen and t in glossary:
                    seen.add(t)
                    relevant.append(t)

    if not relevant:
        return []

    listing = "\n".join(f"{t} => {glossary[t]}" for t in relevant)
    user_msg = {
        "role": "user",
        "content": (
            f"Glossary for the upcoming {from_lang} → {to_lang} translation. "
            f"Use these translations consistently:\n{listing}"
        ),
    }
    assistant_msg = {
        "role": "assistant",
        "content": "Acknowledged. I will use these translations consistently.",
    }
    return [user_msg, assistant_msg]


def _build_summary_messages(summary_text):
    """Convert summary text into a message pair for context injection."""
    if not summary_text:
        return []
    user_msg = {
        "role": "user",
        "content": f"Context summary of the source text so far:\n{summary_text}",
    }
    assistant_msg = {
        "role": "assistant",
        "content": "Understood, I will keep this context in mind.",
    }
    return [user_msg, assistant_msg]


def run(args):
    from_lang = args.from_lang
    to_lang = args.to_lang
    threshold = args.threshold
    keep = args.keep

    with open(args.input_file, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # Extract non-empty lines as translation targets (preserving the original line index)
    content_lines = [(i, line.rstrip("\n")) for i, line in enumerate(all_lines) if line.strip()]
    total = len(content_lines)

    ui = StatusLine(
        label=getattr(args, 'label', None),
        start=getattr(args, 'start', None),
        index=getattr(args, 'index', None),
        count=getattr(args, 'count', None),
    )

    # Determine the resume position from the output file's existing content
    existing_lines = []
    if os.path.exists(args.output_file):
        with open(args.output_file, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()

    if args.fix:
        # Retranslate only lines that are empty. Appending can't preserve position, so rewrite the whole file.
        translated_text = {
            orig_idx: (existing_lines[orig_idx].rstrip("\n") if orig_idx < len(existing_lines) else "")
            for orig_idx, _ in content_lines
        }
        bad_indices = {
            k for k, (orig_idx, _) in enumerate(content_lines)
            if not translated_text[orig_idx].strip()
        }
        if not bad_indices:
            ui.write(f"No empty lines: {args.output_file}\n")
            return
        resume_count = 0
    else:
        resume_count = sum(1 for orig_idx, _ in content_lines if orig_idx < len(existing_lines))
        translated_text = {
            orig_idx: existing_lines[orig_idx].rstrip("\n")
            for orig_idx, _ in content_lines[:resume_count]
        }
        bad_indices = set()

        if total > 0 and resume_count >= total:
            ui.write(f"Already translated: {args.output_file}\n")
            return

    # The summary must be pre-generated with trtools summary (errors if missing)
    summaries = load_summaries(args.input_file, total, threshold, keep)

    chunk_data = []
    glossary = {}
    if args.terms_json and args.terms_tsv:
        chunk_data, glossary = _load_terms(args.terms_json, args.terms_tsv, from_lang, to_lang, ui.write)

    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    system_message = {
        "role": "system",
        "content": (
            f"You are a professional translator. Translate the following {from_lang} "
            f"text to {to_lang}. Maintain consistency with previous translations and "
            f"preserve the context and nuance of the original text. Provide only the "
            f"translation without any explanations or commentary."
        ),
    }

    def build_chat_history(position):
        """Build chat_history as of position (number of lines translated so far).
        The same procedure is used whether starting fresh (position == 0) or resuming."""
        seed_start = position + 1
        seed_end = min(position + threshold + keep, total)
        terms_msgs = _build_terms_messages(seed_start, seed_end, chunk_data, glossary, from_lang, to_lang)
        checkpoint = max((i for i in summaries if i <= position), default=None)
        summary_msgs = _build_summary_messages(summaries.get(checkpoint))
        translation_messages = []
        for orig_idx, line in content_lines[max(0, position - keep):position]:
            translated = translated_text[orig_idx]
            translation_messages.append({
                "role": "user",
                "content": f"Translate the following {from_lang} line into {to_lang}.\n{line}",
            })
            translation_messages.append({"role": "assistant", "content": translated})
        return (
            [system_message] + terms_msgs + summary_msgs
            + translation_messages[-keep * 2:]
        ), translation_messages

    chat_history, translation_messages = build_chat_history(resume_count)

    def translate_line(prompt):
        for attempt in range(1, LINE_RETRY_COUNT + 1):
            user_msg = {"role": "user", "content": prompt}
            chat_history.append(user_msg)
            translated = client.call(chat_history, file=ui.stream)
            ui.stream.end()
            stripped = translated.strip()
            if stripped and "\n" not in stripped:
                asst_msg = {"role": "assistant", "content": stripped}
                chat_history.append(asst_msg)
                return stripped, user_msg, asst_msg
            chat_history.pop()
            if attempt < LINE_RETRY_COUNT:
                ui.stream.error("Invalid translation result.")
                ui.stream.wait_retry(args.retry_wait, f"Retrying ({attempt}/{LINE_RETRY_COUNT})...")
            else:
                raise RuntimeError(f"Invalid translation result (failed {LINE_RETRY_COUNT} times): {prompt!r}")

    start_time = time.time()
    next_compression = None
    next_write_idx = 0 if args.fix else len(existing_lines)

    out_f = open(args.output_file, "w" if (args.fix or not resume_count) else "a", encoding="utf-8")
    try:
        with ui.progress(total, start=resume_count) as prog:
            for k in range(resume_count, total):
                i = k + 1
                orig_idx, line = content_lines[k]
                if args.fix and k not in bad_indices:
                    translated = translated_text[orig_idx]
                    user_msg = {
                        "role": "user",
                        "content": f"Translate the following {from_lang} line into {to_lang}.\n{line}",
                    }
                    asst_msg = {"role": "assistant", "content": translated}
                    chat_history.append(user_msg)
                    chat_history.append(asst_msg)
                else:
                    prompt = f"Translate the following {from_lang} line into {to_lang}.\n{line}"
                    translated, user_msg, asst_msg = translate_line(prompt)
                    translated_text[orig_idx] = translated
                translation_messages.extend([user_msg, asst_msg])
                prog.update(i)

                out_f.writelines(all_lines[next_write_idx:orig_idx])
                out_f.write(translated + "\n")
                out_f.flush()
                next_write_idx = orig_idx + 1

                if i % threshold == 0 and i + keep < total and i in summaries:
                    next_compression = i + keep

                if next_compression is not None and i == next_compression:
                    chat_history, translation_messages = build_chat_history(i)
                    next_compression = None

        out_f.writelines(all_lines[next_write_idx:])
    finally:
        out_f.close()

    elapsed = time.time() - start_time

    ui.write(f"\nTranslation complete: {from_lang} -> {to_lang} ({args.output_file})\n")
    ui.write(f"Elapsed time: {elapsed:.1f}s ({elapsed/60:.1f}min)\n")
