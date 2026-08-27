# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Gemini 3.5 Flash Lite と Gemini 2.5 Flash と Gemma 4 と Gemma 4 31B の翻訳評価スコアを比較する折れ線グラフを生成する。

実行: uv run plot_comparison.py
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
PROJECT_ROOT = HERE.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from trtools.language import resolve_lang

GEMINI_TRENDS = HERE / "TRENDS.jsonl"
GEMINI25_TRENDS = HERE.parent / "gemini-2.5-flash" / "TRENDS.jsonl"
GEMMA4_TRENDS = HERE.parent / "gemma4" / "TRENDS.jsonl"
GEMMA4_31B_TRENDS = HERE.parent / "gemma4-31b" / "TRENDS.jsonl"
OUTPUT_GEMINI35FL = HERE / "compare_gemini35fl.png"
OUTPUT_GEMINI25F = HERE / "compare_gemini25f.png"
OUTPUT_GEMMA4 = HERE / "compare_gemma4.png"
OUTPUT_GEMMA4_31B = HERE / "compare_gemma4_31b.png"

def load_scores(path: Path) -> dict[str, int]:
    scores = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        scores[entry["lang"]] = entry["score"]
    return scores

def plot_sorted_by(ax, gemini_scores, gemini25_scores, gemma4_scores, gemma4_31b_scores, sort_key, title):
    langs = sorted(gemini_scores, key=sort_key, reverse=True)
    names = [resolve_lang(lang) for lang in langs]

    ax.plot([gemini_scores[lang] for lang in langs], names, marker="o", markersize=3, label="Gemini 3.5 Flash Lite")
    ax.plot([gemini25_scores[lang] for lang in langs], names, marker="o", markersize=3, label="Gemini 2.5 Flash")
    ax.plot([gemma4_scores[lang] for lang in langs], names, marker="o", markersize=3, label="Gemma 4")
    ax.plot([gemma4_31b_scores[lang] for lang in langs], names, marker="o", markersize=3, label="Gemma 4 31B")

    ax.set_xlabel("Score")
    ax.set_ylabel("Language")
    ax.set_title(title)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=8)
    ax.legend()
    ax.grid(axis="x", alpha=0.3)

def main():
    gemini_scores = load_scores(GEMINI_TRENDS)
    gemini25_scores = load_scores(GEMINI25_TRENDS)
    gemma4_scores = load_scores(GEMMA4_TRENDS)
    gemma4_31b_scores = load_scores(GEMMA4_31B_TRENDS)

    sort_keys = [
        (lambda lang: gemini_scores[lang], "Sorted by Gemini 3.5 Flash Lite", OUTPUT_GEMINI35FL),
        (lambda lang: gemini25_scores[lang], "Sorted by Gemini 2.5 Flash", OUTPUT_GEMINI25F),
        (lambda lang: gemma4_scores[lang], "Sorted by Gemma 4", OUTPUT_GEMMA4),
        (lambda lang: gemma4_31b_scores[lang], "Sorted by Gemma 4 31B", OUTPUT_GEMMA4_31B),
    ]

    for sort_key, title, output in sort_keys:
        fig, ax = plt.subplots(figsize=(6, 20))
        plot_sorted_by(ax, gemini_scores, gemini25_scores, gemma4_scores, gemma4_31b_scores, sort_key, title)
        fig.tight_layout()
        fig.savefig(output, dpi=150)
        print(f"Saved: {output}")

if __name__ == "__main__":
    main()
