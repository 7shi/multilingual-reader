"""Step 1: ask Jev to pick each text's language from every language + English + Other.

Usage (from the repository root):
    uv run python <this file> [model]          # query (resumable), then aggregate
    uv run python <this file> [model] --agg    # aggregate only

Query: one Choice per text over all 69 options. Texts are the model's translations plus
the English original. Raw probabilities go to calib-jev-<model>.jsonl.

Aggregate: for each target language A, candidates are A itself plus the other languages
ranked by max(row, col), where
    row = P(B | A's own text)    -- what A's text is mistaken for
    col = P(A | B's text)        -- which texts are mistaken for A
The column matters for the gate: a B-text labelled A is only caught if B is among A's
choices, otherwise its mass may land on A. Up to TOP_N (A included) with score >= MIN_SCORE go to
candidates-<model>.json; English and Other are added at check time.
"""
import json
import sys
from pathlib import Path

from trtools.language import LANGUAGES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "results"
NAMES = {code: v["en"] for code, v in LANGUAGES.items()}
OTHER = "Other"
OTHER_DESC = "The text is written in a language not listed here, or in no language."
TOP_N = 5
MIN_SCORE = 0.01


def options(names):
    crit = {n: f"The text is written in {n}." for n in names}
    crit[OTHER] = OTHER_DESC
    return crit


def query(model, out):
    from typesafe_sdk import Choice, TypeSafeClient
    tr_dir = ROOT / "examples/tr/onde" / model / "tr"
    done = set()
    if out.is_file():
        done = {json.loads(line)["lang"] for line in out.open(encoding="utf-8")}
    q = Choice(instructions="Which language is `text` written in?",
               criteria=options(list(NAMES.values())))
    files = [ROOT / "examples/onde-en.txt"] + sorted(tr_dir.glob("onde-*.txt"))
    with TypeSafeClient(timeout=120.0) as client:
        for path in files:
            lang = path.stem.split("-", 1)[1]
            if lang in done:
                continue
            text = path.read_text(encoding="utf-8").rstrip()
            a = client.system_one({"text": text}, {"language": q},
                                  model="jev-1.14.0").choices["language"]
            rec = {"lang": lang, "choice": a.choice,
                   "probabilities": {k: round(v, 4) for k, v in a.probabilities.items()}}
            with out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            top = sorted(rec["probabilities"].items(), key=lambda kv: -kv[1])[:3]
            mark = "" if a.choice == NAMES[lang] else "  <-- MISMATCH"
            print(f"{lang}: {' '.join(f'{k}={v:.2f}' for k, v in top)}{mark}", flush=True)


def aggregate(model, out):
    rows = {r["lang"]: r["probabilities"]
            for r in map(json.loads, out.open(encoding="utf-8"))}
    targets = [lang for lang in rows if lang != "en"]
    candidates = {}
    for a in targets:
        name_a = NAMES[a]
        score = {}
        for b in targets:
            if b == a:
                continue
            name_b = NAMES[b]
            score[name_b] = max(rows[a].get(name_b, 0.0), rows[b].get(name_a, 0.0))
        # Only languages that drew any probability (the API reports 0.01 steps); padding
        # to a fixed count only added alphabetical ties at 0.00.
        others = [(n, s) for n, s in sorted(score.items(), key=lambda kv: -kv[1])
                  if s >= MIN_SCORE][:TOP_N - 1]
        candidates[a] = [name_a] + [n for n, _ in others]
        print(f"{a}: self={rows[a].get(name_a, 0):.2f} English={rows[a].get('English', 0):.2f} "
              f"Other={rows[a].get(OTHER, 0):.2f} | "
              + " ".join(f"{n}={s:.3f}" for n, s in others))
    path = RESULTS / f"candidates-{model}.json"
    path.write_text(json.dumps(candidates, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    print(f"\nwrote {path.name}")
    print("en text: " + " ".join(f"{k}={v:.2f}" for k, v in
                                 sorted(rows["en"].items(), key=lambda kv: -kv[1])[:5]))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    model = args[0] if args else "gpt-6-sol"
    out = RESULTS / f"calib-jev-{model}.jsonl"
    if "--agg" not in sys.argv:
        query(model, out)
    aggregate(model, out)


if __name__ == "__main__":
    main()
