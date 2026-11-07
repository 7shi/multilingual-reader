# Subcommand that checks each translation is in its target language, appending one JSONL
# record per language to langcheck.jsonl.
#
# Jev's five-criterion scoring does not notice a wrong language: French scored as German
# came out higher than as French (experimental/15/README.md section 2). This is a separate
# request, not a sixth question in the scoring one, so SCHEME_ID and every score on disk
# stay as they are. experimental/15/PORT.md is the design.
#
# Two stages, the first that decides wins:
#   copy -- most lines are the original's, verbatim; no model. Jev is weakest on plain
#           English, so the untranslated case is caught without it.
#   jev  -- a Choice over the target, its confusable languages, the source language and
#           Other, with only the translation in the state.
# An undecided Jev answer is `review`, not passed to another model: qwen3.6, tried as the
# referee, named the label for three of five wrong-language texts (PORT.md section 3).

import hashlib
import json
import re
import time
from pathlib import Path

from llm7shi.usage import Usage, append_usage, print_today_totals
from typesafe_sdk import Choice, TypeSafeClient

from .jev import DEFAULT_ATTEMPTS, DEFAULT_MODEL, DEFAULT_TIMEOUT
from .langcheck_candidates import CANDIDATES
from .language import LANGUAGES
from .llm import init_usage_path
from .statusline import StatusLine

INSTRUCTIONS = "Which language is `text` written in?"
OPTION = "The text is written in {}."
OTHER = "Other"
OTHER_DESC = "The text is written in a language not listed here, or in no language."
# P(target) at or above HIGH passes, below LOW is wrong, between is for a person to read.
# Wrong-language texts came out at 0.00-0.02 and the English original at 0.32; correct
# ones at 0.64 and above, all but four of 134 at 0.89 and above.
LOW = 0.2
HIGH = 0.8
# Share of the translation's non-empty lines that may equal a line of the original.
COPY_SHARE = 0.5
# A leading speaker label, as the corpus writes it ("Camille: ...").
LABEL = re.compile(r"^[^:：]{1,40}[:：]\s*")


def langcheck_id():
    """`langcheck@<8 hex>` over everything that determines a verdict."""
    parts = [INSTRUCTIONS, OPTION, OTHER, OTHER_DESC, repr(LOW), repr(HIGH),
             repr(COPY_SHARE), LABEL.pattern]
    for code, names in sorted(CANDIDATES.items()):
        parts.append(code + "=" + ",".join(names))
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return f"langcheck@{digest[:8]}"


LANGCHECK_ID = langcheck_id()


def add_parser(subparsers):
    parser = subparsers.add_parser(
        "langcheck", help="Check with TypeSafe Jev that each translation is in its "
                          "target language, writing one JSONL record per language")
    parser.add_argument("original", help="Original text file")
    parser.add_argument("--langs", nargs="+", required=True,
                        help="Target language codes to check")
    parser.add_argument("-f", "--from", dest="from_lang", default="English",
                        help="Source language (default: English)")
    parser.add_argument("--tr-dir", default="tr",
                        help="Directory holding the translations (default: tr)")
    parser.add_argument("-o", "--output", dest="output_file", default="langcheck.jsonl",
                        help="JSONL file to append to (default: langcheck.jsonl)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"TypeSafe model version (default: {DEFAULT_MODEL})")
    parser.add_argument("--attempts", type=int, default=DEFAULT_ATTEMPTS,
                        help=f"Attempts per language (default: {DEFAULT_ATTEMPTS})")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help=f"Per-request timeout in seconds (default: {DEFAULT_TIMEOUT:g})")
    parser.add_argument("--force", action="store_true",
                        help="Re-check every language, discarding the existing file")
    parser.set_defaults(func=run)
    return parser


def read_done(path, model):
    """Language codes already in the JSONL; a line from another scheme or model stops the run."""
    done = {}
    if not path.is_file():
        return done
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{n}: {e}")
        if record.get("scheme") != LANGCHECK_ID:
            raise SystemExit(f"{path}:{n}: checked on {record.get('scheme')!r}, "
                             f"this run is {LANGCHECK_ID!r}")
        # Copy-stage records ask no model, so they carry none.
        if record.get("model") not in (None, model):
            raise SystemExit(f"{path}:{n}: checked by {record.get('model')!r}, "
                             f"this run is {model!r}")
        done[record["lang"]] = record
    return done


def content_lines(text):
    """Non-empty lines with the speaker label stripped."""
    lines = (LABEL.sub("", line).strip() for line in text.splitlines())
    return [line for line in lines if line]


def copy_share(original_text, translated_text):
    """Share of the translation's content lines that are verbatim lines of the original."""
    original = set(content_lines(original_text))
    lines = content_lines(translated_text)
    if not lines:
        return 0.0
    return sum(line in original for line in lines) / len(lines)


def option_names(lang, source):
    """Target first, then its confusable languages and the source language, deduplicated."""
    names = [LANGUAGES[lang]["en"]] + CANDIDATES.get(lang, []) + [source]
    return list(dict.fromkeys(names))


def build_question(names):
    criteria = {name: OPTION.format(name) for name in names}
    criteria[OTHER] = OTHER_DESC
    return Choice(instructions=INSTRUCTIONS, criteria=criteria)


def ask(client, model, text, names):
    response = client.system_one({"text": text}, {"language": build_question(names)},
                                 model=model)
    if response.model != model:
        raise SystemExit(f"requested {model} but {response.model} answered; "
                         f"the run is abandoned rather than mixing versions")
    answer = response.choices.get("language")
    if answer is None:
        raise ValueError("no answer for language")
    probabilities = {k: round(float(v), 4) for k, v in answer.probabilities.items()}
    if set(probabilities) != set(names) | {OTHER}:
        raise ValueError(f"unexpected options: {sorted(probabilities)}")
    usage = Usage()
    if response.usage:
        usage = Usage(raw={"input_tokens": response.usage.input_tokens,
                           "output_tokens": response.usage.output_tokens})
    return probabilities, usage


def verdict(p_target):
    if p_target >= HIGH:
        return "ok"
    if p_target < LOW:
        return "wrong"
    return "review"


def run(args):
    original = Path(args.original)
    original_text = original.read_text(encoding="utf-8").rstrip()
    out_path = Path(args.output_file)
    tr_dir = Path(args.tr_dir)

    if args.force and out_path.is_file():
        out_path.unlink()
    done = read_done(out_path, args.model)

    pending = []
    for lang in args.langs:
        if lang in done:
            continue
        if lang not in LANGUAGES:
            raise SystemExit(f"no language name for {lang!r}")
        tr_file = tr_dir / f"{original.stem.rsplit('-', 1)[0]}-{lang}.txt"
        if not tr_file.is_file():
            raise SystemExit(f"no translation at {tr_file}")
        pending.append((lang, tr_file))

    print(f"{out_path}: {len(done)} of {len(args.langs)} languages already checked, "
          f"{len(pending)} to go, on {LANGCHECK_ID} with {args.model}.")
    if not pending:
        report(out_path)
        return

    usage_path = init_usage_path(args.model, save_usage=True)
    total_usage = Usage()
    asked = 0
    run_start = time.monotonic()
    try:
        ui = StatusLine(label=pending[0][0], left_count=True)
        with TypeSafeClient(timeout=args.timeout) as client, \
                ui.progress(len(args.langs), start=len(done)) as prog:
            for offset, (lang, tr_file) in enumerate(pending, len(done) + 1):
                prog.update(offset - 1, label=lang)
                started = time.monotonic()
                text = tr_file.read_text(encoding="utf-8").rstrip()
                share = round(copy_share(original_text, text), 4)
                record = {"lang": lang, "scheme": LANGCHECK_ID}
                if share >= COPY_SHARE:
                    record.update(verdict="wrong", stage="copy", detected=args.from_lang,
                                  copy_share=share)
                else:
                    names = option_names(lang, args.from_lang)
                    for attempt in range(1, args.attempts + 1):
                        try:
                            probabilities, usage = ask(client, args.model, text, names)
                            break
                        except SystemExit:
                            raise
                        except Exception as e:
                            ui.write(f"  attempt {attempt}/{args.attempts} failed "
                                     f"for {lang}: {e}\n")
                    else:
                        raise SystemExit(f"GIVING UP on {lang} after {args.attempts} attempts")
                    total_usage = total_usage + usage
                    asked += 1
                    p_target = probabilities[names[0]]
                    record.update(model=args.model, verdict=verdict(p_target), stage="jev",
                                  detected=max(probabilities, key=probabilities.get),
                                  p_target=p_target, copy_share=share,
                                  probabilities=probabilities, usage=usage.to_dict())
                record["seconds"] = round(time.monotonic() - started, 2)
                with out_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                if record["verdict"] != "ok":
                    ui.write(f"  {lang}: {record['verdict']} ({record['stage']}, "
                             f"detected {record['detected']})\n")
                prog.update(offset, label=lang)
    finally:
        if asked:
            append_usage(total_usage, args.model, usage_path)

    elapsed = time.monotonic() - run_start
    print(f"\n{len(pending)} languages in {elapsed:.1f}s, {total_usage}\n")
    report(out_path)
    if asked:
        print_today_totals(usage_path, models=[args.model])


def report(path):
    """One line per language that did not pass."""
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
               if line.strip()]
    flagged = [r for r in records if r["verdict"] != "ok"]
    if not flagged:
        print(f"{path}: every language ok")
        return
    for r in flagged:
        p = f", P(target) {r['p_target']:.2f}" if "p_target" in r else ""
        print(f"{path}: {r['lang']} {r['verdict']} ({r['stage']}, "
              f"detected {r['detected']}{p})")
