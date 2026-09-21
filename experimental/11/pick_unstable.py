#!/usr/bin/env python3
"""Ranks existing onde evaluations by how much the score wobbles between runs.

The current 5-criteria/20-point scheme lets the evaluator model pick anywhere in a
20-point range per criterion, so the same evaluator can score the same translation
very differently across runs. Experiment 11 targets the translations where that
wobble is largest, since a scheme that fails to stabilise those is not worth adopting.

Prints a TSV: translator, lang, range, scores, median.
"""

import argparse
import json
import re
from pathlib import Path
from statistics import median

from trtools.language import LANG_NAMES

# Resolved from this file rather than the working directory, so the selection is the
# same wherever the script is run from.
BASE = Path(__file__).resolve().parent
ONDE = BASE.parent.parent / "examples" / "tr" / "onde"
ORIGINAL = BASE.parent.parent / "examples" / "onde-en.txt"
RUN_RE = re.compile(r"^onde-([a-z0-9.]+)-([123])\.json$")


def line_count(path):
    with open(path, encoding="utf-8") as f:
        return len(f.read().rstrip().splitlines())


def load_totals(model_dir):
    """Collect {lang: [score, ...]} for every language with all 3 runs present."""
    runs = {}
    evals = model_dir / "evals"
    if not evals.is_dir():
        return {}
    for path in sorted(evals.iterdir()):
        m = RUN_RE.match(path.name)
        if not m:
            continue
        lang, run = m.group(1), int(m.group(2))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        total = data.get("total_score")
        if isinstance(total, int):
            runs.setdefault(lang, {})[run] = total
    return {lang: [r[i] for i in (1, 2, 3)]
            for lang, r in runs.items() if len(r) == 3}


def matches_original(model_dir, lang, expected):
    """Whether the translation still lines up with the original.

    trtools refuses to evaluate a translation whose line count differs
    (batch.py skips it, evaluate.py raises), so where the counts disagree the
    stored evaluations belong to an older version of the file and say nothing
    about how stable the current one scores.
    """
    path = model_dir / "tr" / f"onde-{lang}.txt"
    try:
        return line_count(path) == expected
    except OSError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--top", type=int, default=30,
                        help="Number of rows to print (default: 30)")
    parser.add_argument("--per-translator", type=int, default=0,
                        help="Keep at most this many rows per translator (0: no limit)")
    parser.add_argument("--exclude", action="append", default=[], metavar="TRANSLATOR/LANG",
                        help="Drop this translation from the ranking (repeatable)")
    args = parser.parse_args()

    expected = line_count(ORIGINAL)
    rows = []
    for model_dir in sorted(ONDE.iterdir()):
        if not model_dir.is_dir():
            continue
        for lang, scores in load_totals(model_dir).items():
            if not matches_original(model_dir, lang, expected):
                continue
            rows.append({
                "translator": model_dir.name,
                "lang": lang,
                "range": max(scores) - min(scores),
                "scores": scores,
                "median": int(median(scores)),
            })

    excluded = set(args.exclude)
    rows = [r for r in rows if f"{r['translator']}/{r['lang']}" not in excluded]
    rows.sort(key=lambda r: (-r["range"], r["translator"], r["lang"]))

    if args.per_translator:
        kept, seen = [], {}
        for r in rows:
            n = seen.get(r["translator"], 0)
            if n < args.per_translator:
                kept.append(r)
                seen[r["translator"]] = n + 1
        rows = kept

    print("translator\tlang\tlang_name\trange\tscores\tmedian")
    for r in rows[:args.top]:
        name = LANG_NAMES.get(r["lang"], r["lang"])
        scores = ",".join(str(s) for s in r["scores"])
        print(f"{r['translator']}\t{r['lang']}\t{name}\t{r['range']}\t{scores}\t{r['median']}")


if __name__ == "__main__":
    main()
