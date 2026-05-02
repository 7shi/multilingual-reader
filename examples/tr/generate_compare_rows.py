from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from trtools.language import LANG_NAMES

ROOT = Path(__file__).resolve().parent
ONDE_MODELS = ("gemma4", "gpt-oss", "qwen3.6")
ONDE_SCORE_FILES = {
    model: ROOT / "onde" / model / "SCORES.txt" for model in ONDE_MODELS
}
CORE_TOPICS = ("finetuning", "transformer", "momentum")
CORE_SCORE_FILE = ROOT / "core" / "SCORES.txt"
CORE_ONDE_MODEL = "gemma4"
CORE_CODES = ("ja", "zh", "es", "fr", "de")
LINE_RE = re.compile(r"^([a-z0-9.]+)-([a-z0-9.]+):\s+(\d+)/100点$")


@dataclass(frozen=True)
class CompareRow:
    code: str
    display_name: str
    scores: tuple[int, int, int]
    sort_key: tuple


def parse_scores(path: Path) -> dict[tuple[str, str], int]:
    scores: dict[tuple[str, str], int] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = LINE_RE.fullmatch(line)
        if match is None:
            raise ValueError(f"unexpected line in {path}: {line}")
        prefix, code, score = match.groups()
        scores[(prefix, code)] = int(score)
    if not scores:
        raise ValueError(f"no scores found in {path}")
    return scores


def format_score(score: int, max_score: int) -> str:
    return f"**{score}**" if score == max_score else str(score)


def load_compare_rows() -> list[CompareRow]:
    per_model_scores = {
        model: parse_scores(path) for model, path in ONDE_SCORE_FILES.items()
    }
    code_sets = {
        model: {code for prefix, code in scores if prefix == "onde"}
        for model, scores in per_model_scores.items()
    }
    all_codes = set().union(*code_sets.values())

    missing_names = sorted(code for code in all_codes if code not in LANG_NAMES)
    if missing_names:
        raise ValueError(
            "missing language names in LANG_NAMES: " + ", ".join(missing_names)
        )

    rows = []
    for code in sorted(all_codes):
        scores = tuple(per_model_scores[model].get(("onde", code), 0) for model in ONDE_MODELS)
        rows.append(
            CompareRow(
                code=code,
                display_name=LANG_NAMES[code],
                scores=scores,
                sort_key=(*[-s for s in sorted(scores, reverse=True)], code),
            )
        )

    rows.sort(key=lambda row: row.sort_key)
    return rows


def render_compare_rows() -> list[str]:
    rows = load_compare_rows()
    rendered = []
    for row in rows:
        max_score = max(row.scores)
        scores = [format_score(score, max_score) for score in row.scores]
        rendered.append(f"| ({row.code}) {row.display_name} | {' | '.join(scores)} |")
    return rendered


def render_core_rows() -> list[str]:
    core_scores = parse_scores(CORE_SCORE_FILE)
    onde_scores = parse_scores(ONDE_SCORE_FILES[CORE_ONDE_MODEL])

    missing_names = sorted(code for code in CORE_CODES if code not in LANG_NAMES)
    if missing_names:
        raise ValueError(
            "missing language names in LANG_NAMES: " + ", ".join(missing_names)
        )

    rows = []
    for code in CORE_CODES:
        topic_scores = []
        for topic in CORE_TOPICS:
            key = (topic, code)
            if key not in core_scores:
                raise ValueError(f"missing {topic}-{code} in {CORE_SCORE_FILE}")
            topic_scores.append(core_scores[key])

        onde_key = ("onde", code)
        if onde_key not in onde_scores:
            raise ValueError(
                f"missing onde-{code} in {ONDE_SCORE_FILES[CORE_ONDE_MODEL]}"
            )
        onde_score = onde_scores[onde_key]
        average = (sum(topic_scores) + onde_score) / 4
        name = LANG_NAMES[code]
        rows.append(
            (average, code, topic_scores, onde_score, name)
        )
    rows.sort(key=lambda row: (-row[0], row[1]))

    rendered = []
    for average, code, topic_scores, onde_score, name in rows:
        rendered.append(
            f"| ({code}) {name} | {topic_scores[0]} | {topic_scores[1]} | "
            f"{topic_scores[2]} | {onde_score} | {average:.2f} |"
        )
    return rendered


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate README rows for examples/tr score tables."
    )
    parser.add_argument(
        "section",
        nargs="?",
        choices=("compare", "core", "all"),
        default="compare",
        help="which rows to output (default: compare)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        if args.section == "compare":
            lines = render_compare_rows()
        elif args.section == "core":
            lines = render_core_rows()
        else:
            lines = [
                "<!-- compare -->",
                *render_compare_rows(),
                "",
                "<!-- core -->",
                *render_core_rows(),
            ]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
