# Port: Experiment 13's Evaluator into `trtools`

Working document, and a companion to [PLAN.md](PLAN.md). It designed the corpus's own Jev
evaluation path; that path now exists and has been run over the whole corpus, so what is
left here is the reasoning a reader would otherwise have to reconstruct, and the two things
still open.

**Status**: implemented and run. `trtools jev` writes
`examples/tr/onde/{model}/jev.jsonl`; all 16 translators were evaluated on 2026-09-22 and
[examples/tr/onde/JEV.md](../../examples/tr/onde/JEV.md) records the run. `SCORES.txt`,
`TRENDS.jsonl`, the model READMEs and `EVALUATOR` are untouched — that is PLAN.md's step 3.

---

## 1. What Exists

| | |
|---|---|
| `trtools/jev_criteria.py` | the scheme: five criteria, five levels, `JUDGE`/`SCOPE`, `build_state`, `build_questions`, `SCHEME_ID` |
| `trtools/jev.py` | the `jev` subcommand, registered in `trtools/__main__.py` |
| `examples/tr/onde/common.mk` | `jev:`, separate from `evaluate:` |
| `examples/tr/onde/Makefile` | `jev` for all models, `jev-<model>` for one |
| `examples/tr/onde/{model}/jev.jsonl` | 67 records, beside `evals/` rather than replacing it |

`--langs` takes `common.mk`'s `LANGS` rather than discovering languages from `tr/`: the
language list is the corpus's statement of what should exist, so a missing translation is
an error, not a silently shorter run. One run per language; a malformed line in an existing
file, or one scored on another scheme, aborts rather than being skipped; a served model
version other than the pinned one aborts instead of being retried. Each language is
appended and flushed as it finishes, so an interruption loses at most one. Usage is filed
as one `usage.jsonl` entry per model directory, since that file is account-level state.

## 2. The Record

```json
{"lang":"ja","model":"jev-1.13.0","rubric":"degrees@f518286e",
 "scores":{"readability":3.09, "…":0},
 "confidence":{"readability":0.73, "…":0},
 "probabilities":{"readability":[0.0,0.01,0.11,0.68,0.2], "…":[]},
 "usage":{"input_tokens":6878,"output_tokens":83},"seconds":0.31}
```

678 bytes a line, 44 KB a model, about 0.7 MB for all 16 — against the 16 MB the three-run
`evals/` directories hold, and 73.3% smaller than the experiment's per-language JSON for
the same judgments.

Four decisions in it are worth keeping written down.

**`scores` cannot be recomputed from `probabilities`.** The API returns probabilities
rounded to two decimals (some rows sum to 0.99) while the score comes from the
full-precision distribution: over 400 criterion-judgments, `Σ p·i × 5` differs from the
recorded score by a mean absolute 0.044 and a maximum of 0.20. The score is primary and the
distribution corroborates it, not the other way round. `confidence` likewise comes from the
API and is not derivable. Everything that *is* derivable — the totals, the rounded
per-criterion scores, the empty `reasoning` fields `trtools eval` would carry — is dropped,
which only became possible once `trtools` had a reader of its own.

**`scores` holds levels, 0.0–4.0, not the 0–20 points** `POINTS_PER_LEVEL` maps them to.
The level is what Jev answers; the point scale is a presentation choice inherited from the
old rubric, and a later change to it should not invalidate what is on disk.

**`seconds` is processing time**: `time.monotonic()` when the language's processing starts,
subtracted when it ends, so it covers the request and everything around it. `monotonic`
rather than `time.time()` so a clock adjustment mid-run cannot produce a negative figure.
It sits outside `usage` because `usage` is the API's own report and this is measured
locally. The per-line figures do not sum to a run's wall time; the run prints its own total
and JEV.md records it.

**`model` and `rubric` repeat on every line**, which costs a few kilobytes and keeps the
file honest if either changes midway through a resumed run.

## 3. `SCHEME_ID`

```
sha256(judge + scope + the five criterion descriptions + the five level texts
       + the state's key order)[:8]
```

recorded as `"rubric": "degrees@f518286e"`. Hashing only the level texts would not do: what
the model is asked is the instructions — `judge`, the per-criterion description, `scope` —
and what it is asked about is `build_state`'s named keys. Any of them can be reworded
without touching `LEVELS`, and the scores would shift with nothing in the data to show it.
Only strings are hashed, never a serialised SDK object.

`trtools jev --show-scheme` prints the whole thing as Markdown, and JEV.md's appendix is
that output: the corpus carries a readable copy of what it was scored on, and one that goes
stale visibly, since a reworded scheme changes the identifier the `jev.jsonl` files beside
it record.

## 4. What Was Not Ported

The `bands` level set and the `--levels` switch, `EVAL_DIRS`, `--eval-dir`, `--runs`.
Production is one rubric and one run: experiment 12 measured the run-to-run range at 1.12
points, with run 1 alone reproducing the median of three at Pearson 0.998.

`experimental/13/` itself is untouched and stays frozen, so a later edit to the corpus
evaluator cannot change what this experiment claims to mean.

## 5. Still Open

**`trtools agg` cannot read `jev.jsonl`, and would fail silently.**
`find_evaluation_groups` (`aggregate.py:11`) matches only `^(.+)-([123])\.json$` and keeps
only groups with all three runs present (`aggregate.py:27`); a one-run corpus matches
nothing and is discarded with no error and no warning. `trtools trend` shares the function
(`trend.py:9,168,200`). Hence `trtools agg --jev`, reading `jev.jsonl` directly and
asserting that every line in a file agrees on `model` and `rubric`. Now recorded in
PLAN.md section 5.2, which previously said the output's schema was enough.

**`TRENDS.jsonl`'s `analysis` column has no source under Jev.** The `score` column falls
straight out of `jev.jsonl`; the prose does not, because `trend.py:198-250` builds it from
three runs' `reasoning` text and Jev returns none. Models already evaluated keep their
Qwen-written `analysis`; whether their `score` is refreshed to the Jev scale is part of the
same question. Current idea for new models: pass the translation and its Jev scores to
Qwen 3.6 and have it write the one-line summary, so the sentence rests on the text and the
numbers rather than on an evaluator's prose. The alternatives are a fixed sentence derived
from the five criterion scores — free and deterministic, but unable to name a defect kind,
since the levels judge only how much of the document falls short and deliberately not what
is wrong with it — or replacing the prose column with the five scores.

## 6. `port.py`

Renders this experiment's frozen per-language JSON in the corpus's format, into
`jsonl-old/<translator>.jsonl`, which is gitignored: it is a mechanical re-rendering of
`evals-degrees/`, which is committed, and it regenerates in under a second. Its `seconds`
is filled with the experiment's `duration_seconds`, which is request time rather than
processing time — the same field, a different measurement, and the two columns should never
be compared.

It exists for the comparison that re-running all 16 translators made possible, and that
comparison came out clean: identical input token counts model for model, Pearson 0.9995 and
Spearman 0.9980 over 268 translations, and a mean signed difference of -0.006 points. It
also remains the fallback if the paid path is ever unavailable.

## 7. Next, in Order

1. **`TREND-jev.jsonl`.** Deferred to the next session. Section 5's second item is the
   question; a trends file of its own is the shape of the answer, kept apart from
   `TRENDS.jsonl` so that two scales never share a file (PLAN.md section 5.3).

2. **The comparison table, on the Jev scale.** Rebuild what
   [examples/tr/README.md](../../examples/tr/README.md) already shows — the per-language
   table across models, and the `Mean` / `Median` / `Stdev` rows under "Trends by Model"
   that `generate_compare_rows.py compare --sync` computes — from `jev.jsonl` instead of
   `SCORES.txt`, and set the two side by side. This is PLAN.md's step 2, and it is what
   answers the two questions that step exists for:

   - **Does Jev separate the top?** `gpt-5.6-luna` 90.39, `union-alpha` 90.18,
     `gemini-3.7-flash` 87.52, `ox-alpha` 85.90 under the old evaluator — five points of a
     hundred-point scale for the four models anyone is choosing between.
   - **Does the middle band hold?** Spearman against the old table, restricted to the
     translators it scores at 60–70, where the range is narrow and the reference is
     contested.

   Reading the two tables together also makes PLAN.md section 5.4 concrete: the `90 / 80 /
   60` guide is left as it is, so languages re-bucket under the new scale without any
   change in translation quality, and the table has to be read with that in mind.

   Blocked on `trtools agg --jev` (section 5), which is what turns `jev.jsonl` into the
   per-model, per-language numbers such a table is built from.

3. **Then PLAN.md step 3** — `EVALUATOR`, `SUMMARIZER`, and regenerating `SCORES.txt`,
   `TRENDS.jsonl`, the model READMEs and the charts in one pass.
