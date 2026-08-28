#!/usr/bin/env python3
"""
Script that treats the SCORES.txt of three evaluators (Gemini-2.5-flash, gpt-oss-20b,
gpt-oss-120b) as vectors and computes the Euclidean distance between them.

- Input: ../gemini-2.5-flash/SCORES.txt
         ../gpt-oss-20b/SCORES.txt
         ../gpt-oss-120b/SCORES.txt
- Output: prints the Euclidean distance, etc. for each evaluator pair to stdout

Distances are computed using only the model names common to both evaluators.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Paths to SCORES.txt files
SCORES_FILES = {
    "gemini-2.5-flash": "../gemini-2.5-flash/SCORES.txt",
    "gpt-oss-20b": "../gpt-oss-20b/SCORES.txt",
    "gpt-oss-120b": "../gpt-oss-120b/SCORES.txt",
}

# Name of the Markdown file to output results to
OUTPUT_MD = "DISTANCES.md"


def parse_scores_file(filepath: Path) -> Dict[str, int]:
    """Parse a SCORES.txt file and return a {model name: score} dictionary.

    Supports both of the following formats:
        '  1 | aya-expanse-32b-0: 76'
        'aya-expanse-32b-0: 76'
    """

    scores: Dict[str, int] = {}

    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Pattern: any prefix (line number + symbol, etc.) -> model name: score
            # Uses the same regex rule as compare_evaluators.py
            m = re.search(r"(?:\d+[→|])?\s*(.+?):\s*(\d+)", line)
            if not m:
                continue

            model_name = m.group(1).strip()
            score = int(m.group(2))
            scores[model_name] = score

    return scores


def build_aligned_vectors(
    scores_a: Dict[str, int], scores_b: Dict[str, int]
) -> Tuple[List[str], List[int], List[int]]:
    """Build vectors aligned to the common models from two score dictionaries.

    Returns:
        (list of common model names, vector A, vector B)
    """

    common_models = sorted(set(scores_a.keys()) & set(scores_b.keys()))
    vec_a = [scores_a[m] for m in common_models]
    vec_b = [scores_b[m] for m in common_models]
    return common_models, vec_a, vec_b


def euclidean_distance(vec_a: List[int], vec_b: List[int]) -> float:
    """Compute the Euclidean distance.

    d(x, y) = sqrt(sum_i (x_i - y_i)^2)
    """

    if len(vec_a) != len(vec_b):
        raise ValueError("Vector lengths do not match")

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))


def rms_difference(vec_a: List[int], vec_b: List[int]) -> float:
    """Compute the root mean square error (RMSE) per dimension."""

    if len(vec_a) != len(vec_b):
        raise ValueError("Vector lengths do not match")

    n = len(vec_a)
    if n == 0:
        return 0.0

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)) / n)


def build_matrix_section(title: str, evaluator_names: List[str], matrix: Dict[str, Dict[str, float]]) -> List[str]:
    """Build a Markdown distance matrix table (blank above the diagonal)."""

    lines: List[str] = [f"## {title}", ""]
    header = "| Evaluator | " + " | ".join(evaluator_names) + " |"
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
    print("Computing inter-evaluator Euclidean distances")
    print("=" * 60)

    # 1. Load SCORES.txt
    all_scores: Dict[str, Dict[str, int]] = {}

    print("\n[1] Loading SCORES.txt...")
    for name, rel_path in SCORES_FILES.items():
        path = base_dir / rel_path
        if not path.exists():
            raise FileNotFoundError(f"SCORES for {name} not found: {path}")

        scores = parse_scores_file(path)
        all_scores[name] = scores
        print(f"  - {name}: {len(scores)} items")

    # 2. Check the number of common models
    common_models_all = set.intersection(*[set(s.keys()) for s in all_scores.values()])
    print("\n[2] Checking common model count")
    print(f"  - Models common to all evaluators: {len(common_models_all)}")

    # 3. Compute Euclidean distance per pair
    print("\n[3] Computing Euclidean distance per pair")

    evaluator_names = list(all_scores.keys())
    results = []

    # Initialize matrix containers
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

            # Common models for this pair (normally expected to match the models common to all evaluators)
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
            print(f"      Common models: {len(models)}")
            print(f"      Euclidean distance: {dist:.4f}")
            print(f"      Root mean square error: {rmse:.4f}")

            distance_matrix[name_a][name_b] = dist
            distance_matrix[name_b][name_a] = dist
            rmse_matrix[name_a][name_b] = rmse
            rmse_matrix[name_b][name_a] = rmse

    print("\n[4] Summary")
    print("\npair, common models, Euclidean distance, RMSE")
    for r in results:
        print(
            f"- {r['pair']}: n={r['num_models']}, "
            f"distance={r['distance']:.4f}, rmse={r['rmse']:.4f}"
        )

    # 5. Write results to a Markdown file
    output_md_path = base_dir / OUTPUT_MD
    print(f"\n[5] Writing results to {output_md_path}...")

    lines = ["# Inter-evaluator distance matrix", ""]
    lines.extend(build_matrix_section("Euclidean distance", evaluator_names, distance_matrix))
    lines.extend(build_matrix_section("Root mean square error", evaluator_names, rmse_matrix))

    output_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  ✓ Write complete")

    print("\nDone")
    print("=" * 60)


if __name__ == "__main__":
    main()
