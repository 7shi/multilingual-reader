#!/usr/bin/env python3
"""Experiment 11: evaluates every target under one evaluator model, three runs.

Handles one evaluator (-m/--model, -s/--slug) under one condition (--no-think,
--no-evidence) at a time. batch.sh loops this over the three reference evaluators
(qwen3.6, gemma4:31b, gpt-oss:120b) and all three variants; any other evaluator (e.g. a
commercial model) can be added the same way, by invoking this script directly with its
own -m/-s, without touching batch.sh or waiting for it to finish. Both write into the
same evals/evals-nt/evals-ne directories, and agg50.py picks up whatever it finds there,
keyed by the slug in the filename.

Targets come from targets.tsv (translator, lang, lang_name, ...).

Calls eval50.run() in-process rather than shelling out to a subprocess per evaluation.

Existing result files are left alone, so the script can be re-run. A call that keeps
failing stops the whole run (see try_eval) rather than being logged and skipped, since a
missing output file already records what didn't complete.
"""

import argparse
import time
from pathlib import Path
from types import SimpleNamespace

from trtools.llm import DEFAULT_RETRY_WAIT_SECONDS

import eval50

BASE_DIR = Path(__file__).resolve().parent
ORIGINAL = str(BASE_DIR.parent.parent / "examples/onde-en.txt")
RUNS = 3
ATTEMPTS = 3


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


def try_eval(out, args):
    """Retry a failing call up to ATTEMPTS times, then stop the batch.

    A failure leaves no output file, which is itself the record of what didn't
    complete -- re-running the batch retries exactly those, so nothing else needs
    to track failures separately.
    """
    for attempt in range(1, ATTEMPTS + 1):
        try:
            eval50.run(args)
            return
        except Exception as e:
            print(f"  attempt {attempt}/{ATTEMPTS} failed for {out}: {e}")
            out.unlink(missing_ok=True)
    raise SystemExit(f"GIVING UP on {out}")


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
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS)
    cli_args = parser.parse_args()

    variant = variant_dir(cli_args.no_think, cli_args.no_evidence)
    eval_dir = BASE_DIR / variant
    eval_dir.mkdir(parents=True, exist_ok=True)

    targets = load_targets(cli_args.targets)
    total = len(targets) * cli_args.runs
    index = 0
    batch_start = time.time()

    for translator, lang, lang_name in targets:
        tr_file = BASE_DIR.parent.parent / f"examples/tr/onde/{translator}/tr/onde-{lang}.txt"
        if not tr_file.is_file():
            print(f"Missing translation, skipping: {tr_file}")
            continue

        stem = f"onde-{translator}-{lang}-{cli_args.slug}"
        label = f"{lang}: {lang_name} / {cli_args.slug} / {variant}"

        for run in range(1, cli_args.runs + 1):
            out = eval_dir / f"{stem}-{run}.json"
            index += 1
            if out.is_file():
                print(f"[{index}/{total}] exists, skipping: {out}")
                continue
            print(f"\n=== [{index}/{total}] {translator}/{lang} {cli_args.slug} {variant} run {run} ===")
            attempt_start = time.time()
            args = SimpleNamespace(
                original=ORIGINAL, translation=str(tr_file),
                model=cli_args.model, from_lang="English", to_lang=lang_name,
                output_file=str(out), retry_wait=cli_args.retry_wait,
                no_think=cli_args.no_think, no_evidence=cli_args.no_evidence,
                split=cli_args.split, run=run, runs=cli_args.runs,
                label=label, start=batch_start, attempt_start=attempt_start,
                index=index, count=total,
            )
            try_eval(out, args)


if __name__ == "__main__":
    main()
