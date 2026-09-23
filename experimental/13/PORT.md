# Port: Experiment 13's Evaluator into `trtools`

Working document, and a companion to [PLAN.md](PLAN.md). It designed the corpus's own Jev
evaluation path, and that path now exists, has been run over the whole corpus, and has
been measured against the old evaluator ([REPORT.md](REPORT.md)), and the corpus has
switched to it. The port is done; what is left is section 8's open questions, which go
beyond it.
The trend column, the other thing this file carried, is [experiment 14](../14/README.md),
and everything about it — its port into `trtools` and its regeneration — is
[that experiment's PORT.md](../14/PORT.md).

**Status**: switched. `trtools jev` writes `examples/tr/onde/{model}/jev.jsonl`; all 16
translators were evaluated on 2026-09-22 and
[examples/tr/onde/JEV.md](../../examples/tr/onde/JEV.md) records the run. `common.mk`'s
`evaluate:` now runs `trtools jev`, `scores-jev:` totals it into `SCORES-jev.txt`, and the
comparison tables and charts are regenerated from it, in the same pass as
[experiment 14's](../14/PORT.md) trend column. `SCORES.txt` is not replaced: it stays beside
`SCORES-jev.txt`, with `evals/` and `TRENDS.jsonl`, as the old evaluator's record. The
tools that read scores take `--jev` explicitly and read the old record without it;
`examples/tr/Makefile` passes it.

**Done**, in order (section 7):

1. **`trtools agg --jev`** (section 5.1).
2. **Measure the corpus on Jev**: [REPORT.md](REPORT.md). Jev splits the top four into two
   pairs but not within them, and what reorders the middle of the ranking is lost speaker
   labels, which Jev penalises and the old evaluator does not see.
3. **Switch and regenerate**, in the same pass as the trend column's switch in
   [experiment 14's PORT.md](../14/PORT.md) (section 9).

`TIERS` stayed as it is (section 5.2), `build_state`'s wording stayed as it is (section
5.3), and speaker labels needed no decision (REPORT.md section 4).

**What remains** is section 8: `core/` and `fr/` still on the old evaluator, the top pair
Jev leaves tied, whether the ordering inside the old scheme's floor is real, and a second
source text.

---

## 1. What Exists

| | |
|---|---|
| `trtools/jev_criteria.py` | the scheme: five criteria, five levels, `JUDGE`/`SCOPE`, `build_state`, `build_questions`, `SCHEME_ID` |
| `trtools/jev.py` | the `jev` subcommand, registered in `trtools/__main__.py` |
| `examples/tr/onde/common.mk` | `evaluate:` runs `trtools jev`; `scores-jev:` runs `agg --jev` into `SCORES-jev.txt` |
| `examples/tr/onde/{model}/jev.jsonl` | 67 records; `evals/` beside it is the old evaluator's record |
| `trtools/aggregate.py` | `agg --jev --prefix onde`: totals from one `jev.jsonl`, one decimal |
| `examples/tr/onde/{model}/SCORES-jev.txt` | the Jev totals, beside the old evaluator's `SCORES.txt` |
| `experimental/13/report.py`, `REPORT.md` | step 2: the corpus on both scales |

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

## 5. Settled Before the Switch

What was known to be unsolved before section 7's step 3, and how each was settled before it:
5.1 fixed, 5.2 and 5.3 accepted as they are.

### 5.1 Evaluation is solved; aggregation is not

Aggregation fails silently: `find_evaluation_groups` (`aggregate.py:11`) matches only
`^(.+)-([123])\.json$` and keeps only groups where all three runs are present
(`aggregate.py:27`), so a one-run corpus matches nothing and is discarded with no error and
no warning.

**Fix**: `trtools agg --jev`, reading `jev.jsonl` directly and requiring every line in a
file to agree on `model` and `rubric`. Section 7's step 1.

**Done.** `trtools agg --jev --prefix onde jev.jsonl` takes exactly one file, and stops on
mixed `model` or `rubric`, a language twice, a missing criterion or an empty file. The
prefix is an argument because `jev.jsonl` records only the language. The total is
`sum(levels) × POINTS_PER_LEVEL`, printed to **one decimal** as `onde-xx: 85.7` — an integer
ties most of a model's languages on this scale, the reason experiment 14 keeps one decimal
(its README section 4). `make scores-jev` writes it to `SCORES-jev.txt`, beside the old
scale's `SCORES.txt`, which step 3 left in place.

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

The mapped cuts above rest on the four-translator slope, which the full corpus does not
reproduce: over 1,072 it is 0.508 fitted one way and 0.718 the other
([REPORT.md](REPORT.md) section 7), so 86.8 / 79.9 / 66.1 should not be quoted as a
conversion. The decision does not depend on them. At the unchanged cuts the top four go
from 37–48 languages at 90+ to 13–22.

### 5.3 `build_state` tells the evaluator both texts have the same line count — accepted, not fixed

`trtools/jev_criteria.py`'s `line_correspondence` reads *"Both texts have N lines, and line
i of the translation is meant to render line i of the original"*, and `N` is counted from
the **original only**. When a translation is short, that is a false statement handed to the
evaluator, asserting a correspondence that does not exist.

`gemini-3-flash/eu` is **18 lines against the original's 99** — 82% of the document gone —
and Jev scores it `information_completeness` 2.34, its lowest criterion, for a total of
**71.05**. The old evaluator gave it 63.

Whether the wording is *why* the score is high is unproven, and it stays a hypothesis, not
a cause.

It is the only translation in the corpus under 90 lines, so nothing here suggests a
systematic bias. It matters because the tail is the point of the corpus (PLAN.md
section 1): a yardstick for how many languages a model handles cannot place an 18-line stub
at 71.

**Decision: leave the wording as it is.** Changing it changes `SCHEME_ID` — correctly,
since it is an input to the score — and `trtools jev` refuses to add to a file scored on
another scheme, while totals on two schemes cannot sit in one comparison table. Any
rewording means re-evaluating the whole corpus, which is out of proportion to one
translation. A translation whose line count differs from the original's
is found mechanically, without an evaluator, by counting lines: [report.py](report.py)
already sets it aside as `unaligned`. `gemini-3-flash/eu`'s 71.05 is recorded here as that
known exception, not read as a judgment of an 18-line stub.

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

1. ~~**`trtools agg --jev`**~~ (section 5.1). Done.

2. **The comparison table, on the Jev scale.** Rebuild what
   [examples/tr/README.md](../../examples/tr/README.md) already shows — the per-language
   table across models, and the `Mean` / `Median` / `Stdev` rows under "Trends by Model"
   that `generate_compare_rows.py compare --sync` computes — from `jev.jsonl` instead of
   `SCORES.txt`, and set the two side by side: **median, `pstdev`, boxplot five-number
   summary, and `TIERS` counts**, which is the comparison README section 5.4 starts on four
   translators and this extends to all 16. Write that rather than stretching `agg13.py`,
   which is built for pairs: its section 1 gap and section 3 head-to-head read
   `TRANSLATORS[0]` and `[1]` only. It is what answers two questions:

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

   **Done**: `report.py` writes it and [REPORT.md](REPORT.md) reads it. The answers, with a
   third question the full corpus settled for free:

   - **Does Jev separate the top? Partly** (REPORT.md section 2). It separates
     `gpt-5.6-luna` and `union-alpha` from `gemini-3.7-flash` more strongly than the old
     scheme, but the two stay tied, and `gemini-3.7-flash` and `ox-alpha` swap places. The
     tie is section 8 item 2.
   - **Does the middle band hold? It is not specially weak** (REPORT.md section 3). Per
     translation, Spearman inside every ten-point band of the old score is low (+0.07 to
     +0.39), the top band included; the corpus-wide +0.81 is mostly range. Per translator,
     the middle of the ranking does reorder, and the cause is lost speaker labels
     (REPORT.md section 4), not the band.
   - **Is the 0.69 slope stable enough to invert? No** (REPORT.md section 7; README
     section 7 item 4). 0.508 fitted one way, 0.718 the other; 0.69 falls between them.
     It only mattered for quoting an absolute number against a historical one.

3. **Switch and regenerate** — `EVALUATOR` in `common.mk`, then `SCORES.txt` and the
   chart, in one pass. Section 9 is what it touches.

   **In the same pass as the trend column's switch**
   ([experiment 14's PORT.md](../14/PORT.md) section 7). A model README's table and its
   `SCORES.txt` show the same numbers, so moving one to the Jev scale without the other
   would contradict itself inside one file.

## 8. Open Questions

Ordered by how much they would change the plan. Step 2's questions are answered under
section 7.

1. **Scope.** This covers `examples/tr/onde/` only. `examples/tr/core/Makefile` and
   `examples/tr/fr/Makefile` also pin `ollama:qwen3.6`, and nothing here measured anything
   about them. They were left as they are, and `onde/` has now switched, so this is the one
   to take up next. It already shows: `examples/tr/README.md`'s core table stays on the old
   scale, its onde column included, beside a comparison table on Jev's (section 9).
2. **The top pair.** Jev ties `gpt-5.6-luna` and `union-alpha` as the old scheme does
   ([REPORT.md](REPORT.md) section 2), so the compression at the top — the yardstick's
   standing weakness — survives the migration. The migration is still worth it for PLAN.md
   section 2's reason 1, but separating the top needs a different idea.
3. **Is the ordering inside the old scheme's floor real?** README section 7 item 1. The 10
   translations the old scheme scores 0 come back spread over 2.6–31.2. It is the one place
   this scheme claims information its reference does not have. Checking it needs human
   judgment on ten translations. Not a blocker, but it should not be quoted as established.
4. **A second source text.** README section 7 item 9. Everything the corpus knows is 67
   translations of one spoken-dialogue document. For a *multilingual ability* yardstick this
   is the largest unexamined assumption in the project — larger than anything about the
   evaluator — and it is orthogonal to this migration.

## 9. Touch List

Everything that names the evaluator or depends on its scale, and what step 3 did with it.
Not exhaustive for prose mentions. The trend column's files are
[experiment 14's PORT.md](../14/PORT.md) section 8.

| File | What |
|---|---|
| `trtools/aggregate.py` | `agg --jev` (5.1) |
| `examples/tr/onde/common.mk` | `evaluate:` runs `trtools jev`; `all:` takes `scores-jev` in place of `scores`, which stays for regenerating the old record; `jev:`, `trends:` and `EVALUATOR` are gone |
| `examples/tr/onde/Makefile` | The all-model `jev` target is gone; each directory's `make` covers it |
| Each `examples/tr/onde/*/SCORES.txt`, `SCORES-jev.txt` | Both kept: the old scale's and Jev's, side by side, rather than one replacing the other |
| `examples/tr/generate_compare_rows.py` | `--jev` reads `SCORES-jev.txt` and prints one decimal; without it, `SCORES.txt` as before. `TIERS` is unchanged (5.2) |
| `examples/tr/plot_comparison.py` | `--jev` reads `TREND-jev.jsonl`; without it, `TRENDS.jsonl` as before |
| `examples/tr/Makefile` | `sync` and `compare` pass `--jev` |
| `examples/tr/README.md` | Evaluator named as Jev; the tiers' shift noted; the Notes column and the Google and failure-pattern sections rewritten on Jev's numbers, without restating what the tables show; speaker-tag policy updated with REPORT.md section 4 |
| `examples/tr/MODELS.svg`, `compare/*.png` | Regenerated by `make compare` |
| `examples/tr/ADD_MODEL.md`, `ADD_LANG.md` | Evaluator, targets and what to read, now that there are no evaluation logs |
| `examples/tr/onde/README.md`, `JEV.md`, each model's `README.md`, `TEMPLATE/` | Evaluator and output files |
| `examples/tr/onde/gpt-oss/Makefile` | Its past OpenRouter experiment pins `EVALUATOR = ollama:qwen3.6` itself, since `common.mk` no longer defines it |
| `examples/tr/onde/qwen3.6/Makefile` | `ALT_EVALUATOR` is its own; unaffected |

`examples/tr/README.md`'s core table was found overwritten by the comparison table: the
sync matched the first header starting `| Language | `, which was the core table's. The sync
now matches the comparison header by its first link, the core table has a sync of its own,
and it is restored. `core/` is still on the old evaluator (section 8 item 1), so the table
takes its onde column from `gemma4`'s `SCORES.txt`, on the same scale, with or without
`--jev`.
