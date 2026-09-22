#!/usr/bin/env python3
"""One-off: render this experiment's per-language JSON in the corpus's `jev.jsonl` format.

[PORT.md](PORT.md) section 8. Four translators -- `gpt-5.6-luna`, `union-alpha`,
`qwen3.8` and `bonsai2-27b` -- were evaluated here before the corpus had a format to
receive the results, and every field the corpus needs is already in those 268 files:
`expected_scores / 5` gives the levels, and `confidence`, `probabilities`, `usage` and
`model_used` carry over unchanged.

**This is not how the corpus gets its data.** All 16 translators are generated through
`trtools jev`, including these four, so that the production path's wall time and cost are
measured at full scale rather than extrapolated from a quarter of it. What this script is
for is the comparison that becomes possible once they have been: the same languages scored
twice by the same pinned model on the same rubric, once by `eval5_jev.py` and once by the
port, rendered in one format so they can be diffed line by line. Experiment 12's README
section 3.1 puts this evaluator's run-to-run range at 1.12 points, which is the band the
two runs should agree inside. It is also the fallback if the paid path is ever
unavailable.

`scheme_id()` answers a narrower question: whether `trtools/jev_criteria.py` asks Jev the
same wording. It hashes every question's instructions, the level texts and the state's key
order, all read from the frozen code in this directory rather than retyped. Equal hashes
are necessary and not sufficient -- they say nothing about the rest of the request, which
is what the comparison above is for.

This is deliberately not part of `trtools`. It runs against files that exist only in this
directory, and it should be deleted along with this experiment rather than maintained.

Usage, from the repository root:

    uv run experimental/13/port.py --dry-run     # report what would be written
    uv run experimental/13/port.py               # render into experimental/13/jsonl-old/
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from criteria import CRITERION_IDS, DEFAULT_LEVEL_SET, LEVEL_SETS, POINTS_PER_LEVEL
from eval5_jev import build_questions, build_state

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
SOURCE_DIR = BASE_DIR / "evals-degrees"
# Never examples/tr/onde/{model}/jev.jsonl: that file belongs to `trtools jev`, and this
# script's output exists to be compared against it, not to stand in for it.
OUT_DIR = BASE_DIR / "jsonl-old"
ONDE = REPO_ROOT / "examples" / "tr" / "onde"

# The pinned version every file in evals-degrees/ was scored by. A file naming anything
# else is not part of this run and is not silently folded into it.
EXPECTED_MODEL = "jev-1.13.0"
LEVEL_SET = DEFAULT_LEVEL_SET
N_LEVELS = len(LEVEL_SETS[LEVEL_SET])


def scheme_id():
    """Eight hex characters identifying everything that determines a score.

    The level texts alone are not enough. What the model is asked is `build_questions`'s
    instructions -- `judge`, the per-criterion description, and `scope` -- and what it is
    asked about is `build_state`'s named keys. Any of those can be reworded without
    touching LEVEL_SETS, and the scores would move with nothing in the data to show it.

    Only the strings are hashed, never a serialised SDK object, so an unrelated change in
    typesafe_sdk's model shape cannot invalidate results already on disk.
    """
    levels = LEVEL_SETS[LEVEL_SET]
    questions = build_questions(levels)
    parts = []
    for key in CRITERION_IDS:
        instructions = questions[key].instructions
        parts += [key, instructions["judge"], instructions["criterion"],
                  instructions["scope"]]
        if list(questions[key].criteria) != list(levels):
            raise SystemExit(f"{key} was not built on the {LEVEL_SET} levels")
    parts += levels
    # Key order, not the values: the values are per-language text.
    parts += list(build_state("", "", "English", "Japanese"))
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return f"{LEVEL_SET}@{digest[:8]}"


def load(path, rubric):
    """One evaluation file as one `jev.jsonl` record, or raise.

    Every check here is a refusal to convert something this script does not understand.
    A file scored on other levels, by another model version, or with a level missing from
    the distribution would still produce a plausible-looking line, and a plausible-looking
    line is the one failure that would not be noticed later.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    lang = path.stem

    if data.get("level_set") != LEVEL_SET:
        raise ValueError(f"{path}: level set {data.get('level_set')!r}, expected {LEVEL_SET!r}")
    if data.get("levels") != LEVEL_SETS[LEVEL_SET]:
        raise ValueError(f"{path}: level texts differ from criteria.py's {LEVEL_SET} set")
    for field in ("model_used", "model_requested"):
        if data.get(field) != EXPECTED_MODEL:
            raise ValueError(f"{path}: {field} is {data.get(field)!r}, expected {EXPECTED_MODEL!r}")

    for field in ("expected_scores", "confidence", "probabilities"):
        if set(data.get(field, {})) != set(CRITERION_IDS):
            raise ValueError(f"{path}: {field} does not cover the five criteria")

    scores, confidence, probabilities = {}, {}, {}
    for key in CRITERION_IDS:
        probs = data["probabilities"][key]
        if set(probs) != {str(i) for i in range(N_LEVELS)}:
            raise ValueError(f"{path}: {key} has levels {sorted(probs)}")
        # Levels, not points: PORT.md section 2. The 0-20 scale is POINTS_PER_LEVEL's
        # doing and stays a presentation choice.
        scores[key] = round(data["expected_scores"][key] / POINTS_PER_LEVEL, 4)
        confidence[key] = data["confidence"][key]
        probabilities[key] = [probs[str(i)] for i in range(N_LEVELS)]

    usage = data.get("usage") or {}
    return {
        "lang": lang,
        "model": data["model_used"],
        "rubric": rubric,
        "scores": scores,
        "confidence": confidence,
        "probabilities": probabilities,
        "usage": {"input_tokens": usage.get("input_tokens"),
                  "output_tokens": usage.get("output_tokens")},
        # Formally the corpus's `seconds`, but not the same measurement. The corpus times
        # the whole processing of a language; eval5_jev.py timed evaluate() alone, so what
        # goes here is request time, a lower bound. The field is filled anyway to keep the
        # two files the same shape, which is what makes them diffable.
        "seconds": data.get("duration_seconds"),
    }


def convert(translator, rubric, out_dir, force, dry_run):
    """Write one translator's jsonl. Returns (languages, input tokens, output tokens)."""
    src = SOURCE_DIR / translator
    files = sorted(src.glob("*.json"))
    if not files:
        raise SystemExit(f"no evaluation files in {src}")

    corpus_dir = ONDE / translator
    if not corpus_dir.is_dir():
        raise SystemExit(f"no corpus directory for {translator}: {corpus_dir}")
    out_path = out_dir / f"{translator}.jsonl"
    if out_path.exists() and not force:
        raise SystemExit(f"{out_path} exists; pass --force to replace it")

    records = []
    for path in files:
        record = load(path, rubric)
        # The corpus has to have the translation these scores were given to. A language
        # present here and absent there would mean the two directories disagree about
        # what was translated.
        translation = corpus_dir / "tr" / f"onde-{record['lang']}.txt"
        if not translation.is_file():
            raise SystemExit(f"{path}: no translation at {translation}")
        records.append(record)

    records.sort(key=lambda r: r["lang"])
    lines = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text(lines, encoding="utf-8")

    tokens_in = sum(r["usage"]["input_tokens"] or 0 for r in records)
    tokens_out = sum(r["usage"]["output_tokens"] or 0 for r in records)
    api_seconds = sum(r["seconds"] or 0 for r in records)
    print(f"{translator:14} {len(records):3} languages  {len(lines.encode()) / 1024:6.1f} KB"
          f"  {tokens_in:>9,} in  {tokens_out:>6,} out  {api_seconds:6.1f}s in requests"
          f"{'  (dry run)' if dry_run else ''}")
    return len(records), tokens_in, tokens_out, api_seconds


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("translators", nargs="*",
                        help="Translator directories under evals-degrees/ (default: all)")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Report what would be written without writing it")
    parser.add_argument("-o", "--out-dir", type=Path, default=OUT_DIR,
                        help=f"Where to write <translator>.jsonl (default: {OUT_DIR.name}/)")
    parser.add_argument("--force", action="store_true",
                        help="Replace existing output")
    args = parser.parse_args()

    translators = args.translators or sorted(p.name for p in SOURCE_DIR.iterdir() if p.is_dir())
    rubric = scheme_id()
    print(f"rubric: {rubric}\n")

    total_langs = total_in = total_out = 0
    total_seconds = 0.0
    for translator in translators:
        langs, tokens_in, tokens_out, api_seconds = convert(translator, rubric, args.out_dir,
                                                            args.force, args.dry_run)
        total_langs += langs
        total_in += tokens_in
        total_out += tokens_out
        total_seconds += api_seconds
    print(f"\n{len(translators)} translators, {total_langs} languages, "
          f"{total_in:,} input and {total_out:,} output tokens already paid for, "
          f"{total_seconds:.0f}s of request time -- a lower bound on what a run costs.")
    print(f"trtools/jev_criteria.py must produce {rubric}; see PORT.md section 8.")
    print(f"Compare against examples/tr/onde/<translator>/jev.jsonl once `trtools jev` "
          f"has written it.")


if __name__ == "__main__":
    sys.exit(main())
