"""Have qwen3.6 pick each translation's language from a fixed list, answering in plain text.

Usage (from the repository root):
    uv run python <this file> [model]

Covers every translation of the model plus the English original, so the untranslated case
is in the run. Results go to choose-qwen-<model>.jsonl in results/.
"""
import json
import sys
import urllib.request
from pathlib import Path

from trtools.language import LANGUAGES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "results"
ALL_NAMES = [v["en"] for v in LANGUAGES.values()]

def choose(text):
    prompt = ("What language is the following text written in? "
              "Answer with exactly one name from this list and nothing else:\n"
              + ", ".join(ALL_NAMES) + f"\n\n```\n{text}\n```")
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
    model = sys.argv[1] if len(sys.argv) > 1 else "gpt-6-sol"
    tr_dir = ROOT / "examples/tr/onde" / model / "tr"
    out = RESULTS / f"choose-qwen-{model}.jsonl"
    done = set()
    if out.is_file():
        done = {json.loads(line)["lang"] for line in out.open(encoding="utf-8")}

    files = [ROOT / "examples/onde-en.txt"] + sorted(tr_dir.glob("onde-*.txt"))
    for path in files:
        lang = path.stem.split("-", 1)[1]
        if lang in done:
            continue
        expected = LANGUAGES[lang]["en"]
        detected = choose(path.read_text(encoding="utf-8").rstrip())
        result = {"lang": lang, "expected": expected, "detected": detected,
                  "in_list": detected in ALL_NAMES, "ok": detected == expected}
        with out.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(json.dumps(result, ensure_ascii=False) + ("" if result["ok"] else "  <-- MISMATCH"),
              flush=True)

    rows = [json.loads(line) for line in out.open(encoding="utf-8")]
    bad = [f"{r['lang']}->{r['detected']}" for r in rows if not r["ok"]]
    print(f"\n{out.name}: {len(rows)} texts, mismatched: {' '.join(bad) or 'none'}")


if __name__ == "__main__":
    main()
