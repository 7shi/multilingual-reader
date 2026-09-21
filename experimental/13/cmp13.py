#!/usr/bin/env python3
"""Compares the two rubrics over the same 134 translations.

evals-degrees/ holds the old scheme's five criteria asked as five Score questions;
evals50/ holds experiment 11's fifty narrow properties asked as fifty. Same evaluator,
same model version, same translations, one run each -- so whatever separates the two is
the rubric, which is the one thing neither experiment 11 nor experiment 12 could isolate.

Experiment 12 section 3.3 put the two at Pearson +0.90, its strongest result and the one
resting on the fewest targets. This is that number at n=134.

Both schemes produce two totals and the difference between them matters here. A verdict
total rounds each judgment to its most probable level; an expected total is the
probability-weighted position before rounding. Experiment 11 section 3.6 already noted
Jev's weighted total is "markedly better than its rounded verdicts", and this report keeps
them apart rather than picking one.

The old scheme's own scores are read from examples/tr/onde/ in place, as the third
column. It shares a rubric with evals-degrees/ and not with evals50/, so it is a biased
referee between them; the report says so where it matters.

    uv run experimental/13/cmp13.py
"""

import argparse
import json
import re
from collections import Counter
from itertools import combinations
from pathlib import Path
from statistics import mean, median

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent.parent
ONDE = REPO_ROOT / "examples" / "tr" / "onde"
OLD_RUNS = (1, 2, 3)
# Run 1 only: <lang>.json. A later run is <lang>-N.json and is not read here.
NAME_RE = re.compile(r"^[a-z]{2}\.json$")
# (directory, label)
SCHEMES = (("evals-degrees", "5 criteria"), ("evals50", "50 items"))
# The result directories accumulate across runs, one subdirectory per translator, so
# which translators this report covers has to be said rather than inferred from what
# happens to be on disk.
DEFAULT_TRANSLATORS = ("gpt-5.6-luna", "union-alpha")


def load(directory):
    """{(translator, lang): result} from one result directory.

    Layout is <dir>/<translator>/<lang>.json, one subdirectory per translator; see
    eval5_jev.result_path. Only run 1 is read, which is the only run these were produced
    with -- a <lang>-N.json from a multi-run pass is ignored rather than silently
    averaged into a report that says one run each.
    """
    out = {}
    path = BASE / directory
    if not path.is_dir():
        return out
    for f in sorted(path.glob("*/*.json")):
        if NAME_RE.match(f.name):
            out[(f.parent.name, f.stem)] = json.loads(f.read_text(encoding="utf-8"))
    return out


def old_score(translator, lang):
    """The old scheme's score for one translation: the median of its three runs."""
    totals = []
    for run in OLD_RUNS:
        p = ONDE / translator / "evals" / f"onde-{lang}-{run}.json"
        if p.exists():
            totals.append(json.loads(p.read_text(encoding="utf-8"))["total_score"])
    return median(totals) if totals else None


def pearson(a, b):
    ma, mb = mean(a), mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else 0.0


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def kendall(a, b):
    concordant = discordant = 0
    for i, j in combinations(range(len(a)), 2):
        s = (a[i] - a[j]) * (b[i] - b[j])
        if s > 0:
            concordant += 1
        elif s < 0:
            discordant += 1
    total = concordant + discordant
    return (concordant - discordant) / total if total else 0.0


def spread(xs):
    return f"{min(xs):.1f}–{max(xs):.1f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("translators", nargs="*", default=list(DEFAULT_TRANSLATORS),
                    help="Directory names under examples/tr/onde/ to report on "
                         "(default: " + " ".join(DEFAULT_TRANSLATORS) + ")")
    args = ap.parse_args()
    wanted = set(args.translators)
    loaded = {d: {k: v for k, v in load(d).items() if k[0] in wanted}
              for d, _ in SCHEMES}
    missing = [d for d, _ in SCHEMES if not loaded[d]]
    if missing:
        raise SystemExit(f"no results for {', '.join(sorted(wanted))} in "
                         + ", ".join(f"{d}/" for d in missing))
    keys = sorted(set(loaded[SCHEMES[0][0]]) & set(loaded[SCHEMES[1][0]]))
    if not keys:
        raise SystemExit("the two directories share no targets")

    series = {}
    for d, label in SCHEMES:
        series[(label, "weighted")] = [loaded[d][k]["expected_total_score"] for k in keys]
        series[(label, "verdict")] = [float(loaded[d][k]["total_score"]) for k in keys]
    old = [old_score(*k) for k in keys]
    have_old = all(o is not None for o in old)

    print("# Two rubrics, one evaluator, the same translations\n")
    print(f"{len(keys)} translations judged under both schemes, one run each.\n")

    # --- 1. the headline ---
    print("## 1. Do the two rubrics agree?\n")
    print("| Pair | Pearson | Spearman | Kendall |")
    print("|---|---:|---:|---:|")
    for kind in ("weighted", "verdict"):
        a = series[(SCHEMES[0][1], kind)]
        b = series[(SCHEMES[1][1], kind)]
        name = ("probability-weighted totals" if kind == "weighted"
                else "rounded verdict totals")
        print(f"| 5 criteria vs 50 items, {name} | {pearson(a, b):+.2f} | "
              f"{spearman(a, b):+.2f} | {kendall(a, b):+.2f} |")
    print("\nExperiment 12 section 3.3 measured the first of these at +0.90 on 8 targets.\n")

    # --- 2. what each scheme's scale looks like ---
    print("## 2. What each total looks like\n")
    print("| Scheme | Total | Mean | Range | Mean confidence |")
    print("|---|---|---:|---:|---:|")
    for d, label in SCHEMES:
        conf = mean(c for k in keys for c in loaded[d][k]["confidence"].values())
        for kind, name in (("weighted", "probability-weighted"), ("verdict", "rounded")):
            xs = series[(label, kind)]
            shown = f"{conf:.2f}" if kind == "weighted" else ""
            print(f"| {label} | {name} | {mean(xs):.2f} | {spread(xs)} | {shown} |")
    if have_old:
        print(f"| old scheme | 3-run median | {mean(old):.2f} | {spread(old)} | |")
    print()

    # --- 3. the verdict distribution behind the 50-item ceiling ---
    counts = Counter(v for k in keys for v in loaded["evals50"][k]["evaluation"].values())
    n = sum(counts.values())
    print("## 3. The 50-item verdicts\n")
    print("| Verdict | n | Share |")
    print("|---|---:|---:|")
    for v in ("yes", "partial", "no"):
        print(f"| `{v}` | {counts[v]} | {counts[v] / n:.1%} |")
    print()

    # --- 4. against the old scheme ---
    if have_old:
        print("## 4. Against the old scheme\n")
        print("The old scheme *is* the five-criterion rubric, scored by a generative "
              "model. It shares a rubric with one of these schemes and not the other, so "
              "it cannot referee between them; what it can say is whether each tracks "
              "the corpus at all.\n")
        print("| Scheme | Total | Pearson | Spearman | Kendall | Mean diff |")
        print("|---|---|---:|---:|---:|---:|")
        for _, label in SCHEMES:
            for kind, name in (("weighted", "weighted"), ("verdict", "rounded")):
                xs = series[(label, kind)]
                print(f"| {label} | {name} | {pearson(xs, old):+.2f} | "
                      f"{spearman(xs, old):+.2f} | {kendall(xs, old):+.2f} | "
                      f"{mean(x - o for x, o in zip(xs, old)):+.1f} |")
        print()

    # --- 5. where they disagree ---
    a = series[(SCHEMES[0][1], "weighted")]
    b = series[(SCHEMES[1][1], "weighted")]
    offset = mean(x - y for x, y in zip(a, b))
    rows = sorted((x - y - offset, k, x, y) for k, x, y in zip(keys, a, b))
    print("## 5. Largest disagreements between the rubrics, net of the offset\n")
    print(f"The five-criterion total runs {offset:+.1f} points against the 50-item one on "
          "average; that offset is subtracted here.\n")
    print("| | Translator | Lang | 5 criteria | 50 items | Residual |")
    print("|---|---|---|---:|---:|---:|")
    for label, group in (("50 items higher", rows[:5]),
                         ("5 criteria higher", rows[-5:][::-1])):
        for res, (t, l), x, y in group:
            print(f"| {label} | {t} | {l} | {x:.1f} | {y:.1f} | {res:+.1f} |")
    print()


if __name__ == "__main__":
    main()
