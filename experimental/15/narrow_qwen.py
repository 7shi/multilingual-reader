"""Step 0 of PORT.md: qwen3.6 as the fallback, asked over the gate's narrowed options.

Usage (from the repository root):
    bash experimental/15/mislabel.sh   # for the mislabelled cases
    uv run python experimental/15/narrow_qwen.py

Each text is asked with the same options gate_jev.py gives Jev (the label's candidates +
English + Other), listed in the prompt, plain-text answer. Cases are the ones the Jev band
would send to qwen3.6 and the ones qwen3.6 got wrong over all 68.
Results go to results/narrow-qwen.jsonl.
"""
import json
import urllib.request

from calibrate_jev import HERE, NAMES, OTHER, RESULTS, options

ROOT = HERE.parents[1]
ONDE = ROOT / "examples/tr/onde"
# (set, label, what the text actually is)
CASES = [
    ("bonsai2-27b", "sr", "sr"),
    ("bonsai2-27b", "de", "de"),
    ("bonsai2-27b", "sk", "sk"),   # line 6 left in English
    ("bonsai2-27b", "fi", "en"),   # the English source, then bare speaker names
    ("gpt-6-sol", "sr", "sr"),
    ("gpt-6-sol", "ia", "ia"),
    ("mislabel", "sr", "hr"),
    ("mislabel", "fr", "en"),
    ("mislabel", "de", "fr"),
    ("mislabel", "pt", "es"),
    ("mislabel", "zh", "ja"),
]


def ask(text, names):
    prompt = ("What language is the following text written in? "
              "Answer with exactly one name from this list and nothing else:\n"
              + "\n".join(f"- {n}: {d}" for n, d in options(names).items())
              + f"\n\n```\n{text}\n```")
    body = json.dumps({
        "model": "qwen3.6", "think": False, "stream": False,
        "options": {"temperature": 0},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request("http://192.168.0.8:11434/api/chat", body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["message"]["content"].strip()


def main():
    candidates = json.loads((RESULTS / "candidates-gpt-6-sol.json").read_text(encoding="utf-8"))
    out = RESULTS / "narrow-qwen.jsonl"
    done = set()
    if out.is_file():
        done = {(r["set"], r["label"]) for r in map(json.loads, out.open(encoding="utf-8"))}
    for tag, label, actual in CASES:
        if (tag, label) in done:
            continue
        tr_dir = HERE / "mislabel/tr" if tag == "mislabel" else ONDE / tag / "tr"
        names = candidates[label] + ["English"]
        text = (tr_dir / f"onde-{label}.txt").read_text(encoding="utf-8").rstrip()
        raw = ask(text, names)
        # The model sometimes echoes the option's description after the name.
        answer = raw.split(":", 1)[0].strip()
        expected = "English" if actual == "en" else NAMES[actual]
        if expected not in names:
            expected = OTHER
        rec = {"set": tag, "label": label, "actual": actual, "options": names + [OTHER],
               "raw": raw, "answer": answer, "expected": expected, "ok": answer == expected}
        with out.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{tag} {label} (actually {actual}): {answer}"
              + ("" if rec["ok"] else f"  <-- expected {expected}"), flush=True)


if __name__ == "__main__":
    main()
