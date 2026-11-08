# Translation with PLaMo 3 Translate, one request per language for the whole text.
#
# trtools translate cannot drive this model: its chat template skips system messages and
# reads every user/assistant pair as a source/translation example, so the injected
# instructions, glossary and summary would be translated or taken as history. The options
# go in chat-template variables instead, through llm7shi's Client.plamo3translate().
# The glossary is the target language's whole column of the term TSV, since the whole
# text goes in one request anyway.

import csv
import os
import time
from pathlib import Path

from llm7shi import Client

from .language import LANG_NAMES

# The model's language codes where they differ from the corpus's (model card, Supported
# Languages). The output file keeps the corpus's code.
MODEL_CODES = {"zh": "zh-hans"}

# The output of PLaMo 3 Translate may be distributed only when marked as such
# (PLaMo Community License, Article 5).
LICENSE_NOTE = ("Outputs of PLaMo 3 Translate, under the PLaMo Community License: "
                "https://plamo.preferredai.jp/info/plamo-community-license-en")


def add_parser(subparsers):
    parser = subparsers.add_parser(
        "plamo", help="Translate a whole text with PLaMo 3 Translate (one request per language)")
    parser.add_argument("input_file", help="Text file to translate (e.g. ../onde-en.txt)")
    parser.add_argument("--langs", nargs="+", required=True,
                        help="List of target language codes (e.g. ja fr)")
    parser.add_argument("-m", "--model", default="llama.cpp:",
                        help="Model with vendor prefix (default: llama.cpp:, see OPENAI_BASE_URL)")
    parser.add_argument("--terms-dir", default=None,
                        help="Directory of term files; {topic}-{source}.tsv is used (no glossary if omitted)")
    parser.add_argument("--tr-dir", default="tr", help="Translation output directory (default: tr)")
    parser.set_defaults(func=run)
    return parser


def load_glossary(tsv_path, from_lang, to_lang):
    """[{"source": term, "target": translation}, ...] for every row with both columns filled.

    Empty when the TSV has no column for either language, as in trtools translate.
    """
    with open(tsv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        if from_lang not in header or to_lang not in header:
            return []
        from_idx = header.index(from_lang)
        to_idx = header.index(to_lang)
        return [
            {"source": row[from_idx], "target": row[to_idx]}
            for row in reader
            if len(row) > max(from_idx, to_idx) and row[from_idx] and row[to_idx]
        ]


def run(args):
    input_file = Path(args.input_file)
    topic, from_code = input_file.stem.rsplit("-", 1)
    text = input_file.read_text(encoding="utf-8").rstrip("\n")
    source_lines = len(text.splitlines())
    tsv_path = Path(args.terms_dir) / f"{topic}-{from_code}.tsv" if args.terms_dir else None
    os.makedirs(args.tr_dir, exist_ok=True)

    print(LICENSE_NOTE)
    for index, lang in enumerate(args.langs, 1):
        out = Path(args.tr_dir) / f"{topic}-{lang}.txt"
        if out.exists():
            print(f"Skipping {out} (already exists)")
            continue
        glossary = []
        if tsv_path:
            glossary = load_glossary(tsv_path, LANG_NAMES.get(from_code, from_code),
                                     LANG_NAMES.get(lang, lang))
        print(f"\nTranslating {out} ({index}/{len(args.langs)}, {len(glossary)} terms) ...")
        client = Client.plamo3translate(
            MODEL_CODES.get(lang, lang),
            model=args.model,
            source_lang=from_code,
            glossary=glossary or None,
            show_params=False,
            keep_history=False,
            # temperature 0 makes a retry repeat the same output; a stop is reported instead
            retries=1,
            # a runaway guard: a translation is rarely more than a few times its source
            max_length=len(text) * 5 + 100,
        )
        started = time.monotonic()
        resp = client(text)
        result = resp.text.strip()
        if not result:
            raise SystemExit(f"{out}: empty translation")
        if resp.repetition or resp.max_length is not None:
            reason = "repetition" if resp.repetition else "length limit"
            print(f"WARNING: {out}: output stopped ({reason})")
        lines = len(result.splitlines())
        if lines != source_lines:
            print(f"WARNING: {out}: {lines} lines, the source has {source_lines}")
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_text(result + "\n", encoding="utf-8")
        tmp.replace(out)
        print(f"Elapsed time: {time.monotonic() - started:.1f}s")
