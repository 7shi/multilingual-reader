"""Ask ollama:qwen3.6 whether each text is written in the claimed language."""
import json
import sys
import urllib.request

from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
S = HERE / "mislabel"  # built by mislabel.sh
T = ROOT / "examples/tr/onde/gpt-6-sol/tr"

# (claimed language, file, what it really is)
CASES = [
    ("French", f"{S}/tr/onde-fr.txt", "English"),
    ("German", f"{S}/tr/onde-de.txt", "French"),
    ("Portuguese", f"{S}/tr/onde-pt.txt", "Spanish"),
    ("Chinese", f"{S}/tr/onde-zh.txt", "Japanese"),
    ("Serbian", f"{S}/tr/onde-sr.txt", "Croatian"),
    ("French", f"{T}/onde-fr.txt", "French"),
    ("German", f"{T}/onde-de.txt", "German"),
    ("Portuguese", f"{T}/onde-pt.txt", "Portuguese"),
    ("Chinese", f"{T}/onde-zh.txt", "Chinese"),
    ("Serbian", f"{T}/onde-sr.txt", "Serbian"),
]


def ask(lang, text):
    prompt = (f"Is the following text written in {lang}? "
              f"Answer only \"yes\" or \"no\".\n\n```\n{text}\n```")
    body = json.dumps({
        "model": "qwen3.6", "think": False, "stream": False,
        "options": {"temperature": 0},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request("http://192.168.0.8:11434/api/chat", body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["message"]["content"].strip()


if __name__ == "__main__":
    for lang, path, actual in CASES:
        text = open(path, encoding="utf-8").read().rstrip()
        print(f"claimed={lang:<10} actual={actual:<10} -> {ask(lang, text)}", flush=True)
