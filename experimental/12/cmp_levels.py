#!/usr/bin/env python3
"""Compares the two wordings of the Score levels this experiment has been run with.

`evals/` holds the first version, whose levels were the old prompt's CRITICAL GUIDELINES
3-6 copied across: concrete defect names at the bottom of the scale, vague absolutes at
the top. `evals-degrees/` holds the replacement, whose levels say only how much of the
document falls short. Nothing else differs -- same model version, same five criteria,
same eight targets, same three runs -- so every difference below is attributable to the
level text alone, which is the general claim about Score the comparison is here to test.

Both directories are read where they lie, and so are the references: the old scheme's own
runs in examples/tr/onde/ and experiment 11's in experimental/11/. Nothing is copied.

Writes a Markdown report to stdout.

    uv run experimental/12/cmp_levels.py
"""

import argparse
import json
import re
from itertools import combinations
from pathlib import Path
from statistics import mean, median

from criteria import CRITERIA, CRITERION_IDS, EVAL_DIRS, LEVEL_SETS

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent.parent
ONDE = REPO_ROOT / "examples" / "tr" / "onde"
EXP11 = BASE.parent / "11"
TARGETS_TSV = EXP11 / "targets.tsv"
RUNS = (1, 2, 3)
# (level set, directory, label). The banded version first, because it is the control the
# replacement is read against; the directories come from criteria.py, so a set added
# there shows up here without a second list to keep in step.
LABELS = {"bands": "banded (old prompt's guidelines)",
          "degrees": "degrees (replacement)"}
VARIANTS = tuple((name, EVAL_DIRS[name], LABELS.get(name, name))
                 for name in ("bands", "degrees") if name in EVAL_DIRS)
NAME_RE = re.compile(r"^onde-(.+)-([a-z]{2})-jev-(\d+)\.json$")
# Every set has the same number of levels, which criteria.py asserts.
N_LEVELS = len(LEVEL_SETS[VARIANTS[0][0]])


def load(directory):
    """{(translator, lang): [run data in run order]} from one result directory."""
    runs = {}
    path = BASE / directory
    if not path.is_dir():
        return runs
    for f in sorted(path.iterdir()):
        m = NAME_RE.match(f.name)
        if not m:
            continue
        translator, lang, run = m.groups()
        runs.setdefault((translator, lang), {})[int(run)] = json.loads(
            f.read_text(encoding="utf-8"))
    return {k: [v[r] for r in sorted(v)] for k, v in runs.items()}


def load_targets():
    """(translator, lang, lang_name, old 3-run median) rows, in targets.tsv order."""
    rows = []
    for line in TARGETS_TSV.read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip():
            f = line.split("\t")
            rows.append((f[0], f[1], f[2], int(f[5])))
    return rows


def old_corpus_mean(lang):
    """The language's old-scheme mean over every translator in the corpus.

    Experiment 11 treats this as the better-verified reference: a mean over all 16
    translators rather than the single translation per language evaluated here. Each
    translator contributes the median of its three runs.
    """
    per_translator = []
    for evals_dir in sorted(ONDE.glob("*/evals")):
        totals = []
        for run in RUNS:
            p = evals_dir / f"onde-{lang}-{run}.json"
            if p.exists():
                totals.append(json.loads(p.read_text(encoding="utf-8"))["total_score"])
        if totals:
            per_translator.append(median(totals))
    return mean(per_translator) if per_translator else None


def exp11_median(directory, translator, lang, slug):
    """Median total over experiment 11's three runs for one target and evaluator."""
    totals = []
    for run in RUNS:
        p = EXP11 / directory / f"onde-{translator}-{lang}-{slug}-{run}.json"
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


def judgements(data):
    """Every per-criterion judgement in a list of runs, as (probabilities, confidence)."""
    for d in data:
        for key in CRITERION_IDS:
            probs = [d["probabilities"][key][str(i)] for i in range(N_LEVELS)]
            yield probs, d["confidence"][key]


def fmt(x, places=2):
    return "-" if x is None else f"{x:.{places}f}"


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    targets = load_targets()
    loaded = {d: load(d) for _, d, _ in VARIANTS}
    present = [(d, label) for _, d, label in VARIANTS if loaded[d]]
    if not present:
        raise SystemExit("no results found in "
                         + " or ".join(f"{d}/" for _, d, _ in VARIANTS))

    print("# Level wording: banded vs. degrees\n")
    print(f"Same model, criteria, targets and run count; only the {N_LEVELS} level "
          "descriptions differ.\n")

    # --- per-target totals and run-to-run range ---
    print("## 1. Totals and run-to-run range\n")
    header = "| Target | Old median |"
    rule = "|---|---:|"
    for _, label in present:
        header += f" {label} | Range |"
        rule += "---|---:|"
    print(header)
    print(rule)
    ranges = {d: [] for d, _ in present}
    totals = {d: [] for d, _ in present}
    old_medians = []
    for translator, lang, _, old_median in targets:
        row = f"| {translator} / {lang} | {old_median} |"
        old_medians.append(old_median)
        for d, _ in present:
            runs = loaded[d].get((translator, lang))
            if not runs:
                row += " - | - |"
                continue
            scores = [r["total_score"] for r in runs]
            ranges[d].append(max(scores) - min(scores))
            totals[d].append(median(scores))
            row += f" {', '.join(str(s) for s in scores)} | {max(scores) - min(scores)} |"
        print(row)
    row = "| **Mean** | " + fmt(mean(old_medians), 1) + " |"
    for d, _ in present:
        row += f" {fmt(mean(totals[d]), 1)} | **{fmt(mean(ranges[d]), 2)}** |"
    print(row)
    print("\nThe old scheme's own mean range on these 8 targets is 52.4.\n")

    # --- level usage ---
    print("## 2. Where the probability mass goes\n")
    print("| Variant | " + " | ".join(f"L{i}" for i in range(N_LEVELS))
          + " | Mean confidence |")
    print("|---|" + "---:|" * (N_LEVELS + 1))
    for d, label in present:
        js = list(judgements([r for runs in loaded[d].values() for r in runs]))
        mass = [mean(p[i] for p, _ in js) for i in range(N_LEVELS)]
        conf = mean(c for _, c in js)
        print(f"| {label} (mass) | " + " | ".join(fmt(m, 3) for m in mass)
              + f" | {fmt(conf)} |")
        wins = [0] * N_LEVELS
        for p, _ in js:
            wins[max(range(N_LEVELS), key=lambda i: p[i])] += 1
        print(f"| {label} (times most probable, n={len(js)}) | "
              + " | ".join(str(w) for w in wins) + " | |")
    print()

    # --- per-criterion means ---
    print("## 3. Mean score by criterion (0-20)\n")
    print("| Criterion | " + " | ".join(label for _, label in present) + " |")
    print("|---|" + "---:|" * len(present))
    for key in CRITERION_IDS:
        row = f"| {CRITERIA[key][0]} |"
        for d, _ in present:
            vals = [r["expected_scores"][key]
                    for runs in loaded[d].values() for r in runs]
            row += f" {fmt(mean(vals)) if vals else '-'} |"
        print(row)
    print()

    # --- correlations against the references ---
    # Correlated on `expected_total_score`, the probability-weighted total, rather than
    # on the rounded one: rounding five criteria to whole points throws away most of what
    # distinguishes eight targets, and the unrounded position is the thing a Score
    # actually returns. Section 1's ranges stay on the rounded total, which is the figure
    # comparable with the old scheme's 52.4.
    print("## 4. Agreement with the references (n=8)\n")
    print("Correlated on the probability-weighted total, medianed over the 3 runs.\n")
    references = {
        "Old 3-run medians": [old for _, _, _, old in targets],
        "Old per-language corpus mean": [old_corpus_mean(lang)
                                         for _, lang, _, _ in targets],
        "Experiment 11, 50-item Jev": [exp11_median("evals-jev", t, l, "jev")
                                       for t, l, _, _ in targets],
        "gpt-5.6-terra (experiment 11)": [exp11_median("evals", t, l, "gpt-5.6-terra")
                                          for t, l, _, _ in targets],
    }
    print("| Reference | Variant | Pearson | Spearman | Kendall |")
    print("|---|---|---:|---:|---:|")
    for name, ref in references.items():
        for d, label in present:
            own = []
            paired = []
            for (translator, lang, _, _), r in zip(targets, ref):
                runs = loaded[d].get((translator, lang))
                if runs and r is not None:
                    own.append(median([x["expected_total_score"] for x in runs]))
                    paired.append(r)
            if len(paired) < 3:
                print(f"| {name} | {label} | - | - | - |")
                continue
            print(f"| {name} | {label} | {pearson(own, paired):+.2f} | "
                  f"{spearman(own, paired):+.2f} | {kendall(own, paired):+.2f} |")
    print()


if __name__ == "__main__":
    main()
