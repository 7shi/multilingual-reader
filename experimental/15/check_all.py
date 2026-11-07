"""Run the language check over every correctly labelled translation of one onde model.

Usage (from the repository root):
    uv run python <this file> qwen [model]
    uv run python <this file> jev  [model]

Writes one JSON line per language to check-<backend>-<model>.jsonl in results/ and
skips languages already in it, so an interrupted run can simply be restarted. When the
check says no, the backend is then asked which language the text is in ("detected"); rows
from an earlier run that said no without asking get that question on the next run.
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


def make_qwen():
    def chat(prompt):
        body = json.dumps({
            "model": "qwen3.6", "think": False, "stream": False,
            "options": {"temperature": 0},
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        req = urllib.request.Request("http://192.168.0.8:11434/api/chat", body,
                                     {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)["message"]["content"].strip()

    def check(lang_name, text):
        answer = chat(f"Is the following text written in {lang_name}? "
                      f"Answer only \"yes\" or \"no\".\n\n```\n{text}\n```")
        return {"answer": answer, "ok": answer.lower().startswith("yes")}

    def identify(text):
        return {"detected": chat("What language is the following text written in? "
                                 "Answer only with the language's English name.\n\n"
                                 f"```\n{text}\n```")}

    return check, identify


def make_jev():
    from typesafe_sdk import Choice, TypeSafeClient
    client = TypeSafeClient(timeout=120.0)

    def ask(text, criteria):
        q = Choice(instructions="Which language is `text` written in?", criteria=criteria)
        return client.system_one({"text": text}, {"language": q},
                                 model="jev-1.14.0").choices["language"]

    def check(lang_name, text):
        a = ask(text, {
            "English": "The text is written in English.",
            lang_name: f"The text is written in {lang_name}.",
        })
        return {"choice": a.choice, "p_english": round(a.probabilities["English"], 4),
                "ok": a.choice == lang_name}

    def identify(text):
        a = ask(text, {name: None for name in ALL_NAMES})
        top = sorted(a.probabilities.items(), key=lambda kv: -kv[1])[:3]
        return {"detected": a.choice,
                "detected_top3": {k: round(v, 4) for k, v in top}}

    return check, identify


def main():
    backend = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "gpt-6-sol"
    check, identify = {"qwen": make_qwen, "jev": make_jev}[backend]()

    tr_dir = ROOT / "examples/tr/onde" / model / "tr"
    out = RESULTS / f"check-{backend}-{model}.jsonl"

    def text_of(lang):
        return (tr_dir / f"onde-{lang}.txt").read_text(encoding="utf-8").rstrip()

    rows = []
    if out.is_file():
        rows = [json.loads(line) for line in out.open(encoding="utf-8")]

    # Rows from before the identify step: ask now and rewrite the file.
    stale = [r for r in rows if not r["ok"] and "detected" not in r]
    for r in stale:
        r.update(identify(text_of(r["lang"])))
        print(json.dumps(r, ensure_ascii=False) + "  <-- REJECTED (backfilled)", flush=True)
    if stale:
        out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                       encoding="utf-8")

    done = {r["lang"] for r in rows}
    for path in sorted(tr_dir.glob("onde-*.txt")):
        lang = path.stem.split("-", 1)[1]
        if lang in done:
            continue
        lang_name = LANGUAGES[lang]["en"]
        text = text_of(lang)
        result = {"lang": lang, "name": lang_name, **check(lang_name, text)}
        if not result["ok"]:
            result.update(identify(text))
        rows.append(result)
        with out.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        flag = "" if result["ok"] else "  <-- REJECTED"
        print(json.dumps(result, ensure_ascii=False) + flag, flush=True)

    bad = [f"{r['lang']}->{r['detected']}" for r in rows if not r["ok"]]
    print(f"\n{out.name}: {len(rows)} languages, rejected: {' '.join(bad) or 'none'}")
    if backend == "jev":
        top = sorted(rows, key=lambda r: -r["p_english"])[:10]
        print("highest p_english: " +
              " ".join(f"{r['lang']}={r['p_english']:.2f}" for r in top))


if __name__ == "__main__":
    main()
