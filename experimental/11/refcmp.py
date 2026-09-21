#!/usr/bin/env python3
"""Compares evals/, evals-nt/ and evals-ne/ against one evaluator taken as reference.

agg50.py reports each variant on its own terms: how far scores move between runs, how
far they move between evaluators, how much time a call costs. None of that says which
variant to run, because a variant that makes an evaluator steadier can equally be making
it steadily wrong.

This script answers the variant question under an explicit assumption: that one
evaluator (by default gpt-5.6-terra, the evaluator the ground-truth check in README
section 3 found exact on all 8 targets) is the closest thing available to correct. Every
other evaluator and every variant is then scored by how well it reproduces that
reference -- not only in total score, but in which of the reference's 50 item verdicts it
actually reproduces, since a total can match by accident.

The assumption is an assumption. --reference re-runs everything against a different
evaluator, which is the cheapest way to see whether a conclusion depends on it.

Writes a Markdown report to stdout.
"""

import argparse
import json
import re
from pathlib import Path
from statistics import mean, median
from itertools import combinations

from items import GROUPS, ITEM_IDS

BASE = Path(__file__).resolve().parent
# Resolved from this file rather than the working directory, so the report can be
# generated from anywhere -- the corpus is read in place, never copied here.
ONDE = BASE.parent.parent / "examples" / "tr" / "onde"
RUNS = (1, 2, 3)
VARIANTS = ("evals", "evals-nt", "evals-ne")
VERDICT_SCORES = {"yes": 2, "partial": 1, "no": 0}
NAME_RE = re.compile(r"^onde-(.+)-([a-z]{2})-(.+)-(\d+)\.json$")
# A speaker label is a short run of text before the first colon. The colon further into
# the line at ru:9 is sentence punctuation, not a label, and the 25-character cutoff is
# what separates the two.
LABEL_RE = re.compile(r"^[^:：]{1,25}[:：]")


def verdict_of(judged):
    """A judged item's verdict, whichever shape it came back as.

    Without evidence, an item may be the bare verdict string the schema asked for, or
    (if the model wrapped it anyway) a {"verdict": ...} object -- see eval50.py.
    """
    return judged["verdict"] if isinstance(judged, dict) else judged


def evidence_of(judged):
    return judged.get("evidence", "") if isinstance(judged, dict) else ""


def load(variant):
    """Collect {(translator, lang, evaluator): [run data, ...]} from a directory."""
    runs = {}
    directory = BASE / variant
    if not directory.is_dir():
        return runs
    for path in sorted(directory.iterdir()):
        m = NAME_RE.match(path.name)
        if not m:
            continue
        translator, lang, evaluator, run = m.groups()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print(f"<!-- unreadable: {path.name} -->")
            continue
        runs.setdefault((translator, lang, evaluator), {})[int(run)] = data
    return {k: [v[r] for r in sorted(v)] for k, v in runs.items()}


def medians(data):
    """Per-item median verdict score across the runs of one combination."""
    return {i: median([VERDICT_SCORES[verdict_of(d["evaluation"][i])] for d in data])
            for i in ITEM_IDS}


def median_total(data):
    return int(sum(medians(data).values()))


def old_corpus_means(langs):
    """Each language's old-scheme mean over every translator in the corpus.

    README's provisional position treats this as the better-verified reference: it is a
    mean over every translator in the corpus rather than the single translation per
    language this experiment evaluates. Each translator contributes the median of its
    three runs, which is the figure the corpus README quotes. Read where it lives;
    nothing is copied here.
    """
    out = {}
    for lang in langs:
        per_translator = []
        for evals_dir in sorted(ONDE.glob("*/evals")):
            totals = []
            for run in RUNS:
                path = evals_dir / f"onde-{lang}-{run}.json"
                if not path.exists():
                    continue
                try:
                    totals.append(json.loads(path.read_text(encoding="utf-8"))["total_score"])
                except (OSError, json.JSONDecodeError, KeyError):
                    continue
            if totals:
                per_translator.append(median(totals))
        if per_translator:
            out[lang] = mean(per_translator)
    return out


def unlabeled_lines(translator, lang):
    """Lines carrying no speaker label, the ground truth for a01_speaker_label_present.

    The source labels all 99 lines, so any unlabeled line in the translation is a
    dropped label. README section 3 uses the same count.
    """
    path = ONDE / translator / "tr" / f"onde-{lang}.txt"
    if not path.exists():
        return None
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return sum(1 for l in lines if not LABEL_RE.match(l))


def a01_truth(count):
    """The rubric's bands for a01: 0 unlabeled lines is yes, 1-3 partial, 4+ no."""
    if count == 0:
        return 2
    return 1 if count <= 3 else 0


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


def detection(variant_data, targets, evaluator, reference):
    """How many of the reference's defects the evaluator also reports, and how cleanly.

    The reference's non-yes item medians are the defects to be found. Recall is the share
    of them the evaluator also scores below yes; precision is the share of the
    evaluator's own non-yes verdicts that the reference agrees with. Two evaluators can
    land on the same total while sharing almost none of these, which is exactly what the
    totals cannot show.
    """
    found = missed = extra = 0
    for translator, lang in targets:
        ref = variant_data.get((translator, lang, reference))
        own = variant_data.get((translator, lang, evaluator))
        if not ref or not own:
            continue
        ref_items, own_items = medians(ref), medians(own)
        for item in ITEM_IDS:
            if ref_items[item] < 2:
                if own_items[item] < 2:
                    found += 1
                else:
                    missed += 1
            elif own_items[item] < 2:
                extra += 1
    defects = found + missed
    return {
        "defects": defects,
        "recall": found / defects if defects else 0.0,
        "precision": found / (found + extra) if found + extra else 0.0,
        "extra": extra,
    }


def agreement(variant_data, targets, evaluator, reference):
    """Share of item medians where the evaluator and the reference return the same verdict."""
    same = total = 0
    for translator, lang in targets:
        ref = variant_data.get((translator, lang, reference))
        own = variant_data.get((translator, lang, evaluator))
        if not ref or not own:
            continue
        ref_items, own_items = medians(ref), medians(own)
        for item in ITEM_IDS:
            total += 1
            if ref_items[item] == own_items[item]:
                same += 1
    return same / total if total else 0.0


def scores_over(variant_data, targets, evaluator):
    out = []
    for translator, lang in targets:
        data = variant_data.get((translator, lang, evaluator))
        out.append(median_total(data) if data else None)
    return out


def run_range(variant_data, targets, evaluator):
    values = []
    for translator, lang in targets:
        data = variant_data.get((translator, lang, evaluator))
        if data:
            totals = [d["total_score"] for d in data]
            values.append(max(totals) - min(totals))
    return mean(values) if values else 0.0


def call_time(variant_data, targets, evaluator):
    values = [d["duration_seconds"]
              for translator, lang in targets
              for d in variant_data.get((translator, lang, evaluator), [])
              if "duration_seconds" in d]
    return mean(values) if values else None


def group_subtotal(variant_data, targets, evaluator, group):
    values = []
    for translator, lang in targets:
        data = variant_data.get((translator, lang, evaluator))
        if data:
            items = medians(data)
            values.append(sum(v for i, v in items.items() if i[0] == group))
    return mean(values) if values else 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", default=str(BASE / "targets.tsv"))
    parser.add_argument("--reference", default="gpt-5.6-terra",
                        help="evaluator treated as correct (default: gpt-5.6-terra)")
    args = parser.parse_args()

    targets = []
    for line in Path(args.targets).read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip():
            fields = line.split("\t")
            targets.append((fields[0], fields[1]))
    langs = [lang for _, lang in targets]

    data = {v: load(v) for v in VARIANTS}
    variants = [v for v in VARIANTS if data[v]]
    reference = args.reference
    evaluators = sorted({k[2] for k in data[variants[0]]})
    others = [e for e in evaluators if e != reference]

    print("# Experiment 11: which variant, taking one evaluator as reference\n")
    print(f"Reference evaluator: `{reference}`. Variants: "
          + ", ".join(f"`{v}/`" for v in variants) + ".\n")
    print("Every figure below is a median of 3 runs. The reference is assumed correct; "
          "the report measures how far each variant moves the other evaluators toward "
          "or away from it, and what the variant does to the reference itself.\n")

    print("## 1. The reference under each variant\n")
    print("If the reference itself moved between variants, nothing further could be "
          "compared. Its own per-target scores:\n")
    print("| Target | " + " | ".join(variants) + " | Spread |")
    print("| --- | " + " ".join("---: |" for _ in variants) + " ---: |")
    for translator, lang in targets:
        cells = [median_total(data[v][(translator, lang, reference)]) for v in variants]
        print(f"| {translator} / {lang} | " + " | ".join(str(c) for c in cells)
              + f" | {max(cells) - min(cells)} |")
    for label, fn in (("Mean score", lambda v: mean(scores_over(data[v], targets, reference))),
                      ("Mean run-to-run range", lambda v: run_range(data[v], targets, reference)),
                      ("Mean call time", lambda v: call_time(data[v], targets, reference))):
        cells = [fn(v) for v in variants]
        fmt = "{:.0f}s" if label == "Mean call time" else "{:.1f}"
        print(f"| **{label}** | " + " | ".join(fmt.format(c) for c in cells) + " | |")
    print()
    for a, b in combinations(variants, 2):
        moved = sum(1 for translator, lang in targets
                    for item in ITEM_IDS
                    if medians(data[a][(translator, lang, reference)])[item]
                    != medians(data[b][(translator, lang, reference)])[item])
        total = len(targets) * len(ITEM_IDS)
        print(f"- `{a}` vs `{b}`: {moved}/{total} of the reference's item medians differ "
              f"({moved / total:.1%}).")
    print()

    print("## 2. Ground truth on a01_speaker_label_present\n")
    print("Unlabeled lines are counted from the translations, and the rubric's bands "
          "(0 = yes, 1-3 = partial, 4+ = no) turn the count into the correct verdict. "
          "This is the one item that does not depend on the reference assumption.\n")
    truth = {}
    for translator, lang in targets:
        count = unlabeled_lines(translator, lang)
        truth[lang] = None if count is None else a01_truth(count)
        print(f"- {translator} / {lang}: {count} unlabeled lines -> "
              + {2: "yes", 1: "partial", 0: "no"}[truth[lang]])
    print()
    print("| Evaluator | " + " | ".join(f"{v} exact | {v} bias" for v in variants) + " |")
    print("| --- | " + " ".join("---: | ---: |" for _ in variants))
    for evaluator in evaluators:
        cells = []
        for v in variants:
            exact, bias = 0, []
            for translator, lang in targets:
                got = medians(data[v][(translator, lang, evaluator)])["a01_speaker_label_present"]
                if got == truth[lang]:
                    exact += 1
                bias.append(got - truth[lang])
            cells += [f"{exact}/{len(targets)}", f"{mean(bias):+.2f}"]
        print(f"| `{evaluator}` | " + " | ".join(cells) + " |")
    print("\nBias is the mean signed error with yes=2, partial=1, no=0; "
          "positive means scoring higher than the count warrants.\n")

    print(f"## 3. Distance from the reference, per variant\n")
    print("MAD is the mean absolute difference in total score. Recall and precision are "
          "over the reference's non-yes item medians: recall is how many of its defects "
          "the evaluator also reports, precision is how many of the evaluator's own "
          "reports the reference shares. False alarms are the non-yes verdicts the reference "
          "scores yes. Agreement is over all 50 item medians, defects and clean "
          "verdicts alike.\n")
    for v in variants:
        print(f"### {v}\n")
        print("| Evaluator | Mean score | MAD | Pearson | Spearman | Kendall "
              "| Recall | Precision | False alarms | Item agreement |")
        print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        ref_scores = scores_over(data[v], targets, reference)
        print(f"| `{reference}` | {mean(ref_scores):.1f} | 0.0 | - | - | - "
              "| - | - | - | - |")
        for evaluator in others:
            own = scores_over(data[v], targets, evaluator)
            det = detection(data[v], targets, evaluator, reference)
            print(f"| `{evaluator}` | {mean(own):.1f} "
                  f"| {mean(abs(x - r) for x, r in zip(own, ref_scores)):.1f} "
                  f"| {pearson(own, ref_scores):.2f} | {spearman(own, ref_scores):.2f} "
                  f"| {kendall(own, ref_scores):.2f} | {det['recall']:.1%} "
                  f"| {det['precision']:.1%} | {det['extra']} | "
                  f"{agreement(data[v], targets, evaluator, reference):.1%} |")
        print()

    print("## 4. Verdict distribution and evidence fill\n")
    print("| Evaluator | Variant | yes | partial | no | Evidence filled |")
    print("| --- | --- | ---: | ---: | ---: | ---: |")
    for evaluator in evaluators:
        for v in variants:
            counts = {"yes": 0, "partial": 0, "no": 0}
            filled = total = 0
            for translator, lang in targets:
                for d in data[v][(translator, lang, evaluator)]:
                    for item in ITEM_IDS:
                        judged = d["evaluation"][item]
                        counts[verdict_of(judged)] += 1
                        total += 1
                        if evidence_of(judged).strip():
                            filled += 1
            print(f"| `{evaluator}` | {v} | "
                  + " | ".join(f"{counts[k] / total:.1%}" for k in ("yes", "partial", "no"))
                  + f" | {filled / total:.1%} |")
    print()

    print("## 5. Group subtotals, per variant\n")
    print("Out of 20 per group, meaned over the targets.\n")
    print("| Evaluator | Variant | " + " | ".join(g.upper() for g in GROUPS) + " |")
    print("| --- | --- | " + " ".join("---: |" for _ in GROUPS))
    for evaluator in evaluators:
        for v in variants:
            cells = [group_subtotal(data[v], targets, evaluator, g) for g in GROUPS]
            print(f"| `{evaluator}` | {v} | " + " | ".join(f"{c:.1f}" for c in cells) + " |")
    print()

    corpus = old_corpus_means(langs)
    if len(corpus) == len(set(langs)):
        print("## 6. Correlation with the old scheme's per-language corpus mean\n")
        print("An independent reference: each language's old-scheme mean over every "
              "translator in examples/tr/onde/, which README's provisional position "
              "treats as the better-verified of the two old-scheme references. It does "
              "not depend on the reference evaluator assumption either.\n")
        print("| Language | " + " | ".join(langs) + " |")
        print("| --- | " + " ".join("---: |" for _ in langs))
        print("| Old corpus mean | " + " | ".join(f"{corpus[l]:.1f}" for l in langs) + " |\n")
        print("| Evaluator | Variant | Pearson | Spearman | Kendall |")
        print("| --- | --- | ---: | ---: | ---: |")
        reference_values = [corpus[l] for l in langs]
        for evaluator in evaluators:
            for v in variants:
                own = scores_over(data[v], targets, evaluator)
                print(f"| `{evaluator}` | {v} | {pearson(own, reference_values):.2f} "
                      f"| {spearman(own, reference_values):.2f} "
                      f"| {kendall(own, reference_values):.2f} |")
        print()

    print("## 7. Call time, per variant\n")
    print("| Evaluator | " + " | ".join(variants) + " |")
    print("| --- | " + " ".join("---: |" for _ in variants))
    for evaluator in evaluators:
        cells = [call_time(data[v], targets, evaluator) for v in variants]
        print(f"| `{evaluator}` | "
              + " | ".join("-" if c is None else f"{c:.0f}s" for c in cells) + " |")


if __name__ == "__main__":
    main()
