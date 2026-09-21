#!/usr/bin/env python3
"""Compares how much the old and new evaluation schemes wobble.

For each translation and evaluator, both schemes were run five times. The question
is whether replacing five 0-20 scores with fifty yes/partial/no judgements makes the
result depend less on the run and less on which evaluator model was used.

Reads experimental/11/evals for the new scheme and cites the old scheme's results where
they already live, under examples/tr/onde/*/evals/, without copying them anywhere.
Writes a Markdown report to stdout.
"""

import argparse
import json
import re
from pathlib import Path
from statistics import median, pstdev

from items import GROUPS, ITEM_IDS

BASE = Path(__file__).resolve().parent
ONDE = Path("examples/tr/onde")
OLD_RUNS = (1, 2, 3)
OLD_CRITERIA = ["readability", "fluency", "terminology",
                "contextual_adaptation", "information_completeness"]
VERDICT_SCORES = {"yes": 2, "partial": 1, "no": 0}
NAME_RE = re.compile(r"^onde-(.+)-([a-z]{2})-(.+)-(\d+)\.json$")


def load_old(targets, reference):
    """Cite the accumulated old-scheme results in place.

    examples/tr/onde/*/evals/ holds three runs per translation, produced by the
    reference evaluator under the old scheme. They are read where they are; nothing
    is copied into this directory.
    """
    runs = {}
    for translator, lang in targets:
        for run in OLD_RUNS:
            path = ONDE / translator / "evals" / f"onde-{lang}-{run}.json"
            if not path.exists():
                print(f"<!-- missing: {path} -->")
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                print(f"<!-- unreadable: {path} -->")
                continue
            runs.setdefault((translator, lang, reference), {})[run] = data
    return runs


def load(directory):
    """Collect {(translator, lang, evaluator): {run: data}} from a directory."""
    runs = {}
    d = BASE / directory
    if not d.is_dir():
        return runs
    for path in sorted(d.iterdir()):
        m = NAME_RE.match(path.name)
        if not m:
            continue
        translator, lang, evaluator, run = m.groups()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print(f"<!-- unreadable: {path.name} -->")
            continue
        runs.setdefault((translator, lang, evaluator), {})[int(run)] = data
    return runs


def load_timing(directory):
    """Per-call duration, keyed by evaluator.

    Each result file records its own "duration_seconds" (wall-clock time for that
    evaluation call), which is used when present. Older files written before that
    field existed fall back to the file-mtime difference between consecutive runs
    of the same (translation, evaluator): mtime(run n) - mtime(run n-1). That
    fallback cannot measure run 1 of each pair -- it would need the previous call's
    finish time, which belongs to a different (translation, evaluator) -- so runs 2
    and 3 are used instead.
    """
    mtimes = {}
    measured = {}
    d = BASE / directory
    if not d.is_dir():
        return {}
    for path in sorted(d.iterdir()):
        m = NAME_RE.match(path.name)
        if not m:
            continue
        translator, lang, evaluator, run = m.groups()
        key = (translator, lang, evaluator)
        mtimes.setdefault(key, {})[int(run)] = path.stat().st_mtime
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if "duration_seconds" in data:
            measured.setdefault(evaluator, []).append(data["duration_seconds"])

    durations = {evaluator: list(values) for evaluator, values in measured.items()}
    for key, by_run in mtimes.items():
        evaluator = key[2]
        if evaluator in durations:
            continue  # measured durations take precedence over the mtime estimate
        for run in (2, 3):
            if run in by_run and (run - 1) in by_run:
                durations.setdefault(evaluator, []).append(by_run[run] - by_run[run - 1])
    return durations


def think_vs_nothink_table(evals, evals_nt, targets, evaluators):
    """Score and timing, thinking on vs off, per translation and evaluator.

    evals/evals_nt are keyed like the `new` summary but also carry a "duration"
    entry (mean seconds per call) added by summarise() when the field is present.
    """
    lines = ["| Translation | Evaluator | Think score | No-think score | Diff | "
             "Think time | No-think time |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for translator, lang in targets:
        for evaluator in evaluators:
            t = evals.get((translator, lang, evaluator))
            nt = evals_nt.get((translator, lang, evaluator))
            if not t or not nt:
                continue
            t_time = f"{t['duration']:.0f}s" if t.get("duration") is not None else "-"
            nt_time = f"{nt['duration']:.0f}s" if nt.get("duration") is not None else "-"
            lines.append(
                f"| {translator} / {lang} | {evaluator} | {t['median_score']} "
                f"| {nt['median_score']} | {nt['median_score'] - t['median_score']:+d} "
                f"| {t_time} | {nt_time} |")
    return lines


def timing_table(durations):
    lines = ["| Evaluator | Calls | Median | Mean | Min | Max |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    all_values = []
    for evaluator in sorted(durations):
        values = durations[evaluator]
        all_values += values
        lines.append(
            f"| {evaluator} | {len(values)} | {median(values):.0f}s | "
            f"{sum(values) / len(values):.0f}s | {min(values):.0f}s | {max(values):.0f}s |")
    if all_values:
        lines.append(
            f"| all | {len(all_values)} | {median(all_values):.0f}s | "
            f"{sum(all_values) / len(all_values):.0f}s | {min(all_values):.0f}s | "
            f"{max(all_values):.0f}s |")
    return lines


def verdict_of(judged):
    """A judged item's verdict, whichever shape it came back as.

    Without evidence, an item may be the bare verdict string the schema asked for, or
    (if the model wrapped it anyway) a {"verdict": ...} object -- see eval50.py's
    verdict_of / build_schema for why both occur.
    """
    return judged["verdict"] if isinstance(judged, dict) else judged


def item_scores(data, new):
    """Per-criterion (old) or per-item (new) scores for one run."""
    ev = data["evaluation"]
    if new:
        return {i: VERDICT_SCORES[verdict_of(ev[i])] for i in ITEM_IDS}
    return {c: ev[c]["score"] for c in OLD_CRITERIA}


def summarise(runs, new):
    """Per (translation, evaluator): the run totals, their spread, and the median score.

    The median score follows trtools/aggregate.py: take the median of each criterion
    across runs, then sum. That is the number the score tables are built from, so it
    is the one worth comparing.
    """
    out = {}
    for key, by_run in runs.items():
        data_list = [by_run[r] for r in sorted(by_run)]
        totals = [d["total_score"] for d in data_list]
        per_run = [item_scores(d, new) for d in data_list]
        keys = per_run[0].keys()
        aggregated = sum(median([p[k] for p in per_run]) for k in keys)
        durations = [d["duration_seconds"] for d in data_list if "duration_seconds" in d]
        out[key] = {
            "runs": len(totals),
            "totals": totals,
            "range": max(totals) - min(totals),
            "stdev": pstdev(totals) if len(totals) > 1 else 0.0,
            "median_score": int(aggregated),
            "per_run": per_run,
            "duration": sum(durations) / len(durations) if durations else None,
        }
    return out


def fmt(values):
    return ", ".join(str(v) for v in values)


def wobble_table(old, new, targets, reference):
    """Old vs new under the reference evaluator, which is the only one the old scheme ran."""
    lines = ["| Translation | Old runs | Old range | New runs | New range | Change |",
             "| --- | --- | ---: | --- | ---: | ---: |"]
    for translator, lang in targets:
        key = (translator, lang, reference)
        o, n = old.get(key), new.get(key)
        if not o or not n:
            continue
        lines.append(
            f"| {translator} / {lang} | {fmt(o['totals'])} | {o['range']} "
            f"| {fmt(n['totals'])} | {n['range']} | {n['range'] - o['range']:+d} |")
    return lines


def new_wobble_table(new, targets, evaluators):
    """New-scheme run-to-run range under every evaluator."""
    lines = ["| Translation | " + " | ".join(evaluators) + " |",
             "| --- | " + " | ".join("---" for _ in evaluators) + " |"]
    for translator, lang in targets:
        cells = []
        for evaluator in evaluators:
            n = new.get((translator, lang, evaluator))
            cells.append(f"{fmt(n['totals'])} (range {n['range']})" if n else "-")
        lines.append(f"| {translator} / {lang} | " + " | ".join(cells) + " |")
    return lines


def evaluator_spread_table(old, new, targets, evaluators, reference):
    """How far the new scheme's score moves when the evaluator model is swapped.

    The old scheme has no counterpart here: it was only ever run under the reference
    evaluator, so its column is context, not a comparison.
    """
    lines = ["| Translation | Old (" + reference + ") | " +
             " | ".join(evaluators) + " | New spread |",
             "| --- | ---: | " + " | ".join("---:" for _ in evaluators) + " | ---: |"]
    for translator, lang in targets:
        meds = []
        for evaluator in evaluators:
            n = new.get((translator, lang, evaluator))
            meds.append(n["median_score"] if n else None)
        present = [m for m in meds if m is not None]
        if len(present) < 2:
            continue
        o = old.get((translator, lang, reference))
        cells = " | ".join("-" if m is None else str(m) for m in meds)
        lines.append(f"| {translator} / {lang} | {o['median_score'] if o else '-'} "
                     f"| {cells} | {max(present) - min(present)} |")
    return lines


def pair_gap_summary(new, targets, evaluator_a, evaluator_b):
    """Mean/mean-absolute-difference between two evaluators, in the old scheme's format.

    README's "It moves when the evaluator changes" section quotes the old scheme's
    qwen3.6-vs-gpt-oss-120b gap (mean 49.6 vs 69.5, mean absolute difference 21.6) on a
    different set of translations (examples/tr/onde/qwen3.6/*, all translated by
    qwen3.6). This computes the same statistic for the new scheme on targets.tsv's set,
    so the two are directly comparable in the same units even though the underlying
    translations differ.
    """
    a_scores, b_scores = [], []
    for translator, lang in targets:
        a = new.get((translator, lang, evaluator_a))
        b = new.get((translator, lang, evaluator_b))
        if not a or not b:
            continue
        a_scores.append(a["median_score"])
        b_scores.append(b["median_score"])
    if not a_scores:
        return None
    mean_a = sum(a_scores) / len(a_scores)
    mean_b = sum(b_scores) / len(b_scores)
    mad = sum(abs(x - y) for x, y in zip(a_scores, b_scores)) / len(a_scores)
    return mean_a, mean_b, mad, len(a_scores)


def unstable_items(new):
    """Count how often each item's verdict disagrees between runs.

    If the remaining wobble sits in a few items, their wording is at fault; if it is
    spread thinly over all fifty, the scheme itself is the limit.
    """
    counts = {i: 0 for i in ITEM_IDS}
    total = 0
    for stats in new.values():
        total += 1
        for i in ITEM_IDS:
            if len({p[i] for p in stats["per_run"]}) > 1:
                counts[i] += 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    lines = [f"Combinations measured: {total}", "",
             "| Item | Runs disagreed | Share |", "| --- | ---: | ---: |"]
    for item, n in ranked:
        if n == 0:
            continue
        lines.append(f"| {item} | {n} | {n / total:.0%} |")
    steady = sum(1 for _, n in ranked if n == 0)
    lines += ["", f"Items that never disagreed: {steady}/50"]
    return lines


def mean_of(stats, field):
    values = [v[field] for v in stats.values()]
    return sum(values) / len(values) if values else 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", default=str(BASE / "targets.tsv"))
    args = parser.parse_args()

    targets = []
    for line in Path(args.targets).read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip():
            fields = line.split("\t")
            targets.append((fields[0], fields[1]))

    reference = "qwen3.6"
    old = summarise(load_old(targets, reference), new=False)
    new = summarise(load("evals"), new=True)
    new_nt = summarise(load("evals-nt"), new=True)
    evaluators = sorted({k[2] for k in new})

    print("# Experiment 11: old vs new evaluation scheme\n")
    print(f"Old scheme: 5 criteria x 0-20. New scheme: 50 items x yes/partial/no.")
    print(f"Combinations: old {len(old)}, new {len(new)}.\n")

    rows = []
    for failures in sorted(BASE.glob("FAILURES*.txt")):
        rows += [l for l in failures.read_text(encoding="utf-8").splitlines() if l.strip()]
    if rows:
        print("## Calls that never returned usable output\n")
        print("Valid JSON that did not fit the schema, after 3 attempts. "
              "The retry inside call_json only covers decode errors, so these "
              "get through to the caller.\n")
        counts = {}
        for row in rows:
            counts[row.split("\t")[0]] = counts.get(row.split("\t")[0], 0) + 1
        for scheme in sorted(counts):
            print(f"- {scheme}: {counts[scheme]}")
        print()

    print(f"## Run-to-run wobble under the reference evaluator ({reference})\n")
    print("How far the total score moves across runs on the same translation.\n")
    print("\n".join(wobble_table(old, new, targets, reference)))
    ref_old = {k: v for k, v in old.items() if k[2] == reference}
    ref_new = {k: v for k, v in new.items() if k[2] == reference}
    print(f"\nMean range: old {mean_of(ref_old, 'range'):.1f}, new {mean_of(ref_new, 'range'):.1f}.")
    print(f"Mean stdev: old {mean_of(ref_old, 'stdev'):.2f}, new {mean_of(ref_new, 'stdev'):.2f}.\n")

    print("## Run-to-run wobble of the new scheme, by evaluator\n")
    print("\n".join(new_wobble_table(new, targets, evaluators)))
    print(f"\nMean range: {mean_of(new, 'range'):.1f}. Mean stdev: {mean_of(new, 'stdev'):.2f}.\n")

    print("## Dependence on the evaluator model\n")
    print("How far the new scheme's aggregated score moves when the evaluator is swapped.\n")
    print("\n".join(evaluator_spread_table(old, new, targets, evaluators, reference)))
    print()

    gap = pair_gap_summary(new, targets, "qwen3.6", "gpt-oss-120b")
    if gap:
        mean_q, mean_g, mad, n = gap
        print("### qwen3.6 vs gpt-oss:120b, new scheme, in the old table's terms\n")
        print("README's \"It moves when the evaluator changes\" quotes the old scheme's "
              "qwen3.6-vs-gpt-oss:120b gap (mean 49.6 vs 69.5, mean absolute difference "
              "21.6) on a different set of translations (examples/tr/onde/qwen3.6/*, all "
              f"translated by qwen3.6). The same two evaluators on the new scheme, over "
              f"targets.tsv's {n} translations:\n")
        print(f"Mean {mean_q:.1f} against {mean_g:.1f}, with a mean absolute difference of "
              f"{mad:.1f} points.\n")

    print("## Where the remaining wobble sits\n")
    print("\n".join(unstable_items(new)))
    print()

    durations = load_timing("evals")
    if durations:
        print("## Timing (new scheme, thinking on)\n")
        print("Per-call duration in seconds. Files that record their own "
              "\"duration_seconds\" use that; older files fall back to the file-mtime "
              "difference between run n and run (n-1), for n in {2, 3} -- run 1 of each "
              "(translation, evaluator) is excluded there, since it would need the "
              "previous call's finish time, which belongs to a different translation.\n")
        print("\n".join(timing_table(durations)))
        print()

    durations_nt = load_timing("evals-nt")
    if durations_nt:
        print("## Timing (new scheme, no-think)\n")
        print("\n".join(timing_table(durations_nt)))
        print()

    if new_nt:
        print("## Thinking on vs off\n")
        print("Same 50-item scheme, same targets and evaluators, run with "
              "`--no-think --no-evidence`. Score is the median-of-runs total; time is the "
              "mean call duration from \"duration_seconds\". gpt-oss:120b ignores "
              "`--no-think`, so its rows are thinking-on/evidence-off, not no-think.\n")
        print("\n".join(think_vs_nothink_table(new, new_nt, targets, evaluators)))
        print()

    print("## Group subtotals (new scheme)\n")
    print("| Translation | Evaluator | " + " | ".join(
        f"{g.upper()}" for g in GROUPS) + " | Total |")
    print("| --- | --- | " + " | ".join("---:" for _ in GROUPS) + " | ---: |")
    for key in sorted(new):
        subtotals = {g: 0 for g in GROUPS}
        for i in ITEM_IDS:
            subtotals[i[0]] += median([p[i] for p in new[key]["per_run"]])
        cells = " | ".join(f"{int(subtotals[g])}" for g in GROUPS)
        print(f"| {key[0]} / {key[1]} | {key[2]} | {cells} | {new[key]['median_score']} |")


if __name__ == "__main__":
    main()
