#!/usr/bin/env python3
"""Script that quantitatively analyzes the variance (standard deviation, range) of
3-run evaluations per evaluator.

The median is used for aggregation (same as trtools agg).
For a 3-point sample, the median is "the middle value after discarding one outlier",
which automatically excludes single-run collapses caused by evaluator hallucination
(a stray zero score, extreme scores), making it more robust than the mean.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict
import statistics

EVALUATORS = {
    "gpt-oss-120b": "GPT-OSS 120B",
    "gemma-4-31b": "gemma-4-31b",
    "gemini-2.5-flash": "gemini-2.5-flash",
    "qwen3.6": "qwen3.6",
}

BASE_DIR = Path(__file__).parent.parent


def load_data(evaluator_dir: Path) -> dict[str, list[dict]]:
    """Load all JSON files in an evaluator directory and return a key -> data list mapping.
    Each entry includes total_score and per-criterion scores.
    Keys are the filename with the trailing -N stripped."""
    groups: dict[str, list[tuple[int, dict]]] = defaultdict(list)

    for json_file in sorted(evaluator_dir.rglob("*.json")):
        m = re.match(r"^(.+)-([123])$", json_file.stem)
        if not m:
            continue
        base_key = json_file.parent.name + "/" + m.group(1)
        run_num = int(m.group(2))
        try:
            data = json.loads(json_file.read_text())
            total = data.get("total_score")
            if total is None:
                continue
            criteria = {k: v["score"] for k, v in data.get("evaluation", {}).items()
                        if isinstance(v, dict) and "score" in v}
            groups[base_key].append((run_num, {"total": int(total), "criteria": criteria}))
        except Exception:
            continue

    result: dict[str, list[dict]] = {}
    for key, runs in groups.items():
        runs.sort()
        result[key] = [d for _, d in runs]
    return result


def compute_stats(data_map: dict[str, list[dict]]) -> dict:
    """Compute variance statistics for items that have all 3 evaluation runs."""
    complete = {k: v for k, v in data_map.items() if len(v) == 3}
    incomplete = {k: v for k, v in data_map.items() if len(v) != 3}

    total_scores = {k: [d["total"] for d in v] for k, v in complete.items()}
    ranges = [max(v) - min(v) for v in total_scores.values()]
    stdevs = [statistics.stdev(v) for v in total_scores.values()]

    # Counts per range bucket
    range_buckets = {0: 0, "1-5": 0, "6-10": 0, "11-20": 0, ">20": 0}
    for r in ranges:
        if r == 0:
            range_buckets[0] += 1
        elif r <= 5:
            range_buckets["1-5"] += 1
        elif r <= 10:
            range_buckets["6-10"] += 1
        elif r <= 20:
            range_buckets["11-20"] += 1
        else:
            range_buckets[">20"] += 1

    # Average range and average sigma per criterion
    criteria_stats: dict[str, dict] = defaultdict(lambda: {"ranges": [], "stdevs": []})
    for runs in complete.values():
        all_criteria = set()
        for d in runs:
            all_criteria.update(d["criteria"].keys())
        for crit in all_criteria:
            scores = [d["criteria"].get(crit) for d in runs]
            if any(s is None for s in scores):
                continue
            scores = [int(s) for s in scores]
            criteria_stats[crit]["ranges"].append(max(scores) - min(scores))
            criteria_stats[crit]["stdevs"].append(statistics.stdev(scores))

    criteria_summary = {}
    for crit, cs in criteria_stats.items():
        if cs["ranges"]:
            criteria_summary[crit] = {
                "range_mean": statistics.mean(cs["ranges"]),
                "stdev_mean": statistics.mean(cs["stdevs"]),
            }

    return {
        "complete": len(complete),
        "incomplete": len(incomplete),
        "range_mean": statistics.mean(ranges) if ranges else 0,
        "range_median": statistics.median(ranges) if ranges else 0,
        "range_max": max(ranges) if ranges else 0,
        "stdev_mean": statistics.mean(stdevs) if stdevs else 0,
        "stdev_median": statistics.median(stdevs) if stdevs else 0,
        "stdev_max": max(stdevs) if stdevs else 0,
        "stdev_stdev": statistics.stdev(stdevs) if len(stdevs) >= 2 else 0,
        "range_buckets": range_buckets,
        "criteria_summary": criteria_summary,
        "top_variance": sorted(
            [(k, [d["total"] for d in v], max([d["total"] for d in v]) - min([d["total"] for d in v]))
             for k, v in complete.items()],
            key=lambda x: x[2],
            reverse=True,
        )[:10],
    }


def print_report(evaluator_id: str, label: str, stats: dict):
    print(f"\n{'='*60}")
    print(f"Evaluator: {label}  ({stats['complete']} complete / {stats['incomplete']} incomplete)")
    print(f"{'='*60}")
    print(f"  Total score range (max-min)")
    print(f"    Mean   : {stats['range_mean']:.2f}")
    print(f"    Median : {stats['range_median']:.1f}")
    print(f"    Max    : {stats['range_max']}")
    print(f"  Standard deviation (within 3 runs)")
    print(f"    Mean   : {stats['stdev_mean']:.2f}")
    print(f"    Median : {stats['stdev_median']:.2f}")
    print(f"    Max    : {stats['stdev_max']:.2f}")
    print(f"    Sigma of sigma : {stats['stdev_stdev']:.2f}")

    bkt = stats["range_buckets"]
    total = stats["complete"]
    print(f"\n  Range distribution ({total} items)")
    for label_b, count in bkt.items():
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 2)
        print(f"    {str(label_b):>5}pt diff: {count:4d} items ({pct:5.1f}%) {bar}")

    if stats["criteria_summary"]:
        print(f"\n  Average range per criterion (descending):")
        sorted_crit = sorted(stats["criteria_summary"].items(),
                             key=lambda x: x[1]["range_mean"], reverse=True)
        for crit, cs in sorted_crit:
            print(f"    {crit:<28} range_mean={cs['range_mean']:.2f}  stdev_mean={cs['stdev_mean']:.2f}")

    print(f"\n  Top 10 highest-variance items:")
    for key, scores, rng in stats["top_variance"]:
        print(f"    {rng:3d}pt diff  {scores}  {key}")


def main():
    show_evaluators = sys.argv[1:] if len(sys.argv) > 1 else list(EVALUATORS.keys())

    for ev_id in show_evaluators:
        if ev_id not in EVALUATORS:
            print(f"Unknown evaluator: {ev_id}")
            continue
        ev_dir = BASE_DIR / ev_id
        if not ev_dir.exists():
            print(f"Directory not found: {ev_dir}")
            continue
        data_map = load_data(ev_dir)
        stats = compute_stats(data_map)
        print_report(ev_id, EVALUATORS[ev_id], stats)

    print()


if __name__ == "__main__":
    main()
