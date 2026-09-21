# Experiment 11: 50 yes/partial/no items instead of 5 scores out of 20

## Purpose

`trtools eval` scores a translation on five criteria worth 20 points each. Nothing in the
prompt says what separates a 14 from a 17, so the evaluator model decides — and it decides
differently every run, and differently again when the model is swapped.

This experiment replaces the five wide scores with fifty narrow judgements. Each item names
one concrete property the translation should have, and the evaluator answers `yes`,
`partial` or `no`. Scoring maps them to 2, 1 and 0, so the scale stays 0-100 and the
existing quality bands still read the same way.

The question is not whether the scores go up or down. It is whether the score stops
depending on **which run** it came from and **which evaluator model** produced it.

## What the current scheme does

Everything below is measured from [examples/tr/onde/](../../examples/tr/onde/).

### It moves between runs

Across the translations selected for this experiment, the same evaluator on the same
translation spans a **mean range of 52.4 points** over three runs (mean stdev 22.16). See
[targets.tsv](targets.tsv) for the individual figures; they run from 46 to 66 points.

### It moves when the evaluator changes

`examples/tr/onde/qwen3.6/gpt-oss-120b/` holds a second evaluation of the same eight
translations by `gpt-oss:120b` instead of `qwen3.6`:

| Language | qwen3.6 | gpt-oss | Difference |
|---|---:|---:|---:|
| Kannada | 26 | 73 | +47 |
| Esperanto | 27 | 64 | +37 |
| Estonian | 53 | 84 | +31 |
| Telugu | 39 | 62 | +23 |
| Hindi | 29 | 43 | +14 |
| Turkish | 63 | 77 | +14 |
| Korean | 75 | 74 | -1 |
| Serbian | 85 | 79 | -6 |

Mean 49.6 against 69.5, with a mean absolute difference of 21.6 points. The record in
`examples/tr/onde/qwen3.6/README.md` is explicit that this is not a difference in what the
two models *see* — both detect the same contamination, hallucination and mistranslation —
but in how harshly they score it. `qwen3.6` deducts mercilessly for broken grammar and
lands in the 20s-40s; `gpt-oss` credits the surviving meaning and lands in the 60s-80s.

That is the dependence this experiment is trying to remove. Because the ruler moves with
the model, the evaluator has to be pinned to one model for scores to be comparable at all.

### Two of the zeros are not judgements

`examples/tr/onde/gemini-3-flash/evals/onde-eu-2.json` scores every criterion 0 while its
own rationale is positive:

> **readability (0/20)**: "The translated segment is clear and logically structured, making
> complex quantum concepts accessible in Basque"
>
> **fluency (0/20)**: "The Basque used in the provided portion is highly natural, idiomatic,
> and well-suited to a podcast dialogue."

The zeros come from guideline 1 of the prompt — *if missing/incomplete, assign 0 points to
ALL criteria* — firing on a truncated translation. The other two runs scored 72 and 63
because the cliff did not fire. That 72-point spread measures the cliff, not the text.

`examples/tr/onde/gpt-5.6-luna/evals/onde-no-3.json` is a different failure: every rationale
is an empty string and `overall_comment` is the literal `"string"`, the schema placeholder.
The evaluator returned the shape of an answer without an answer, and it was recorded as a 0
beside a 95 and a 90.

So the new scheme drops both cliffs from the prompt (guideline 1, and guideline 3's
*structural defects = 0-5 points*). Fifty items already spread a collapsed translation
across the properties it fails, without an instruction that overrides everything else.
Degenerate output is caught in code instead — see `check_sane` in [eval50.py](eval50.py).

## The 50 items

Five groups of ten, each item worth 0-2, for 100 points. The items were taken from the
vocabulary the existing evaluations actually use when they deduct points, so each one
corresponds to a failure mode that has been observed rather than an abstract virtue.

| Group | Covers | Drawn from deductions like |
|---|---|---|
| A. Structural integrity | speaker labels, line correspondence, truncation, repetition | *orphaned speaker names*, *truncation*, *degenerate repetition* |
| B. Language purity | target language, contamination, script, leakage | *mixed-language*, *script injection*, *meta-commentary*, *CoT leakage*, *JSON fragments* |
| C. Semantic fidelity | content, omission, addition, numbers, polarity, anaphora | *functional omissions*, *mistranslation*, *false friends* |
| D. Terminology | standard terms, consistency, notation, borrowing policy | *inconsistent terminology*, *notation*, *transliteration* |
| E. Fluency and naturalness | grammar, syntax, register, orthography | *literal*, *calque*, *register*, *orthographic errors* |

Every item is phrased positively, so `yes` always means good. The full list with the wording
sent to the evaluator is in [items.py](items.py).

All items share one three-level rule rather than fifty separate rubrics:

| Verdict | Rule |
|---|---|
| `yes` | The property holds throughout; not a single instance of the defect |
| `partial` | Mostly holds, with scattered exceptions (roughly 1-3 lines) |
| `no` | Recurs, or affects a wide part of the document (roughly 4+ lines) |

## Method

Nothing in `trtools` was changed. The experiment runs beside it.

| File | Role |
|---|---|
| [pick_unstable.py](pick_unstable.py) | Ranks existing evaluations by run-to-run range and picks the targets |
| [items.py](items.py) | The 50 item definitions |
| [eval50.py](eval50.py) | Runs one evaluation; builds the schema from the item list |
| [agg50.py](agg50.py) | Aggregates the new scheme, cites the old one in place, writes the comparison |
| [batch.sh](batch.sh) | Drives the run |

### Targets

Selected by instability, not by quality band: if the scheme cannot steady the translations
that wobble most, it is not worth adopting. Translations whose line count no longer matches
the original were excluded, because `trtools` refuses to evaluate those (`batch.py` skips
them, `evaluate.py` raises), so their stored evaluations belong to an older version of the
file.

See [targets.tsv](targets.tsv): eight translations from eight different translation models,
spanning Slavic, Japonic, Dravidian, Celtic, Koreanic and Indo-Aryan languages plus a
constructed one, with old-scheme ranges of 46-66 points.

### Runs

The new scheme runs under `qwen3.6` (the evaluator the score tables are built on),
`gemma4:31b` and `gpt-oss:120b`, three runs each — 72 evaluations.

The old scheme is not run. Its run-to-run baseline is the three `qwen3.6` runs per
translation already in `examples/tr/onde/*/evals/`, which `agg50.py` reads where they are;
nothing is copied here. Its evaluator baseline is the `gpt-oss:120b` comparison above.

Thinking is left on for the main runs, in `evals/`. The `--no-think` in
`examples/tr/onde/common.mk` reaches the translation phase only — `trtools/batch.py:169`
hardcodes `no_think=False` for evaluation — so every accumulated evaluation ran with
thinking on, and `evals/` matches that. Turning it off also breaks the *old* scheme's
structured output: the nested `ReasoningAndScore` comes back as a flat integer and
`trtools eval` raises `TypeError`. The new scheme has no such nesting, so `--no-think` is
safe to run against it — see "Thinking on vs off" below.

### Thinking on vs off

`batch.sh` also runs the identical 50-item scheme with `--no-think`, writing to `evals-nt/`
instead of `evals/` (same targets, evaluators and run count — 72 more evaluations). Each
result file records its own `duration_seconds` (wall-clock time for that file's evaluation
call, covering every chunk under `--split`) and `no_think`, so the two variants can be
compared on both score and speed without relying on file mtimes. `agg50.py` reads both
directories and reports the comparison under "Thinking on vs off" and the two "Timing"
sections; `load_timing` prefers the recorded `duration_seconds` field and falls back to the
mtime-difference estimate only for older files that predate the field.

This sub-experiment has not been run yet — only the scripts are in place.

### Splitting

Fifty items in one call may be more than a model can hold together, so `eval50.py` keeps the
items as data and builds the schema from any subset. `--split` steps the work down without
changing the output format:

| Step | Calls per run | Notes |
|---|---|---|
| `none` (default) | 1 | All 50 items at once |
| `group` | 5 | One call per group of 10 |
| `item` | 50 | One item per call, verdict only, no shared context |

## Results

Full tables are in [SCORES.md](SCORES.md), generated by `agg50.py` from the 72 evaluations
(8 targets x 3 evaluators x 3 runs). `FAILURES.txt` is empty: every call returned a
schema-conforming JSON on the first attempt.

### Run-to-run wobble narrows sharply

Under `qwen3.6`, the same eight translations that spanned a mean range of 52.4 points
(mean stdev 22.16) under the old scheme span a mean range of 9.6 points (mean stdev 4.17)
under the new one — roughly a fifth of the old spread. Every individual translation
improved; none regressed. Averaged across all three evaluators the new scheme's mean range
is 9.2, so the improvement is not specific to `qwen3.6`.

### Dependence on the evaluator narrows, but does not disappear

The old scheme's evaluator gap (`qwen3.6` vs `gpt-oss:120b`, mean 49.6 vs 69.5, mean
absolute difference 21.6) is not measured on the same eight translations, so the comparison
is directional rather than exact. Still, the new scheme's spread across all three
evaluators averages 13.25 points per translation (from the "New spread" column), and the
three evaluators' means across the eight targets converge to within a point of each other:
`gemma4:31b` 90.1, `qwen3.6` 88.9, `gpt-oss:120b` 88.4. That last figure is dragged down by
one outlier (see below); without it, the three sit at 90.1, 88.9 and 92.4.

The remaining spread is not evenly distributed: `gemini-3.5-flash-lite/kn` has a 40-point
spread between evaluators, and `gpt-5.6-terra/pl` has 22. The other six targets sit at 10
points or under. So the new scheme has not made the evaluator irrelevant — it has made most
translations insensitive to which evaluator scores them, while a minority still swing hard.

### `gpt-oss:120b` reaches the top of the scale

Under the old scheme `gpt-oss:120b` never appeared in this dataset scoring above 84. Under
the new scheme it scores 98, 98 and 96 on three different targets, and 88-94 on three more.
Naming the properties individually let it reach the ceiling when a translation actually
clears them, which the old scheme's wide, unstructured criteria did not.

Its one low score, 49 on `gemini-3.5-flash-lite/kn`, is not a degenerate response: the
evaluation cites concrete evidence for each failing item (line correspondence broken,
sentences trailing off, an untranslated English word, propositional content diverging from
the original, dropped sentences). On this target `gpt-oss:120b` was the most critical
evaluator, not the most lenient one — the opposite of the pattern the old scheme showed. It
is the reason `gpt-oss:120b`'s mean above is pulled down; the two other evaluators may be
under-crediting the same defects rather than `gpt-oss:120b` over-penalizing them.

### `gemma4:31b` is not uniformly lenient

Compared item-by-item against `qwen3.6` on the same eight targets, `gemma4:31b` scores
higher on five, lower on two, and about equal on one. Its mean (90.1) is close to the other
two evaluators' means, not far above them. Naming the properties appears to have constrained
it about as much as it constrained the other two models.

### The remaining wobble is spread thin, not concentrated

Across the 24 evaluator/translation combinations, 49 of the 50 items disagreed across runs
at least once; only `d06_abbreviations` never did. The three items with the highest
disagreement rate (`a01_speaker_label_present`, `a03_speaker_attribution`,
`c01_propositional_content`, each 50%) sit in different groups (A and C) and cover unrelated
properties, so this is not a case of one or two badly worded items driving the numbers. Per
the framing in the original handoff notes, this points toward the approach having reached
its structural limit — narrower per-item wording would not obviously help — rather than
toward rewriting a specific item.

### Cost: the 50-item call is slower, and evaluators differ a lot in how much

Per-call duration, from each file's own `duration_seconds` field (all 72 calls, not the
48 that file-mtime differences could reach): `gpt-oss:120b` medians 149s (~2.5 min) per
call, `qwen3.6` medians 210s (~3.5 min); `gemma4:31b` medians 557s (~9.3 min), with one
call taking 2912s (~49 min). This matches the handoff note that `gemma4:31b` was the slow
one to run. See the "Timing" table in [SCORES.md](SCORES.md).

### Conclusion

Fifty narrow yes/partial/no items produce a score that is far more stable across runs and
noticeably (though not completely) more stable across evaluator models than five wide
0-20 criteria. The ceiling problem for `gpt-oss:120b` and the leniency concern for
`gemma4:31b` both turned out to be artifacts of the old scale rather than properties of the
models. The concrete case where an evaluator swing had a real number (49 vs 87-89 on one
target) points to a difference in what each model actually inspects (line-level scrutiny vs
whole-document impression), which naming the properties does not by itself resolve.

## Reproducing

```bash
uv run experimental/11/pick_unstable.py --per-translator 1 --exclude gpt-5.6-luna/no -n 8 \
  > experimental/11/targets.tsv
bash experimental/11/batch.sh          # runs evals/ (thinking) and evals-nt/ (no-think), then compares
uv run experimental/11/agg50.py        # SPLIT=group on batch.sh to step the new scheme down
```
