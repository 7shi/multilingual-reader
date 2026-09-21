#!/usr/bin/env python3
"""Aggregates experiment 13: the corpus's top two translators, all 67 languages, one run.

Experiment 12 ends with a scheme it has only ever run on 8 targets -- the 8 the old
scheme was *least* stable on -- and two open questions that n=8 cannot answer. This
reads the 134 evaluations that answer them, against the old scheme's own scores for the
same translations, read where they live in examples/tr/onde/.

The old scheme separates `gpt-5.6-luna` and `union-alpha` by 0.22 points averaged over 67
languages, which is to say it does not separate them. That makes the pair useful in two
different ways at once, and the report below keeps them apart:

- **Agreement.** Per language, within one translator, the old corpus scores are a paired
  reference with n=67 rather than experiment 12's n=8. Whether this evaluator tracks them
  is the question experiment 12 section 3.3 could only gesture at.
- **Separation.** Whether the two translators come apart under this scheme is worth
  reporting but cannot be scored, because the reference has no opinion. A gap here is a
  claim the old scheme can neither confirm nor refute; this report says which direction
  and how large, and stops there.

The third thing it measures is the ceiling. Experiment 12 section 3.4 found level 3 the
most probable level in 100 of 120 judgments and level 4 in 5, and could not tell a
correct level 3 from one wide enough to absorb everything. These are the best translations
in the corpus, so if the top level is reachable at all it is reachable here. (The bottom
of the scale stays untested; that needs its own targets.)

Writes a Markdown report to stdout. Partial results are fine -- every table says what it
was computed from -- so this can be run while the evaluation is still going.

    uv run experimental/13/agg13.py
"""

import argparse
import json
import re
from itertools import combinations
from pathlib import Path
from statistics import mean, median

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent.parent
ONDE = REPO_ROOT / "examples" / "tr" / "onde"

# The criteria and the levels are read out of the result files rather than imported from
# experiment 12, which produced them. Experiment 12 is a finished record, and its
# criteria.py is free to change; an import would let this report describe a rubric the
# results on disk were never scored on, and do it silently. Every result file carries the
# level set it was placed on, so the data can say what it is.
#
# The pair, in the order the old scheme ranks them, so "first minus second" below is
# positive when this evaluator agrees with that ranking. Named on the command line the
# same way eval5_jev.py names them, rather than discovered from the result files, because
# that order is an input and not something the data can supply.
DEFAULT_TRANSLATORS = ("gpt-5.6-luna", "union-alpha")
OLD_RUNS = (1, 2, 3)
# Run 1 only: <lang>.json. A later run is <lang>-N.json and is not read here.
NAME_RE = re.compile(r"^[a-z]{2}\.json$")


def load(eval_dir):
    """{(translator, lang): result} from one result directory.

    Layout is <dir>/<translator>/<lang>.json, one subdirectory per translator; see
    eval5_jev.result_path. Only run 1 is read, which is the only run these were produced
    with -- a <lang>-N.json from a multi-run pass is ignored rather than silently
    averaged into a report that says one run each.
    """
    out = {}
    directory = BASE / eval_dir
    if not directory.is_dir():
        return out
    for path in sorted(directory.glob("*/*.json")):
        if NAME_RE.match(path.name):
            out[(path.parent.name, path.stem)] = json.loads(
                path.read_text(encoding="utf-8"))
    return out


def rubric_of(data):
    """(criterion ids, level count, level set name), taken from the results themselves.

    Every file must agree, because a report that mixes two rubrics is meaningless and a
    directory that holds both is a mistake worth stopping on rather than averaging over.
    """
    seen = {(tuple(r["expected_scores"]), len(r["levels"]), r.get("level_set", "?"))
            for r in data.values()}
    if len(seen) > 1:
        raise SystemExit("results were scored on more than one rubric: "
                         + ", ".join(sorted(f"{name} ({n} levels)"
                                            for _, n, name in seen)))
    criteria, n_levels, level_set = seen.pop()
    return list(criteria), n_levels, level_set


def heading(criterion):
    """A criterion key as a column heading: contextual_adaptation -> Contextual adaptation."""
    return criterion.replace("_", " ").capitalize()


def old_runs(translator, lang):
    """The old scheme's three run totals for one translation, as they are on disk."""
    totals = []
    for run in OLD_RUNS:
        path = ONDE / translator / "evals" / f"onde-{lang}-{run}.json"
        if path.exists():
            totals.append(json.loads(path.read_text(encoding="utf-8"))["total_score"])
    return totals


def old_score(translator, lang):
    """The old scheme's score for one translation: the median of its three runs.

    Read from the corpus in place. This is the reference experiments 11 and 12 use, but
    it is NOT the figure SCORES.txt and the corpus README quote: trtools/aggregate.py
    totals the five criteria's medians rather than taking the median of the three totals.
    The two agree on 60% of the corpus's 1,072 translations and differ by a mean absolute
    0.60 points (maximum 7), and README section 5.5 checks that nothing here turns on the
    choice -- the compression fit moves from 0.690 to 0.688. Kept as the median of totals
    for continuity with experiments 11 and 12.
    """
    totals = []
    for run in OLD_RUNS:
        path = ONDE / translator / "evals" / f"onde-{lang}-{run}.json"
        if path.exists():
            totals.append(json.loads(path.read_text(encoding="utf-8"))["total_score"])
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


def argmax_level(result, criterion):
    probs = result["probabilities"][criterion]
    return max(range(N_LEVELS), key=lambda i: probs[str(i)])


def section_reference_stability(data, langs, TRANSLATORS):
    """Is the disagreement this evaluator's, or the reference's?

    Every old score here is the median of three runs whose spread the corpus records, and
    experiment 11 measured that spread at a mean of 52.4 points on its worst targets. If
    the largest disagreements sit where the old scheme could not agree with itself, they
    are not evidence against this evaluator. That is a testable claim rather than an
    excuse, so it is tested: bucket the translations by the old scheme's own 3-run range
    and see whether agreement falls as the reference gets noisier.
    """
    rows = []
    for t in TRANSLATORS:
        for l in langs:
            runs = old_runs(t, l)
            if (t, l) in data and len(runs) == len(OLD_RUNS):
                rows.append((max(runs) - min(runs),
                             data[(t, l)]["expected_total_score"], median(runs)))
    if len(rows) < 10:
        return
    print("## 7. Agreement against the reference's own stability\n")
    print("Each translation bucketed by the spread of the three old runs behind its "
          "median.\n")
    print("| Old 3-run range | n | Pearson | Spearman | Mean abs diff |")
    print("|---|---:|---:|---:|---:|")
    for name, lo, hi in (("0-9 (steady)", 0, 10), ("10-19", 10, 20),
                         ("20+ (noisy)", 20, 10 ** 9)):
        sel = [(own, old) for rng, own, old in rows if lo <= rng < hi]
        if len(sel) < 3:
            print(f"| {name} | {len(sel)} | - | - | - |")
            continue
        own = [a for a, _ in sel]
        old = [b for _, b in sel]
        print(f"| {name} | {len(sel)} | {pearson(own, old):+.2f} | "
              f"{spearman(own, old):+.2f} | "
              f"{mean(abs(a - b) for a, b in sel):.1f} |")
    ranges = [r for r, _, _ in rows]
    absdiff = [abs(own - old) for _, own, old in rows]
    print(f"\nAcross all {len(rows)} translations, the size of the disagreement and the "
          f"old scheme's own 3-run range correlate at Pearson "
          f"**{pearson(absdiff, ranges):+.2f}** "
          f"(Spearman {spearman(absdiff, ranges):+.2f}).\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("translators", nargs="*", default=list(DEFAULT_TRANSLATORS),
                    help="Directory names under examples/tr/onde/, highest-ranked first "
                         "(default: " + " ".join(DEFAULT_TRANSLATORS) + ")")
    ap.add_argument("-d", "--eval-dir", default="evals-degrees",
                    help="Result directory under experimental/13 "
                         "(default: evals-degrees, which is where the default level set "
                         "of this experiment's eval5_jev.py writes)")
    args = ap.parse_args()

    TRANSLATORS = tuple(args.translators)
    # Only the named translators. The directory holds one subdirectory per translator
    # and accumulates across runs, so a later pass over a different pair would otherwise
    # be silently averaged into this report's level counts and confidence figures.
    data = {k: v for k, v in load(args.eval_dir).items() if k[0] in TRANSLATORS}
    if not data:
        raise SystemExit(
            f"no results for {', '.join(TRANSLATORS)} in {BASE / args.eval_dir}")
    CRITERION_IDS, N_LEVELS, level_set = rubric_of(data)
    langs = sorted({lang for _, lang in data})
    both = [l for l in langs if all((t, l) in data for t in TRANSLATORS)]

    print(f"# Experiment 13: {' vs '.join(TRANSLATORS)}, all languages\n")
    print(f"{len(data)} evaluations, one run each, over {len(langs)} languages "
          f"({len(both)} with both translators present), on the `{level_set}` level "
          f"set.\n")

    # --- 1. Overall, per translator ---
    print("## 1. Corpus means\n")
    print("| Translator | `jev` mean | Old mean | n |")
    print("|---|---:|---:|---:|")
    means, old_means = {}, {}
    for t in TRANSLATORS:
        own = [data[(t, l)]["expected_total_score"] for l in langs if (t, l) in data]
        old = [old_score(t, l) for l in langs if (t, l) in data]
        old = [o for o in old if o is not None]
        means[t] = mean(own) if own else None
        # The same languages this scheme scored, so the two gaps below are comparable.
        old_means[t] = mean(old) if old else None
        print(f"| {t} | {mean(own):.2f} | {mean(old):.2f} | {len(own)} |")
    if all(means[t] is not None for t in TRANSLATORS):
        gap = means[TRANSLATORS[0]] - means[TRANSLATORS[1]]
        line = (f"\n`{TRANSLATORS[0]}` minus `{TRANSLATORS[1]}`: **{gap:+.2f}** points "
                f"under this scheme")
        if all(old_means[t] is not None for t in TRANSLATORS):
            old_gap = old_means[TRANSLATORS[0]] - old_means[TRANSLATORS[1]]
            line += f", against **{old_gap:+.2f}** under the old one"
        print(line + ".\n")

    # --- 2. Agreement with the old scheme, per translator ---
    print("## 2. Agreement with the old scheme, language by language\n")
    print("Paired per translation; the old score is the median of that translation's "
          "three runs in the corpus.\n")
    print("| Set | n | Pearson | Spearman | Kendall | Mean diff | Mean abs diff |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    pooled_own, pooled_old = [], []
    for t in TRANSLATORS:
        own, old = [], []
        for l in langs:
            o = old_score(t, l)
            if (t, l) in data and o is not None:
                own.append(data[(t, l)]["expected_total_score"])
                old.append(o)
        if len(own) < 3:
            continue
        pooled_own += own
        pooled_old += old
        diffs = [a - b for a, b in zip(own, old)]
        print(f"| {t} | {len(own)} | {pearson(own, old):+.2f} | {spearman(own, old):+.2f} "
              f"| {kendall(own, old):+.2f} | {mean(diffs):+.1f} | "
              f"{mean(abs(d) for d in diffs):.1f} |")
    if len(pooled_own) >= 3:
        diffs = [a - b for a, b in zip(pooled_own, pooled_old)]
        print(f"| **pooled** | {len(pooled_own)} | {pearson(pooled_own, pooled_old):+.2f} "
              f"| {spearman(pooled_own, pooled_old):+.2f} "
              f"| {kendall(pooled_own, pooled_old):+.2f} | {mean(diffs):+.1f} | "
              f"{mean(abs(d) for d in diffs):.1f} |")
    print()

    # --- 3. Head to head ---
    # Two translators is what a head-to-head is; with any other number the rest of the
    # report still stands, so this section is skipped rather than the run refused.
    if both and len(TRANSLATORS) == 2:
        print("## 3. Head to head, per language\n")
        wins = {t: 0 for t in TRANSLATORS}
        ties = 0
        old_wins = {t: 0 for t in TRANSLATORS}
        old_ties = 0
        for l in both:
            a = data[(TRANSLATORS[0], l)]["expected_total_score"]
            b = data[(TRANSLATORS[1], l)]["expected_total_score"]
            if a == b:
                ties += 1
            else:
                wins[TRANSLATORS[0] if a > b else TRANSLATORS[1]] += 1
            oa, ob = old_score(TRANSLATORS[0], l), old_score(TRANSLATORS[1], l)
            if oa is None or ob is None or oa == ob:
                old_ties += 1
            else:
                old_wins[TRANSLATORS[0] if oa > ob else TRANSLATORS[1]] += 1
        print(f"| Scheme | {TRANSLATORS[0]} | {TRANSLATORS[1]} | tied |")
        print("|---|---:|---:|---:|")
        print(f"| `jev` | {wins[TRANSLATORS[0]]} | {wins[TRANSLATORS[1]]} | {ties} |")
        print(f"| old (3-run medians) | {old_wins[TRANSLATORS[0]]} | "
              f"{old_wins[TRANSLATORS[1]]} | {old_ties} |")
        # Only the languages where both schemes take a side. A tie expresses no
        # preference to agree or disagree with, and the old scheme has 13 of them, so
        # counting those in the denominator would understate the agreement.
        contested = agree = 0
        for l in both:
            oa, ob = old_score(TRANSLATORS[0], l), old_score(TRANSLATORS[1], l)
            if oa is None or ob is None or oa == ob:
                continue
            ja = data[(TRANSLATORS[0], l)]["expected_total_score"]
            jb = data[(TRANSLATORS[1], l)]["expected_total_score"]
            if ja == jb:
                continue
            contested += 1
            agree += (ja - jb) * (oa - ob) > 0
        if contested:
            print(f"\nBoth schemes take a side in {contested} of the {len(both)} "
                  f"languages, and pick the same translator in **{agree}/{contested}** "
                  f"of them ({agree / contested:.0%}).\n")

    # --- 4. The ceiling ---
    print("## 4. Where the probability mass goes\n")
    js = [(r["probabilities"][c], r["confidence"][c])
          for r in data.values() for c in CRITERION_IDS]  # noqa: F821
    print("| | " + " | ".join(f"L{i}" for i in range(N_LEVELS)) + " | Mean confidence |")
    print("|---|" + "---:|" * (N_LEVELS + 1))
    mass = [mean(p[str(i)] for p, _ in js) for i in range(N_LEVELS)]
    print("| Mean mass | " + " | ".join(f"{m:.3f}" for m in mass)
          + f" | {mean(c for _, c in js):.2f} |")
    winsl = [0] * N_LEVELS
    for p, _ in js:
        winsl[max(range(N_LEVELS), key=lambda i: p[str(i)])] += 1
    print(f"| Times most probable (n={len(js)}) | "
          + " | ".join(str(w) for w in winsl) + " | |")
    print("\nExperiment 12, on its 8 unstable targets, put 0.175 mass on L4 and made it "
          "the most probable level 5 times in 120.\n")

    # --- 5. Per criterion ---
    print("## 5. Mean score by criterion (0-20)\n")
    print("| Criterion | " + " | ".join(TRANSLATORS) + " |")
    print("|---|" + "---:|" * len(TRANSLATORS))
    for c in CRITERION_IDS:
        row = f"| {heading(c)} |"
        for t in TRANSLATORS:
            vals = [data[(t, l)]["expected_scores"][c] for l in langs if (t, l) in data]
            row += f" {mean(vals):.2f} |" if vals else " - |"
        print(row)
    print()

    # --- 6. Disagreement, net of the offset ---
    # Ranked by residual rather than by raw difference. If this scheme sits a constant
    # distance below the old one -- which section 2's mean diff column says outright --
    # then the largest raw differences are just the lowest-scoring languages, and say
    # nothing about where the two schemes actually disagree. Subtracting each set's own
    # mean difference leaves the part that is about the language rather than the scale.
    rows = []
    for t in TRANSLATORS:
        pairs = []
        for l in langs:
            o = old_score(t, l)
            if (t, l) in data and o is not None:
                pairs.append((l, data[(t, l)]["expected_total_score"], o))
        if len(pairs) < 3:
            continue
        offset = mean(own - o for _, own, o in pairs)
        rows += [(own - o - offset, t, l, own, o) for l, own, o in pairs]
    if rows:
        rows.sort()
        print("## 6. Where the two schemes disagree, net of the offset\n")
        print("Each set's own mean difference is subtracted, so this ranks disagreement "
              "about the language rather than about the scale.\n")
        print("| | Translator | Lang | `jev` | Old | Diff | Residual |")
        print("|---|---|---|---:|---:|---:|---:|")
        for label, group in (("jev lower", rows[:5]), ("jev higher", rows[-5:][::-1])):
            for res, t, l, own, o in group:
                print(f"| {label} | {t} | {l} | {own:.1f} | {o:.0f} | {own - o:+.1f} "
                      f"| {res:+.1f} |")
        print()

    section_reference_stability(data, langs, TRANSLATORS)


if __name__ == "__main__":
    main()
