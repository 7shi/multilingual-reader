#!/usr/bin/env python3
"""Experiment 13: experiment 12's evaluator, run over the corpus's top two translators.

A copy of experiment 12's eval5_jev.py, together with the criteria.py it reads. Experiment
12 is a finished record and its rubric is free to change; a copy is what keeps this run
reproducible against the levels it was actually scored on, at the cost of the two files
having to be diffed rather than shared. See README.md for what this run is for -- in
short, experiment 12's conclusions rest on 8 targets chosen for being the ones the old
scheme handled worst, and this is the same comparison at n=67 per translator.

What the evaluator does is unchanged from experiment 12, and the rest of this docstring
describes it. `trtools eval` scores a translation on five criteria worth 20 points each,
and experiment 11 documents what goes wrong with that: the same evaluator on the same
translation swings by a mean of 52.4 points across three runs, because nothing in the
rubric separates a 14 from a 17. Experiment 11's answer was to replace the rubric with 50
narrow yes/partial/no items. This script keeps the rubric and replaces the evaluator
instead.

Each criterion becomes one TypeSafe System One Score question over five ordered severity
levels. Two things follow from that, neither of them a change to what is being judged:

- **The intermediate scores stop being discretionary.** A Score returns the
  probability-weighted position across the levels, so a value between "minor issues" and
  "clean" comes out of the distribution rather than out of the model picking a number.
  That is the gap the old rubric left open and the 50-item scheme closed by removing the
  scale altogether.
- **The five judgments are independent.** Each question is scored on its own against the
  same state, so a weak reading of one criterion cannot drag the other four with it --
  the single overall judgement experiment 11 blames for averaging over an evaluator's
  blind spots is not what is being asked.

How those levels are worded is itself a variable, and `--levels` selects between the two
wordings criteria.py holds: `degrees`, the default, which says only how much of the
document falls short, and `bands`, the old prompt's guidelines with their defect names.
Experiment 12's README section 3 is the comparison that settled it. This experiment runs
`degrees` only; `bands` is carried along because criteria.py was copied whole, and running
it here would answer nothing experiment 12 has not already answered.

Output files use `trtools eval`'s schema, so trtools/aggregate.py and trtools/trend.py
read them as they stand. `reasoning` and `overall_comment` come back empty, since Jev
emits no text; both are written anyway so the shape matches, and neither is read by the
aggregation. The distribution behind each score is kept in fields those scripts ignore,
including the unrounded 0-100 total.

Token usage is always recorded to the shared account-level usage.jsonl
(llm7shi.usage.find_usage_file); Jev is a paid API and there is no flag to turn it off.
The state is billed once per request, so the five questions cost barely more than one.

Requires a TypeSafe API key in `TYPESAFE_API_KEY`.

    uv run experimental/13/eval5_jev.py
"""

import argparse
import json
import time
from pathlib import Path
from types import SimpleNamespace

from trtools.language import LANGUAGES
from trtools.statusline import StatusLine
from llm7shi.usage import Usage, append_usage, find_usage_file, print_today_totals
from typesafe_sdk import Score, TypeSafeClient

from criteria import (CRITERIA, CRITERION_IDS, DEFAULT_LEVEL_SET, EVAL_DIRS,
                      LEVEL_SETS, POINTS_PER_LEVEL)

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
ORIGINAL = str(REPO_ROOT / "examples/onde-en.txt")
ONDE = REPO_ROOT / "examples" / "tr" / "onde"
# The corpus's top two translators under the old scheme, which ranks them 0.22 points
# apart over 67 languages. Experiment 12 ran the 8 targets the old scheme was least
# stable on, which is the worst possible sample to generalise from; naming other
# directories under examples/tr/onde/ on the command line points this anywhere else.
DEFAULT_TRANSLATORS = ("gpt-5.6-luna", "union-alpha")
# One run, not three. Three is what experiment 12's README section 3.1 needed in order
# to measure this evaluator's run-to-run range at all, and the answer was 1.12 points:
# run 1 alone reproduces the median of three at Pearson 0.998 and Spearman 1.000, and no
# correlation in its section 3.3 moves by more than 0.02. Repeating a judgment that does
# not vary costs three times as much and settles nothing. Pass --runs 3 to re-establish
# that on a new model version, which is the one occasion it is worth paying for.
RUNS = 1
ATTEMPTS = 3

# A version, not the `jev-latest` alias, so a model release cannot silently make later
# runs incomparable with the ones already on disk. Bump deliberately and re-run the whole
# directory. Every response's own version is checked against what was requested.
DEFAULT_MODEL = "jev-1.13.0"


def build_state(original_text, translated_text, from_lang, to_lang):
    """Named JSON state: both texts plus the facts every criterion is judged against."""
    n_lines = original_text.count("\n") + 1
    return {
        "task": f"Quality evaluation of a dialogue transcript translated from "
                f"{from_lang} into {to_lang}",
        "source_language": from_lang,
        "target_language": to_lang,
        "line_correspondence": f"Both texts have {n_lines} lines, and line i of the "
                               f"translation is meant to render line i of the original.",
        "original": original_text,
        "translation": translated_text,
    }


def build_questions(levels):
    """One Score per criterion, all sharing the same five severity levels.

    The levels say how badly a criterion is missed and are the same for all five; only
    what is being judged changes, so that goes in `instructions`.
    """
    return {
        key: Score(
            instructions={
                "judge": "How well does `translation` meet the criterion below, "
                         "read against `original`?",
                "criterion": description,
                "scope": "Judge this criterion alone, over the whole document. The "
                         "other four are asked about by their own questions.",
            },
            criteria=levels,
        )
        for key, (_, description) in CRITERIA.items()
    }


def read_answers(response, levels):
    """{criterion: (expected level, confidence, {level: probability})}, in rubric order."""
    answers = {}
    for key in CRITERION_IDS:
        answer = response.scores.get(key)
        if answer is None:
            raise ValueError(f"no answer for {key}")
        probabilities = {int(level): float(p) for level, p in answer.probabilities.items()}
        if set(probabilities) != set(range(len(levels))):
            raise ValueError(f"unexpected levels for {key}: {sorted(probabilities)}")
        answers[key] = (answer.score, answer.confidence, probabilities)
    return answers


def points(level):
    """A level, or a probability-weighted position between levels, on the 0-20 scale."""
    return level * POINTS_PER_LEVEL


def evaluate(client, args, state):
    """One request, returning the answers, the Usage and the resolved model version.

    All five questions go in a single request: they are independent, the state is billed
    once per request, and there is nothing to split.

    A version other than args.expect_model raises SystemExit rather than an ordinary
    exception, so it aborts the batch instead of being retried -- the alias having moved
    is not a transient failure.
    """
    response = client.system_one(state, build_questions(args.levels), model=args.model)
    if args.expect_model and response.model != args.expect_model:
        raise SystemExit(
            f"requested {args.model} but {response.model} answered, and the run is "
            f"pinned to {args.expect_model}. Results already in the output directory "
            f"were produced by {args.expect_model}; bump DEFAULT_MODEL and re-run the "
            f"whole directory, or pass --expect-model to override.")
    usage = Usage()
    if response.usage:
        usage = Usage(raw={"input_tokens": response.usage.input_tokens,
                           "output_tokens": response.usage.output_tokens})
    return read_answers(response, args.levels), usage, response.model


def run(client, args, ui):
    """Evaluate one translation and write the result.

    Returns this run's Usage and the model version that produced it, so the usage record
    is filed under the version billed rather than under the alias requested.
    """
    original_text = Path(args.original).read_text(encoding="utf-8").rstrip()
    translated_text = Path(args.translation).read_text(encoding="utf-8").rstrip()

    orig_lines = original_text.count("\n") + 1
    tr_lines = translated_text.count("\n") + 1
    if orig_lines != tr_lines:
        ui.write(f"Warning: line count mismatch ({orig_lines} vs {tr_lines})\n")

    state = build_state(original_text, translated_text, args.from_lang, args.to_lang)

    call_start = time.time()
    answers, usage, served_model = evaluate(client, args, state)
    duration_seconds = time.time() - call_start

    expected = {key: points(answers[key][0]) for key in CRITERION_IDS}
    scores = {key: round(expected[key]) for key in CRITERION_IDS}
    total_score = sum(scores.values())
    expected_total = sum(expected.values())

    ui.write("=== Translation Evaluation Result (Jev) ===\n")
    width = max(len(heading) for heading, _ in CRITERIA.values())
    for n, key in enumerate(CRITERION_IDS, 1):
        heading = CRITERIA[key][0]
        ui.write(f"{n}. {heading.ljust(width)}: {scores[key]:2d}/20 "
                 f"(expected {expected[key]:5.2f}, confidence {answers[key][1]:.2f})\n")
    ui.write(f"Total score: {total_score}/100 (expected {expected_total:.1f})\n")
    ui.write(f"Duration: {duration_seconds:.1f}s\n")
    ui.write(f"Model: {served_model}\n")
    ui.write(f"{usage}\n")

    if args.output_file:
        output_data = {
            "original_file": args.original,
            "translation_file": args.translation,
            "source_language": args.from_lang,
            "target_language": args.to_lang,
            # The version the API resolved the request to, not the alias asked for.
            "model_used": served_model,
            "model_requested": args.model,
            # trtools eval's shape. `reasoning` and `overall_comment` are empty because
            # Jev writes no text; they are present so aggregate.py and trend.py, which
            # read neither, still see the structure they expect.
            "evaluation": {
                **{key: {"reasoning": "", "score": scores[key]} for key in CRITERION_IDS},
                "overall_comment": "",
            },
            "total_score": total_score,
            # Everything below is Jev's own output, which trtools ignores.
            "duration_seconds": round(duration_seconds, 1),
            "expected_scores": {key: round(expected[key], 4) for key in CRITERION_IDS},
            "expected_total_score": round(expected_total, 4),
            "confidence": {key: round(answers[key][1], 4) for key in CRITERION_IDS},
            "probabilities": {key: {level: round(p, 4)
                                    for level, p in sorted(answers[key][2].items())}
                              for key in CRITERION_IDS},
            # The wording this run was produced under, so a result file says which of
            # criteria.py's level sets it belongs to without relying on its directory.
            "level_set": args.level_set,
            "levels": args.levels,
            "usage": usage.to_dict(),
        }
        Path(args.output_file).write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        ui.write(f"\nSaved evaluation result as JSON: {args.output_file}\n")

    return usage, served_model


def evaluate_target(client, make_args, runs, attempts, index, total, usage_path, ui):
    """Run one target for `runs` runs, retrying each up to `attempts` times.

    The StatusLine and its progress bar belong to the batch and are passed in: the bar
    counts targets completed out of the whole run, so a target must not open one of its
    own. With the default of one run there would be nothing for a per-target bar to show
    anyway.

    Existing output files are skipped, so a re-run fills in only what is missing; a run
    that keeps failing stops the whole batch, since a missing output file already records
    what did not complete. The target's runs are summed into one usage.jsonl entry,
    written once the target is done.
    """
    args0 = make_args(1)

    pending = []
    for run_no in range(1, runs + 1):
        args = make_args(run_no)
        out = Path(args.output_file)
        if out.is_file():
            ui.write(f"[{index}/{total}] exists, skipping: {out}\n")
        else:
            pending.append((run_no, args, out))

    if not pending:
        return Usage()

    target_usage = Usage()
    served_model = args0.model
    for run_no, args, out in pending:
        suffix = f" run {run_no}" if runs > 1 else ""
        ui.write(f"\n=== [{index}/{total}] {args.label}{suffix} ===\n")
        for attempt in range(1, attempts + 1):
            try:
                usage, served_model = run(client, args, ui)
                break
            except Exception as e:
                ui.write(f"  attempt {attempt}/{attempts} failed for {out}: {e}\n")
                out.unlink(missing_ok=True)
        else:
            raise SystemExit(f"GIVING UP on {out}")
        target_usage = target_usage + usage

    append_usage(target_usage, served_model, usage_path)
    return target_usage


def result_path(eval_dir, translator, lang, run_no):
    """<eval_dir>/<translator>/<lang>.json, with -N appended from the second run on.

    One directory per translator, because a 67-language run in a flat directory is not
    browsable and every name in it repeated the topic, the translator, the evaluator and
    a run number that is almost always 1. The topic is gone because this experiment only
    reads examples/tr/onde/; the evaluator is gone because the result directory already
    names the scheme, and a second evaluator belongs in its own -d rather than in a
    filename.

    The run number is kept from run 2 on rather than dropped entirely: it has to be a
    function of (translator, lang, run) alone, or an interrupted --runs 3 could not tell
    which of its runs are already on disk.
    """
    name = f"{lang}.json" if run_no == 1 else f"{lang}-{run_no}.json"
    return eval_dir / translator / name


def label_for(translator, lang, lang_name, eval_dir_name, name_width=0):
    """The status line's description for one target.

    `name_width` pads the language name so every label in a batch is the same length.
    The status line redraws in place, and a name that shrinks from "Serbo-Croatian" to
    "Thai" moves everything after it, which reads as flicker over 134 targets.
    """
    return f"{translator} / {lang}: {lang_name:<{name_width}} / {eval_dir_name}"


def load_targets(translators):
    """(translator, lang, lang_name) for every language each named translator covers.

    Taken from the corpus directory rather than from a list checked in here. A
    translator's tr/ directory already states which languages it has, and this experiment
    wants all of them, so a list would be a copy of that with nothing added and one more
    thing to fall out of step. Experiment 11 needed a file because its 8 targets encoded
    a selection; "every language this translator has" encodes nothing.

    A missing directory or an unknown language code stops the run rather than being
    skipped: both mean the command line does not say what it was thought to say.
    """
    targets = []
    for translator in translators:
        tr_dir = ONDE / translator / "tr"
        if not tr_dir.is_dir():
            raise SystemExit(f"no such translator directory: {tr_dir}")
        paths = sorted(tr_dir.glob("onde-??.txt"))
        if not paths:
            raise SystemExit(f"no translations in {tr_dir}")
        for path in paths:
            lang = path.stem.rsplit("-", 1)[1]
            if lang not in LANGUAGES:
                raise SystemExit(f"no language name for {lang!r} ({path})")
            targets.append((translator, lang, LANGUAGES[lang]["en"]))
    return targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"TypeSafe model version (default: {DEFAULT_MODEL})")
    parser.add_argument("--expect-model",
                        help="Version the response must report, if not --model itself; "
                             "empty accepts whatever answers, which an alias needs")
    parser.add_argument("-l", "--levels", default=DEFAULT_LEVEL_SET,
                        choices=sorted(LEVEL_SETS),
                        help="Which wording of the severity levels to score on "
                             f"(default: {DEFAULT_LEVEL_SET}); see criteria.py")
    parser.add_argument("-d", "--eval-dir",
                        help="Result directory under experimental/13 (default: the one "
                             "criteria.py gives the chosen level set)")
    parser.add_argument("translators", nargs="*", default=list(DEFAULT_TRANSLATORS),
                        help="Directory names under examples/tr/onde/, each evaluated in "
                             "every language it has (default: "
                             + " ".join(DEFAULT_TRANSLATORS) + ")")
    parser.add_argument("--runs", type=int, default=RUNS,
                        help=f"Runs per target (default: {RUNS}); 3 re-measures the "
                             "run-to-run range, which a new model version needs")
    parser.add_argument("--timeout", type=float, default=120.0,
                        help="Per-request timeout in seconds (default: 120)")
    cli_args = parser.parse_args()

    # A version is its own pin; only an alias needs --expect-model spelled out.
    expect_model = (cli_args.model if cli_args.expect_model is None
                    else cli_args.expect_model)

    # Each level set has its own directory by default, so two wordings cannot end up
    # mixed in one -- a result file's score means nothing without the levels it was
    # placed on. -d overrides it, for a run that is deliberately kept elsewhere.
    eval_dir_name = cli_args.eval_dir or EVAL_DIRS[cli_args.levels]
    eval_dir = BASE_DIR / eval_dir_name
    eval_dir.mkdir(parents=True, exist_ok=True)
    usage_path = find_usage_file()

    targets = load_targets(cli_args.translators)
    total = len(targets)
    index = 0
    total_usage = Usage()

    # One StatusLine and one bar for the whole batch. The bar counts targets finished
    # out of all of them -- 0 at the start, 134/134 at the end -- rather than runs within
    # a target, which at the default of one run per target could only ever read (1/1).
    # Neither `index` nor `count` is passed, so that (m/n) is the bar's own count and
    # sits at the right end rather than being a second, fixed pair beside the label.
    #
    # No `start` either. It would add an elapsed-time column measured from the batch
    # start, which is what the trailing clock already shows now that one task spans the
    # whole batch; when each target had its own bar the two clocks meant different
    # things.
    name_width = max(len(name) for _, _, name in targets)
    ui = StatusLine(label=label_for(*targets[0], eval_dir_name, name_width))
    with TypeSafeClient(timeout=cli_args.timeout) as client, \
            ui.progress(total, start=0) as prog:
        for translator, lang, lang_name in targets:
            index += 1
            label = label_for(translator, lang, lang_name, eval_dir_name, name_width)
            # Before the work, so the label names what is running rather than what last
            # finished; the completed count is advanced once the target is done.
            prog.update(index - 1, label)

            tr_file = ONDE / translator / "tr" / f"onde-{lang}.txt"
            if not tr_file.is_file():
                ui.write(f"Missing translation, skipping: {tr_file}\n")
                prog.update(index, label)
                continue

            (eval_dir / translator).mkdir(parents=True, exist_ok=True)

            def make_args(run_no):
                return SimpleNamespace(
                    original=ORIGINAL, translation=str(tr_file),
                    model=cli_args.model, from_lang="English", to_lang=lang_name,
                    output_file=str(
                        result_path(eval_dir, translator, lang, run_no)),
                    expect_model=expect_model,
                    level_set=cli_args.levels, levels=LEVEL_SETS[cli_args.levels],
                    run=run_no, runs=cli_args.runs, label=label,
                )

            total_usage = total_usage + evaluate_target(
                client, make_args, cli_args.runs, ATTEMPTS, index, total, usage_path, ui)
            prog.update(index, label)

    print(f"\nTotal usage: {total_usage}\n")
    print_today_totals(usage_path)


if __name__ == "__main__":
    main()
