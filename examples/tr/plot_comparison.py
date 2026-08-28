"""Generate a single line graph comparing translation evaluation scores across the given models.

Run: uv run plot_comparison.py -o compare/gemini35fl.png \
    -i gemini-3.5-flash-lite -l "Gemini 3.5 Flash Lite" \
    -i gemini-2.5-flash -l "Gemini 2.5 Flash"
"""
import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
PROJECT_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from trtools.language import resolve_lang

ONDE_DIR = HERE / "onde"


def load_scores(model: str) -> dict[str, int]:
    path = ONDE_DIR / model / "TRENDS.jsonl"
    scores = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        scores[entry["lang"]] = entry["score"]
    return scores


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", required=True, type=Path, help="Output file path")
    parser.add_argument(
        "-i", "--model", action="append", required=True,
        help="Model name (refers to onde/<model>/TRENDS.jsonl; the first one given is the sort basis)",
    )
    parser.add_argument("-l", "--label", action="append", required=True, help="Legend label")
    args = parser.parse_args()
    if len(args.model) != len(args.label):
        parser.error("-i and -l must be given the same number of times")
    return args


def main() -> None:
    args = parse_args()
    scores_list = [load_scores(model) for model in args.model]

    langs = sorted(scores_list[0], key=lambda lang: scores_list[0][lang], reverse=True)
    names = [resolve_lang(lang) for lang in langs]

    fig, ax = plt.subplots(figsize=(6, 20))
    for scores, label in zip(scores_list, args.label):
        ax.plot([scores[lang] for lang in langs], names, marker="o", markersize=3, label=label)

    ax.set_xlabel("Score")
    ax.set_ylabel("Language")
    ax.set_title(f"Sorted by {args.label[0]}")
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=8)
    ax.legend()
    ax.grid(axis="x", alpha=0.3)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.output, dpi=150)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
