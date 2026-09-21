# Plan: Replacing the Corpus Evaluator with the Five-Criterion Jev Scheme

Working document. [README.md](README.md) is the experiment record and states only what was
measured; this file holds the decision that record is being used for, and it changes as the
decision does. Nothing here is committed to in code yet.

**Status**: provisional decision taken, not started. Last updated with the section 4 run
(`qwen3.8` / `bonsai2-27b`) in hand.

---

## 1. The Decision

Replace `ollama:qwen3.6` with [eval5_jev.py](eval5_jev.py)'s five-criterion Jev scheme as
the evaluator for `examples/tr/onde/`, and re-evaluate all 16 translators so the corpus is
on one scale.

### Why, in order of weight

1. **The current evaluator is unusable on a single translation.** Experiment 11 measured
   the same evaluator on the same translation swinging by a mean of **52.4 points** across
   three runs. The corpus stores 3-run medians because of it. The five-criterion Jev
   scheme's run-to-run range is **1.12** ([experiment 12 section 3.1](../12/README.md)).
   This is the argument; the rest is secondary.
2. **One run replaces three.** 16 translators × 67 languages = **1,072 evaluations**
   against the current 3,216, at roughly **$0.21** and **five minutes**. Cost and wall time
   stop being design constraints at all.
3. **It tracks the corpus at both ends.** Spearman +0.69 against the old scheme on its two
   best translators (README section 3.2) and +0.96 on `qwen3.8` / `bonsai2-27b`
   (section 4.2), with the caveat section 4.2 states about range.
4. **It has resolution where the old scheme has none.** The old scheme pins 10 of
   `bonsai2-27b`'s 67 translations to a flat 0; the same 10 come back spread over 2.6–31.2
   (section 4.4). It also separates the ternary-quantized model from its parent in 66 of 67
   languages against the old scheme's 62.
5. **It ends the evaluator evaluating itself.** `qwen3.6` is one of the 16 translators in
   the corpus.

### What is being given up

`qwen3.6` runs locally through Ollama: free, offline, and regenerable indefinitely. Jev is
a paid API pinned to a version (`jev-1.13.0`). If that version is retired the corpus cannot
be regenerated on its scale — it can only be re-pinned and re-run whole. At 1,072
evaluations for $0.21 that is an acceptable answer, but it is a change in kind:
reproducibility stops being a property of the tooling and becomes a property of the
re-run being cheap. Accepted deliberately, not overlooked.

---

## 2. Sequence

**Run first, switch second.** The corpus's middle band — translators the old scheme scores
at 60–70 — is the one part of the range nothing has been checked against (README section 6
item 2), and the full re-evaluation *is* that check: 1,072 translations spanning the whole
scale, each with an old 3-run median to compare against. Switching `common.mk` before
looking at that result would make an unverified run the record.

1. **Evaluate all 16 translators into a directory beside the existing `evals/`.** The
   current corpus stays untouched and every number in it stays reproducible while this is
   decided.
2. **Check the middle band before anything else.** Two things to look for:
   - Spearman against the old 3-run medians, restricted to translators the old scheme puts
     at 60–70. The question is whether it holds up where the old scheme's own rankings are
     most contested; section 4.2 warns that the +0.96 at the bottom is mostly range.
   - Mean difference in that band. Section 4.3's fit `jev = 0.69 × old + 24.7` crosses zero
     at old = 79.6, so it predicts `jev` reading slightly *above* the old scheme there.
     A second, independent check on the same fit.
3. **Then switch `common.mk` and regenerate** `SCORES.txt`, `TRENDS.jsonl` and each
   `README.md` in one pass.

---

## 3. Blockers

These are known and unsolved. Each has to be settled before step 3, not during it.

### 3.1 `SUMMARIZER` cannot be Jev

`examples/tr/onde/common.mk` line 10 reads `SUMMARIZER = $(EVALUATOR)`, so changing the
evaluator silently changes what generates the trend prose too. `trtools/trend.py` passes
merged results to an LLM to write a sentence per language; Jev is a System One model that
returns typed judgments and cannot do it.

**Fix**: decouple the two lines and leave the summarizer on a generative model. Whether it
stays `ollama:qwen3.6` or moves is a separate question, and not this one.

### 3.2 `trtools batch --eval-only` has no Jev backend

`common.mk`'s `evaluate:` target runs `trtools batch --eval-only --evaluator $(EVALUATOR)`,
which goes through `trtools`'s generative evaluation path. `eval5_jev.py` is a standalone
script. Its output is in `trtools eval`'s schema, so `trtools agg` and `trtools trend` read
it as it stands (README section 2) — but the filenames differ: the experiment writes
`<dir>/<translator>/<lang>.json` and the corpus expects `evals/onde-<lang>-<run>.json`.

Two options:

| | Change | Cost |
|---|---|---|
| **A** (preferred) | Point `common.mk`'s `evaluate:` at a corpus-facing Jev script, with the corpus's own naming | Small; leaves experiments 11–13's frozen copies alone |
| B | Add a Jev backend inside `trtools` | Larger; puts a paid API dependency in the shared tool, and the frozen experiment copies still cannot use it |

A also keeps the property that made the experiment copies frozen in the first place: a
later edit to the corpus evaluator must not change what experiment 13 claims to mean.

### 3.3 The scale changes, and `TRENDS.jsonl` is a time series

`jev = 0.69 × old + 24.7`. Every accumulated number moves, and not by a constant: the new
scheme reads below the old one above 79.6 and above it below (section 4.3).

`SCORES.txt` and the per-model `README.md` tables are regenerated wholesale, so they are
fine. **`TRENDS.jsonl` is not** — it accumulates, and appending new-scale entries to
old-scale ones corrupts it silently, with no error and no visible seam.

**Fix**: regenerate all of it in one pass, record the changeover point, and keep the
existing `evals/` rather than deleting it, so the old-scale record survives as its own
thing. Never mix the two in one file.

---

## 4. Open Questions

Ordered by how much they would change the plan.

1. **Does the middle band hold?** Step 2. If Spearman collapses at 60–70 the whole thing
   stops — that is where translator rankings are actually decided, and an evaluator that
   works at the extremes and not the middle is a check, not a replacement.
2. **Fluency.** README sections 3.5 and 6 item 3: fluency sits ~2.5 points below every
   other criterion and nothing says whether that is machine translation or one criterion's
   wording. **After the switch every corpus number carries it**, so the cheap test —
   reword that one criterion, re-run 134 — is worth doing before the freeze rather than
   after. This is the one open question with a deadline.
3. **Scope.** This plan covers `examples/tr/onde/` only. `examples/tr/core/Makefile` and
   `examples/tr/fr/Makefile` also pin `ollama:qwen3.6`, and nothing in experiment 13
   measured anything about them. Proposed: leave them, revisit once `onde/` has settled.
4. **Is the 0.69 slope stable enough to invert?** README section 6 item 4. If it is, old
   and new scores can be put on one scale and the migration keeps continuity with published
   numbers. If the slope moves with the translator, the two scales stay separate
   permanently and the changeover is a hard break. The full re-run produces the data to
   answer this at n=1,072.
5. **Is the ordering inside the old scheme's floor real?** README section 6 item 1. The 10
   translations the old scheme scores 0 come back spread over 2.6–31.2, and that is the one
   place this scheme claims information its reference does not have. Checking it needs
   human judgment on ten translations. Not a blocker — the old scheme's 0s are not a
   competing answer — but it is unverified and should not be quoted as if it were.
6. **Three runs of both schemes on one target set.** README section 6 item 7. Would replace
   section 4.6's borrowed noise figures (1.12 and 2.25, from different experiments on
   different targets) with a measurement. Cheap, and it is what the choice between the
   five-criterion and fifty-item schemes turns on — but that choice is already made for the
   corpus on cost and comparability (section 3.7), so this is confirmation rather than
   input.

---

## 5. Touch List

Everything that names the evaluator, for when step 3 happens. Not exhaustive for prose
mentions.

| File | What |
|---|---|
| `examples/tr/onde/common.mk` | `EVALUATOR`, and `SUMMARIZER` decoupled from it (3.1) |
| `examples/tr/onde/common.mk` | `evaluate:` target (3.2) |
| `examples/tr/ADD_MODEL.md` | States the evaluator is fixed to `ollama:qwen3.6` "to keep the scoring criteria consistent" |
| `examples/tr/onde/README.md` | Corpus-level description |
| Each `examples/tr/onde/*/README.md` | Regenerated by `trtools trend --sync` |
| Each `examples/tr/onde/*/SCORES.txt` | Regenerated by `trtools agg` |
| Each `examples/tr/onde/*/TRENDS.jsonl` | See 3.3 — regenerate, do not append |
| `examples/tr/onde/gpt-oss/Makefile` | Has its own `OR_EVALUATOR`; decide whether it follows |
| `examples/tr/onde/qwen3.6/Makefile` | Has `ALT_EVALUATOR = ollama:gpt-oss:120b`; probably unaffected |
