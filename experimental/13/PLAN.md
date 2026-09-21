# Plan: Replacing the Corpus Evaluator with the Five-Criterion Jev Scheme

Working document. [README.md](README.md) is the experiment record and states only what was
measured; this file holds the decision that record is being used for, and it changes as the
decision does.

**Status**: decision taken, step 1 ready to run and not yet run. Twelve translators remain
to evaluate. Next session picks up at section 2.

---

## 1. What the Corpus Is For

This has to be stated first, because it reorders everything else.

The corpus is not trying to evaluate translation quality in general. It is trying to give
**a yardstick for multilingual translation ability**: how many languages a model handles
acceptably, and which ones it does not. That is why
`examples/tr/generate_compare_rows.py` already ranks by `(median, pstdev)`, draws a boxplot
per model, and classifies languages into `TIERS` with a `practical range (80-89)` band.

Several things follow that do not follow from "measure quality accurately":

- **Ranking matters; absolute scores do not.** Compression that preserves order is
  harmless. README section 4.3's slope of 0.69 is therefore much less of a problem than it
  first looked.
- **The tail matters as much as the average.** "How many languages" is a coverage question,
  and coverage lives in counts, dispersion and the bottom of the distribution — not in the
  mean.
- **The instrument has to survive new models.** It is pointed at models that did not exist
  when it was built, which puts a premium on stability and on not saturating.

---

## 2. The Decision

Replace `ollama:qwen3.6` with [eval5_jev.py](eval5_jev.py)'s five-criterion Jev scheme as
the evaluator for `examples/tr/onde/`, and re-evaluate all 16 translators so the corpus is
on one scale.

### Why, in order of weight

1. **The statistics a coverage yardstick needs are the ones the current evaluator
   destroys.** This is README section 5.3 and it is the argument. The corpus mean was the
   only summary robust to an evaluator that swings 52.4 points across three runs on one
   translation. Counting languages above 80 moves by a mean of 4.4 languages (up to 11)
   between single runs; the three runs behind each translator's *worst* language spread by
   a mean of 15.1 points. Averaging 67 languages suppresses that noise, counting and
   minimum-taking amplify it. The five-criterion Jev scheme's run-to-run range is **1.12**
   ([experiment 12 section 3.1](../12/README.md)), which is what makes those statistics
   usable at all.
2. **One run replaces three.** 16 translators × 67 languages = **1,072 evaluations**
   against the current 3,216, at roughly **$0.21** and five minutes. Cost and wall time
   stop being design constraints.
3. **It tracks the corpus at both ends.** Spearman +0.69 against the old scheme on its two
   best translators (README section 3.2) and +0.96 on `qwen3.8` / `bonsai2-27b` (section
   4.2), with the caveat section 4.2 states about range.
4. **It has resolution where the old scheme has none.** The old scheme pins 10 of
   `bonsai2-27b`'s 67 translations to a flat 0; the same 10 come back spread over 2.6–31.2
   (section 4.4). It separates the ternary-quantized model from its parent in 66 of 67
   languages against the old scheme's 62. For a coverage yardstick this is the floor
   working rather than collapsing.
5. **It ends the evaluator evaluating itself.** `qwen3.6` is one of the 16 translators.

### What it does not buy

**Top-end discrimination, as far as anything shows.** README section 5.4: the median of the
top pair moves from 93/92 to 88.0/87.2. New models arrive at the top, so this is the
yardstick's weakest point and it is not yet improved. Section 4 below keeps it as the first
open question.

### What is being given up

`qwen3.6` runs locally through Ollama: free, offline, and regenerable indefinitely. Jev is
a paid API pinned to a version (`jev-1.13.0`). If that version is retired the corpus cannot
be regenerated on its scale — it can only be re-pinned and re-run whole. At 1,072
evaluations for $0.21 that is an acceptable answer, but it is a change in kind:
reproducibility stops being a property of the tooling and becomes a property of the re-run
being cheap. Accepted deliberately, not overlooked.

---

## 3. Sequence

**Run first, switch second.** The full re-evaluation is itself the check on the corpus's
middle band — translators the old scheme scores at 60–70, the one part of the range nothing
has been compared against. Switching `common.mk` before looking at that result would make
an unverified run the record.

### Step 1 — evaluate the remaining twelve (ready to run)

Four translators are already done and their files are skipped, so the whole corpus can be
named. From the repository root, with `TYPESAFE_API_KEY` set:

```bash
uv run experimental/13/eval5_jev.py \
  gemma4 gemma4-31b gpt-oss qwen3.6-27b qwen3.6 qwen3.8 \
  bonsai2-27b \
  muse-glimmer ox-alpha union-alpha \
  gpt-5.6-luna gpt-5.6-terra \
  gemini-3.5-flash-lite gemini-2.5-flash gemini-3-flash gemini-3.7-flash
```

Same order as `onde/Makefile`'s `MODELS`. **804 new evaluations, about $0.16, three to four
minutes**, pinned to `jev-1.13.0`, one run each, resumable. Results land in
`experimental/13/evals-degrees/<translator>/<lang>.json`, beside the four already there and
nowhere near `examples/tr/onde/*/evals/`, so the current corpus stays untouched and
reproducible while this is being decided.

**Do not run `eval50_jev.py` over the corpus.** Ranking is what the yardstick needs, the
five-criterion scheme is what README section 3.7 recommends for it, and the fifty-item
scheme costs twice the input tokens to return the same ordering. It stays available for
diagnosing one translator at a time.

### Step 2 — report the corpus on the yardstick's own terms

`agg13.py` is built for pairs: section 1's gap and section 3's head-to-head read
`TRANSLATORS[0]` and `[1]` only, so passing 16 names gives a half-meaningful report. Its
section 2 correlations and section 5 criterion means are fine at any count.

What is actually wanted is the existing instrument's output on the new scale — **median,
`pstdev`, boxplot five-number summary, and `TIERS` counts** — beside the current old-scale
values, which is the comparison README section 5.4 starts on four translators and this run
extends to all 16. Write that rather than stretching `agg13.py`.

Two things to read off it before anything is switched:

- **The middle band.** Spearman against the old reference, restricted to translators the
  old scheme puts at 60–70. Section 4.2 warns that the +0.96 at the bottom is mostly range;
  the middle band has a narrow range *and* a contested reference, so it is where the two
  explanations come apart.
- **The top four.** Whether `jev` spreads `gpt-5.6-luna`, `union-alpha`, `gemini-3.7-flash`
  and `ox-alpha` — 90.39, 90.18, 87.52, 85.90 under the old scheme, five points of a
  hundred-point scale for the four models anyone is choosing between.

### Step 3 — switch and regenerate

Only then: `common.mk`, then `SCORES.txt`, `TRENDS.jsonl`, each model `README.md` and the
chart, in one pass.

---

## 4. Open Questions

Ordered by how much they would change the plan.

1. **Does `jev` separate the top of the corpus?** README section 5.4 says it does not on
   the one pair measured. The top four sit within five points under the old scheme, and
   that compression is the yardstick's standing weakness — a known concern from evaluator
   selection generally, not just here. Step 1 supplies `gemini-3.7-flash` and `ox-alpha`,
   so step 2 answers it. If the answer is no, the migration is still worth it for section
   2's reason 1, but the top of the table stays unresolved and needs a different idea.
2. **Does the middle band hold?** Step 2. If Spearman collapses at 60–70, an evaluator that
   works at the extremes and not the middle is a check, not a replacement.
3. **Scope.** This plan covers `examples/tr/onde/` only. `examples/tr/core/Makefile` and
   `examples/tr/fr/Makefile` also pin `ollama:qwen3.6`, and nothing here measured anything
   about them. Proposed: leave them, revisit once `onde/` has settled.
4. **Is the 0.69 slope stable enough to invert?** README section 7 item 4. Lower priority
   than it was: ranking survives monotone compression, so this only matters for quoting an
   absolute number against a historical one. The full re-run answers it at n=1,072 for
   free.
5. **Is the ordering inside the old scheme's floor real?** README section 7 item 1. The 10
   translations the old scheme scores 0 come back spread over 2.6–31.2. It is the one place
   this scheme claims information its reference does not have. Checking it needs human
   judgment on ten translations. Not a blocker, but it should not be quoted as established.
6. **A second source text.** README section 7 item 9. Everything the corpus knows is 67
   translations of one spoken-dialogue document. For a *multilingual ability* yardstick this
   is the largest unexamined assumption in the project — larger than anything about the
   evaluator — and it is orthogonal to this migration.

**Removed from this list: fluency.** It was carried here as the one open question with a
deadline, on the grounds that every corpus number would inherit the bias once the scale was
frozen. README sections 5.1 and 5.2 close it from data already on disk: the fifty-item
scheme's own fluency group and the old generative evaluator over all 16 translators both
put fluency lowest, and it is the criterion that best separates the top four. There is
nothing to fix before the freeze.

---

## 5. Blockers

Known and unsolved. Each has to be settled before step 3, not during it.

### 5.1 `SUMMARIZER` cannot be Jev

`examples/tr/onde/common.mk` line 10 reads `SUMMARIZER = $(EVALUATOR)`, so changing the
evaluator silently changes what generates the trend prose too. `trtools/trend.py` passes
merged results to an LLM to write a sentence per language; Jev is a System One model that
returns typed judgments and cannot do it.

**Fix**: decouple the two lines and leave the summarizer on a generative model. Whether it
stays `ollama:qwen3.6` is a separate question.

### 5.2 `trtools batch --eval-only` has no Jev backend

`common.mk`'s `evaluate:` target runs `trtools batch --eval-only --evaluator $(EVALUATOR)`,
which goes through `trtools`'s generative evaluation path. `eval5_jev.py` is a standalone
script. Its output is in `trtools eval`'s schema, so `trtools agg` and `trtools trend` read
it as it stands (README section 2) — but the filenames differ: the experiment writes
`<dir>/<translator>/<lang>.json` and the corpus expects `evals/onde-<lang>-<run>.json`.

| | Change | Cost |
|---|---|---|
| **A** (preferred) | Point `common.mk`'s `evaluate:` at a corpus-facing Jev script, with the corpus's own naming | Small; leaves experiments 11–13's frozen copies alone |
| B | Add a Jev backend inside `trtools` | Larger; puts a paid API dependency in the shared tool, and the frozen experiment copies still cannot use it |

A also keeps the property that made the experiment copies frozen: a later edit to the
corpus evaluator must not change what experiment 13 claims to mean.

### 5.3 `TRENDS.jsonl` is a time series

`SCORES.txt`, the per-model tables and the chart are regenerated wholesale, so the scale
change is fine for them. **`TRENDS.jsonl` accumulates**, and appending new-scale entries to
old-scale ones corrupts it silently, with no error and no visible seam.

**Fix**: regenerate in one pass, record the changeover point, and keep the existing
`evals/` rather than deleting it so the old-scale record survives as its own thing. Never
mix the two in one file.

### 5.4 `TIERS` is calibrated to the old scale — accepted, not fixed

`generate_compare_rows.py`'s `TIERS` cuts at 90 / 80 / 60. Under `jev = 0.69 × old + 24.7`
those land at **86.8 / 79.9 / 66.1**, so only the `practical range` boundary at 80 survives
— it sits almost exactly on the crossover. Left unchanged, the other two re-bucket without
any change in translation quality: `gpt-5.6-luna` goes from 44 languages at 90+ to 24, and
from 17 in 80–89 to 35 (README section 5.4).

**Decision: leave 90/80/60 as they are.** The tiers are rough guides, the boundary that
defines "practical" is the one that holds, and re-cutting them would trade a meaningful
number for an arbitrary one. Recorded here so the shift is not later mistaken for a change
in the models.

---

## 6. Touch List

Everything that names the evaluator or depends on its scale, for when step 3 happens. Not
exhaustive for prose mentions.

| File | What |
|---|---|
| `examples/tr/onde/common.mk` | `EVALUATOR`, and `SUMMARIZER` decoupled from it (5.1) |
| `examples/tr/onde/common.mk` | `evaluate:` target (5.2) |
| `examples/tr/ADD_MODEL.md` | States the evaluator is fixed to `ollama:qwen3.6` "to keep the scoring criteria consistent" |
| `examples/tr/onde/README.md` | Corpus-level description |
| Each `examples/tr/onde/*/README.md` | Regenerated by `trtools trend --sync` |
| Each `examples/tr/onde/*/SCORES.txt` | Regenerated by `trtools agg` |
| Each `examples/tr/onde/*/TRENDS.jsonl` | See 5.3 — regenerate, do not append |
| `examples/tr/generate_compare_rows.py` | `TIERS` shifts meaning; see 5.4 — no code change, but the README wording around the tiers may need one |
| `examples/tr/MODELS.svg`, `compare/MODELS.png` | Regenerated by `generate_compare_rows.py graph`; note the SVG carries a timestamp, so it shows a diff even when the chart is identical |
| `examples/tr/onde/gpt-oss/Makefile` | Has its own `OR_EVALUATOR`; decide whether it follows |
| `examples/tr/onde/qwen3.6/Makefile` | Has `ALT_EVALUATOR = ollama:gpt-oss:120b`; probably unaffected |

---

## 7. Note on the Reference

`SCORES.txt` and everything drawn from it total the **five criteria's medians**
(`trtools/aggregate.py:67`). `agg13.py` uses the **median of the three total scores**, as
experiments 11 and 12 did. They agree on 60% of the corpus's 1,072 translations, differ by
a mean absolute 0.60 points, and refitting the compression against `SCORES.txt` gives
`0.688 × old + 24.8` against `0.690 × old + 24.7` (README section 5.5).

Nothing turns on it, but step 2's report is compared against the published corpus numbers,
so it should use `SCORES.txt`'s definition rather than `agg13.py`'s.
