#!/usr/bin/env python3
"""Experiment 11: evaluates every target under one evaluator model against 50
yes/partial/no items, three runs each.

The production evaluator (trtools eval) asks for five scores on a 0-20 scale, which
leaves the evaluator model a 20-point range of discretion per criterion. This script
replaces that with 50 concrete properties judged on three levels, to test whether the
score stops depending on which evaluator model is used, and on which run.

Scoring: yes=2, partial=1, no=0, summed over 50 items, so the scale stays 0-100.

Judging 50 items in a single call may exceed what a model can hold together, so the
item set is data and the schema is built from any subset of it: --split steps the
work down from one call to five (one per group) to fifty (one per item).

Handles one evaluator (-m/--model, -s/--slug) under one condition (--no-think,
--no-evidence) at a time. batch.sh loops this over the three reference evaluators
(qwen3.6, gemma4:31b, gpt-oss:120b) and all three variants; any other evaluator (e.g. a
commercial model) can be added the same way, by invoking this script directly with its
own -m/-s, without touching batch.sh or waiting for it to finish. Both write into the
same evals/evals-nt/evals-ne directories, and agg50.py picks up whatever it finds there,
keyed by the slug in the filename.

Targets come from targets.tsv (translator, lang, lang_name, ...).

Existing result files are left alone, so the script can be re-run. A call that keeps
failing stops the whole run (see evaluate_target) rather than being logged and skipped,
since a missing output file already records what didn't complete.
"""

import argparse
import json
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Literal

from pydantic import BaseModel, Field, create_model

from llm7shi import Client
from trtools.llm import init_usage_path
from trtools.statusline import StatusLine
from llm7shi.usage import Usage, append_usage, print_today_totals

from items import GROUPS, ITEM_IDS, CRITERIA

BASE_DIR = Path(__file__).resolve().parent
ORIGINAL = str(BASE_DIR.parent.parent / "examples/onde-en.txt")
RUNS = 3
ATTEMPTS = 3

VERDICT_SCORES = {"yes": 2, "partial": 1, "no": 0}


# Values a model emits when it echoes the schema instead of filling it in.
PLACEHOLDERS = {"string", "str", "...", "n/a"}

ANCHOR = """Judge each item on three levels:

- `yes`: the property holds throughout the document; not a single instance of the defect.
- `partial`: the property mostly holds but there are scattered exceptions (roughly 1-3 lines).
- `no`: the defect recurs, or it affects a wide part of the document (roughly 4 lines or more,
  or a single occurrence whose effect spreads through the whole text).

Read the ENTIRE document from beginning to end before judging."""

ANCHOR_EVIDENCE = ("Judge only what you can point at in the text: for any item you do not "
                    "answer `yes`, quote the passage that made you say so.")

ANCHOR_TAIL = ("Judge each item independently; do not let one item's verdict pull the "
               "others along.")


Verdict = Literal["yes", "partial", "no"]


class ItemJudgement(BaseModel):
    evidence: str = Field(description="One sentence at most, quoting the passage responsible. Empty when the verdict is yes.")
    verdict: Verdict = Field(description="Whether the property holds")


def build_schema(item_ids, with_evidence=True, with_comment=False):
    """Build a Pydantic model covering exactly the given items.

    Without evidence, an item's field is the bare Verdict literal rather than a
    single-field {"verdict": ...} object: models asked for a one-field object tend to
    flatten it and hand back the value directly anyway (see check_sane / verdict_of),
    so asking for the flat shape up front matches what they actually produce.
    """
    judgement = ItemJudgement if with_evidence else Verdict
    fields = {
        item_id: (judgement, Field(description=CRITERIA[item_id]))
        for item_id in item_ids
    }
    if with_comment:
        fields["overall_comment"] = (
            str,
            Field(description="Overall comment on the translation quality as a whole"),
        )
    return create_model("Evaluation", **fields)


def chunks_for(split):
    """Split the item ids into the batches sent to the model, one batch per call."""
    if split == "none":
        return [ITEM_IDS]
    if split == "group":
        return [[i for i in ITEM_IDS if i[0] == g] for g in GROUPS]
    return [[i] for i in ITEM_IDS]


def verdict_of(judged):
    """A judged item's verdict, whichever shape it came back as.

    build_schema asks for a bare Verdict literal when evidence is off, but a model can
    still wrap it in a single-field {"verdict": ...} object out of habit (the reverse of
    the flattening this schema shape was chosen to avoid -- see build_schema), so both
    shapes are accepted here rather than only the one the schema requested.
    """
    return judged["verdict"] if isinstance(judged, dict) else judged


def check_sane(result, item_ids, with_evidence):
    """Reject degenerate output so the run is retried instead of recorded.

    Existing runs show two failure shapes: every criterion scored 0 with an empty
    rationale, and schema placeholders emitted verbatim. Both look like real data
    downstream, so they have to be caught here. An all-yes verdict with no evidence
    is not degenerate -- that is what a clean translation looks like.
    """
    verdicts = []
    for item_id in item_ids:
        judged = result.get(item_id)
        verdict = verdict_of(judged) if isinstance(judged, dict) else judged
        if verdict not in VERDICT_SCORES:
            raise ValueError(f"missing/invalid verdict for {item_id}: {judged!r}")
        verdicts.append(verdict)
        if isinstance(judged, dict):
            evidence = judged.get("evidence", "")
            if evidence.strip().lower() in PLACEHOLDERS:
                raise ValueError(f"placeholder evidence for {item_id}: {evidence!r}")

    if with_evidence and all(v != "yes" for v in verdicts):
        if not any(isinstance(result[i], dict) and result[i].get("evidence", "").strip()
                   for i in item_ids):
            raise ValueError("every item reports a defect but none cites evidence")

    comment = result.get("overall_comment", "")
    if comment.strip().lower() in PLACEHOLDERS:
        raise ValueError(f"placeholder overall_comment: {comment!r}")


def evaluate(client, original_text, translated_text, from_lang, to_lang, split,
             no_evidence=False, prog=None, done=0):
    """Run every chunk and merge the judgements into one dict.

    Each chunk is one call, so the progress bar advances per chunk: with --split that
    is real movement through the item list, and with a single call it still marks the
    run as finished.
    """
    # --split item calls are one item at a time with no shared context, so there is
    # nothing to summarise at the "last" call -- overall_comment stays off there
    # regardless of --no-evidence.
    has_context = split != "item"
    with_evidence = has_context and not no_evidence
    batches = chunks_for(split)
    merged = {}
    n_lines = original_text.count("\n") + 1

    for n, item_ids in enumerate(batches, 1):
        last = n == len(batches)
        schema = build_schema(item_ids, with_evidence, with_comment=last and has_context)
        anchor = ANCHOR
        if with_evidence:
            anchor += f" {ANCHOR_EVIDENCE}"
        anchor += f" {ANCHOR_TAIL}"
        task = (
            f"Evaluate this translation from {from_lang} to {to_lang}.\n\n"
            f"Both texts have {n_lines} lines, and line i of the translation is meant to "
            f"render line i of the original.\n\n{anchor}"
        )
        if len(batches) > 1:
            task += f"\n\nThis pass covers {len(item_ids)} of the {len(ITEM_IDS)} items."
        prompts = [
            f"<original>\n{original_text}\n</original>",
            f"<translation>\n{translated_text}\n</translation>",
            task,
        ]
        data = client(prompts, schema=schema).data
        if data is None:
            raise ValueError(f"no valid JSON after {client.retries} attempts")
        result = data.model_dump()
        check_sane(result, item_ids, with_evidence)
        merged.update(result)
        if prog is not None:
            prog.update(done + n)

    return merged


def tally(evaluation):
    """Convert verdicts into per-group subtotals and a 0-100 total."""
    group_scores = {g: 0 for g in GROUPS}
    for item_id in ITEM_IDS:
        score = VERDICT_SCORES[verdict_of(evaluation[item_id])]
        group_scores[item_id[0]] += score
    return group_scores, sum(group_scores.values())


def run(args, ui, prog, done):
    """Evaluate one translation and write the result, given an args namespace.

    Built by evaluate_target(), which also builds `ui` and `prog` -- shared across
    all of a target's runs, so the whole target advances one continuous progress bar
    instead of each run opening and freezing its own. `done` is this run's starting
    offset into that shared bar. Returns the Usage summed over every LLM call this
    evaluation made.
    """
    original_text = Path(args.original).read_text(encoding="utf-8").rstrip()
    translated_text = Path(args.translation).read_text(encoding="utf-8").rstrip()

    orig_lines = original_text.count("\n") + 1
    tr_lines = translated_text.count("\n") + 1
    if orig_lines != tr_lines:
        ui.write(f"Warning: line count mismatch ({orig_lines} vs {tr_lines})\n")

    client = Client(model=args.model, include_thoughts=(not args.no_think), file=ui.stream,
                    show_params=False, max_length=8192, keep_history=False,
                    add_json_descriptions=True)

    call_start = args.attempt_start if args.attempt_start is not None else time.time()
    evaluation = evaluate(client, original_text, translated_text,
                          args.from_lang, args.to_lang, args.split,
                          no_evidence=args.no_evidence, prog=prog, done=done)
    ui.stream.end()
    duration_seconds = time.time() - call_start

    group_scores, total_score = tally(evaluation)

    ui.write("=== 50-item Evaluation Result ===\n")
    width = max(len(name) for name in GROUPS.values())
    for group, name in GROUPS.items():
        ui.write(f"{group.upper()}. {name.ljust(width)}: {group_scores[group]:2d}/20\n")
    ui.write(f"Total score: {total_score}/100\n")

    counts = {v: 0 for v in VERDICT_SCORES}
    for item_id in ITEM_IDS:
        counts[verdict_of(evaluation[item_id])] += 1
    ui.write(f"Verdicts: yes={counts['yes']} partial={counts['partial']} no={counts['no']}\n")
    ui.write(f"Duration: {duration_seconds:.1f}s\n")

    usage = sum(client.usages, Usage())
    ui.write(f"{usage}\n")

    if args.output_file:
        output_data = {
            "original_file": args.original,
            "translation_file": args.translation,
            "source_language": args.from_lang,
            "target_language": args.to_lang,
            "model_used": args.model,
            "split": args.split,
            "no_think": args.no_think,
            "no_evidence": args.no_evidence,
            "duration_seconds": round(duration_seconds, 1),
            "evaluation": evaluation,
            "group_scores": group_scores,
            "total_score": total_score,
        }
        Path(args.output_file).write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        ui.write(f"\nSaved evaluation result as JSON: {args.output_file}\n")

    return usage


def evaluate_target(make_args, runs, attempts, index, total):
    """Run one target for `runs` runs, retrying each up to `attempts` times.

    `make_args(run_no)` builds the run() namespace for one run; its output_file is
    checked first, so re-running the batch retries only what's missing. A run that
    keeps failing stops the whole batch (see main()) rather than being logged and
    skipped, since a missing output file already records what didn't complete.

    `index`/`total` count targets, not runs (matching trtools.batch's ev_index). A
    single StatusLine/progress bar is opened for the whole target and shared across
    its `runs` runs, rather than each run opening and freezing its own -- that
    per-run open/close is what left a stack of frozen bars behind. Nothing is opened
    at all when every run is already done: that case has no work to show progress on.

    Returns a list of (output_path, Usage) for the runs actually executed.
    """
    args0 = make_args(1)
    steps = len(chunks_for(args0.split))

    pending = []
    for run_no in range(1, runs + 1):
        args = make_args(run_no)
        args.index = index
        args.count = total
        out = Path(args.output_file)
        if out.is_file():
            print(f"[{index}/{total}] exists, skipping: {out}")
        else:
            pending.append((run_no, args, out))

    if not pending:
        return []

    ui = StatusLine(label=args0.label, start=args0.start, index=index, count=total)
    results = []
    with ui.progress(runs * steps, start=(pending[0][0] - 1) * steps) as prog:
        for run_no, args, out in pending:
            done = (run_no - 1) * steps
            ui.write(f"\n=== [{index}/{total}] {args.label} run {run_no} ===\n")
            for attempt in range(1, attempts + 1):
                try:
                    usage = run(args, ui, prog, done)
                    break
                except Exception as e:
                    ui.write(f"  attempt {attempt}/{attempts} failed for {out}: {e}\n")
                    out.unlink(missing_ok=True)
            else:
                raise SystemExit(f"GIVING UP on {out}")
            results.append((out, usage))
    return results


def variant_dir(no_think, no_evidence):
    if no_think:
        return "evals-nt"
    if no_evidence:
        return "evals-ne"
    return "evals"


def load_targets(path):
    """Read (translator, lang, lang_name) from targets.tsv, skipping its header row."""
    targets = []
    for line in Path(path).read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip():
            fields = line.split("\t")
            targets.append((fields[0], fields[1], fields[2]))
    return targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--model", required=True, help="Evaluator model")
    parser.add_argument("-s", "--slug", required=True,
                        help="Name used for this evaluator in result filenames")
    parser.add_argument("--no-think", action="store_true", help="Disable thinking")
    parser.add_argument("--no-evidence", action="store_true",
                        help="Drop the per-item evidence field")
    parser.add_argument("--targets", default=str(BASE_DIR / "targets.tsv"))
    parser.add_argument("--runs", type=int, default=RUNS)
    parser.add_argument("--split", choices=["none", "group", "item"], default="none")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name")
    cli_args = parser.parse_args()

    variant = variant_dir(cli_args.no_think, cli_args.no_evidence)
    eval_dir = BASE_DIR / variant
    eval_dir.mkdir(parents=True, exist_ok=True)

    usage_path = init_usage_path(cli_args.model, cli_args.save_usage)

    targets = load_targets(cli_args.targets)
    total = len(targets)
    index = 0
    batch_start = time.time()
    total_usage = Usage()

    for translator, lang, lang_name in targets:
        tr_file = BASE_DIR.parent.parent / f"examples/tr/onde/{translator}/tr/onde-{lang}.txt"
        if not tr_file.is_file():
            print(f"Missing translation, skipping: {tr_file}")
            continue

        stem = f"onde-{translator}-{lang}-{cli_args.slug}"
        label = f"{lang}: {lang_name} / {cli_args.slug} / {variant}"

        def make_args(run_no):
            return SimpleNamespace(
                original=ORIGINAL, translation=str(tr_file),
                model=cli_args.model, from_lang="English", to_lang=lang_name,
                output_file=str(eval_dir / f"{stem}-{run_no}.json"),
                no_think=cli_args.no_think, no_evidence=cli_args.no_evidence,
                split=cli_args.split, run=run_no, runs=cli_args.runs,
                label=label, start=batch_start, attempt_start=time.time(),
            )

        index += 1
        results = evaluate_target(make_args, cli_args.runs, ATTEMPTS, index, total)

        if usage_path is not None:
            for out, usage in results:
                append_usage(usage, cli_args.model, usage_path)
                total_usage = total_usage + usage

    if usage_path is not None:
        print(f"\nTotal usage: {total_usage}\n")
        print_today_totals(usage_path)


if __name__ == "__main__":
    main()
