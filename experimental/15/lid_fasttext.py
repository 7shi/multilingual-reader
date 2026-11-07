"""Language identification with fastText's lid.176 over the whole corpus, no API.

Usage (from the repository root):
    uv run python experimental/15/lid_fasttext.py [ftz|bin]

Needs the dev dependency fasttext-predict and the model in experimental/15/lid/
(gitignored), from https://dl.fbaipublicfiles.com/fasttext/supervised-models/.
Run `bash experimental/15/mislabel.sh` first so the wrong-language controls are included.

Per text, two readings:
    whole   the text joined into one line (fastText predicts per line), P(label)
    lines   the share of content lines (speaker label stripped, MIN_CHARS or longer)
            whose top prediction is the label; catches a text partly left in the source

Writes results/lid-<model>.jsonl and prints the texts that fall short.
"""
import json
import sys
from pathlib import Path

import fasttext

from trtools.langcheck import content_lines

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TR = ROOT / "examples/tr"
MIN_CHARS = 30


def texts():
    """(set, label, path, actually in the label)"""
    for d in sorted((TR / "onde").glob("*/tr")):
        if not (d.parent / "jev.jsonl").is_file():
            continue  # a set still being produced
        for p in sorted(d.glob("onde-*.txt")):
            yield d.parent.name, p.stem.split("-", 1)[1], p, True
    for name in ("core", "fr"):
        for p in sorted((TR / name / "tr").glob("*-*.txt")):
            topic, lang = p.stem.rsplit("-", 1)
            yield f"{name}:{topic}", lang, p, True
    for p in sorted((HERE / "mislabel/tr").glob("onde-*.txt")):
        yield "mislabel", p.stem.split("-", 1)[1], p, False


def predict(model, text, k=3):
    labels, probs = model.predict(text, k=k)
    return {l.removeprefix("__label__"): round(float(p), 4) for l, p in zip(labels, probs)}


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "ftz"
    model = fasttext.load_model(str(HERE / f"lid/lid.176.{kind}"))
    out = HERE / f"results/lid-{kind}.jsonl"
    rows = []
    for tag, label, path, correct in texts():
        lines = content_lines(path.read_text(encoding="utf-8"))
        whole = predict(model, " ".join(lines), k=176)
        long = [l for l in lines if len(l) >= MIN_CHARS]
        tops = [next(iter(predict(model, l, k=1))) for l in long]
        rows.append({
            "set": tag, "label": label, "correct": correct,
            "p_label": whole.get(label, 0.0),
            "top": dict(list(whole.items())[:3]),
            "line_share": round(sum(t == label for t in tops) / len(tops), 4) if tops else None,
            "lines": len(tops),
            "line_others": {t: tops.count(t) for t in sorted(set(tops)) if t != label},
        })
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                   encoding="utf-8")
    good = [r for r in rows if r["correct"]]
    print(f"{out.name}: {len(good)} correct texts, {len(rows) - len(good)} controls")
    for key in ("p_label", "line_share"):
        vals = sorted(r[key] for r in good if r[key] is not None)
        print(f"  correct {key}: min {vals[0]:.2f}, 1% {vals[len(vals) // 100]:.2f}, "
              f"5% {vals[len(vals) // 20]:.2f}")
    print("\nCorrect texts with p_label < 0.9 or line_share < 0.9:")
    for r in sorted(good, key=lambda r: r["p_label"]):
        if r["p_label"] < 0.9 or (r["line_share"] or 0) < 0.9:
            print(f"  {r['set']} {r['label']}: p={r['p_label']:.2f} lines={r['line_share']} "
                  f"top={r['top']} others={r['line_others']}")
    print("\nControls:")
    for r in rows:
        if not r["correct"]:
            print(f"  {r['set']} {r['label']}: p={r['p_label']:.2f} lines={r['line_share']} "
                  f"top={r['top']}")


if __name__ == "__main__":
    main()
