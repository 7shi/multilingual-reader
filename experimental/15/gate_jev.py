"""Step 2: check each translation against its label with the narrowed choices.

Usage (from the repository root):
    uv run python <this file> <tr dir> [candidates json]

For a text labelled A (from its file name onde-A.txt), Jev picks from A's candidates
(calibrate_jev.py, default candidates-gpt-6-sol.json) plus English and Other.
Writes gate-<tr dir's parent name>.jsonl in results/; resumable.
"""
import json
import sys
from pathlib import Path

from calibrate_jev import NAMES, RESULTS, options

THRESHOLD = 0.5  # p(target) below this is flagged


def main():
    tr_dir = Path(sys.argv[1]).resolve()
    cand_path = Path(sys.argv[2]) if len(sys.argv) > 2 else RESULTS / "candidates-gpt-6-sol.json"
    candidates = json.loads(cand_path.read_text(encoding="utf-8"))
    tag = tr_dir.parent.name
    out = RESULTS / f"gate-{tag}.jsonl"
    done = set()
    if out.is_file():
        done = {json.loads(line)["lang"] for line in out.open(encoding="utf-8")}

    from typesafe_sdk import Choice, TypeSafeClient
    with TypeSafeClient(timeout=120.0) as client:
        for path in sorted(tr_dir.glob("onde-*.txt")):
            lang = path.stem.split("-", 1)[1]
            if lang in done:
                continue
            target = NAMES[lang]
            q = Choice(instructions="Which language is `text` written in?",
                       criteria=options(candidates[lang] + ["English"]))
            text = path.read_text(encoding="utf-8").rstrip()
            a = client.system_one({"text": text}, {"language": q},
                                  model="jev-1.14.0").choices["language"]
            p = {k: round(v, 4) for k, v in a.probabilities.items()}
            rec = {"lang": lang, "choice": a.choice, "p_target": p[target],
                   "flagged": p[target] < THRESHOLD, "probabilities": p}
            with out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            top = sorted(p.items(), key=lambda kv: -kv[1])[:3]
            print(f"{lang}: p_target={p[target]:.2f} | "
                  + " ".join(f"{k}={v:.2f}" for k, v in top)
                  + ("  <-- FLAGGED" if rec["flagged"] else ""), flush=True)

    rows = [json.loads(line) for line in out.open(encoding="utf-8")]
    flagged = [f"{r['lang']}->{r['choice']}" for r in rows if r["flagged"]]
    print(f"\n{out.name}: {len(rows)} texts, flagged: {' '.join(flagged) or 'none'}")
    low = sorted(rows, key=lambda r: r["p_target"])[:10]
    print("lowest p_target: " + " ".join(f"{r['lang']}={r['p_target']:.2f}" for r in low))


if __name__ == "__main__":
    main()
