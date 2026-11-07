"""Why correct translations fall short in `trtools langcheck`: the same texts, asked in variants.

Usage (from the repository root):
    bash experimental/15/mislabel.sh   # for the mislabelled controls
    uv run python experimental/15/variants_jev.py           # query (resumable), then table
    uv run python experimental/15/variants_jev.py --table   # table only

Cases are the corpus run's false `wrong` and lowest `review` verdicts, plus wrong-language
controls that a variant must still catch. Variants change one thing each from the
langcheck@be2794c4 question:

    base        as trtools langcheck asks
    nolabel     speaker labels stripped (Camille and Luc are French names)
    noother     no `Other` option
    nolabel_no  both
    otherbrief  `Other` described as "None of the listed languages."
    nolabel_ob  speaker labels stripped and the brief `Other`

Writes results/variants-jev.jsonl.
"""
import json
import sys
from pathlib import Path

from trtools.langcheck import (INSTRUCTIONS, OPTION, OTHER, OTHER_DESC, content_lines,
                               option_names)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results/variants-jev.jsonl"
ONDE = ROOT / "examples/tr/onde"
FR = ROOT / "examples/tr/fr/tr"
BRIEF = "None of the listed languages."

# (case id, text path, label, source language, the text is actually in the label: bool)
CASES = [
    ("gemini-2.5-flash/de", ONDE / "gemini-2.5-flash/tr/onde-de.txt", "de", "English", True),
    ("gemma4-e2b/de", ONDE / "gemma4-e2b/tr/onde-de.txt", "de", "English", True),
    ("qwen3.5-4b/de", ONDE / "qwen3.5-4b/tr/onde-de.txt", "de", "English", True),
    ("flint/de", ONDE / "flint/tr/onde-de.txt", "de", "English", True),
    ("gpt-6-sol/de", ONDE / "gpt-6-sol/tr/onde-de.txt", "de", "English", True),
    ("ornith-1.5/zh", ONDE / "ornith-1.5/tr/onde-zh.txt", "zh", "English", True),
    ("gemini-3.5-flash-lite/zh", ONDE / "gemini-3.5-flash-lite/tr/onde-zh.txt", "zh",
     "English", True),
    ("qwen3.8-flash-next/es", ONDE / "qwen3.8-flash-next/tr/onde-es.txt", "es", "English", True),
    ("gemini-3.7-flash/es", ONDE / "gemini-3.7-flash/tr/onde-es.txt", "es", "English", True),
    ("flint/hr", ONDE / "flint/tr/onde-hr.txt", "hr", "English", True),
    ("bonsai2-27b/sr", ONDE / "bonsai2-27b/tr/onde-sr.txt", "sr", "English", True),
    ("gemma4-e4b/ia", ONDE / "gemma4-e4b/tr/onde-ia.txt", "ia", "English", True),
    ("fr:transformer/en", FR / "transformer-en.txt", "en", "French", True),
    ("fr:finetuning/es", FR / "finetuning-es.txt", "es", "French", True),
    # Controls: must stay low on P(label).
    ("mislabel/de=fr", HERE / "mislabel/tr/onde-de.txt", "de", "English", False),
    ("mislabel/pt=es", HERE / "mislabel/tr/onde-pt.txt", "pt", "English", False),
    ("mislabel/zh=ja", HERE / "mislabel/tr/onde-zh.txt", "zh", "English", False),
    ("mislabel/sr=hr", HERE / "mislabel/tr/onde-sr.txt", "sr", "English", False),
    ("bonsai2-27b/fi=en", ONDE / "bonsai2-27b/tr/onde-fi.txt", "fi", "English", False),
]
# name -> (strip labels, Other description or None)
VARIANTS = {
    "base": (False, OTHER_DESC),
    "nolabel": (True, OTHER_DESC),
    "noother": (False, None),
    "nolabel_no": (True, None),
    "otherbrief": (False, BRIEF),
    "nolabel_ob": (True, BRIEF),
}


def question(names, other_desc):
    from typesafe_sdk import Choice
    criteria = {n: OPTION.format(n) for n in names}
    if other_desc is not None:
        criteria[OTHER] = other_desc
    return Choice(instructions=INSTRUCTIONS, criteria=criteria)


def query():
    from typesafe_sdk import TypeSafeClient
    done = set()
    if OUT.is_file():
        done = {(r["case"], r["variant"]) for r in map(json.loads, OUT.open(encoding="utf-8"))}
    with TypeSafeClient(timeout=120.0) as client:
        for case, path, label, source, _ in CASES:
            raw = path.read_text(encoding="utf-8").rstrip()
            names = option_names(label, source)
            for variant, (strip, other_desc) in VARIANTS.items():
                if (case, variant) in done:
                    continue
                text = "\n".join(content_lines(raw)) if strip else raw
                a = client.system_one({"text": text}, {"language": question(names, other_desc)},
                                      model="jev-1.14.0").choices["language"]
                p = {k: round(float(v), 4) for k, v in a.probabilities.items()}
                rec = {"case": case, "variant": variant, "p_label": p[names[0]],
                       "probabilities": p}
                with OUT.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"{case} {variant}: {p[names[0]]:.2f}", flush=True)


def table():
    rows = {(r["case"], r["variant"]): r for r in map(json.loads, OUT.open(encoding="utf-8"))}
    print("| case | " + " | ".join(VARIANTS) + " |")
    print("|---|" + "---:|" * len(VARIANTS))
    for case, *_, correct in CASES:
        cells = []
        for v in VARIANTS:
            r = rows.get((case, v))
            cells.append("" if r is None else f"{r['p_label']:.2f}")
        print(f"| {case}{'' if correct else ' (wrong)'} | " + " | ".join(cells) + " |")
    print("\nTop competitor per cell, for P(label) < 0.8:")
    for (case, v), r in rows.items():
        if r["p_label"] < 0.8:
            top = sorted(r["probabilities"].items(), key=lambda kv: -kv[1])[:3]
            print(f"  {case} {v}: " + " ".join(f"{k}={x:.2f}" for k, x in top))


if __name__ == "__main__":
    if "--table" not in sys.argv:
        query()
    table()
