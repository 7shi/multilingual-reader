# Plan: Replacing the Corpus Evaluator with the Five-Criterion Jev Scheme

[README.md](README.md) is the experiment record and states only what was measured; this
file holds the decision that record was used for.

**Status**: frozen, 2026-09-23. The decision stands and step 1 is done — the whole corpus
went through `trtools jev` rather than the experiment's script, so the production path's
cost and wall time were measured at full scale; [PORT.md](PORT.md) is that design and
[examples/tr/onde/JEV.md](../../examples/tr/onde/JEV.md) the run. **Everything still ahead —
steps 2 and 3, the open questions, the blockers and the touch list — moved to
[PORT.md](PORT.md)**, and this file is not edited again.

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
   against the current 3,216, measured at **$0.3165 and 5m22.6s** (estimated at $0.21 and
   five minutes). Cost and wall time stop being design constraints.
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
evaluations for $0.3165 (estimated at $0.21) that is an acceptable answer, but it is a
change in kind:
reproducibility stops being a property of the tooling and becomes a property of the re-run
being cheap. Accepted deliberately, not overlooked.

---

## 3. Sequence

**Run first, switch second.** The full re-evaluation is itself the check on the corpus's
middle band — translators the old scheme scores at 60–70, the one part of the range nothing
has been compared against. Switching `common.mk` before looking at that result would make
an unverified run the record.

### Step 1 — evaluate the whole corpus (done)

This section planned 804 evaluations of the twelve translators not already covered, run by
`eval5_jev.py` into `experimental/13/evals-degrees/` (estimated at about $0.16 and three to
four minutes). It was carried out differently, for a reason this file did not anticipate:
the estimates in section 2 were extrapolated from a quarter of the corpus run by the
experiment's script, and converting the four already-evaluated translators would have left
them unchecked at exactly the scale the decision rests on.

What ran instead was `make jev` from `examples/tr/onde/`, evaluating **all 16 translators,
1,072 evaluations, for $0.3165 in 5m22.6s**, through `trtools jev` — the production path,
designed in [PORT.md](PORT.md) and recorded in
[JEV.md](../../examples/tr/onde/JEV.md). Results are in
`examples/tr/onde/<translator>/jev.jsonl`, beside `evals/` rather than replacing it, so the
current corpus stays untouched and reproducible while this is being decided.

Re-running the four also checked the port against this experiment: identical input token
counts, Pearson 0.9995 over 268 translations, and a mean signed difference of -0.006
points.

**Do not run `eval50_jev.py` over the corpus.** Ranking is what the yardstick needs, the
five-criterion scheme is what README section 3.7 recommends for it, and the fifty-item
scheme costs twice the input tokens to return the same ordering. It stays available for
diagnosing one translator at a time.

### Steps 2 and 3

Reporting the corpus on the yardstick's own terms, then switching and regenerating: moved
to [PORT.md](PORT.md) section 7, together with the two things the comparison has to be read
for — the middle band and the top four.

---

## 4. Open Questions

Moved to [PORT.md](PORT.md) section 8: whether Jev separates the top
of the corpus, whether the middle band holds, scope, the 0.69 slope, the ordering inside the
old scheme's floor, and a second source text.

**Removed from this list: fluency.** It was carried here as the one open question with a
deadline, on the grounds that every corpus number would inherit the bias once the scale was
frozen. README sections 5.1 and 5.2 close it from data already on disk: the fifty-item
scheme's own fluency group and the old generative evaluator over all 16 translators both
put fluency lowest, and it is the criterion that best separates the top four. There is
nothing to fix before the freeze.

---

## 5. Blockers

Moved. The evaluator's to [PORT.md](PORT.md) section 5: 5.2 aggregation (now 5.1), 5.4
`TIERS` accepted as it is (5.2), 5.5 `build_state`'s line count (5.3). The trend column's to
[experiment 14's PORT.md](../14/PORT.md): 5.1 `SUMMARIZER` cannot be Jev (its section 2),
5.3 `TRENDS.jsonl` is a time series (its section 4).

## 6. Touch List

Moved to [PORT.md](PORT.md) section 9, and for the trend column's files to
[experiment 14's PORT.md](../14/PORT.md).

---

## 7. Note on the Reference

`SCORES.txt` and everything drawn from it total the **five criteria's medians**
(`trtools/aggregate.py:67`). `agg13.py` uses the **median of the three total scores**, as
experiments 11 and 12 did. They agree on 60% of the corpus's 1,072 translations, differ by
a mean absolute 0.60 points, and refitting the compression against `SCORES.txt` gives
`0.688 × old + 24.8` against `0.690 × old + 24.7` (README section 5.5).

Nothing turns on it, but step 2's report is compared against the published corpus numbers,
so it should use `SCORES.txt`'s definition rather than `agg13.py`'s.
