# Subcommand that pre-generates a summary of the original text (cache for trtools translate)
#
# The summary is output "in English" and does not depend on the target language (to_lang).
# So generating it once per original text (topic) lets it be reused across
# all to_lang values / multiple translate runs for that topic.
# It is saved as {topic}-summary.jsonl in the same directory as the source
# (the topic name is the input filename with the "-<language code>" suffix removed).
# translate only reads this file and does not auto-generate it; it errors if missing.

import json
from pathlib import Path
from llm7shi import Client


def add_parser(subparsers):
    parser = subparsers.add_parser("summary", help="Pre-generate a summary of the original text (cache for trtools translate)")
    parser.add_argument("input_files", nargs="+", help="Text files to summarize (multiple allowed)")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="Source language (e.g. French, English, Japanese)")
    parser.add_argument("-m", "--model", required=True, help="Summary generation model")
    parser.add_argument("--threshold", type=int, default=10,
                        help="Interval for summary generation, in lines (match translate; default: 10)")
    parser.add_argument("--keep", type=int, default=5,
                        help="Number of lines to keep for checkpoint calculation (match translate; default: 5)")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking (for Qwen3 models)")
    parser.set_defaults(func=run)


def read_content_lines(input_file):
    """Extract non-empty lines (preserving the original line index)."""
    with open(input_file, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    return [(i, line.rstrip("\n")) for i, line in enumerate(all_lines) if line.strip()]


def topic_summary_path(input_file):
    """Derive the summary cache path from the input file's topic name.
    e.g. examples/finetuning-fr.txt -> examples/finetuning-summary.jsonl"""
    p = Path(input_file)
    topic, _, _ = p.stem.rpartition("-")
    topic = topic or p.stem
    return p.parent / f"{topic}-summary.jsonl"


def summary_checkpoints(total, threshold, keep):
    """Return the list of checkpoints (lines translated so far) at which to generate a summary."""
    checkpoints = []
    i = threshold
    while i <= total:
        if i + keep < total:
            checkpoints.append(i)
        i += threshold
    return checkpoints


def _read_cache(path):
    summaries = {}
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    summaries[entry["i"]] = entry["summary"]
    return summaries


def load_summaries(input_file, total, threshold, keep):
    """Load the already-generated summary cache. Errors if anything is missing."""
    checkpoints = summary_checkpoints(total, threshold, keep)
    if not checkpoints:
        return {}

    path = topic_summary_path(input_file)
    summaries = _read_cache(path)
    missing = [i for i in checkpoints if i not in summaries]
    if missing:
        raise FileNotFoundError(
            f"Summary cache is missing entries: {path} (missing lines: {missing})\n"
            f"Run `trtools summary {input_file} -f <from_lang> -m <model> "
            f"--threshold {threshold} --keep {keep}` first."
        )
    return summaries


def _generate_one(input_file, from_lang, threshold, keep, client):
    content_lines = read_content_lines(input_file)
    total = len(content_lines)
    checkpoints = summary_checkpoints(total, threshold, keep)
    path = topic_summary_path(input_file)

    if not checkpoints:
        print(f"Summary not needed (line count is at or below threshold+keep): {input_file}")
        return

    summaries = _read_cache(path)
    missing = [i for i in checkpoints if i not in summaries]
    if not missing:
        print(f"Summary already generated: {path}")
        return

    # The conversation starts over for each file
    client.history = []
    client.set_system_prompt(
        f"You are analyzing a {from_lang} text. Summarize the text so far in 2-3 "
        f"sentences (in English). Focus on topics and narrative context. If a "
        f"previous summary exists, integrate the new content with it rather than "
        f"starting over."
    )
    prev_end = 0
    with open(path, "a", encoding="utf-8") as out_f:
        for i in checkpoints:
            chunk_text = "\n".join(line for _, line in content_lines[prev_end:i])
            if i in summaries:
                # Cached summaries are replayed into the history without a call
                client.history.append({"role": "user", "content": chunk_text})
                client.history.append({"role": "assistant", "content": summaries[i]})
            else:
                summary_text = client(chunk_text).text.strip()
                summaries[i] = summary_text
                out_f.write(json.dumps({"i": i, "summary": summary_text}, ensure_ascii=False) + "\n")
                out_f.flush()
                print(f"Generated summary ({i}/{total} lines)")
            prev_end = i

    print(f"Saved summary: {path}")


def run(args):
    client = Client(
        model=args.model,
        include_thoughts=(not args.no_think),
        show_params=False,
        max_length=8192,
    )

    n = len(args.input_files)
    for idx, input_file in enumerate(args.input_files, 1):
        print(f"[{idx}/{n}] {input_file}")
        _generate_one(input_file, args.from_lang, args.threshold, args.keep, client)
