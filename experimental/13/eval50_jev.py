#!/usr/bin/env python3
"""Experiment 13: experiment 11's 50-item scheme, run over this experiment's targets.

A copy of experiment 11's eval50_jev.py together with the items.py it reads, adapted to
take translator directory names rather than a target list, to default to one run, and to
carry the handful of helpers it used to import from eval50.py -- which is a generative
evaluator's script and has no business being imported by a run that never calls one.

This is the second scheme over the same 134 translations. eval5_jev.py asks the old
rubric's five criteria; this asks fifty narrow properties. Experiment 12 section 3.3 found
the two agreeing at Pearson +0.90 on eight targets, which is the strongest agreement
either experiment produced and rests on the smallest sample in either. Same targets, same
model, same day: whatever separates them here is the rubric.

What the evaluator does is unchanged from experiment 11, and the rest of this docstring
describes it. The 50 yes/partial/no items are asked as TypeSafe System One Score questions
instead of as one schema filled in by a generative model.

eval50.py hands a generative evaluator a Pydantic schema covering the items and reads
back whatever it writes. Jev does not generate: each item is its own Score question,
answered independently against the same state, and what comes back is a probability
distribution over the three rubric levels. That difference is the point of this script:

- **The `partial` band cannot be skipped.** Discussion 4 of README.md locates the local
  evaluators' inflation in an unused middle band (`gemma4:31b` 2.2%, against 23-25% for
  the commercial pair). A Score answer always places probability on all three levels, so
  the band is used by construction, and `expected_total_score` records the weighted
  position before it is rounded to a verdict.
- **Ignorance becomes visible.** Future Work 6 asks for a way to stop an unassessable
  property from silently scoring `yes`. `confidence` is that signal, recorded per item
  without a rubric change: a near-uniform distribution is an evaluator that has nothing
  to go on, which the verdict alone cannot show.
- **Items cannot contaminate each other.** ANCHOR_TAIL in eval50.py has to *ask* the
  model not to let one verdict pull the others along; here each question is scored on
  its own against the state, so the request carries no such instruction.

Jev emits no text, so there is no evidence field, no `overall_comment` and no thinking to
switch off: the `--no-think` / `--no-evidence` variants have no counterpart here, and this
script writes a single condition.

Results go to `evals50/`, beside the five-criterion scheme's `evals-degrees/`. The schema
is experiment 11's: `evaluation` maps each item to the verdict string of its most probable
level, and `total_score` is that verdict tally on the same 0-100 scale, so experiment 11's
agg50.py and refcmp.py can read these files as they stand once pointed at the directory.
The distribution Jev actually returned is kept alongside, in fields those scripts ignore.

Jev is a paid API, so token usage is always recorded to the shared account-level
usage.jsonl (llm7shi.usage.find_usage_file) -- there is no flag to turn it off.
The state is billed once per request here, so `--split` is expensive: a measured run of
all 50 items in one request costs about 12.7k input tokens (a ~5k-token state plus ~150
per question), where `--split item` would resend the state 50 times for roughly 250k.
That is the opposite of what check_align3_jev.py in the dante-norton repo found by
regression (`input = n * (state + question)`, R^2 0.974) on its own much smaller states,
so it is worth re-measuring rather than assuming, but for this workload one request is
both the cheapest and the fastest option.

The model is requested by version rather than by the `jev-latest` alias, and every
response's own version is checked against it, recorded in each result file and used as
the usage record's model name -- so a release cannot quietly land halfway through a
directory of results.

Requires a TypeSafe API key in `TYPESAFE_API_KEY`.

    uv run experimental/13/eval50_jev.py
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

from items import GROUPS, ITEM_IDS, CRITERIA

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
ORIGINAL = str(REPO_ROOT / "examples/onde-en.txt")
ONDE = REPO_ROOT / "examples" / "tr" / "onde"

# The corpus's top two translators under the old scheme, which ranks them 0.22 points
# apart over 67 languages. The same default as eval5_jev.py, because the point of running
# this scheme here is that it is the same targets.
DEFAULT_TRANSLATORS = ("gpt-5.6-luna", "union-alpha")

# One run. Experiment 12's README section 3.1 measured this evaluator's run-to-run range
# at 1.12 points on the five-criterion rubric and found run 1 alone reproducing the median
# of three at Spearman 1.000; experiment 11 section 3.6 puts the 50-item range at 2.25,
# which is larger but still far below anything a second run would resolve. Pass --runs 3
# to re-measure it on a new model version.
RUNS = 1
ATTEMPTS = 3

# Carried over from eval50.py rather than imported from it: that module is the generative
# evaluator's script, and importing it here would pull an LLM client and its dependencies
# into a run that never calls one.
VERDICT_SCORES = {"yes": 2, "partial": 1, "no": 0}


def chunks_for(split):
    """Split the item ids into the batches sent to the model, one batch per call."""
    if split == "none":
        return [ITEM_IDS]
    if split == "group":
        return [[i for i in ITEM_IDS if i[0] == g] for g in GROUPS]
    return [[i] for i in ITEM_IDS]


def tally(evaluation):
    """Convert verdicts into per-group subtotals and a 0-100 total."""
    group_scores = {g: 0 for g in GROUPS}
    for item_id in ITEM_IDS:
        group_scores[item_id[0]] += VERDICT_SCORES[evaluation[item_id]]
    return group_scores, sum(group_scores.values())


def load_targets(translators):
    """(translator, lang, lang_name) for every language each named translator covers.

    Identical to eval5_jev.py's, so the two schemes cannot drift onto different targets.
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


def label_for(translator, lang, lang_name, eval_dir_name):
    """The status line's description for one target."""
    return f"{translator} / {lang}: {lang_name} / {eval_dir_name}"

# A version, not the `jev-latest` alias: a model release must not silently make later
# runs incomparable with the ones already in evals-jev/. Bump this deliberately and
# re-run the whole directory. `client.models.list()` advertises only the aliases, so the
# version a release resolves to has to be read off a response (or the docs) -- which is
# also why every response's own version is checked against what was requested.
DEFAULT_MODEL = "jev-1.13.0"

# Rubric levels in ascending order, so a level's index is already its point value and
# matches eval50.VERDICT_SCORES. The wording is ANCHOR's, rephrased to stand alone:
# a Score level is read on its own, not as one bullet of a list the model was shown.
LEVELS = [
    ("no", "The property fails repeatedly, or across a wide part of the translation: "
           "roughly four lines or more, or a single occurrence whose effect spreads "
           "through the whole text."),
    ("partial", "The property mostly holds. The exceptions are scattered and confined "
                "to roughly one to three lines."),
    ("yes", "The property holds throughout the translation; not a single instance of "
            "the defect."),
]
VERDICTS = [verdict for verdict, _ in LEVELS]
CRITERIA_LEVELS = [description for _, description in LEVELS]

assert all(VERDICT_SCORES[v] == i for i, v in enumerate(VERDICTS)), \
    "level order must match eval50's point values"

# Confidence at or below which an item is reported as one the evaluator had little to go
# on for. It is a reporting threshold only and never changes a verdict. 0.5 sits halfway
# between the 0.33 of a flat distribution over the three levels and certainty; on the
# first measured target it flagged 35 of 50 items, so it is currently reporting how
# unsure Jev is about this task rather than singling out a few items.
LOW_CONFIDENCE = 0.5


def build_state(original_text, translated_text, from_lang, to_lang):
    """Named JSON state: both texts plus the facts every item is judged against.

    The items themselves are deliberately not listed here: each question already carries
    its own property, and a state-side copy of all 50 would put 49 irrelevant properties
    in front of every question.
    """
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


def build_questions(item_ids):
    """One Score per item, all sharing the same three rubric levels.

    The property goes in `instructions` rather than into every level, because the levels
    say how far a property holds and are the same for all 50 items; only what is being
    judged changes.
    """
    return {
        item_id: Score(
            instructions={
                "judge": "How far does `translation` satisfy the property below, "
                         "read against `original`?",
                "property": CRITERIA[item_id],
                "scope": "Judge this property alone. Every other kind of defect is "
                         "asked about by its own question.",
            },
            criteria=CRITERIA_LEVELS,
        )
        for item_id in item_ids
    }


def read_answers(response, item_ids):
    """Turn one response into {item_id: (verdict, expected score, confidence, probs)}.

    The verdict is the most probable level, which is what makes the output comparable
    with a generative evaluator's; the expected score is Jev's own weighted position on
    the same 0-2 scale, kept because rounding it to a verdict is what throws away the
    resolution this variant exists to gain.
    """
    answers = {}
    for item_id in item_ids:
        answer = response.scores.get(item_id)
        if answer is None:
            raise ValueError(f"no answer for {item_id}")
        probabilities = {int(level): float(p) for level, p in answer.probabilities.items()}
        if set(probabilities) != set(range(len(LEVELS))):
            raise ValueError(f"unexpected levels for {item_id}: {sorted(probabilities)}")
        level = max(probabilities, key=lambda k: probabilities[k])
        answers[item_id] = (VERDICTS[level], answer.score, answer.confidence, probabilities)
    return answers


def evaluate(client, args, state):
    """Ask every chunk and merge the answers, returning them, the summed Usage and the
    resolved model version every response agreed on.

    A version other than args.expect_model raises SystemExit rather than an ordinary
    exception, so it aborts the batch instead of being retried: the alias having moved is
    not a transient failure, and each retry is another 50 questions billed.
    """
    merged = {}
    usage = Usage()
    served = None
    for item_ids in chunks_for(args.split):
        response = client.system_one(state, build_questions(item_ids), model=args.model)
        if args.expect_model and response.model != args.expect_model:
            raise SystemExit(
                f"requested {args.model} but {response.model} answered, and the run is "
                f"pinned to {args.expect_model}. Results already in the output directory "
                f"were produced by {args.expect_model}; bump DEFAULT_MODEL and re-run the "
                f"whole directory, or pass --expect-model to override.")
        served = response.model
        merged.update(read_answers(response, item_ids))
        if response.usage:
            usage = usage + Usage(raw={"input_tokens": response.usage.input_tokens,
                                       "output_tokens": response.usage.output_tokens})
    return merged, usage, served


def expected_tally(answers):
    """Per-group subtotals and total from the expected scores, before rounding.

    The same arithmetic as eval50.tally, on Jev's weighted positions instead of the
    verdicts they round to, so the two totals sit side by side in the output file.
    """
    group_scores = {g: 0.0 for g in GROUPS}
    for item_id in ITEM_IDS:
        group_scores[item_id[0]] += answers[item_id][1]
    return group_scores, sum(group_scores.values())


def run(client, args, ui):
    """Evaluate one translation and write the result.

    Returns this run's Usage and the model version that produced it, so the usage
    record is filed under the version billed rather than under the alias requested.
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

    evaluation = {item_id: answers[item_id][0] for item_id in ITEM_IDS}
    group_scores, total_score = tally(evaluation)
    expected_group_scores, expected_total = expected_tally(answers)

    ui.write("=== 50-item Evaluation Result (Jev) ===\n")
    width = max(len(name) for name in GROUPS.values())
    for group, name in GROUPS.items():
        ui.write(f"{group.upper()}. {name.ljust(width)}: {group_scores[group]:2d}/20 "
                 f"(expected {expected_group_scores[group]:5.1f})\n")
    ui.write(f"Total score: {total_score}/100 (expected {expected_total:.1f})\n")

    counts = {v: 0 for v in VERDICT_SCORES}
    for verdict in evaluation.values():
        counts[verdict] += 1
    ui.write(f"Verdicts: yes={counts['yes']} partial={counts['partial']} no={counts['no']}\n")

    confidences = [answers[i][2] for i in ITEM_IDS]
    low = sum(1 for c in confidences if c <= LOW_CONFIDENCE)
    ui.write(f"Confidence: mean {sum(confidences) / len(confidences):.2f}, "
             f"{low} item(s) at or below {LOW_CONFIDENCE}\n")
    ui.write(f"Duration: {duration_seconds:.1f}s\n")
    ui.write(f"Model: {served_model}\n")
    ui.write(f"{usage}\n")

    if args.output_file:
        output_data = {
            "original_file": args.original,
            "translation_file": args.translation,
            "source_language": args.from_lang,
            "target_language": args.to_lang,
            # The version the API resolved the request to, not the alias asked for:
            # that is what the verdicts below actually came from.
            "model_used": served_model,
            "model_requested": args.model,
            "split": args.split,
            "duration_seconds": round(duration_seconds, 1),
            "evaluation": evaluation,
            "group_scores": group_scores,
            "total_score": total_score,
            # Everything below is Jev's own output, which agg50.py and refcmp.py ignore.
            "expected_scores": {i: round(answers[i][1], 4) for i in ITEM_IDS},
            "expected_group_scores": {g: round(s, 4)
                                      for g, s in expected_group_scores.items()},
            "expected_total_score": round(expected_total, 4),
            "confidence": {i: round(answers[i][2], 4) for i in ITEM_IDS},
            "probabilities": {i: {VERDICTS[level]: round(p, 4)
                                  for level, p in sorted(answers[i][3].items())}
                              for i in ITEM_IDS},
            "usage": usage.to_dict(),
        }
        Path(args.output_file).write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        ui.write(f"\nSaved evaluation result as JSON: {args.output_file}\n")

    return usage, served_model


def evaluate_target(client, make_args, runs, attempts, index, total, usage_path, ui):
    """Run one target for `runs` runs, retrying each up to `attempts` times.

    The StatusLine and its progress bar belong to the batch and are passed in: the bar
    counts targets finished out of the whole run, so a target must not open one of its
    own. Experiment 11's version advanced it per request, which mattered when --split
    made a target several requests; here the bar is coarser and --split is not the
    default.

    Existing output files are skipped so a re-run fills in only what is missing, and a
    run that keeps failing stops the whole batch rather than being logged and skipped.

    The target's runs are summed into one `usage_path` entry, written once the target is
    done -- one record per target rather than per run, matching how the runs are already
    grouped everywhere else here. Each run's own Usage is in its result file regardless,
    so an interrupted target loses the shared record, not the numbers.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"TypeSafe model version (default: {DEFAULT_MODEL})")
    parser.add_argument("--expect-model",
                        help="Version the response must report, if not --model itself; "
                             "empty accepts whatever answers, which an alias needs")
    parser.add_argument("-d", "--eval-dir", default="evals50",
                        help="Result directory under experimental/13 (default: evals50)")
    parser.add_argument("translators", nargs="*", default=list(DEFAULT_TRANSLATORS),
                        help="Directory names under examples/tr/onde/, each evaluated in "
                             "every language it has (default: "
                             + " ".join(DEFAULT_TRANSLATORS) + ")")
    parser.add_argument("--runs", type=int, default=RUNS,
                        help=f"Runs per target (default: {RUNS}); 3 re-measures the "
                             "run-to-run range, which a new model version needs")
    parser.add_argument("--split", choices=["none", "group", "item"], default="none",
                        help="Items per request: all 50, 10, or 1. Splitting resends the "
                             "state per request, so it costs several times as much")
    parser.add_argument("--timeout", type=float, default=120.0,
                        help="Per-request timeout in seconds (default: 120)")
    cli_args = parser.parse_args()

    # A version is its own pin; only an alias needs --expect-model spelled out.
    expect_model = (cli_args.model if cli_args.expect_model is None
                    else cli_args.expect_model)

    eval_dir = BASE_DIR / cli_args.eval_dir
    eval_dir.mkdir(parents=True, exist_ok=True)
    usage_path = find_usage_file()

    targets = load_targets(cli_args.translators)
    total = len(targets)
    index = 0
    total_usage = Usage()

    # One StatusLine and one bar for the whole batch, counting targets finished out of
    # all of them. No `start`: it would add an elapsed column measured from the batch
    # start, which is what the trailing clock already shows now that one task spans the
    # whole run.
    ui = StatusLine(label=label_for(*targets[0], cli_args.eval_dir))
    with TypeSafeClient(timeout=cli_args.timeout) as client, \
            ui.progress(total, start=0) as prog:
        for translator, lang, lang_name in targets:
            index += 1
            label = label_for(translator, lang, lang_name, cli_args.eval_dir)
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
                    split=cli_args.split, run=run_no, runs=cli_args.runs,
                    label=label,
                )

            total_usage = total_usage + evaluate_target(
                client, make_args, cli_args.runs, ATTEMPTS, index, total, usage_path, ui)
            prog.update(index, label)

    print(f"\nTotal usage: {total_usage}\n")
    print_today_totals(usage_path)


if __name__ == "__main__":
    main()
