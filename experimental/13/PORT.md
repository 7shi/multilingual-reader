# Port: Experiment 13's Evaluator into `trtools`

Working document, and a companion to [PLAN.md](PLAN.md). It designed the corpus's own Jev
evaluation path, and that path now exists and has been run over the whole corpus. What is
left is to measure the corpus on it and switch the evaluator over: sections 5, 7, 8 and 9.
The trend column, the other thing this file carried, is [experiment 14](../14/README.md),
and everything about it — its port into `trtools` and its regeneration — is
[that experiment's PORT.md](../14/PORT.md).

**Status**: implemented and run; work remains. `trtools jev` writes
`examples/tr/onde/{model}/jev.jsonl`; all 16 translators were evaluated on 2026-09-22 and
[examples/tr/onde/JEV.md](../../examples/tr/onde/JEV.md) records the run. `EVALUATOR`,
`SCORES.txt` and the chart are untouched — that is section 7's step 3.

**What remains**, in order (section 7):

1. **`trtools agg --jev`** — `trtools agg` cannot read `jev.jsonl` and discards it
   silently (section 5.1).
2. **Measure the corpus on Jev** — the comparison table on the Jev scale beside the old
   one, read for whether Jev separates the top four and whether the middle band holds
   (section 8's first two questions).
3. **Switch and regenerate** — `EVALUATOR`, then `SCORES.txt` and the chart, in the same pass
   as the trend column's switch in [experiment 14's PORT.md](../14/PORT.md) (section 9 is
   what it touches).

Before step 3: settle `build_state`'s line count (section 5.3). `TIERS` stays as it is
(section 5.2).

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

Known and unsolved. Each has to be settled before section 7's step 3, not during it.

### 5.1 Evaluation is solved; aggregation is not

Aggregation fails silently: `find_evaluation_groups` (`aggregate.py:11`) matches only
`^(.+)-([123])\.json$` and keeps only groups where all three runs are present
(`aggregate.py:27`), so a one-run corpus matches nothing and is discarded with no error and
no warning.

**Fix**: `trtools agg --jev`, reading `jev.jsonl` directly and requiring every line in a
file to agree on `model` and `rubric`. Section 7's step 1.

### 5.2 `TIERS` is calibrated to the old scale — accepted, not fixed

`generate_compare_rows.py`'s `TIERS` cuts at 90 / 80 / 60. Under `jev = 0.69 × old + 24.7`
those land at **86.8 / 79.9 / 66.1**, so only the `practical range` boundary at 80 survives
— it sits almost exactly on the crossover. Left unchanged, the other two re-bucket without
any change in translation quality: `gpt-5.6-luna` goes from 44 languages at 90+ to 24, and
from 17 in 80–89 to 35 (README section 5.4).

**Decision: leave 90/80/60 as they are.** The tiers are rough guides, the boundary that
defines "practical" is the one that holds, and re-cutting them would trade a meaningful
number for an arbitrary one. Recorded here so the shift is not later mistaken for a change
in the models.

### 5.3 `build_state` tells the evaluator both texts have the same line count

`trtools/jev_criteria.py`'s `line_correspondence` reads *"Both texts have N lines, and line
i of the translation is meant to render line i of the original"*, and `N` is counted from
the **original only**. When a translation is short, that is a false statement handed to the
evaluator, asserting a correspondence that does not exist.

`gemini-3-flash/eu` is **18 lines against the original's 99** — 82% of the document gone —
and Jev scores it `information_completeness` 2.34, its lowest criterion, for a total of
**71.05**. The old evaluator gave it 63.

Whether the wording is *why* the score is high is unproven. The test is cheap: re-evaluate
that one language with the count taken from the translation, or with the sentence dropped,
and compare. Until then it is a hypothesis, not a cause.

It is the only translation in the corpus under 90 lines, so nothing here suggests a
systematic bias. It matters because the tail is the point of the corpus (PLAN.md
section 1): a yardstick for how many languages a model handles cannot place an 18-line stub
at 71.

**Fix**: settle the wording before step 3 regenerates anything. Changing it changes
`SCHEME_ID` — correctly, since it is an input to the score — which means re-running all
1,072 evaluations at the cost JEV.md records, $0.32 and five and a half minutes.

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

**Run first, switch second.** The comparison in step 2 is itself the check on the corpus's
middle band — translators the old scheme scores at 60–70, the one part of the range nothing
has been compared against. Switching `common.mk` before looking at that result would make
an unverified run the record.

1. **`trtools agg --jev`** (section 5.1). Step 2 needs the per-model, per-language numbers
   it produces, and so does step 3.

2. **The comparison table, on the Jev scale.** Rebuild what
   [examples/tr/README.md](../../examples/tr/README.md) already shows — the per-language
   table across models, and the `Mean` / `Median` / `Stdev` rows under "Trends by Model"
   that `generate_compare_rows.py compare --sync` computes — from `jev.jsonl` instead of
   `SCORES.txt`, and set the two side by side: **median, `pstdev`, boxplot five-number
   summary, and `TIERS` counts**, which is the comparison README section 5.4 starts on four
   translators and this extends to all 16. Write that rather than stretching `agg13.py`,
   which is built for pairs: its section 1 gap and section 3 head-to-head read
   `TRANSLATORS[0]` and `[1]` only. It is what answers section 8's first two questions:

   - **Does Jev separate the top?** `gpt-5.6-luna` 90.39, `union-alpha` 90.18,
     `gemini-3.7-flash` 87.52, `ox-alpha` 85.90 under the old evaluator — five points of a
     hundred-point scale for the four models anyone is choosing between.
   - **Does the middle band hold?** Spearman against the old table, restricted to the
     translators it scores at 60–70. README section 4.2 warns that the +0.96 at the bottom
     is mostly range; the middle band has a narrow range *and* a contested reference, so it
     is where the two explanations come apart.

   Reading the two tables together also makes section 5.2 concrete: languages re-bucket
   under the new scale without any change in translation quality. The report is compared
   against the published corpus numbers, so it uses `SCORES.txt`'s definition of a total
   rather than `agg13.py`'s (PLAN.md section 7).

3. **Switch and regenerate** — `EVALUATOR` in `common.mk`, then `SCORES.txt` and the
   chart, in one pass. Section 9 is what it touches.

   **In the same pass as the trend column's switch**
   ([experiment 14's PORT.md](../14/PORT.md) section 7). A model README's table and its
   `SCORES.txt` show the same numbers, so moving one to the Jev scale without the other
   would contradict itself inside one file.

## 8. Open Questions

Ordered by how much they would change the plan.

1. **Does `jev` separate the top of the corpus?** README section 5.4 says it does not on the
   one pair measured. The top four sit within five points under the old scheme, and that
   compression is the yardstick's standing weakness. Step 2 answers it. If the answer is no,
   the migration is still worth it for PLAN.md section 2's reason 1, but the top of the
   table stays unresolved and needs a different idea.
2. **Does the middle band hold?** Step 2. If Spearman collapses at 60–70, an evaluator that
   works at the extremes and not the middle is a check, not a replacement.
3. **Scope.** This covers `examples/tr/onde/` only. `examples/tr/core/Makefile` and
   `examples/tr/fr/Makefile` also pin `ollama:qwen3.6`, and nothing here measured anything
   about them. Proposed: leave them, revisit once `onde/` has settled.
4. **Is the 0.69 slope stable enough to invert?** README section 7 item 4. Lower priority
   than it was: ranking survives monotone compression, so this only matters for quoting an
   absolute number against a historical one. Step 2 answers it at n=1,072 for free.
5. **Is the ordering inside the old scheme's floor real?** README section 7 item 1. The 10
   translations the old scheme scores 0 come back spread over 2.6–31.2. It is the one place
   this scheme claims information its reference does not have. Checking it needs human
   judgment on ten translations. Not a blocker, but it should not be quoted as established.
6. **A second source text.** README section 7 item 9. Everything the corpus knows is 67
   translations of one spoken-dialogue document. For a *multilingual ability* yardstick this
   is the largest unexamined assumption in the project — larger than anything about the
   evaluator — and it is orthogonal to this migration.

## 9. Touch List

Everything that names the evaluator or depends on its scale, for step 3. Not exhaustive for
prose mentions. The trend column's files are
[experiment 14's PORT.md](../14/PORT.md) section 8.

| File | What |
|---|---|
| `trtools/aggregate.py` | `agg --jev` (5.1) |
| `examples/tr/onde/common.mk` | `EVALUATOR`, `evaluate:`, `scores:` |
| `examples/tr/ADD_MODEL.md` | States the evaluator is fixed to `ollama:qwen3.6` "to keep the scoring criteria consistent" |
| `examples/tr/onde/README.md` | Corpus-level description |
| Each `examples/tr/onde/*/SCORES.txt` | Regenerated by `trtools agg` |
| `examples/tr/generate_compare_rows.py` | `TIERS` shifts meaning; see 5.2 — no code change, but the README wording around the tiers may need one |
| `examples/tr/MODELS.svg`, `compare/MODELS.png` | Regenerated by `generate_compare_rows.py graph`; note the SVG carries a timestamp, so it shows a diff even when the chart is identical |
| `examples/tr/onde/gpt-oss/Makefile` | Has its own `OR_EVALUATOR`; decide whether it follows |
| `examples/tr/onde/qwen3.6/Makefile` | Has `ALT_EVALUATOR = ollama:gpt-oss:120b`; probably unaffected |
