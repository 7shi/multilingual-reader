from __future__ import annotations

import argparse
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

# onde/*/plot_comparison.py と同様に matplotlib でグラフを生成する（graph サブコマンド用）
import matplotlib.pyplot as plt

from trtools.language import LANGUAGES, LANG_NAMES

ROOT = Path(__file__).resolve().parent
ONDE_MAKEFILE = ROOT / "onde" / "Makefile"
MODELS_RE = re.compile(r"^MODELS\s*=\s*((?:.*\\\n)*.*)$", re.MULTILINE)


def load_onde_models() -> tuple[str, ...]:
    text = ONDE_MAKEFILE.read_text(encoding="utf-8")
    match = MODELS_RE.search(text)
    if match is None:
        raise ValueError(f"MODELS assignment not found in {ONDE_MAKEFILE}")
    return tuple(match.group(1).replace("\\", " ").split())


ONDE_MODELS = load_onde_models()
ONDE_SCORE_FILES = {
    model: ROOT / "onde" / model / "SCORES.txt" for model in ONDE_MODELS
}
CORE_TOPICS = ("finetuning", "transformer", "momentum")
CORE_SCORE_FILE = ROOT / "core" / "SCORES.txt"
CORE_ONDE_MODEL = "gemma4"
CORE_CODES = ("ja", "zh", "es", "fr", "de")
LINE_RE = re.compile(r"^([a-z0-9.]+)-([a-z0-9.]+):\s+(\d+)/100点$")
README_FILE = ROOT / "README.md"
GRAPH_OUTPUT = ROOT / "compare" / "MODELS.png"
STATS_HEADER = "| モデル | 平均 | 標準偏差 | 備考 |"
SYNC_HEADERS = {
    "compare": "| Language | ",
    "stats": STATS_HEADER,
}


@dataclass(frozen=True)
class CompareRow:
    code: str
    display_name: str
    display_name_ja: str
    scores: tuple[int, ...]
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
                display_name_ja=LANGUAGES[code]["ja"],
                scores=scores,
                sort_key=(*[-s for s in sorted(scores, reverse=True)], code),
            )
        )

    rows.sort(key=lambda row: row.sort_key)
    return rows


def render_compare_header(linked: bool) -> list[str]:
    if linked:
        model_cells = [f"[{model}](onde/{model}/README.md)" for model in ONDE_MODELS]
    else:
        model_cells = list(ONDE_MODELS)
    header = f"| Language | {' | '.join(model_cells)} |"
    separator = f"| --- | {' | '.join(['---:'] * len(ONDE_MODELS))} |"
    return [header, separator]


def render_compare_rows() -> list[str]:
    rows = load_compare_rows()
    rendered = []
    for row in rows:
        max_score = max(row.scores)
        scores = [format_score(score, max_score) for score in row.scores]
        rendered.append(f"| {row.display_name} | {' | '.join(scores)} |")
    return rendered


def compute_stats() -> dict[str, tuple[float, float]]:
    rows = load_compare_rows()
    stats = {}
    for i, model in enumerate(ONDE_MODELS):
        scores = [row.scores[i] for row in rows]
        stats[model] = (statistics.mean(scores), statistics.pstdev(scores))
    return stats


def load_existing_model_notes() -> dict[str, tuple[str, str]]:
    """model -> (モデル欄の表示文字列, 備考) を既存の stats 表から読み取る
    （平均・標準偏差は再計算するため無視）。モデル欄には手動で追記した
    括弧書き（パラメータ規模など）が含まれることがあるため、先頭の
    空白区切りトークン（モデル名本体）をキーにして引き当てる。
    """
    readme_lines = README_FILE.read_text(encoding="utf-8").splitlines()
    header_idx = next(
        (i for i, line in enumerate(readme_lines) if line == STATS_HEADER),
        None,
    )
    if header_idx is None:
        return {}

    notes: dict[str, tuple[str, str]] = {}
    i = header_idx + 2  # header line + separator line
    while i < len(readme_lines) and readme_lines[i].startswith("|"):
        cols = [c.strip() for c in readme_lines[i].split("|")[1:-1]]
        model_cell, _mean, _stdev, remark = cols
        model = model_cell.split(" ", 1)[0]
        notes[model] = (model_cell, remark)
        i += 1
    return notes


def render_stats_header() -> list[str]:
    return [STATS_HEADER, "| --- | ---: | ---: | --- |"]


def render_stats_rows() -> list[str]:
    stats = compute_stats()
    notes = load_existing_model_notes()
    rendered = []
    for model in sorted(ONDE_MODELS, key=lambda m: -stats[m][0]):
        mean, stdev = stats[model]
        model_cell, remark = notes.get(model, (model, ""))
        rendered.append(f"| {model_cell} | {mean:.2f} | {stdev:.2f} | {remark} |")
    return rendered


def plot_model_stats() -> None:
    rows = load_compare_rows()
    stats = compute_stats()
    notes = load_existing_model_notes()
    models = sorted(ONDE_MODELS, key=lambda m: -stats[m][0])
    labels = [notes.get(m, (m, ""))[0] for m in models]
    data = [[row.scores[ONDE_MODELS.index(m)] for row in rows] for m in models]

    fig, ax = plt.subplots(figsize=(8, len(models) * 0.6 + 1))
    ax.boxplot(data, orientation="horizontal", tick_labels=labels)

    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score")
    ax.set_title("Score distribution by model")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    GRAPH_OUTPUT.parent.mkdir(exist_ok=True)
    fig.savefig(GRAPH_OUTPUT, dpi=150)
    print(f"Saved: {GRAPH_OUTPUT}")


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
        name = LANGUAGES[code]["ja"]
        rows.append(
            (average, code, topic_scores, onde_score, name)
        )
    rows.sort(key=lambda row: (-row[0], row[1]))

    rendered = []
    for average, code, topic_scores, onde_score, name in rows:
        rendered.append(
            f"| {name} | {topic_scores[0]} | {topic_scores[1]} | "
            f"{topic_scores[2]} | {onde_score} | {average:.2f} |"
        )
    return rendered


TIERS = [
    ("高品質（90点以上）", 90, 101),
    ("実用範囲（80〜89点）", 80, 90),
    ("中品質（60〜79点）", 60, 80),
]


def render_classify_rows(overall: bool = False) -> list[str]:
    rows = load_compare_rows()

    lines = [f"{len(rows)} languages total", ""]

    if overall:
        lines.append("**overall**:")
        all_rows = sorted(rows, key=lambda r: -max(r.scores))
        for label, lo, hi in TIERS:
            tier_rows = [r for r in all_rows if lo <= max(r.scores) < hi]
            if tier_rows:
                names = "、".join(r.display_name_ja for r in tier_rows)
                lines.append(f"- {label}: {names}")
    else:
        for i, model in enumerate(ONDE_MODELS):
            lines.append(f"**{model}**:")
            model_rows = sorted(rows, key=lambda r, i=i: -r.scores[i])
            for label, lo, hi in TIERS:
                tier_rows = [r for r in model_rows if lo <= r.scores[i] < hi]
                if tier_rows:
                    names = "、".join(
                        f"**{r.display_name_ja}**" if r.scores[i] == max(r.scores) else r.display_name_ja
                        for r in tier_rows
                    )
                    lines.append(f"- {label}: {names}")
            lines.append("")

    bottom = sorted(
        [r for r in rows if max(r.scores) < 60],
        key=lambda r: -max(r.scores),
    )
    if bottom:
        names = "、".join(r.display_name_ja for r in bottom)
        lines.append(f"- 致命的な欠陥（60点未満）: {names}")

    return lines


def sync_section(section: str, table_lines: list[str]) -> None:
    header_prefix = SYNC_HEADERS[section]
    readme_lines = README_FILE.read_text(encoding="utf-8").splitlines()

    header_idx = next(
        (i for i, line in enumerate(readme_lines) if line.startswith(header_prefix)),
        None,
    )
    if header_idx is None:
        raise ValueError(f"header line starting with {header_prefix!r} not found in {README_FILE}")

    rows_end = header_idx + 2  # header line + separator line
    while rows_end < len(readme_lines) and readme_lines[rows_end].startswith("|"):
        rows_end += 1

    new_lines = readme_lines[:header_idx] + table_lines + readme_lines[rows_end:]
    README_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate README rows for examples/tr score tables."
    )
    subparsers = parser.add_subparsers(dest="section")

    compare_parser = subparsers.add_parser("compare", help="onde comparison table (default)")
    compare_parser.add_argument(
        "--sync",
        action="store_true",
        help="write the generated rows into README.md between the section's markers",
    )
    subparsers.add_parser("core", help="core language table")
    subparsers.add_parser("all", help="compare + stats + core tables")
    subparsers.add_parser("graph", help="generate compare/MODELS.png (score boxplot per model)")
    classify_parser = subparsers.add_parser("classify", help="classify languages by score tier")
    classify_parser.add_argument(
        "--overall",
        action="store_true",
        help="show overall best-score classification instead of per-model",
    )

    parser.set_defaults(section="compare", sync=False, overall=False)
    args = parser.parse_args()

    if args.section == "graph":
        try:
            plot_model_stats()
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        return 0

    try:
        if args.section == "compare":
            compare_lines = render_compare_header(linked=args.sync) + render_compare_rows()
            stats_lines = render_stats_header() + render_stats_rows()
        elif args.section == "core":
            lines = render_core_rows()
        elif args.section == "classify":
            lines = render_classify_rows(overall=args.overall)
        else:
            lines = [
                "<!-- compare -->",
                *render_compare_header(linked=False),
                *render_compare_rows(),
                "",
                "<!-- stats -->",
                *render_stats_header(),
                *render_stats_rows(),
                "",
                "<!-- core -->",
                *render_core_rows(),
            ]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.section == "compare":
        if args.sync:
            sync_section("compare", compare_lines)
            sync_section("stats", stats_lines)
            print(
                f"synced {len(compare_lines)} lines (compare) and "
                f"{len(stats_lines)} lines (stats) into {README_FILE}"
            )
            return 0
        for line in compare_lines + [""] + stats_lines:
            print(line)
        return 0

    if args.sync:
        sync_section(args.section, lines)
        print(f"synced {len(lines)} lines into {README_FILE}")
        return 0

    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
