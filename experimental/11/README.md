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

[pick_unstable.py](pick_unstable.py) ranks every stored old-scheme evaluation by how much
its total score moves across three runs under the same evaluator (`qwen3.6`), and
[targets.tsv](targets.tsv) keeps the worst one per translation model — the translations a
new scheme most needs to steady, not a cross-section of quality bands:

| Translator | Language | Old scores (3 runs) | Old range | Old median |
|---|---|---|---:|---:|
| gpt-5.6-terra | Polish | 69, 81, 15 | 66 | 69 |
| gpt-oss | Interlingua | 89, 73, 34 | 55 | 73 |
| qwen3.8 | Japanese | 56, 78, 25 | 53 | 56 |
| gemini-3.5-flash-lite | Kannada | 29, 61, 80 | 51 | 61 |
| ox-alpha | Irish | 38, 68, 89 | 51 | 68 |
| qwen3.6-27b | Korean | 92, 42, 77 | 50 | 77 |
| gemini-2.5-flash | Russian | 91, 44, 86 | 47 | 86 |
| gemini-3-flash | Hindi | 91, 81, 45 | 46 | 81 |

Mean range 52.4 points, mean stdev 22.16 — on the *same* translation, scored by the *same*
model, three separate times. `pick_unstable.py --per-translator 1` also spreads the pick
across eight different translation models (Slavic, Japonic, Dravidian, Celtic, Koreanic and
Indo-Aryan languages plus a constructed one), so the wobble isn't a quirk of one model's
output; translations whose line count no longer matched the original were excluded first,
since `trtools` refuses to evaluate those (`batch.py` skips them, `evaluate.py` raises) and
their stored evaluations would belong to an older version of the file.

Run the identical eight translations through the new 50-item scheme, same reference
evaluator (`qwen3.6`, `evals/`, thinking on):

| Translator | Language | New scores (3 runs) | New range | Range change |
|---|---|---|---:|---:|
| gpt-5.6-terra | Polish | 87, 72, 69 | 18 | -48 |
| gpt-oss | Interlingua | 80, 89, 80 | 9 | -46 |
| qwen3.8 | Japanese | 86, 89, 84 | 5 | -48 |
| gemini-3.5-flash-lite | Kannada | 81, 79, 95 | 16 | -35 |
| ox-alpha | Irish | 85, 92, 89 | 7 | -44 |
| qwen3.6-27b | Korean | 84, 93, 100 | 16 | -34 |
| gemini-2.5-flash | Russian | 96, 100, 95 | 5 | -42 |
| gemini-3-flash | Hindi | 97, 98, 98 | 1 | -45 |

Mean range 9.6 points, mean stdev 4.17 — roughly a fifth of the old spread, and every
single translation improved; none regressed. This holds up under the other two evaluators
too (see "Results" below), so it isn't specific to `qwen3.6`.

Run-to-run stability is only half of what makes a score trustworthy; the other half is not
moving when a *different* model does the judging. Same eight translations, new scheme,
median across the three runs above, against `gemma4:31b` and `gpt-oss:120b` as evaluators
too, next to the old scheme's `qwen3.6` median as a reference point:

| Translator | Language | Old (qwen3.6) | New (gemma4:31b) | New (gpt-oss:120b) | New (qwen3.6) | New spread |
|---|---|---:|---:|---:|---:|---:|
| gpt-5.6-terra | Polish | 69 | 70 | 92 | 74 | 22 |
| gpt-oss | Interlingua | 73 | 94 | 88 | 84 | 10 |
| qwen3.8 | Japanese | 56 | 92 | 96 | 88 | 8 |
| gemini-3.5-flash-lite | Kannada | 61 | 89 | 49 | 87 | 40 |
| ox-alpha | Irish | 68 | 96 | 98 | 89 | 9 |
| qwen3.6-27b | Korean | 77 | 84 | 94 | 94 | 10 |
| gemini-2.5-flash | Russian | 85 | 98 | 98 | 97 | 1 |
| gemini-3-flash | Hindi | 81 | 98 | 92 | 98 | 6 |

"New spread" is the range across the three new-scheme evaluators alone (old is not
comparable here — it was only ever run under `qwen3.6`). It averages 13.25 points per
translation, and six of the eight targets sit at 10 points or under; `gemini-3.5-flash-lite
/ kn` (40) and `gpt-5.6-terra / pl` (22) are the exceptions. Every new-scheme evaluator also
reads noticeably higher than the old `qwen3.6` baseline on nearly every row — the "roughly
halves" framing below is about the *gap between evaluators* narrowing, not about the
absolute scores converging on the old ones (see "It moves between runs" above and the
Results section's "Dependence on the evaluator narrows" for why that's expected, not a
defect: the old scheme's discretion is what produced the low baseline in the first place).

The next section asks the same question the old scheme's own numbers already answer: how
far apart do two evaluators land on the *same* translation.

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

This table is old-scheme only, and on a different set of translations from the rest of
this experiment (`examples/tr/onde/qwen3.6/*`, all translated by `qwen3.6`, vs
`targets.tsv`'s one-per-translator set). The new scheme was never run against this
specific set — but the same two evaluators (`qwen3.6`, `gpt-oss:120b`) were both already
run against `targets.tsv` for the rest of this experiment, so the analogous gap can be
read straight off that existing data: mean 88.9 against 88.4, with a mean absolute
difference of 10.5 points (`agg50.py`'s "qwen3.6 vs gpt-oss:120b, new scheme, in the old
table's terms" section). Against the old scheme's 49.6/69.5/21.6, the evaluator gap on
this pair roughly halves under the new scheme — smaller than the "Dependence on the
evaluator model" section's three-evaluator spread suggests on its own, since `gemma4:31b`
sits closer to `gpt-oss:120b` than `qwen3.6` does on a few of these targets.

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

[targets.tsv](targets.tsv), selected by instability rather than quality band — see "It
moves between runs" above for the table and the exclusion rule (line-count mismatches).

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
call, covering every chunk under `--split`), `no_think` and `no_evidence` (see below), so
the two variants can be compared on both score and speed without relying on file mtimes.
`agg50.py` reads both directories and reports the comparison under "Thinking on vs off" and
the two "Timing" sections; `load_timing` prefers the recorded `duration_seconds` field and
falls back to the mtime-difference estimate only for older files that predate the field.

`duration_seconds` counts time spent on failed retries too. `batch.sh` records one
`attempt-start` timestamp per output file, before `try_eval`'s retry loop, and passes it to
every retried `eval50.py` invocation via `--attempt-start`; `eval50.py` measures from that
timestamp instead of its own process start when it is given, so a file that needed 2 of its
3 allotted attempts reports the full wall-clock time, not just the successful attempt's.

Without thinking, models had nowhere to put their reasoning except the answer itself: they
padded every one of the 50 items with an extra explanation field beyond what the schema
asked for, bloating the answer enough to hit `--max-length` mid-response. `--no-evidence`
(new `eval50.py` flag, used only for `evals-nt`) drops the per-item `evidence` field —
`overall_comment` at the end of the call is unaffected — which removes the pressure that was
causing the padding.

Dropping evidence also exposed a schema mismatch: asked for a single-field
`{"verdict": ...}` object per item, models tended to flatten it and hand back the bare
string directly (e.g. `"a01_speaker_label_present": "no"`), which crashed `check_sane` with
`missing verdict for ...`. The schema for a no-evidence item is now the bare
`Literal["yes", "partial", "no"]` itself rather than a wrapping object, matching what models
actually produce; `check_sane`, `tally()` and `agg50.py`'s `item_scores()` all go through a
shared `verdict_of()` that also tolerates the wrapped-object shape, in case some model wraps
it anyway.

One caveat applies to the whole comparison: `gpt-oss:120b` does not honor `--no-think`. It
keeps producing its reasoning regardless of the flag, so its `evals-nt/` rows are "thinking
on, evidence off", not no-think at all. Only `qwen3.6` and `gemma4:31b` give a genuine
thinking-on-vs-off contrast; see the results section below.

`evals-nt/` is complete (72/72) with `FAILURES-evals-nt.txt` empty — no call failed to
return schema-conforming JSON under `--no-think --no-evidence` either.

### Evidence on vs off

`evals-nt/` changes two things at once, so it cannot say how much of its effect belongs to
thinking and how much to the missing evidence. `evals-ne/` is the third variant that fills
that cell: `--no-evidence` alone, thinking left on.

| Variant | Thinking | Evidence |
|---|---|---|
| `evals/` | on | on |
| `evals-nt/` | off (`gpt-oss:120b` excepted, as above) | off |
| `evals-ne/` | on | off |

Beyond separating the two, this variant asks whether writing evidence takes effort away from
the verdict itself. The `evidence` strings in `evals/` frequently cite line numbers that are
wrong — `evals/onde-gemini-3-flash-hi-qwen3.6-1.json` marks `a01_speaker_label_present`
`partial` on the grounds of two lines missing a speaker label, where the translation has
five, which by the item's own rule (1-3 lines `partial`, 4+ `no`) should have been `no`.
That is not a surprise on its own: `eval50.py` passes the texts as plain multi-line strings
with no line numbers in them, so an exact citation is something the model has to count out
for itself. The open question is whether producing it also moves the verdict, or whether it
is an unreliable but harmless side output.

`agg50.py` reports this under "Evidence on vs off (thinking on)", alongside a per-item
comparison of which verdicts move against `evals/`. The scores alone would not settle it: a
variant can leave the total where it was while individual verdicts move in both directions
and cancel, which is what `gemma4:31b` does between `evals/` and `evals-nt/` (see the
results below).

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
(8 targets x 3 evaluators x 3 runs). `FAILURES-evals.txt` is empty: every call returned a
schema-conforming JSON on the first attempt.

### Run-to-run wobble narrows sharply, under every evaluator

The `qwen3.6` figures (mean range 52.4 -> 9.6) are in "It moves between runs" above.
Averaged across all three evaluators the new scheme's mean range is 9.2, so the
improvement isn't specific to `qwen3.6` — see the full per-translation, per-evaluator
breakdown in [SCORES.md](SCORES.md).

### Dependence on the evaluator narrows, but does not disappear

The old scheme's evaluator gap (`qwen3.6` vs `gpt-oss:120b`, mean 49.6 vs 69.5, mean
absolute difference 21.6) is not measured on the same eight translations, so the comparison
is directional rather than exact — see "It moves when the evaluator changes" above for the
same pair's gap on `targets.tsv` itself (mean 88.9 vs 88.4, mean absolute difference 10.5).
Still, the new scheme's spread across all three
evalators averages 13.25 points per translation (from the "New spread" column), and the
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

### Thinking off is much faster, and what it costs depends on the evaluator

`evals-nt/` finished all 72 evaluations with no failures. The per-translation numbers are in
the "Thinking on vs off" table in [SCORES.md](SCORES.md); per evaluator they average out as:

| Evaluator | Mean score (think) | Mean score (no-think) | Mean call time (think) | Mean call time (no-think) | Mean run-to-run range |
|---|---:|---:|---:|---:|---:|
| `qwen3.6` | 88.9 | 74.0 | 245s | 23s | 9.6 -> 13.6 |
| `gemma4:31b` | 90.1 | 89.8 | 798s | 110s | 6.8 -> 2.8 |
| `gpt-oss:120b`* | 88.4 | 87.9 | 160s | 160s | 11.1 -> 12.5 |

\* **`gpt-oss:120b` ignores `--no-think`.** Via Ollama it keeps emitting its reasoning with
`think=False` set, confirmed directly against the running model. Its `evals-nt/` row is
therefore "thinking on + `--no-evidence`", and the unchanged call time (160s either way,
against 10x and 7x speedups for the two models that do honor the flag) is what that looks
like from the outside. Read that row as an evidence-on-vs-off comparison, not a thinking one.

For the two genuine cases the results diverge:

- `qwen3.6` loses a lot. Its mean drops 14.9 points, and every one of the eight targets
  scores the same or lower without thinking — two of them collapse by ~30 points
  (`gemini-3.5-flash-lite/kn` 87 -> 56, `ox-alpha/ga` 89 -> 57). Its run-to-run range widens
  too (9.6 -> 13.6), so the cheaper score is both harsher and noisier. The 10x speedup
  (245s -> 23s per call) does not buy a usable evaluation.
- `gemma4:31b` loses almost nothing. Its mean moves 0.4 points (differences scatter both
  ways, -10 to +8), and its run-to-run range actually narrows from 6.8 to 2.8. At 798s ->
  110s per call, turning thinking off makes the slowest evaluator in this set roughly as
  cheap as the others while leaving its aggregate scores where they were.

That `gemma4:31b`'s per-target differences still reach ±10 while its mean barely moves means
this is not "no-think is free for `gemma4:31b`" — individual verdicts do move. It is that
the movement has no consistent direction, which is what a model does when the 50-item rubric
is carrying the judgement instead of the reasoning.

Note that `evals-nt/` varies two things at once (thinking off *and* evidence off), so it
cannot separate the two effects on its own: attributing the `qwen3.6` drop to thinking alone
would need the thinking-on/evidence-off run. That is what `evals-ne/` is for (see "Evidence
on vs off" above); it has not been run yet, so the attribution stays open.

### Limitation: rare catastrophic defects are diluted, not just de-emphasized

The old scheme's harshness was not pure noise. `examples/tr/onde/qwen3.6/tr/onde-kn.txt`
(the `qwen3.6`-vs-`gpt-oss:120b` comparison earlier in this document, Kannada) has, in 2 of
its 99 lines, a word that mixes Kannada with Arabic or Odia characters mid-word — genuinely
unreadable at that point, not just awkward. `qwen3.6`'s old-scheme score (26) treats this as
grounds to mark the whole document down across all five criteria; `gpt-oss:120b`'s (73)
reads it as one defect among several and scores the other 97 lines on their own, mostly
adequate, merits.

Run the same 2-line defect through the new scheme's rule for the matching item
(`b05_script_consistency`, "only the writing system the target language's orthography uses
appears in the text"): 2 lines falls in the `partial` band (roughly 1-3 lines), costing 1 of
2 points on that one item — 1 point out of the 100-point total. A model that reliably stays
mediocre-but-coherent for 99 lines and a model that is excellent for 97 and produces
unreadable garbage in 2 would score almost identically under this scheme, even though the
second is arguably less trustworthy to deploy unsupervised. Spreading the rubric across 50
independently-scored properties is exactly what narrows run-to-run and evaluator wobble (see
above), but the same averaging also flattens a rare, severe failure into noise. The scheme
was designed to measure average per-property quality, not worst-case reliability, and it
does not distinguish the two.

### Conclusion

Fifty narrow yes/partial/no items produce a score that is far more stable across runs and
noticeably (though not completely) more stable across evaluator models than five wide
0-20 criteria. The ceiling problem for `gpt-oss:120b` and the leniency concern for
`gemma4:31b` both turned out to be artifacts of the old scale rather than properties of the
models. The concrete case where an evaluator swing had a real number (49 vs 87-89 on one
target) points to a difference in what each model actually inspects (line-level scrutiny vs
whole-document impression), which naming the properties does not by itself resolve. The
scheme also trades away the old scheme's (crude but real) sensitivity to rare catastrophic
defects for its gain in run-to-run and evaluator stability — see the limitation above.

## Reproducing

```bash
uv run experimental/11/pick_unstable.py --per-translator 1 --exclude gpt-5.6-luna/no -n 8 \
  > experimental/11/targets.tsv
bash experimental/11/batch.sh          # runs evals/, evals-nt/ and evals-ne/, then compares
uv run experimental/11/agg50.py        # SPLIT=group on batch.sh to step the new scheme down
```
