# Subcommand that evaluates translations with TypeSafe's Jev, one request per language,
# appending one JSONL record each to jev.jsonl.
#
# This is not `trtools eval` with another model behind it. Jev is a System One model: it
# returns a probability distribution over five ordered severity levels per criterion and
# no prose, so there is no `reasoning` to store and no rubric text for the model to
# interpret loosely. experimental/13/PORT.md is the design and says what each field means;
# experimental/13/README.md is what it was chosen on.
#
# One run per language, not three. Experiment 12 measured this evaluator's run-to-run
# range at 1.12 points, with run 1 alone reproducing the median of three at Pearson 0.998.

import json
import time
from pathlib import Path

from llm7shi.usage import Usage, append_usage, print_today_totals
from typesafe_sdk import TypeSafeClient

from .jev_criteria import (CRITERIA, CRITERION_IDS, JUDGE, LEVELS, POINTS_PER_LEVEL,
                           SCHEME_ID, SCOPE, build_questions, build_state)
from .language import LANGUAGES
from .llm import init_usage_path
from .statusline import StatusLine

# A version, not the `jev-latest` alias, so a model release cannot silently make later
# runs incomparable with the ones already on disk. Bump deliberately and re-run whole.
DEFAULT_MODEL = "jev-1.13.0"
DEFAULT_ATTEMPTS = 3
DEFAULT_TIMEOUT = 120.0


def add_parser(subparsers):
    parser = subparsers.add_parser(
        "jev", help="Evaluate translations with TypeSafe Jev, writing one JSONL record "
                    "per language")
    parser.add_argument("original", nargs="?", help="Original text file")
    parser.add_argument("--show-scheme", action="store_true",
                        help="Print what Jev is asked -- the scheme id, the criteria, the "
                             "levels and the state's keys -- as Markdown, and exit")
    parser.add_argument("--langs", nargs="+",
                        help="Target language codes to evaluate")
    parser.add_argument("-f", "--from", dest="from_lang", default="English",
                        help="Source language (default: English)")
    parser.add_argument("--tr-dir", default="tr",
                        help="Directory holding the translations (default: tr)")
    parser.add_argument("-o", "--output", dest="output_file", default="jev.jsonl",
                        help="JSONL file to append to (default: jev.jsonl)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"TypeSafe model version (default: {DEFAULT_MODEL})")
    parser.add_argument("--expect-model",
                        help="Version the response must report, if not --model itself; "
                             "empty accepts whatever answers, which an alias needs")
    parser.add_argument("--attempts", type=int, default=DEFAULT_ATTEMPTS,
                        help=f"Attempts per language (default: {DEFAULT_ATTEMPTS})")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help=f"Per-request timeout in seconds (default: {DEFAULT_TIMEOUT:g})")
    parser.add_argument("--force", action="store_true",
                        help="Re-evaluate every language, discarding the existing file")
    parser.set_defaults(func=run)
    return parser


def read_done(path):
    """Language codes already in the JSONL.

    A line that does not parse, or that was scored on another scheme, stops the run. The
    alternative is appending today's judgments to yesterday's under a scheme that has
    since been reworded, which nothing downstream could detect.
    """
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
        if record.get("rubric") != SCHEME_ID:
            raise SystemExit(f"{path}:{n}: scored on {record.get('rubric')!r}, "
                             f"this run is {SCHEME_ID!r}")
        done[record["lang"]] = record
    return done


def read_answers(response):
    """{criterion: (expected level, confidence, [probability per level])}, in rubric order."""
    answers = {}
    for key in CRITERION_IDS:
        answer = response.scores.get(key)
        if answer is None:
            raise ValueError(f"no answer for {key}")
        probabilities = {int(level): float(p) for level, p in answer.probabilities.items()}
        if set(probabilities) != set(range(len(LEVELS))):
            raise ValueError(f"unexpected levels for {key}: {sorted(probabilities)}")
        answers[key] = (answer.score, answer.confidence,
                        [round(probabilities[i], 4) for i in range(len(LEVELS))])
    return answers


def evaluate(client, args, state, expect_model):
    """One request, returning the answers, its Usage and the model version that answered.

    All five questions go in a single request: they are independent, the state is billed
    once per request, and there is nothing to split.

    A version other than the expected one raises SystemExit rather than an ordinary
    exception, so it aborts the run instead of being retried -- the alias having moved is
    not a transient failure.
    """
    response = client.system_one(state, build_questions(), model=args.model)
    if expect_model and response.model != expect_model:
        raise SystemExit(f"requested {args.model} but {response.model} answered; "
                         f"the run is abandoned rather than mixing versions")
    usage = Usage()
    if response.usage:
        usage = Usage(raw={"input_tokens": response.usage.input_tokens,
                           "output_tokens": response.usage.output_tokens})
    return read_answers(response), usage, response.model


def show_scheme():
    """Print the scheme as Markdown, for pasting into a record of a run.

    The wording lives in jev_criteria.py because SCHEME_ID has to be computed from what is
    actually sent; a copy anywhere else would be a second source of truth. This prints that
    copy on demand instead, so a corpus directory can carry a readable one whose staleness
    is detectable: change the wording and SCHEME_ID changes with it, and the printed id no
    longer matches the `rubric` in the jev.jsonl files beside it.
    """
    print(f"### `{SCHEME_ID}`\n")
    print("Five criteria, each asked as one TypeSafe Score question over the same five "
          "ordered levels.\n")
    print("**Asked of every criterion**\n")
    print(f"- `judge`: {JUDGE}")
    print(f"- `scope`: {SCOPE}\n")
    print("**Criteria**\n")
    print("| Key | Heading | `criterion` |")
    print("| --- | --- | --- |")
    for key, (heading, description) in CRITERIA.items():
        print(f"| `{key}` | {heading} | {description} |")
    print(f"\n**Levels**, worth {POINTS_PER_LEVEL:g} points each on the 0-20 scale the "
          f"corpus reports\n")
    print("| Level | Wording |")
    print("| ---: | --- |")
    for n, level in enumerate(LEVELS):
        print(f"| {n} | {level} |")
    keys = ", ".join(f"`{k}`" for k in build_state("", "", "English", "Japanese"))
    print(f"\n**State keys**, in order: {keys}")


def run(args):
    if args.show_scheme:
        show_scheme()
        return
    if not args.original or not args.langs:
        raise SystemExit("the original text file and --langs are required "
                         "unless --show-scheme is given")

    original = Path(args.original)
    original_text = original.read_text(encoding="utf-8").rstrip()
    out_path = Path(args.output_file)
    tr_dir = Path(args.tr_dir)

    if args.force and out_path.is_file():
        out_path.unlink()
    done = read_done(out_path)

    # --langs is the corpus's statement of what should exist, so a language missing from
    # tr/ is an error rather than a shorter run.
    pending = []
    for lang in args.langs:
        if lang in done:
            continue
        if lang not in LANGUAGES:
            raise SystemExit(f"no language name for {lang!r}")
        tr_file = tr_dir / f"{original.stem.rsplit('-', 1)[0]}-{lang}.txt"
        if not tr_file.is_file():
            raise SystemExit(f"no translation at {tr_file}")
        pending.append((lang, LANGUAGES[lang]["en"], tr_file))

    print(f"{out_path}: {len(done)} of {len(args.langs)} languages already evaluated, "
          f"{len(pending)} to go, on {SCHEME_ID} with {args.model}.")
    if not pending:
        return

    # A version is its own pin; only an alias needs --expect-model spelled out.
    expect_model = args.model if args.expect_model is None else args.expect_model
    # Jev is a paid API, so usage is always recorded
    usage_path = init_usage_path(args.model, save_usage=True)
    total_usage = Usage()
    served_model = args.model
    run_start = time.monotonic()

    ui = StatusLine(label=pending[0][0], left_count=True)
    with TypeSafeClient(timeout=args.timeout) as client, \
            ui.progress(len(args.langs), start=len(done)) as prog:
        for offset, (lang, lang_name, tr_file) in enumerate(pending, len(done) + 1):
            prog.update(offset - 1, label=lang)
            # The whole processing of this language, not the request alone: the file
            # read, the retries and building the record are part of what a run costs.
            started = time.monotonic()

            translated_text = tr_file.read_text(encoding="utf-8").rstrip()
            state = build_state(original_text, translated_text, args.from_lang, lang_name)
            for attempt in range(1, args.attempts + 1):
                try:
                    answers, usage, served_model = evaluate(client, args, state,
                                                            expect_model)
                    break
                except SystemExit:
                    raise
                except Exception as e:
                    ui.write(f"  attempt {attempt}/{args.attempts} failed for {lang}: {e}\n")
            else:
                raise SystemExit(f"GIVING UP on {lang} after {args.attempts} attempts")

            total_usage = total_usage + usage
            record = {
                "lang": lang,
                "model": served_model,
                "rubric": SCHEME_ID,
                "scores": {key: round(answers[key][0], 4) for key in CRITERION_IDS},
                "confidence": {key: round(answers[key][1], 4) for key in CRITERION_IDS},
                "probabilities": {key: answers[key][2] for key in CRITERION_IDS},
                "usage": usage.to_dict(),
                "seconds": round(time.monotonic() - started, 2),
            }
            # Append per language, so an interruption loses at most one.
            with out_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                f.flush()
            prog.update(offset, label=lang)

    elapsed = time.monotonic() - run_start
    # One usage.jsonl entry for the whole run: it is account-level state, and one line
    # per language would bury everything else in it.
    append_usage(total_usage, served_model, usage_path)
    print(f"\n{len(pending)} languages in {elapsed:.1f}s "
          f"({elapsed / len(pending):.2f}s each), {total_usage}\n")
    print_today_totals(usage_path, models=[served_model])
