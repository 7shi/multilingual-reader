#!/usr/bin/env python3
"""Experiment 11: evaluates a translation against 50 yes/partial/no items.

The production evaluator (trtools eval) asks for five scores on a 0-20 scale, which
leaves the evaluator model a 20-point range of discretion per criterion. This script
replaces that with 50 concrete properties judged on three levels, to test whether the
score stops depending on which evaluator model is used, and on which run.

Scoring: yes=2, partial=1, no=0, summed over 50 items, so the scale stays 0-100.

Judging 50 items in a single call may exceed what a model can hold together, so the
item set is data and the schema is built from any subset of it: --split steps the
work down from one call to five (one per group) to fifty (one per item).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, create_model

sys.path.insert(0, str(Path(__file__).resolve().parent))

from items import GROUPS, ITEMS, ITEM_IDS, CRITERIA  # noqa: E402

from trtools.llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS  # noqa: E402
from trtools.statusline import StatusLine  # noqa: E402

VERDICT_SCORES = {"yes": 2, "partial": 1, "no": 0}

# Values a model emits when it echoes the schema instead of filling it in.
PLACEHOLDERS = {"string", "str", "...", "n/a"}

ANCHOR = """Judge each item on three levels:

- `yes`: the property holds throughout the document; not a single instance of the defect.
- `partial`: the property mostly holds but there are scattered exceptions (roughly 1-3 lines).
- `no`: the defect recurs, or it affects a wide part of the document (roughly 4 lines or more,
  or a single occurrence whose effect spreads through the whole text).

Read the ENTIRE document from beginning to end before judging. Judge only what you can point
at in the text: for any item you do not answer `yes`, quote the passage that made you say so.
Judge each item independently; do not let one item's verdict pull the others along."""


class ItemJudgement(BaseModel):
    evidence: str = Field(description="One sentence at most, quoting the passage responsible. Empty when the verdict is yes.")
    verdict: Literal["yes", "partial", "no"] = Field(description="Whether the property holds")


class BareJudgement(BaseModel):
    verdict: Literal["yes", "partial", "no"] = Field(description="Whether the property holds")


def build_schema(item_ids, with_evidence=True, with_comment=False):
    """Build a Pydantic model covering exactly the given items."""
    judgement = ItemJudgement if with_evidence else BareJudgement
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


def check_sane(result, item_ids, with_evidence):
    """Reject degenerate output so call_json retries instead of recording it.

    Existing runs show two failure shapes: every criterion scored 0 with an empty
    rationale, and schema placeholders emitted verbatim. Both look like real data
    downstream, so they have to be caught here. An all-yes verdict with no evidence
    is not degenerate -- that is what a clean translation looks like.
    """
    verdicts = []
    for item_id in item_ids:
        judged = result.get(item_id)
        if not isinstance(judged, dict) or "verdict" not in judged:
            raise ValueError(f"missing verdict for {item_id}")
        verdicts.append(judged["verdict"])
        evidence = judged.get("evidence", "")
        if evidence.strip().lower() in PLACEHOLDERS:
            raise ValueError(f"placeholder evidence for {item_id}: {evidence!r}")

    if with_evidence and all(v != "yes" for v in verdicts):
        if not any(result[i].get("evidence", "").strip() for i in item_ids):
            raise ValueError("every item reports a defect but none cites evidence")

    comment = result.get("overall_comment", "")
    if comment.strip().lower() in PLACEHOLDERS:
        raise ValueError(f"placeholder overall_comment: {comment!r}")


def evaluate(client, original_text, translated_text, from_lang, to_lang, split, file,
             prog=None, done=0):
    """Run every chunk and merge the judgements into one dict.

    Each chunk is one call, so the progress bar advances per chunk: with --split that
    is real movement through the item list, and with a single call it still marks the
    run as finished.
    """
    with_evidence = split != "item"
    batches = chunks_for(split)
    merged = {}
    n_lines = original_text.count("\n") + 1

    for n, item_ids in enumerate(batches, 1):
        last = n == len(batches)
        schema = build_schema(item_ids, with_evidence, with_comment=last and with_evidence)
        task = (
            f"Evaluate this translation from {from_lang} to {to_lang}.\n\n"
            f"Both texts have {n_lines} lines, and line i of the translation is meant to "
            f"render line i of the original.\n\n{ANCHOR}"
        )
        if len(batches) > 1:
            task += f"\n\nThis pass covers {len(item_ids)} of the {len(ITEM_IDS)} items."
        prompts = [
            f"<original>\n{original_text}\n</original>",
            f"<translation>\n{translated_text}\n</translation>",
            task,
        ]
        result = client.call_json(prompts, schema=schema, file=file)
        check_sane(result, item_ids, with_evidence)
        merged.update(result)
        if prog is not None:
            prog.update(done + n)

    return merged


def tally(evaluation):
    """Convert verdicts into per-group subtotals and a 0-100 total."""
    group_scores = {g: 0 for g in GROUPS}
    for item_id in ITEM_IDS:
        score = VERDICT_SCORES[evaluation[item_id]["verdict"]]
        group_scores[item_id[0]] += score
    return group_scores, sum(group_scores.values())


def main():
    parser = argparse.ArgumentParser(description="Evaluate a translation on 50 yes/partial/no items")
    parser.add_argument("--original", required=True, help="Original text file")
    parser.add_argument("--translation", required=True, help="Translated text file")
    parser.add_argument("-m", "--model", required=True, help="Model used for evaluation")
    parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language")
    parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language")
    parser.add_argument("-o", "--output", dest="output_file", help="Filename to save the evaluation result as JSON")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"Wait time on retry, in seconds (default: {DEFAULT_RETRY_WAIT_SECONDS}s)")
    parser.add_argument("--no-think", action="store_true", help="Disable thinking")
    parser.add_argument("--split", choices=["none", "group", "item"], default="none",
                        help="How many calls to spread the 50 items over (default: none, a single call)")
    parser.add_argument("--run", type=int, default=1, help="Current evaluation run number")
    parser.add_argument("--runs", type=int, default=1, help="Total number of evaluation runs")
    parser.add_argument("--label", help="Label shown on the status line")
    parser.add_argument("--start", type=float, help="Batch start time (Unix timestamp)")
    parser.add_argument("--index", type=int, help="Position of this evaluation within the batch")
    parser.add_argument("--count", type=int, help="Total number of evaluations in the batch")
    args = parser.parse_args()

    ui = StatusLine(label=args.label, start=args.start, index=args.index, count=args.count)

    original_text = Path(args.original).read_text(encoding="utf-8").rstrip()
    translated_text = Path(args.translation).read_text(encoding="utf-8").rstrip()

    orig_lines = original_text.count("\n") + 1
    tr_lines = translated_text.count("\n") + 1
    if orig_lines != tr_lines:
        ui.write(f"Warning: line count mismatch ({orig_lines} vs {tr_lines})\n")

    client = LLMClient(model=args.model, think=(not args.no_think), retry_wait=args.retry_wait)

    # One step per call, so a split run shows progress through the item list rather
    # than sitting still until the whole evaluation is done.
    steps = len(chunks_for(args.split))
    done = (args.run - 1) * steps
    with ui.progress(args.runs * steps, start=done) as prog:
        evaluation = evaluate(client, original_text, translated_text,
                              args.from_lang, args.to_lang, args.split, ui.stream,
                              prog=prog, done=done)
        ui.stream.end()

    group_scores, total_score = tally(evaluation)

    ui.write("=== 50-item Evaluation Result ===\n")
    width = max(len(name) for name in GROUPS.values())
    for group, name in GROUPS.items():
        ui.write(f"{group.upper()}. {name.ljust(width)}: {group_scores[group]:2d}/20\n")
    ui.write(f"Total score: {total_score}/100\n")

    counts = {v: 0 for v in VERDICT_SCORES}
    for item_id in ITEM_IDS:
        counts[evaluation[item_id]["verdict"]] += 1
    ui.write(f"Verdicts: yes={counts['yes']} partial={counts['partial']} no={counts['no']}\n")

    if args.output_file:
        output_data = {
            "original_file": args.original,
            "translation_file": args.translation,
            "source_language": args.from_lang,
            "target_language": args.to_lang,
            "model_used": args.model,
            "split": args.split,
            "evaluation": evaluation,
            "group_scores": group_scores,
            "total_score": total_score,
        }
        Path(args.output_file).write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        ui.write(f"\nSaved evaluation result as JSON: {args.output_file}\n")


if __name__ == "__main__":
    main()
