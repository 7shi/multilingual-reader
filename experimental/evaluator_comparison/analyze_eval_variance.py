#!/usr/bin/env python3
"""3回評価の変動（標準偏差・レンジ）を評価者ごとに定量分析するスクリプト

集約には中央値を採用している（aggregate_evaluations.py と同様）。
3点サンプルでは中央値＝「外れ値1件を捨てた中間値」となり、
評価者ハルシネーションによる1回崩壊（0点混入・極端なスコア）を
自動的に除外できるため、平均値より堅牢。
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
    """評価者ディレクトリ内の全JSONを読み込み、キー→データリストを返す。
    各データは total_score と観点別スコアを含む。
    キーはファイル名から末尾の -N を除いたもの。"""
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
    """3回評価が揃っているアイテムの変動統計を計算する。"""
    complete = {k: v for k, v in data_map.items() if len(v) == 3}
    incomplete = {k: v for k, v in data_map.items() if len(v) != 3}

    total_scores = {k: [d["total"] for d in v] for k, v in complete.items()}
    ranges = [max(v) - min(v) for v in total_scores.values()]
    stdevs = [statistics.stdev(v) for v in total_scores.values()]

    # レンジ別の件数
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

    # 観点別の平均レンジと平均σ
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
    print(f"評価者: {label}  ({stats['complete']} 件完全 / {stats['incomplete']} 件不完全)")
    print(f"{'='*60}")
    print(f"  合計スコアレンジ（max-min）")
    print(f"    平均   : {stats['range_mean']:.2f}")
    print(f"    中央値 : {stats['range_median']:.1f}")
    print(f"    最大   : {stats['range_max']}")
    print(f"  標準偏差（3回内）")
    print(f"    平均   : {stats['stdev_mean']:.2f}")
    print(f"    中央値 : {stats['stdev_median']:.2f}")
    print(f"    最大   : {stats['stdev_max']:.2f}")
    print(f"    σのσ  : {stats['stdev_stdev']:.2f}")

    bkt = stats["range_buckets"]
    total = stats["complete"]
    print(f"\n  レンジ分布（{total}件）")
    for label_b, count in bkt.items():
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 2)
        print(f"    {str(label_b):>5}点差: {count:4d}件 ({pct:5.1f}%) {bar}")

    if stats["criteria_summary"]:
        print(f"\n  観点別 平均レンジ（降順）:")
        sorted_crit = sorted(stats["criteria_summary"].items(),
                             key=lambda x: x[1]["range_mean"], reverse=True)
        for crit, cs in sorted_crit:
            print(f"    {crit:<28} レンジ平均={cs['range_mean']:.2f}  σ平均={cs['stdev_mean']:.2f}")

    print(f"\n  変動上位10件:")
    for key, scores, rng in stats["top_variance"]:
        print(f"    {rng:3d}点差  {scores}  {key}")


def main():
    show_evaluators = sys.argv[1:] if len(sys.argv) > 1 else list(EVALUATORS.keys())

    for ev_id in show_evaluators:
        if ev_id not in EVALUATORS:
            print(f"不明な評価者: {ev_id}")
            continue
        ev_dir = BASE_DIR / ev_id
        if not ev_dir.exists():
            print(f"ディレクトリが見つかりません: {ev_dir}")
            continue
        data_map = load_data(ev_dir)
        stats = compute_stats(data_map)
        print_report(ev_id, EVALUATORS[ev_id], stats)

    print()


if __name__ == "__main__":
    main()
