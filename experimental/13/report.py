#!/usr/bin/env python3
"""Step 2 of PORT.md section 7: the whole corpus on the Jev scale, beside the old one.

The experiment measured four translators; `trtools jev` has since evaluated all 16. This
sets the two scales side by side over the full 16 x 67 and answers PORT.md section 8's
first two questions -- does Jev separate the top four, and does the middle band hold --
plus question 4, the slope, which n=1,072 answers for free.

The old side is `SCORES.txt`, the published numbers, so a total is the sum of the five
criteria's medians (PLAN.md section 7), not `agg13.py`'s median of three totals. The Jev
side is read from `jev.jsonl` through `trtools agg --jev`'s own reader and rounded to one
decimal as `SCORES-jev.txt` is, so the report does not depend on that file having been
regenerated.

Unlike `agg13.py`, which reads `TRANSLATORS[0]` and `[1]` only, nothing here is built for
pairs: the top four are compared all against all.

Writes a Markdown report to stdout. REPORT.md is its output with the reading around it.

    uv run experimental/13/report.py
"""

import re
import statistics as st
import unicodedata
import sys
import csv
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
from matplotlib.cbook import boxplot_stats
from scipy import stats as ss

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from trtools.aggregate import aggregate_evaluations, aggregate_jev  # noqa: E402
from trtools.jev_criteria import CRITERION_IDS, POINTS_PER_LEVEL  # noqa: E402
from trtools.language import LANGUAGES  # noqa: E402

ONDE = ROOT / "examples" / "tr" / "onde"
MODELS_RE = re.compile(r"^MODELS\s*=\s*((?:.*\\\n)*.*)$", re.MULTILINE)
MODELS = MODELS_RE.search((ONDE / "Makefile").read_text()).group(1).replace("\\", " ").split()

# The top four by the old evaluator's mean, as PORT.md section 7 names them.
TOP = ["gpt-5.6-luna", "union-alpha", "gemini-3.7-flash", "ox-alpha"]
# generate_compare_rows.py's TIERS, plus the remainder, unchanged (PORT.md section 5.2).
TIERS = [("90+", 90, 101), ("80-89", 80, 90), ("60-79", 60, 80), ("<60", 0, 60)]
# Bands of the old score for translation-level agreement.
BANDS = [(0, 60), (60, 70), (70, 80), (80, 90), (90, 101)]
DIVERGENCES = 15
TERMS = ROOT / "examples" / "tr" / "terms" / "onde-en.tsv"
ORIGINAL = ROOT / "examples" / "onde-en.txt"
SPEAKERS = ("Camille", "Luc")
# What a translated line can do with the speaker label the glossary prescribes. `dropped`
# has no label at all and `swapped` names the other speaker: both lose who is speaking.
# `mixed-script` is a label whose name mixes writing systems (`Λυկ:`), and `off-glossary`
# one spelled otherwise than the glossary (`Камил:` where it says `Camille`); the speaker
# is still readable from either.
LABEL_CLASSES = ("dropped", "swapped", "mixed-script", "off-glossary")
LOST = ("dropped", "swapped")
# The first token of a line, up to whitespace or any separator the corpus's languages put
# after a speaker's name (Armenian `.` and `՝`, Khmer `៖`, Burmese ` - `, full-width `：`).
FIRST_TOKEN_RE = re.compile(r"[^\s:：․։៖.՝\-]+")
# A label is that token, one of those separators, whitespace and more text. A full stop
# only separates after an Armenian name; elsewhere `Nee. Dit ...` is a sentence.
LABEL_TAIL_RE = re.compile(r"\s?([:：․։៖.՝\-])\s+\S")
# A token must start this many lines to count as a translation's own name for a speaker.
# Each speaker has about fifty.
MIN_LABEL_LINES = 10


def load_old(model):
    scores = {}
    for line in (ONDE / model / "SCORES.txt").read_text().splitlines():
        name, value = line.split(":")
        scores[name.split("-", 1)[1]] = int(value)
    return scores


def load_jev(model):
    results = aggregate_jev(ONDE / model / "jev.jsonl", "onde")
    return {name.split("-", 1)[1]: round(r["total"], 1) for name, r in results.items()}


def criterion_means(model):
    """Mean points per criterion, old (median of three) and Jev, over all languages."""
    evals = sorted(str(p) for p in (ONDE / model / "evals").glob("*.json"))
    old = aggregate_evaluations(evals).values()
    jev = aggregate_jev(ONDE / model / "jev.jsonl", "onde").values()
    return ({c: st.mean(r["statistics"][c]["median"] for r in old) for c in CRITERION_IDS},
            {c: st.mean(r["levels"][c] * POINTS_PER_LEVEL for r in jev) for c in CRITERION_IDS})


def load_glossary():
    """{lang: {speaker: name}} from the term table the translators were given."""
    with TERMS.open(encoding="utf-8", newline="") as f:
        rows = {r["English"]: r for r in csv.DictReader(f, delimiter="\t")}
    return {code: {s: rows[s][info["en"]] for s in SPEAKERS}
            for code, info in LANGUAGES.items() if info["en"] in rows[SPEAKERS[0]]}


def script(ch):
    """The writing system of a letter, from its Unicode name (`GREEK`, `ARMENIAN`, ...)."""
    return unicodedata.name(ch, "?").split()[0].split("-")[0]


def classify_labels(model, lang, names, speakers):
    """Counter of LABEL_CLASSES over one translation's lines.

    Line i is checked against the speaker of the original's line i and the glossary's
    name for that speaker in this language. A name the translation uses consistently but
    the glossary does not -- one of its two commonest label tokens, on at least
    MIN_LABEL_LINES lines -- is mapped to the speaker it most often stands for, so that
    naming the other speaker by it counts as `swapped`. A label spelled some other way is
    only ever `off-glossary` or `mixed-script`: the check cannot tell which speaker an
    unknown spelling means.

    None for a translation whose line count differs from the original's: its lines no
    longer align, so line i's speaker is unknown (PORT.md section 5.3's `eu`).
    """
    lines = (ONDE / model / "tr" / f"onde-{lang}.txt").read_text(encoding="utf-8").splitlines()
    if len(lines) != len(speakers):
        return None
    tokens = []
    for line in lines:
        m = FIRST_TOKEN_RE.match(line)
        tail = m and LABEL_TAIL_RE.match(line, m.end())
        if tail and tail.group(1) == "." and script(m.group(0)[0]) != "ARMENIAN":
            tail = None
        tokens.append(m.group(0) if tail else "")
    own = {}
    for token, count in Counter(tokens).most_common(3):
        if token and count >= MIN_LABEL_LINES and len(own) < 2:
            own[token] = Counter(speakers[i] for i, t in enumerate(tokens)
                                 if t == token).most_common(1)[0][0]
    counts = Counter()
    for i, (line, token) in enumerate(zip(lines, tokens)):
        expected = speakers[i]
        other = SPEAKERS[1 - SPEAKERS.index(expected)]
        if line.startswith(names[expected]):
            continue
        if line.startswith(names[other]) or own.get(token) == other:
            counts["swapped"] += 1
        elif not token:
            counts["dropped"] += 1
        elif len({script(c) for c in token if c.isalpha()}) > 1:
            counts["mixed-script"] += 1
        else:
            counts["off-glossary"] += 1
    return counts


def summary(values):
    b = boxplot_stats(values)[0]
    return {
        "mean": st.mean(values), "min": b["whislo"], "q1": b["q1"], "median": b["med"],
        "q3": b["q3"], "max": b["whishi"], "pstdev": st.pstdev(values),
        "tiers": [sum(lo <= v < hi for v in values) for _, lo, hi in TIERS],
    }


def correlations(x, y):
    return (ss.pearsonr(x, y)[0], ss.spearmanr(x, y)[0], ss.kendalltau(x, y)[0],
            st.pstdev(x), st.pstdev(y))


def main():
    old = {m: load_old(m) for m in MODELS}
    jev = {m: load_jev(m) for m in MODELS}
    langs = sorted(old[MODELS[0]])
    for m in MODELS:
        if sorted(old[m]) != langs or sorted(jev[m]) != langs:
            raise SystemExit(f"{m}: SCORES.txt and jev.jsonl cover different languages")
    scales = {"old": old, "jev": jev}
    stats = {(m, s): summary([scales[s][m][l] for l in langs]) for m in MODELS for s in scales}
    n = len(MODELS) * len(langs)

    print(f"Computed from `SCORES.txt` and `jev.jsonl` for {len(MODELS)} translators x "
          f"{len(langs)} languages = {n} translations.\n")

    print("## Per Translator\n")
    print("Five-number summary as `generate_compare_rows.py graph` draws it (whiskers at "
          "1.5 IQR), and the tier counts at the unchanged 90 / 80 / 60 cuts.\n")
    print("| Translator | scale | mean | min | q1 | median | q3 | max | pstdev | "
          + " | ".join(t[0] for t in TIERS) + " |")
    print("|---|---|" + "---:|" * (7 + len(TIERS)))
    for m in MODELS:
        for s in scales:
            x = stats[(m, s)]
            cells = [f"{x['mean']:.2f}"] + [f"{x[k]:.1f}" for k in ("min", "q1", "median", "q3", "max")]
            cells += [f"{x['pstdev']:.2f}"] + [str(c) for c in x["tiers"]]
            print(f"| {m if s == 'old' else ''} | {s} | " + " | ".join(cells) + " |")

    print("\n## Ranking\n")
    print("By `(median, pstdev)`, the order `generate_compare_rows.py` sorts the chart in.\n")
    orders = {s: sorted(MODELS, key=lambda m: (-stats[(m, s)]["median"], stats[(m, s)]["pstdev"]))
              for s in scales}
    print("| # | old | median | jev | median |")
    print("|---:|---|---:|---|---:|")
    for i, (a, b) in enumerate(zip(orders["old"], orders["jev"]), 1):
        print(f"| {i} | {a} | {stats[(a, 'old')]['median']:.1f} | "
              f"{b} | {stats[(b, 'jev')]['median']:.1f} |")
    means = {s: [stats[(m, s)]["mean"] for m in MODELS] for s in scales}
    print(f"\nOver the {len(MODELS)} translators' means: Spearman "
          f"{ss.spearmanr(means['old'], means['jev'])[0]:+.3f}, Kendall "
          f"{ss.kendalltau(means['old'], means['jev'])[0]:+.3f}.")

    print("\n## The Top Four, Pairwise\n")
    print("Per language, first minus second. `agree` counts the languages where both "
          "scales take a side and it is the same side.\n")
    print("| Pair | scale | mean Δ | median Δ | win / loss / tie | sign p | Wilcoxon p | dz | agree |")
    print("|---|---|---:|---:|---|---:|---:|---:|---|")
    for a, b in combinations(TOP, 2):
        signs = {}
        for s in scales:
            d = np.array([scales[s][a][l] - scales[s][b][l] for l in langs])
            signs[s] = np.sign(d)
            w, lo, t = int((d > 0).sum()), int((d < 0).sum()), int((d == 0).sum())
            p_sign = ss.binomtest(w, w + lo).pvalue
            p_wil = ss.wilcoxon(d[d != 0]).pvalue
            both = ((signs["old"] != 0) & (signs["jev"] != 0)) if s == "jev" else None
            agree = (f"{int(((signs['old'] == signs['jev']) & both).sum())} / {int(both.sum())}"
                     if s == "jev" else "")
            print(f"| {a + ' vs ' + b if s == 'old' else ''} | {s} | {d.mean():+.2f} | "
                  f"{np.median(d):+.1f} | {w} / {lo} / {t} | {p_sign:.2g} | {p_wil:.2g} | "
                  f"{d.mean() / d.std(ddof=1):+.2f} | {agree} |")

    print("\n## Agreement by the Old Score's Band\n")
    print("Translation level, pooled over every translator. `sd` is the population "
          "standard deviation of each scale inside the band: correlation falls with range "
          "whatever the evaluator is doing (README section 4.2).\n")
    all_old = [old[m][l] for m in MODELS for l in langs]
    all_jev = [jev[m][l] for m in MODELS for l in langs]
    print("| Old band | n | Pearson | Spearman | Kendall | sd old | sd jev |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    rows = [("all", list(range(n)))]
    rows += [(f"{lo}-{hi - 1}", [i for i, v in enumerate(all_old) if lo <= v < hi]) for lo, hi in BANDS]
    for label, idx in rows:
        r = correlations([all_old[i] for i in idx], [all_jev[i] for i in idx])
        print(f"| {label} | {len(idx)} | {r[0]:+.3f} | {r[1]:+.3f} | {r[2]:+.3f} | "
              f"{r[3]:.2f} | {r[4]:.2f} |")

    print("\n## Agreement per Translator\n")
    print("| Translator | old mean | Pearson | Spearman | Kendall | sd old | sd jev |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for m in sorted(MODELS, key=lambda m: -stats[(m, "old")]["mean"]):
        r = correlations([old[m][l] for l in langs], [jev[m][l] for l in langs])
        print(f"| {m} | {stats[(m, 'old')]['mean']:.2f} | {r[0]:+.3f} | {r[1]:+.3f} | "
              f"{r[2]:+.3f} | {r[3]:.2f} | {r[4]:.2f} |")

    print("\n## Per Criterion\n")
    print("Mean points out of 20 over all languages; Δ is Jev minus old.\n")
    short = {c: c.split("_")[0][:11] for c in CRITERION_IDS}
    print("| Translator | " + " | ".join(f"{short[c]} old | jev | Δ" for c in CRITERION_IDS) + " |")
    print("|---|" + "---:|" * (3 * len(CRITERION_IDS)))
    for m in sorted(MODELS, key=lambda m: -stats[(m, "old")]["mean"]):
        o, j = criterion_means(m)
        print(f"| {m} | " + " | ".join(f"{o[c]:.1f} | {j[c]:.1f} | {j[c] - o[c]:+.1f}"
                                        for c in CRITERION_IDS) + " |")

    print("\n## Speaker Labels\n")
    print("Every line of the original starts with `Camille:` or `Luc:`, and the "
          "translators were given each language's rendering of both names in "
          "`examples/tr/terms/onde-en.tsv`. Lines per class over all languages; a language "
          f"counts under `languages` if any of its lines is {' or '.join(LOST)}. IC is "
          "`information_completeness` in points out of 20, and the last two columns split "
          "Jev's by the same test, within one translator.\n")
    glossary = load_glossary()
    speakers = [line.split(":", 1)[0] for line in ORIGINAL.read_text(encoding="utf-8").splitlines()]
    print("| Translator | languages | " + " | ".join(LABEL_CLASSES)
          + " | unaligned | IC old | IC jev | IC Δ | IC jev, intact | IC jev, lost |")
    print("|---|" + "---:|" * (len(LABEL_CLASSES) + 7))
    pooled = []
    for m in sorted(MODELS, key=lambda m: -stats[(m, "old")]["mean"]):
        evals = sorted(str(p) for p in (ONDE / m / "evals").glob("*.json"))
        old_ic = {k.split("-", 1)[1]: r["statistics"]["information_completeness"]["median"]
                  for k, r in aggregate_evaluations(evals).items()}
        jev_ic = {k.split("-", 1)[1]: r["levels"]["information_completeness"] * POINTS_PER_LEVEL
                  for k, r in aggregate_jev(ONDE / m / "jev.jsonl", "onde").items()}
        total, lost, unaligned = Counter(), {}, 0
        for l in langs:
            counts = classify_labels(m, l, glossary[l], speakers)
            if counts is None:
                unaligned += 1
                continue
            total += counts
            lost[l] = sum(counts[c] for c in LOST)
        pooled += [(lost[l], old_ic[l], jev_ic[l]) for l in lost]
        split = [[jev_ic[l] for l in lost if bool(lost[l]) == flag] for flag in (False, True)]
        cells = [f"{st.mean(x):.1f}" if x else "" for x in split]
        o, j = st.mean(old_ic.values()), st.mean(jev_ic.values())
        print(f"| {m} | {sum(1 for k in lost.values() if k)} | "
              + " | ".join(str(total[c]) for c in LABEL_CLASSES)
              + f" | {unaligned} | {o:.1f} | {j:.1f} | {j - o:+.1f} | {cells[0]} | {cells[1]} |")
    d, o, j = zip(*pooled)
    print(f"\nOver the {len(pooled)} aligned translations, Spearman between lost labels "
          f"and IC: old {ss.spearmanr(d, o)[0]:+.3f}, Jev {ss.spearmanr(d, j)[0]:+.3f}.")
    for label, keep in (("intact", lambda k: k == 0), ("lost", lambda k: k > 0)):
        sel = [(oo, jj) for k, oo, jj in pooled if keep(k)]
        print(f"- {label}: n = {len(sel)}, IC old {st.mean(s[0] for s in sel):.2f}, "
              f"Jev {st.mean(s[1] for s in sel):.2f}")

    print("\n## The Slope\n")
    fit = ss.linregress(all_old, all_jev)
    print(f"Least squares over all {n}: `jev = {fit.slope:.3f} × old + {fit.intercept:.2f}`, "
          f"r = {fit.rvalue:.3f}. The old tier cuts map to "
          + ", ".join(f"{c} -> {fit.slope * c + fit.intercept:.1f}" for c in (60, 80, 90)) + ".")
    rev = ss.linregress(all_jev, all_old)
    print(f"Regressing the other way and inverting gives slope {1 / rev.slope:.3f}; the two "
          f"bracket the line a symmetric fit would draw, and differ because r < 1.")

    print(f"\n## Largest Divergences\n")
    print(f"The {DIVERGENCES} translations whose old score most exceeds its Jev score, "
          f"then the {DIVERGENCES} the other way.\n")
    pairs = [(old[m][l] - jev[m][l], m, l) for m in MODELS for l in langs]
    pairs.sort()
    print("| Translator | lang | old | jev | old − jev |")
    print("|---|---|---:|---:|---:|")
    for d, m, l in pairs[::-1][:DIVERGENCES] + pairs[:DIVERGENCES]:
        print(f"| {m} | {l} | {old[m][l]} | {jev[m][l]:.1f} | {d:+.1f} |")


if __name__ == "__main__":
    main()
