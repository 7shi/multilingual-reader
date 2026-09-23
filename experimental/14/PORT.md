# Port: The Trend Column into `trtools trend --jev`

A companion to [README.md](README.md). The README is the design this experiment settled;
this is how it went into `trtools`.

**Status**: frozen, 2026-09-23. The port is done and the corpus has switched; nothing is
left for this file. `trtools trend --jev` exists (sections 1–4) and its prompts match
experiment 14's (section 6); every model directory has its `TREND-jev.jsonl`, and its table
is synced into the model's README. `common.mk`'s `all:` runs `trends-jev` in place of
`trends`, and `TRENDS.jsonl` stays as the old-scale record. This file covers the trend column end to end:
the port, `SUMMARIZER`, and regenerating the column and the README tables it renders.
Measuring the corpus on Jev and switching the evaluator over is the other half of the
migration and is [experiment 13's PORT.md](../13/PORT.md); the two meet only at the switch
(section 7).

**What it waited on is settled.** Experiment 13's PORT.md steps 1 and 2 are done and Jev
replaces the evaluator; its section 5.3 left `build_state` as it is, so `SCHEME_ID` stays
`degrees@f518286e` and the `jev.jsonl` files already on disk are stage 1's input as they
stand.

---

## 1. What It Does

Per language of one model directory:

1. Read the language's record from `jev.jsonl` — the five `scores`, levels 0.0–4.0.
2. **Stage 1**: send the original, the translation and [README.md](README.md) section 2's
   stage-1 prompt, with the five scores as points out of 20 and their total. The reply is
   the comment, in English, as plain text.
3. **Stage 2**: send the comment alone, under a header carrying the Jev total, with the
   stage-2 prompt — the shortfall rule and the `LEVELS` text for the weakest criterion's
   level included. The reply, cleaned by `trend.py`'s `_clean`, is `analysis`.
4. Append `{"lang", "score", "analysis"}` to `TREND-jev.jsonl`.

Both calls to the same generative model, without thinking, sharing no history.

## 2. Command Line

A `--jev` mode on `trtools trend` rather than a subcommand of its own: the rendering,
`--sync`, the resume and the language retry are `trend.py`'s already, and only where the
phrase comes from changes.

```
uv run trtools trend --jev jev.jsonl --original ../../../onde-en.txt \
    -m $(SUMMARIZER) -o TREND-jev.jsonl --sync README.md
```

- `--jev FILE` replaces the positional evaluation files. Every line must agree on `model`
  and `rubric`, as `trtools agg --jev` requires ([experiment 13's PORT.md](../13/PORT.md)
  section 5.1); a mixed file aborts. The file is read by `aggregate.py`'s `aggregate_jev`
  itself, with the prefix taken from `--original` (`onde-en.txt` → `onde`), so the check,
  the total and the translation's file name all come from one place.
- `--original` is the source text; the translation is `tr/onde-{lang}.txt`, found the way
  `trtools jev` finds it (`--tr-dir`, default `tr`).
- `-o` defaults to `TREND-jev.jsonl` under `--jev`, never `TRENDS.jsonl`.
- `--no-think` has no effect under `--jev`: both stages run without thinking regardless.
- `--render-only -o TREND-jev.jsonl --sync README.md` works unchanged — `render_table` reads
  `score` and `analysis`, and a one-decimal score prints as it is.

### `common.mk`

```make
SUMMARIZER = ollama:qwen3.6

trends-jev:
	uv run trtools trend --jev jev.jsonl --original $(DIR)/onde-en.txt \
		-m $(SUMMARIZER) -o TREND-jev.jsonl --sync README.md
```

Until the switch it took `TREND_SYNC=` to write the file without syncing, and
`examples/tr/onde/Makefile` had a `trends-jev` that ran every model directory that way; both
went at the switch, once the sync was due.

`SUMMARIZER = $(EVALUATOR)` has to be decoupled first: once `EVALUATOR` is Jev, a
summarizer that follows it would be a model that writes no prose. Today both are
`ollama:qwen3.6`, so writing the summarizer out changes nothing and can land with this port.
`trends-jev` replaces `trends` in `all:` at the switch (section 7).

## 3. The Prompts

The adopted wording is `trend14.py`'s `two_stage_eval_prompts` and
`two_stage_trend_prompts` with `shortfall_rule=True` and a level — run 14's `level`
variant — copied as fixed strings. None of the experiment's switches come across.

- Stage 1 is `evaluate.py`'s prompt with its closing sentence replaced, so the guideline
  lines are shared text. Keep them in one place, since the two drifting apart would make
  stage 1 read the scores against bands the old evaluator no longer used; but copy rather
  than import `evaluate.py`'s prompt-building, which lives inside its `run()`. Both hold:
  the guideline lines are `evaluate.py`'s module-level `GUIDELINES`, which its `run()`
  formats and `trend.py` imports, and the lines around them are `trend.py`'s own.
  `evaluate.py`'s prompt was checked to be unchanged by the move, byte for byte.
- Stage 1 must **not** go through `evaluate.py`'s `run()`: it refuses a translation whose
  line count differs from the original's, and `gemini-3-flash/eu` has 18 lines of 99 and
  still needs a phrase.
- The criterion headings and `LEVELS` come from `trtools/jev_criteria.py`, the same strings
  Jev was asked with.

## 4. The File

`TREND-jev.jsonl`, the same three keys as `TRENDS.jsonl` and nothing more
([README.md](README.md) section 4).

**It is a file of its own because `TRENDS.jsonl` is a time series.** `SCORES.txt`, the
per-model tables and the chart are regenerated wholesale, so the scale change is fine for
them; `TRENDS.jsonl` accumulates, and appending new-scale entries to old-scale ones would
corrupt it silently, with no error and no visible seam. The existing `TRENDS.jsonl` and
`evals/` stay as the old-scale record. Never mix the two in one file.

- **`score`** is `sum(scores) × POINTS_PER_LEVEL`, rounded to one decimal — not
  `trend.py`'s `int(median)`, which on the Jev scale ties most of a model's languages.
- **The comment is not kept** in the file. It is printed to the console as it streams, so a
  suspect phrase can be traced while the run is watched; experiment 14 found that the
  phrase is only as right as the comment behind it (PLAN.md section 15). Keeping comments on
  disk was considered after the port and declined: the column is a short phrase, and
  tracing it is not worth a second file.
- **Resume** is `trend.py`'s: a language already in the file is skipped, and each is
  appended as it finishes, so an interruption loses at most one.

## 5. Not Ported

- `trend14.py`'s wording switches — `--locate`, `--summary`, `--two-stage`,
  `--shortfall-rule`, `--jev-level` and the rest — and its target lists. The port has one
  wording.
- The comparison with the phrase in `TRENDS.jsonl`, which was how the experiment judged a
  wording.
- `USAGE_PATH`: the summarizer is local, and nothing is billed.

## 6. Checking the Port

- **The prompts are the adopted ones.** For a handful of run 14's targets, the port's two
  prompts must equal `trend14.py --two-stage` stage 1 and `--comments --shortfall-rule
  --jev-level` stage 2, character for character.
- **One model directory end to end**, then the table synced into its README, before the
  corpus. In the event the trial below stood in for it, and the corpus was run next.
- **Wall time.** Experiment 14 measured 12.0 seconds a phrase: about 13 minutes for a
  model's 67 languages and 3.5 hours for all 16.

**Done so far.** The prompts equal `trend14.py`'s for all 32 targets of `ALL_TARGETS` and
`FOCUS_TARGETS` together, every level from 0 to 4, stage 2 fed run 13's own comments where
it has one. A trial on `gemini-3-flash`'s `de`, `eu` and `ja`, into a copy of its README,
ran end to end — `eu` at 18 lines included — resumed, rendered with `--render-only`, and
stopped on a `jev.jsonl` mixing two rubrics.

**The corpus run.** `make trends-jev` in `examples/tr/onde/` wrote all 16 directories'
`TREND-jev.jsonl` in 290 minutes: 1,072 phrases at 16.2 seconds each, against experiment
14's 12.0. Every file holds the 67 languages of its `jev.jsonl` once each, with the three
keys only; the phrases run to a median of five words and nine at most.
- The phrases themselves are not re-judged here. Their quality is experiment 14's result,
  and claims in them are checked the way [PLAN.md](PLAN.md) section 17 describes.

## 7. The Switch

**Done**, in the same pass as the evaluator's. The corpus's `TREND-jev.jsonl` was written
ahead of it (section 6); the switch synced each table into its README and moved `all:` over.
`SCORES.txt` was in the end not regenerated but kept as the old scale's record, beside
`SCORES-jev.txt`; the README table shows the same numbers as the latter.

Once the port is checked, per model directory: `make trends-jev`, which writes
`TREND-jev.jsonl` and syncs its table into the model's `README.md`; then `all:` takes
`trends-jev` in place of `trends`. About 3.5 hours for all 16.

**In the same pass as the evaluator's switch**
([experiment 13's PORT.md](../13/PORT.md) section 7 step 3). A model README's table and its
`SCORES.txt` show the same numbers, so moving one to the Jev scale without the other would
contradict itself inside one file. `TREND-jev.jsonl` can be written ahead of that pass —
nothing reads it until `--sync` does — so the 3.5 hours need not sit inside it; the sync is
what has to coincide.

## 8. Touch List

| File | What |
|---|---|
| `trtools/trend.py` | `--jev` (sections 1–4) |
| `trtools/evaluate.py` | The guideline lines moved into `GUIDELINES`, its prompt unchanged (section 3) |
| `examples/tr/onde/common.mk` | `SUMMARIZER` decoupled from `EVALUATOR`; `trends-jev:`; `all:` switched from `trends` to `trends-jev`, and `trends:` removed (section 2) |
| `examples/tr/onde/Makefile` | `trends-jev` for every model directory, without syncing, until the switch (section 2) |
| `examples/tr/plot_comparison.py` | Reads its scores from `TREND-jev.jsonl` |
| Each `examples/tr/onde/*/TREND-jev.jsonl` | New, written by `trtools trend --jev` (section 4) |
| Each `examples/tr/onde/*/README.md` | Its table regenerated by `--sync` from `TREND-jev.jsonl` |
| Each `examples/tr/onde/*/TRENDS.jsonl` | Not appended to; kept as the old-scale record (section 4) |
