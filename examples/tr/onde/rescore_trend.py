# Rebuilds each model's TREND-jev.jsonl after a Jev version bump without writing new
# phrases: the phrase comes from the archived jev-<old>/TREND-jev.jsonl, the score from
# the new jev.jsonl. The README table is then synced as `trtools trend --render-only`
# would. JEV-1.14.md says why the phrases are kept.
#
# Usage, from examples/tr/onde/: uv run rescore_trend.py [--archive jev-1.13.0] MODEL...

import argparse
import json
from pathlib import Path

from trtools.aggregate import aggregate_jev
from trtools.trend import load_jsonl, render_table, sync_readme

PREFIX = "onde"


def rescore(model_dir, archive):
    old_path = model_dir / archive / "TREND-jev.jsonl"
    new_path = model_dir / "TREND-jev.jsonl"
    if new_path.exists():
        raise SystemExit(f"{new_path} already exists")
    old = load_jsonl(old_path)
    totals = aggregate_jev(model_dir / "jev.jsonl", PREFIX)
    langs = {name[len(PREFIX) + 1:]: result for name, result in totals.items()}
    # Both files must cover the same languages; a phrase with no score, or a score with
    # no phrase, means the re-evaluation is incomplete.
    if set(old) != set(langs):
        raise SystemExit(f"{model_dir}: languages differ between {old_path} and jev.jsonl: "
                         f"{sorted(set(old) ^ set(langs))}")

    records = {}
    with new_path.open("w", encoding="utf-8") as f:
        # In the archive's order, so the two files diff line by line.
        for lang, record in old.items():
            record = {"lang": lang, "score": round(langs[lang]["total"], 1),
                      "analysis": record["analysis"]}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            records[lang] = record
    sync_readme(model_dir / "README.md", render_table(records, "en"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("models", nargs="+", help="Model directories")
    parser.add_argument("--archive", default="jev-1.13.0",
                        help="Directory holding the previous version's files "
                             "(default: jev-1.13.0)")
    args = parser.parse_args()
    for model in args.models:
        rescore(Path(model), args.archive)


if __name__ == "__main__":
    main()
