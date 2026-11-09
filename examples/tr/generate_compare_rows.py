from __future__ import annotations

import argparse
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

# Generates a graph with matplotlib, same as plot_comparison.py (for the graph subcommand)
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.cbook import boxplot_stats

from trtools.language import LANG_NAMES

# Fix the SVG element id salt so regenerating the chart doesn't churn
# unrelated ids in the diff.
matplotlib.rcParams["svg.hashsalt"] = "tr-compare-models-chart"

ROOT = Path(__file__).resolve().parent
ONDE_MAKEFILE = ROOT / "onde" / "Makefile"
PLAMO_MAKEFILE = ROOT / "plamo" / "Makefile"
MODELS_RE = re.compile(r"^MODELS\s*=\s*((?:.*\\\n)*.*)$", re.MULTILINE)


def load_models(makefile: Path) -> tuple[str, ...]:
    text = makefile.read_text(encoding="utf-8")
    match = MODELS_RE.search(text)
    if match is None:
        raise ValueError(f"MODELS assignment not found in {makefile}")
    return tuple(match.group(1).replace("\\", " ").split())


ONDE_MODELS = load_models(ONDE_MAKEFILE)
# plamo/ (plamo/PLAN.md): PLaMo's own languages, compared only among themselves.
PLAMO_MODELS = load_models(PLAMO_MAKEFILE)


COMMON_MK = ROOT / "common.mk"
LANGS_RE = re.compile(r"^(CORE_LANGS|EXTRA_LANGS)\s*=\s*((?:.*\\\n)*.*)$", re.MULTILINE)


def load_corpus_codes() -> frozenset[str]:
    """The corpus's languages, CORE_LANGS + EXTRA_LANGS. A model that translates others
    has them cut from the comparison, and the corpus languages it lacks count as 0."""
    text = COMMON_MK.read_text(encoding="utf-8")
    found = {name: value for name, value in LANGS_RE.findall(text)}
    if set(found) != {"CORE_LANGS", "EXTRA_LANGS"}:
        raise ValueError(f"CORE_LANGS and EXTRA_LANGS not found in {COMMON_MK}")
    return frozenset(" ".join(found.values()).replace("\\", " ").split())


CORPUS_CODES = load_corpus_codes()
# --jev reads Jev's totals; without it, the previous evaluator's (qwen3.6, median of three),
# which stay beside them as the old scale's record. Set in main().
JEV = False


def score_file_name() -> str:
    return "SCORES-jev.txt" if JEV else "SCORES.txt"


def onde_score_file(model: str) -> Path:
    return ROOT / "onde" / model / score_file_name()


def plamo_score_file(model: str) -> Path:
    return ROOT / "plamo" / model / score_file_name()


def core_score_file() -> Path:
    return ROOT / "core" / score_file_name()


CORE_TOPICS = ("finetuning", "transformer", "momentum")
CORE_ONDE_MODEL = "gemma4"
CORE_CODES = ("ja", "zh", "es", "fr", "de")
LINE_RE = re.compile(r"^([a-z0-9.]+)-([a-z0-9.-]+):\s+(\d+(?:\.\d+)?)$")
README_FILE = ROOT / "README.md"
PLAMO_README_FILE = ROOT / "plamo" / "README.md"
GRAPH_OUTPUT = ROOT / "compare" / "MODELS.png"
GRAPH_SVG_OUTPUT = ROOT / "MODELS.svg"
PLAMO_GRAPH_OUTPUT = ROOT / "compare" / "PLAMO.png"
PLAMO_GRAPH_SVG_OUTPUT = ROOT / "PLAMO.svg"
COMPARE_TOP = 3
COMPARE_HEADER = "| Language | " + " | ".join(
    f"Score {i} | Model {i}" for i in range(1, COMPARE_TOP + 1)
) + " |"
STATS_HEADER = "| Model | Mean | Median | Stdev | Notes |"
PLAMO_STATS_HEADER = "| PLaMo model | Mean | Median | Stdev | Notes |"
PLAMO_LANGS_HEADER = "| Language | " + " | ".join(
    model.removeprefix("plamo-3-translate-").upper() for model in PLAMO_MODELS
) + " |"
SYNC_HEADERS = {
    "compare": COMPARE_HEADER,
    "stats": STATS_HEADER,
    "core": "| Language | finetuning |",
    "plamo-stats": PLAMO_STATS_HEADER,
    "plamo-langs": PLAMO_LANGS_HEADER,
}
# The plamo tables live in plamo/'s own README, apart from the main comparison.
SYNC_FILES = {
    "plamo-stats": PLAMO_README_FILE,
    "plamo-langs": PLAMO_README_FILE,
}


@dataclass(frozen=True)
class CompareRow:
    code: str
    display_name: str
    scores: tuple[float, ...]
    sort_key: tuple


def parse_scores(path: Path) -> dict[tuple[str, str], float]:
    scores: dict[tuple[str, str], float] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = LINE_RE.fullmatch(line)
        if match is None:
            raise ValueError(f"unexpected line in {path}: {line}")
        prefix, code, score = match.groups()
        scores[(prefix, code)] = float(score)
    if not scores:
        raise ValueError(f"no scores found in {path}")
    return scores


def load_compare_rows() -> list[CompareRow]:
    per_model_scores = {
        model: parse_scores(onde_score_file(model)) for model in ONDE_MODELS
    }
    code_sets = {
        model: {code for prefix, code in scores if prefix == "onde" and code in CORPUS_CODES}
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


def render_compare_header() -> list[str]:
    return [COMPARE_HEADER, "| --- |" + " ---: | --- |" * COMPARE_TOP]


def render_compare_rows() -> list[str]:
    rows = load_compare_rows()
    rendered = []
    for row in rows:
        # Ties are not merged: each model gets its own entry, ordered by score
        # (descending) and then by model name.
        ranked = sorted(zip(ONDE_MODELS, row.scores), key=lambda x: (-x[1], x[0]))
        cells = []
        for model, score in ranked[:COMPARE_TOP]:
            cells += [f"{score:.1f}" if JEV else f"{score:g}", model]
        rendered.append(f"| {row.display_name} | {' | '.join(cells)} |")
    return rendered


def compute_stats() -> dict[str, tuple[float, float, float]]:
    rows = load_compare_rows()
    stats = {}
    for i, model in enumerate(ONDE_MODELS):
        scores = [row.scores[i] for row in rows]
        stats[model] = (
            statistics.mean(scores),
            statistics.median(scores),
            statistics.pstdev(scores),
        )
    return stats


def load_existing_model_notes(
    header: str = STATS_HEADER, readme: Path = README_FILE
) -> dict[str, tuple[str, str]]:
    """Read model -> (model column display string, notes) from the existing stats table
    (median/stdev are ignored since they're recomputed). The model column may contain
    manually appended parenthetical notes (parameter scale, etc.), so entries are keyed
    by the leading whitespace-separated token (the base model name).
    """
    readme_lines = readme.read_text(encoding="utf-8").splitlines()
    header_idx = next(
        (i for i, line in enumerate(readme_lines) if line == header),
        None,
    )
    if header_idx is None:
        return {}

    notes: dict[str, tuple[str, str]] = {}
    i = header_idx + 2  # header line + separator line
    while i < len(readme_lines) and readme_lines[i].startswith("|"):
        cols = [c.strip() for c in readme_lines[i].split("|")[1:-1]]
        model_cell, _mean, _median, _stdev, remark = cols
        model = model_cell.split(" ", 1)[0]
        notes[model] = (model_cell, remark)
        i += 1
    return notes


def render_stats_header() -> list[str]:
    return [STATS_HEADER, "| --- | ---: | ---: | ---: | --- |"]


def render_stats_rows() -> list[str]:
    stats = compute_stats()
    notes = load_existing_model_notes()
    rendered = []
    for model in sorted(ONDE_MODELS, key=lambda m: (-stats[m][1], stats[m][2])):
        mean, median, stdev = stats[model]
        model_cell, remark = notes.get(model, (model, ""))
        rendered.append(
            f"| {model_cell} | {mean:.2f} | {median:.2f} | {stdev:.2f} | {remark} |"
        )
    return rendered


def plot_model_stats(top: int | None = None) -> None:
    rows = load_compare_rows()
    notes = load_existing_model_notes()

    per_model_scores = {
        model: [row.scores[ONDE_MODELS.index(model)] for row in rows]
        for model in ONDE_MODELS
    }
    if top is not None:
        per_model_scores = {
            model: sorted(scores, reverse=True)[:top]
            for model, scores in per_model_scores.items()
        }
    title = "Score distribution by model"
    if top is not None:
        title += f" (top {top})"
    output = GRAPH_OUTPUT if top is None else GRAPH_OUTPUT.with_name(f"MODELS{top}.png")
    draw_boxplot(per_model_scores, notes, title, output,
                 GRAPH_SVG_OUTPUT if top is None else None)


def plot_plamo_stats() -> None:
    per_model_scores = {model: list(scores.values()) for model, scores in load_plamo_scores().items()}
    notes = load_existing_model_notes(PLAMO_STATS_HEADER, PLAMO_README_FILE)
    draw_boxplot(per_model_scores, notes, "Score distribution of PLaMo 3 Translate (its languages)",
                 PLAMO_GRAPH_OUTPUT, PLAMO_GRAPH_SVG_OUTPUT)


def draw_boxplot(
    per_model_scores: dict[str, list[float]],
    notes: dict[str, tuple[str, str]],
    title: str,
    output: Path,
    svg_output: Path | None,
) -> None:
    medians = {model: statistics.median(scores) for model, scores in per_model_scores.items()}
    stdevs = {model: statistics.pstdev(scores) for model, scores in per_model_scores.items()}
    models = sorted(per_model_scores, key=lambda m: (-medians[m], stdevs[m]))
    labels = [notes.get(m, (m, ""))[0] for m in models]
    data = [per_model_scores[m] for m in models]

    fig, ax = plt.subplots(figsize=(8, len(models) * 0.6 + 1))
    ax.boxplot(data, orientation="horizontal", tick_labels=labels)

    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    output.parent.mkdir(exist_ok=True)
    fig.savefig(output, dpi=150)
    print(f"Saved: {output}")

    if svg_output is not None:
        fig.savefig(svg_output)
        print(f"Saved: {svg_output}")

    print(f"{'label':<20} {'min':>5} {'q1':>5} {'median':>6} {'q3':>5} {'max':>5}")
    for label, stats in zip(labels, boxplot_stats(data)):
        print(
            f"{label:<20} {stats['whislo']:>5.0f} {stats['q1']:>5.0f} "
            f"{stats['med']:>6.0f} {stats['q3']:>5.0f} {stats['whishi']:>5.0f}"
        )


def load_plamo_scores() -> dict[str, dict[str, float]]:
    """Each PLaMo model's onde scores by language code, over its own languages (no cut
    to the corpus's, and no zeros for the corpus languages it lacks)."""
    per_model = {}
    for model in PLAMO_MODELS:
        scores = parse_scores(plamo_score_file(model))
        per_model[model] = {code: score for (prefix, code), score in scores.items() if prefix == "onde"}
    codes = {frozenset(scores) for scores in per_model.values()}
    if len(codes) != 1:
        raise ValueError("PLaMo models cover different languages")
    missing_names = sorted(code for code in next(iter(codes)) if code not in LANG_NAMES)
    if missing_names:
        raise ValueError("missing language names in LANG_NAMES: " + ", ".join(missing_names))
    return per_model


def render_plamo_stats() -> list[str]:
    per_model = load_plamo_scores()
    notes = load_existing_model_notes(PLAMO_STATS_HEADER, PLAMO_README_FILE)
    stats = {
        model: (
            statistics.mean(scores.values()),
            statistics.median(scores.values()),
            statistics.pstdev(scores.values()),
        )
        for model, scores in per_model.items()
    }
    rendered = [PLAMO_STATS_HEADER, "| --- | ---: | ---: | ---: | --- |"]
    for model in sorted(PLAMO_MODELS, key=lambda m: (-stats[m][1], stats[m][2])):
        mean, median, stdev = stats[model]
        model_cell, remark = notes.get(model, (model, ""))
        rendered.append(f"| {model_cell} | {mean:.2f} | {median:.2f} | {stdev:.2f} | {remark} |")
    return rendered


def render_plamo_langs() -> list[str]:
    """Each language's score at every size, ordered by the last (largest) size."""
    per_model = load_plamo_scores()
    largest = PLAMO_MODELS[-1]
    codes = sorted(per_model[largest], key=lambda c: (-per_model[largest][c], c))
    rendered = [PLAMO_LANGS_HEADER, "| --- |" + " ---: |" * len(PLAMO_MODELS)]
    for code in codes:
        cells = [f"{per_model[model][code]:.1f}" for model in PLAMO_MODELS]
        rendered.append(f"| {LANG_NAMES[code]} | {' | '.join(cells)} |")
    return rendered


def render_core_header() -> list[str]:
    return [
        "| Language | finetuning | transformer | momentum | onde | Average |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]


def render_core_rows() -> list[str]:
    # The onde column is gemma4's, the translator of core/, on the same scale.
    core_file = core_score_file()
    core_scores = parse_scores(core_file)
    onde_file = onde_score_file(CORE_ONDE_MODEL)
    onde_scores = parse_scores(onde_file)

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
                raise ValueError(f"missing {topic}-{code} in {core_file}")
            topic_scores.append(core_scores[key])

        onde_key = ("onde", code)
        if onde_key not in onde_scores:
            raise ValueError(f"missing onde-{code} in {onde_file}")
        onde_score = onde_scores[onde_key]
        average = (sum(topic_scores) + onde_score) / 4
        name = LANG_NAMES[code]
        rows.append(
            (average, code, topic_scores, onde_score, name)
        )
    rows.sort(key=lambda row: (-row[0], row[1]))

    fmt = ".1f" if JEV else "g"
    rendered = []
    for average, code, topic_scores, onde_score, name in rows:
        cells = [format(score, fmt) for score in (*topic_scores, onde_score)]
        rendered.append(f"| {name} | {' | '.join(cells)} | {average:.2f} |")
    return rendered


TIERS = [
    ("high quality (90+)", 90, 101),
    ("practical range (80-89)", 80, 90),
    ("medium quality (60-79)", 60, 80),
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
                names = ", ".join(r.display_name for r in tier_rows)
                lines.append(f"- {label}: {names}")
    else:
        for i, model in enumerate(ONDE_MODELS):
            lines.append(f"**{model}**:")
            model_rows = sorted(rows, key=lambda r, i=i: -r.scores[i])
            for label, lo, hi in TIERS:
                tier_rows = [r for r in model_rows if lo <= r.scores[i] < hi]
                if tier_rows:
                    names = ", ".join(
                        f"**{r.display_name}**" if r.scores[i] == max(r.scores) else r.display_name
                        for r in tier_rows
                    )
                    lines.append(f"- {label}: {names}")
            lines.append("")

    bottom = sorted(
        [r for r in rows if max(r.scores) < 60],
        key=lambda r: -max(r.scores),
    )
    if bottom:
        names = ", ".join(r.display_name for r in bottom)
        lines.append(f"- critical flaws (below 60): {names}")

    return lines


def sync_section(section: str, table_lines: list[str]) -> None:
    header_prefix = SYNC_HEADERS[section]
    readme_file = SYNC_FILES.get(section, README_FILE)
    readme_lines = readme_file.read_text(encoding="utf-8").splitlines()

    header_idx = next(
        (i for i, line in enumerate(readme_lines) if line.startswith(header_prefix)),
        None,
    )
    if header_idx is None:
        raise ValueError(f"header line starting with {header_prefix!r} not found in {readme_file}")

    rows_end = header_idx + 2  # header line + separator line
    while rows_end < len(readme_lines) and readme_lines[rows_end].startswith("|"):
        rows_end += 1

    new_lines = readme_lines[:header_idx] + table_lines + readme_lines[rows_end:]
    readme_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate README rows for examples/tr score tables."
    )
    # On every subcommand, so it can follow the subcommand's name like --sync does.
    scale = argparse.ArgumentParser(add_help=False)
    scale.add_argument(
        "--jev",
        action="store_true",
        help="read Jev's totals (SCORES-jev.txt) instead of the previous evaluator's "
             "(SCORES.txt)",
    )
    subparsers = parser.add_subparsers(dest="section")

    compare_parser = subparsers.add_parser("compare", help="onde comparison table (default)", parents=[scale])
    compare_parser.add_argument(
        "--sync",
        action="store_true",
        help="write the generated rows into README.md between the section's markers",
    )
    core_parser = subparsers.add_parser("core", help="core language table", parents=[scale])
    core_parser.add_argument(
        "--sync",
        action="store_true",
        help="write the generated rows into README.md's core table",
    )
    plamo_parser = subparsers.add_parser("plamo", help="plamo/ tables (stats and per language)", parents=[scale])
    plamo_parser.add_argument(
        "--sync",
        action="store_true",
        help="write the generated rows into plamo/README.md's tables",
    )
    subparsers.add_parser("all", help="compare + stats + core tables", parents=[scale])
    graph_parser = subparsers.add_parser("graph", help="generate compare/MODELS.png (score boxplot per model)", parents=[scale])
    graph_parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="use only each model's top-N languages by score (writes compare/MODELS<N>.png)",
    )
    graph_parser.add_argument(
        "--plamo",
        action="store_true",
        help="plot plamo/'s models instead (writes compare/PLAMO.png and PLAMO.svg)",
    )
    classify_parser = subparsers.add_parser("classify", help="classify languages by score tier", parents=[scale])
    classify_parser.add_argument(
        "--overall",
        action="store_true",
        help="show overall best-score classification instead of per-model",
    )

    parser.set_defaults(section="compare", sync=False, overall=False, jev=False, plamo=False)
    args = parser.parse_args()
    global JEV
    JEV = args.jev

    if args.section == "graph":
        try:
            if args.plamo:
                plot_plamo_stats()
            else:
                plot_model_stats(top=args.top)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        return 0

    try:
        if args.section == "compare":
            compare_lines = render_compare_header() + render_compare_rows()
            stats_lines = render_stats_header() + render_stats_rows()
        elif args.section == "core":
            lines = render_core_header() + render_core_rows()
        elif args.section == "plamo":
            plamo_stats_lines = render_plamo_stats()
            plamo_langs_lines = render_plamo_langs()
        elif args.section == "classify":
            lines = render_classify_rows(overall=args.overall)
        else:
            lines = [
                "<!-- compare -->",
                *render_compare_header(),
                *render_compare_rows(),
                "",
                "<!-- stats -->",
                *render_stats_header(),
                *render_stats_rows(),
                "",
                "<!-- core -->",
                *render_core_header(),
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

    if args.section == "plamo":
        if args.sync:
            sync_section("plamo-stats", plamo_stats_lines)
            sync_section("plamo-langs", plamo_langs_lines)
            print(
                f"synced {len(plamo_stats_lines)} lines (plamo-stats) and "
                f"{len(plamo_langs_lines)} lines (plamo-langs) into {PLAMO_README_FILE}"
            )
            return 0
        for line in plamo_stats_lines + [""] + plamo_langs_lines:
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
