# Jev Evaluation of the Corpus

A record of the run that produced `{model}/jev.jsonl`. When it ran it replaced nothing:
the corpus's published scores still came from `ollama:qwen3.6` over `evals/`, and switching
that over was a separate decision
([experimental/13/PLAN.md](../../../experimental/13/PLAN.md)). The corpus has since
switched: `SCORES-jev.txt`, the trend column and the charts come from these files, and
`evals/`, `SCORES.txt` and `TRENDS.jsonl` remain beside them as the previous evaluator's
record.

## What Ran

`make jev` from this directory, on 2026-09-22, evaluating all 16 models in
`MODELS` order. That target has since gone: each model's `make evaluate` runs the same
command now.

| | |
|---|---|
| Evaluator | `jev-1.13.0`, pinned to the version rather than the `jev-latest` alias |
| Scheme | `degrees@f518286e` — five criteria, five severity levels, hashed over everything that determines a score |
| Runs | One per language. Experiment 12 measured this evaluator's run-to-run range at 1.12 points, with run 1 alone reproducing the median of three at Pearson 0.998 |
| Coverage | 16 models × 67 languages = **1,072 evaluations** |
| Output | `{model}/jev.jsonl`, one JSONL record per language, beside `evals/` |

The record format and the reasoning behind each field are in
[experimental/13/PORT.md](../../../experimental/13/PORT.md).

## Tokens, Time and Cost

`time` is the sum of the per-language `seconds` in each `jev.jsonl`, which measures the
processing of a language end to end rather than the API call alone.

| Model | input | output | time |
|---|---:|---:|---:|
| gemma4 | 477,838 | 5,561 | 20.9s |
| gemma4-31b | 477,609 | 5,561 | 19.9s |
| gpt-oss | 460,627 | 5,561 | 19.6s |
| qwen3.6-27b | 471,989 | 5,561 | 20.6s |
| qwen3.6 | 468,598 | 5,561 | 21.5s |
| qwen3.8 | 465,660 | 5,561 | 18.3s |
| bonsai2-27b | 459,674 | 5,561 | 19.3s |
| muse-glimmer | 466,467 | 5,561 | 19.5s |
| ox-alpha | 469,911 | 5,561 | 19.0s |
| union-alpha | 471,322 | 5,561 | 18.5s |
| gpt-5.6-luna | 472,594 | 5,561 | 19.6s |
| gpt-5.6-terra | 470,909 | 5,561 | 19.4s |
| gemini-3.5-flash-lite | 473,261 | 5,561 | 19.5s |
| gemini-2.5-flash | 465,790 | 5,561 | 18.9s |
| gemini-3-flash | 489,167 | 5,561 | 19.7s |
| gemini-3.7-flash | 475,131 | 5,561 | 19.4s |
| **Total** | **7,536,547** | **88,976** | **313.6s** |

The run cost **$0.3165** and took **5m22.6s** of wall time: $0.0198 and 20.2 seconds a
model, $0.000295 an evaluation. The per-language `seconds` account for 313.6s of the wall
time; the remaining 9.0s is process startup and the resume scan, sixteen times over.

Output tokens are 5,561 for every model without exception — five Score answers per
language carry no prose, so the reply's length does not depend on what is being judged.
Input varies by only 6.4% across the corpus (459,674 to 489,167), which is the length of
the translations themselves.

Per language: median **0.28s**, minimum 0.22s, maximum 2.21s.

[PLAN.md](../../../experimental/13/PLAN.md) section 2 estimated 1,072 evaluations at
roughly $0.21 and five minutes, extrapolated from a quarter of them run by the
experiment's own script. The time was right; the cost came in **51% over** at $0.3165.
Neither figure changes what section 2 concluded from them -- three runs of this would be
$0.95 and sixteen minutes, and the old evaluator's 3,216 evaluations are neither -- but
the estimate should be quoted as $0.32 from here on.

## Checked Against Experiment 13

Four of the sixteen — `gpt-5.6-luna`, `union-alpha`, `qwen3.8` and `bonsai2-27b` — were
already evaluated by `experimental/13/eval5_jev.py` on the same pinned model and the same
rubric. Re-running them rather than converting their results is what makes this
comparison possible, and it is the check on the port.

**The input token counts are identical, model for model**, to the experiment's: 472,594 /
471,322 / 465,660 / 459,674. The two implementations send the same prompt, byte for byte.

Scores, as 0–100 totals over 67 languages each:

| Model | mean Δ | Pearson | Spearman |
|---|---:|---:|---:|
| gpt-5.6-luna | -0.082 | 0.9940 | 0.9873 |
| union-alpha | +0.091 | 0.9927 | 0.9872 |
| qwen3.8 | -0.019 | 0.9984 | 0.9965 |
| bonsai2-27b | -0.013 | 0.9995 | 0.9987 |
| **All 268** | **-0.006** | **0.9995** | **0.9980** |

The mean signed difference over 268 translations is -0.006 points, so the port carries no
systematic shift. Mean absolute difference is 0.517 and the median 0.375; 26 of 268 differ
by more than the 1.12 points experiment 12 measured as the run-to-run range, which is what
a mean range with tails produces rather than evidence of a second effect. Only 12 of 268
came back bit-identical: the evaluator is not deterministic, and was never claimed to be.

## What This Run Does Not Do

`SCORES.txt`, `TRENDS.jsonl`, each model's `README.md` and the charts are untouched and
still describe the `evals/` scale. `trtools agg` cannot read `jev.jsonl` yet — its file
discovery requires three runs per language — and `trtools trend` has no prose to summarise
under an evaluator that returns none. Both are open items in
[experimental/13/PORT.md](../../../experimental/13/PORT.md) and
[experimental/14/PORT.md](../../../experimental/14/PORT.md). Both have since been done,
with `trtools agg --jev` and `trtools trend --jev`.

## Appendix: What Jev Was Asked

Printed by `trtools jev --show-scheme`, whose output this section is. The wording lives in
`trtools/jev_criteria.py`, because the identifier below is a hash of what is actually sent
and a second copy could only disagree with it. This is that copy, kept here so a corpus
directory says what its scores mean. It goes stale visibly: reword anything under it and
the identifier changes, and the `rubric` in every `jev.jsonl` beside this file stops
matching.

### `degrees@f518286e`

Five criteria, each asked as one TypeSafe Score question over the same five ordered levels.

**Asked of every criterion**

- `judge`: How well does `translation` meet the criterion below, read against `original`?
- `scope`: Judge this criterion alone, over the whole document. The other four are asked about by their own questions.

**Criteria**

| Key | Heading | `criterion` |
| --- | --- | --- |
| `readability` | Readability & comprehensibility | Whether target language readers can easily understand the content, whether complex concepts are explained clearly, and whether the sentence structure is logical and easy to follow |
| `fluency` | Fluency & naturalness | Whether the translated text sounds natural and smooth to native speakers of the target language, whether there are unnatural expressions or awkward grammar, and whether vocabulary choices are appropriate and contemporary |
| `terminology` | Terminology appropriateness | Whether technical terms are appropriately handled according to the reader's understanding level, whether explanations or paraphrases are provided when necessary, and whether term selection is consistent |
| `contextual_adaptation` | Contextual adaptation | Whether the original text's intent and purpose are effectively conveyed, whether expressions consider the target readers' cultural background, and whether expressions are improved or optimized as needed |
| `information_completeness` | Information completeness | Whether important information from the original text is conveyed without omission, whether appropriate supplements are provided to aid reader understanding, and whether redundancy is eliminated while keeping the content concise and clear |

**Levels**, worth 5 points each on the 0-20 scale the corpus reports

| Level | Wording |
| ---: | --- |
| 0 | The criterion is not met anywhere in the translation: it fails over the whole document, or there is no usable target-language text to judge against it. |
| 1 | The criterion fails across most of the translation, over far more than a handful of lines. |
| 2 | The criterion fails repeatedly, or across a wide part of the translation: roughly four lines or more, or a single occurrence whose effect spreads through the whole text. |
| 3 | The criterion is mostly met. The places where it falls short are scattered and confined to roughly one to three lines. |
| 4 | The criterion is met throughout the translation; not a single place where it falls short. |

**State keys**, in order: `task`, `source_language`, `target_language`, `line_correspondence`, `original`, `translation`
