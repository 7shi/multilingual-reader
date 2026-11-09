# Whole-text translation, one request per language, for general models.
#
# The counterpart of trtools plamo for models without PLaMo 3 Translate's chat template
# (examples/tr/plamo/PLAN.md): the model gets only what PLaMo's template variables carry,
# the source and target languages and the glossary, as a system message, and the source
# text alone as the user message. No summary, no surrounding context, and no request to
# keep the lines, since PLaMo is not asked either. The loop over languages is shared with
# trtools plamo, which differs only in its client.

import csv
import os
import time
from pathlib import Path

from llm7shi import Client
from llm7shi.usage import append_usage, print_today_totals

from .language import LANG_NAMES
from .llm import init_usage_path
from .statusline import StatusLine


def add_parser(subparsers):
    parser = subparsers.add_parser(
        "whole", help="Translate a whole text in one request per language (general models)")
    add_common_arguments(parser)
    parser.add_argument("-m", "--model", required=True,
                        help="Model with vendor prefix (e.g. ollama:gemma4:31b-it-qat)")
    parser.add_argument("--no-think", action="store_true", help="Disable thinking")
    parser.set_defaults(func=run)
    return parser


def add_common_arguments(parser):
    """The arguments trtools plamo and trtools whole share."""
    parser.add_argument("input_file", help="Text file to translate (e.g. ../onde-en.txt)")
    parser.add_argument("--langs", nargs="+", required=True,
                        help="List of target language codes (e.g. ja fr)")
    parser.add_argument("--terms-dir", default=None,
                        help="Directory of term files; {topic}-{source}.tsv is used (no glossary if omitted)")
    parser.add_argument("--tr-dir", default="tr", help="Translation output directory (default: tr)")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name (recorded by default for openai: and gpt- models)")


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


def translate_each(args, make_client):
    """Translate args.input_file into each of args.langs, one request per language.

    make_client(from_code, lang, glossary, max_length, stream) returns a Client for
    one language, streaming to `stream`; each call sends the whole text as its prompt.
    The display follows trtools translate's: a status line per language, its bar
    counting the translated lines as they stream in. A language whose output
    file exists is skipped. A line count different from the source's, a stop by
    repetition or by length, and a code fence around the text are warned about, and
    the translation is saved as it came: these count as part of the performance. Only
    blank lines are dropped when the source has none, since a model may set its lines
    apart as paragraphs, which is layout rather than translation.
    Each language's usage is shown and recorded as in trtools translate.
    """
    input_file = Path(args.input_file)
    topic, from_code = input_file.stem.rsplit("-", 1)
    text = input_file.read_text(encoding="utf-8").rstrip("\n")
    source_lines = len(text.splitlines())
    source_has_blank = any(not line.strip() for line in text.splitlines())
    tsv_path = Path(args.terms_dir) / f"{topic}-{from_code}.tsv" if args.terms_dir else None
    os.makedirs(args.tr_dir, exist_ok=True)
    usage_path = init_usage_path(args.model, args.save_usage)

    # The batch's start, for the elapsed time on every language's status line
    batch_start = getattr(args, "start", None) or time.time()
    from_lang = LANG_NAMES.get(from_code, from_code)

    for index, lang in enumerate(args.langs, 1):
        to_lang = LANG_NAMES.get(lang, lang)
        out = Path(args.tr_dir) / f"{topic}-{lang}.txt"
        ui = StatusLine(label=lang, start=batch_start, index=index, count=len(args.langs))
        if out.exists():
            ui.write(f"Already translated: {out}\n")
            continue
        glossary = load_glossary(tsv_path, from_lang, to_lang) if tsv_path else []
        ui.write(f"\nTranslating: {from_lang} -> {to_lang} ({out}, {len(glossary)} glossary terms)\n")
        start_time = time.time()
        with ui.progress(source_lines) as prog:
            stream = LineCountingStream(ui.stream, lambda n: prog.update(min(n, source_lines)))
            # a runaway guard: a translation is rarely more than a few times its source
            client = make_client(from_code, lang, glossary, len(text) * 5 + 100, stream)
            try:
                resp = client(text)
            finally:
                ui.stream.end()
                # Recorded even on failure, since the tokens were spent either way
                usage = sum(client.usages) if client.usages else None
                if usage is not None and usage_path is not None:
                    append_usage(usage, args.model, usage_path)
            result = resp.text.strip()
            if not source_has_blank:
                result = drop_blank_lines(result)
            lines = len(result.splitlines())
            prog.update(min(lines, source_lines))
        if not result:
            raise SystemExit(f"{out}: empty translation")
        if resp.repetition or resp.max_length is not None:
            reason = "repetition" if resp.repetition else "length limit"
            ui.write(f"WARNING: {out}: output stopped ({reason})\n")
        if result.startswith("```") or result.endswith("```"):
            ui.write(f"WARNING: {out}: code fence around the translation (kept)\n")
        if lines != source_lines:
            ui.write(f"WARNING: {out}: {lines} lines, the source has {source_lines}\n")
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_text(result + "\n", encoding="utf-8")
        tmp.replace(out)

        elapsed = time.time() - start_time
        ui.write(f"\nTranslation complete: {from_lang} -> {to_lang} ({out})\n")
        ui.write(f"Elapsed time: {elapsed:.1f}s ({elapsed/60:.1f}min)\n")
        if usage is not None:
            ui.write(f"Usage: {usage}\n")
            if usage_path is not None:
                print()
                print_today_totals(usage_path, models=[args.model])


class LineCountingStream:
    """Passes the streamed display through, calling on_line(n) with the number of
    non-blank answer lines so far, for the progress bar. The thinking section, which
    llm7shi opens with a 🤔 header and closes with a 💡 one, is not counted."""

    def __init__(self, stream, on_line):
        self._stream = stream
        self._on_line = on_line
        self._thinking = False
        self._current = ""
        self._count = 0

    def write(self, text):
        self._stream.write(text)
        for part in text.splitlines(keepends=True):
            if "🤔" in part:
                self._thinking, self._current = True, ""
                continue
            if "💡" in part:
                self._thinking, self._current = False, ""
                continue
            if self._thinking:
                continue
            self._current += part
            if self._current.endswith("\n"):
                if self._current.strip():
                    self._count += 1
                    self._on_line(self._count)
                self._current = ""

    def __getattr__(self, name):
        return getattr(self._stream, name)


def drop_blank_lines(text):
    return "\n".join(line for line in text.splitlines() if line.strip())


def system_message(from_lang, to_lang, glossary):
    """trtools translate's instructions, without its wording on consistency between
    lines, and the whole glossary in its glossary messages' format."""
    content = (
        f"You are a professional translator. Translate the following {from_lang} text "
        f"to {to_lang}. Preserve the context and nuance of the original text. Provide "
        f"only the translation without any explanations or commentary."
    )
    if glossary:
        listing = "\n".join(f"{g['source']} => {g['target']}" for g in glossary)
        content += f"\n\nGlossary for this {from_lang} → {to_lang} translation:\n{listing}"
    return {"role": "system", "content": content}


def run(args):
    def make_client(from_code, lang, glossary, max_length, stream):
        client = Client(
            model=args.model,
            file=stream,
            include_thoughts=not args.no_think,
            show_params=False,
            # the system message is sent with every call, and calls do not add to it
            keep_history=False,
            # one attempt: a stop is reported and kept, not retried
            retries=1,
            max_length=max_length,
        )
        client.history = [system_message(LANG_NAMES.get(from_code, from_code),
                                         LANG_NAMES.get(lang, lang), glossary)]
        return client

    translate_each(args, make_client)
