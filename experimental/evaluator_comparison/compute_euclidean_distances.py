#!/usr/bin/env python3
"""
3つの評価者 (Gemini-2.5-flash, gpt-oss-20b, gpt-oss-120b) の
SCORES.txt をベクトルと見なし、ユークリッド距離を計算するスクリプト。

- 入力: ../gemini-2.5-flash/SCORES.txt
        ../gpt-oss-20b/SCORES.txt
        ../gpt-oss-120b/SCORES.txt
- 出力: 標準出力に評価者ペアごとのユークリッド距離などを表示

距離は共通して出現するモデル名のみを用いて計算する。
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

# SCORES.txtファイルのパス設定
SCORES_FILES = {
    "gemini-2.5-flash": "../gemini-2.5-flash/SCORES.txt",
    "gpt-oss-20b": "../gpt-oss-20b/SCORES.txt",
    "gpt-oss-120b": "../gpt-oss-120b/SCORES.txt",
}

# 結果を出力するMarkdownファイル名
OUTPUT_MD = "DISTANCES.md"


def parse_scores_file(filepath: Path) -> Dict[str, int]:
    """SCORES.txtファイルをパースして {モデル名: スコア} の辞書を返す。

    対応フォーマット例:
        '  1 | aya-expanse-32b-0: 76/100点'
        'aya-expanse-32b-0: 76/100点'
    のどちらにも対応する。
    """

    scores: Dict[str, int] = {}

    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # パターン: 任意の前置き (行番号+記号など) → モデル名: スコア/100点
            # compare_evaluators.py と同じ正規表現ルールを使用する
            m = re.search(r"(?:\d+[→|])?\s*(.+?):\s*(\d+)/100点", line)
            if not m:
                continue

            model_name = m.group(1).strip()
            score = int(m.group(2))
            scores[model_name] = score

    return scores


def build_aligned_vectors(
    scores_a: Dict[str, int], scores_b: Dict[str, int]
) -> Tuple[List[str], List[int], List[int]]:
    """2つのスコア辞書から、共通モデルに揃えたベクトルを構築する。

    返り値:
        (共通モデル名リスト, ベクトルA, ベクトルB)
    """

    common_models = sorted(set(scores_a.keys()) & set(scores_b.keys()))
    vec_a = [scores_a[m] for m in common_models]
    vec_b = [scores_b[m] for m in common_models]
    return common_models, vec_a, vec_b


def euclidean_distance(vec_a: List[int], vec_b: List[int]) -> float:
    """ユークリッド距離を計算する。

    d(x, y) = sqrt(sum_i (x_i - y_i)^2)
    """

    if len(vec_a) != len(vec_b):
        raise ValueError("ベクトル長が一致しません")

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))


def rms_difference(vec_a: List[int], vec_b: List[int]) -> float:
    """1次元あたりの二乗平均平方根誤差 (RMSE) を計算する。"""

    if len(vec_a) != len(vec_b):
        raise ValueError("ベクトル長が一致しません")

    n = len(vec_a)
    if n == 0:
        return 0.0

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)) / n)


def build_matrix_section(title: str, evaluator_names: List[str], matrix: Dict[str, Dict[str, float]]) -> List[str]:
    """Markdown用の距離マトリクス表を組み立てる（対角より上は空欄）。"""

    lines: List[str] = [f"## {title}", ""]
    header = "| 評価者 | " + " | ".join(evaluator_names) + " |"
    separator = "|:--| " + " | ".join([":--:" for _ in evaluator_names]) + " |"
    lines.append(header)
    lines.append(separator)

    for row_idx, row_name in enumerate(evaluator_names):
        row_cells: List[str] = []
        for col_idx, col_name in enumerate(evaluator_names):
            if col_idx <= row_idx:
                row_cells.append("")
            else:
                row_cells.append(f"{matrix[row_name][col_name]:.4f}")
        lines.append(f"| {row_name} | " + " | ".join(row_cells) + " |")

    lines.append("")
    return lines


def main() -> None:
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("評価者間ユークリッド距離の計算")
    print("=" * 60)

    # 1. SCORES.txt を読み込み
    all_scores: Dict[str, Dict[str, int]] = {}

    print("\n[1] SCORES.txt を読み込み中...")
    for name, rel_path in SCORES_FILES.items():
        path = base_dir / rel_path
        if not path.exists():
            raise FileNotFoundError(f"{name} の SCORES が見つかりません: {path}")

        scores = parse_scores_file(path)
        all_scores[name] = scores
        print(f"  - {name}: {len(scores)} 件")

    # 2. 共通モデル数を確認
    common_models_all = set.intersection(*[set(s.keys()) for s in all_scores.values()])
    print("\n[2] 共通モデル数の確認")
    print(f"  - 全評価者共通モデル数: {len(common_models_all)} 件")

    # 3. ペアごとにユークリッド距離を計算
    print("\n[3] ペアごとのユークリッド距離を計算")

    evaluator_names = list(all_scores.keys())
    results = []

    # マトリクス用の入れ物を初期化
    distance_matrix: Dict[str, Dict[str, float]] = {
        name: {other: (0.0 if name == other else 0.0) for other in evaluator_names}
        for name in evaluator_names
    }
    rmse_matrix: Dict[str, Dict[str, float]] = {
        name: {other: (0.0 if name == other else 0.0) for other in evaluator_names}
        for name in evaluator_names
    }

    for i in range(len(evaluator_names)):
        for j in range(i + 1, len(evaluator_names)):
            name_a = evaluator_names[i]
            name_b = evaluator_names[j]

            # ペアごとの共通モデル（通常は全評価者共通と同じになる想定）
            models, vec_a, vec_b = build_aligned_vectors(
                all_scores[name_a], all_scores[name_b]
            )

            dist = euclidean_distance(vec_a, vec_b)
            rmse = rms_difference(vec_a, vec_b)

            results.append(
                {
                    "pair": f"{name_a} vs {name_b}",
                    "num_models": len(models),
                    "distance": dist,
                    "rmse": rmse,
                }
            )

            print(f"  - {name_a} vs {name_b}:")
            print(f"      共通モデル数: {len(models)}")
            print(f"      ユークリッド距離: {dist:.4f}")
            print(f"      二乗平均平方根誤差: {rmse:.4f}")

            distance_matrix[name_a][name_b] = dist
            distance_matrix[name_b][name_a] = dist
            rmse_matrix[name_a][name_b] = rmse
            rmse_matrix[name_b][name_a] = rmse

    print("\n[4] サマリー")
    print("\nペア, 共通モデル数, ユークリッド距離, 二乗平均平方根誤差")
    for r in results:
        print(
            f"- {r['pair']}: n={r['num_models']}, "
            f"distance={r['distance']:.4f}, rmse={r['rmse']:.4f}"
        )

    # 5. Markdownファイルに結果を書き出し
    output_md_path = base_dir / OUTPUT_MD
    print(f"\n[5] 結果を {output_md_path} に書き出し中...")

    lines = ["# 評価者間距離マトリクス", ""]
    lines.extend(build_matrix_section("ユークリッド距離", evaluator_names, distance_matrix))
    lines.extend(build_matrix_section("二乗平均平方根誤差", evaluator_names, rmse_matrix))

    output_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  ✓ 書き出し完了")

    print("\n完了")
    print("=" * 60)


if __name__ == "__main__":
    main()
