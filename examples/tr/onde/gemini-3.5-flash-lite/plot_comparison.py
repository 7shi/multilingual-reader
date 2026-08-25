# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Gemini 3.5 Flash Lite と Gemma 4 の翻訳評価スコアを比較する折れ線グラフを生成する。

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
GEMMA4_TRENDS = HERE.parent / "gemma4" / "TRENDS.jsonl"
OUTPUT = HERE / "compare_gemma4.png"

def load_scores(path: Path) -> dict[str, int]:
    scores = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        scores[entry["lang"]] = entry["score"]
    return scores

def plot_sorted_by(ax, gemini_scores, gemma4_scores, sort_key, title):
    langs = sorted(gemini_scores, key=sort_key, reverse=True)
    names = [resolve_lang(lang) for lang in langs]

    ax.plot([gemini_scores[lang] for lang in langs], names, marker="o", markersize=3, label="Gemini 3.5 Flash Lite")
    ax.plot([gemma4_scores[lang] for lang in langs], names, marker="o", markersize=3, label="Gemma 4")

    ax.set_xlabel("Score")
    ax.set_ylabel("Language")
    ax.set_title(title)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=8)
    ax.legend()
    ax.grid(axis="x", alpha=0.3)

def main():
    gemini_scores = load_scores(GEMINI_TRENDS)
    gemma4_scores = load_scores(GEMMA4_TRENDS)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 20))
    plot_sorted_by(ax1, gemini_scores, gemma4_scores, lambda lang: gemini_scores[lang], "Sorted by Gemini 3.5 Flash Lite")
    plot_sorted_by(ax2, gemini_scores, gemma4_scores, lambda lang: gemma4_scores[lang], "Sorted by Gemma 4")
    fig.tight_layout()

    fig.savefig(OUTPUT, dpi=150)
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()
