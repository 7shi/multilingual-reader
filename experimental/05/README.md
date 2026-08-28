# Translation Experiment Using trtools translate

This experiment directory builds on the term pre-extraction approach from [experimental/04](../04/), but migrates the translation script to `trtools translate`.

## Background and Motivation

In experimental/04, term extraction, translation fixing, and translation itself were all handled by a single integrated script. To establish a proofreading workflow for the term TSV (extract → human review/edit → translate), this was split into `trtools term extract/translate`.

In experimental/05:

- **Terms are extracted and proofread beforehand with `trtools term`** (`examples/terms/finetuning-fr.tsv`)
- **Translation is run with `trtools translate`** (referencing the shared term file)
- Same threshold=10, keep=5, no-CoT settings as experimental/04

Because multiple translation runs share the same proofread term dictionary, this fundamentally eliminates run-to-run terminology drift (variation such as `affinage` → `refinamiento` / `ajuste fino`).

## Translation System

### trtools translate

```bash
uv run trtools translate <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**Main options:**

| Option | Value | Description |
|---|---|---|
| `--threshold` | 10 | Interval (in lines) for generating a summary |
| `--keep` | 5 | Number of translation pairs kept after compression |
| `--no-think` | (flag) | Disable CoT (no impact on translation quality, faster) |
| `--terms-json` | `examples/terms/finetuning-fr.json` | Term chunk map |
| `--terms-tsv` | `examples/terms/finetuning-fr.tsv` | Term-to-translation mapping |

### Term File

`examples/terms/finetuning-fr.tsv` is a TSV generated and proofread with `trtools term extract/translate`.
Since all runs share the same term dictionary, no run-to-run terminology drift occurs.

| Language | Column |
|---|---|
| French (source) | Column 1 |
| English | Column 2 |
| Spanish (target) | Column 3 |

### batch.sh

```bash
bash batch.sh
```

For the two models in MODELS.txt (gemma4-26b, gemma4-e4b), this runs **3 translations × 3 evaluations**.

**File naming:**

```
tr/<model>-<trrun>.txt              e.g. tr/gemma4-26b-1.txt
evals/<model>-<trrun>-eval-<evrun>.json
```

Unlike experimental/04, no `-terms.json` file is generated under tr/ (a shared term file is used instead).

## Target Models

Same two models as experimental/03 and experimental/04.

| Model | experimental/04 score | Reason for selection |
|---|:---:|---|
| gemma4-26b | 96 / 96 / 99 | No sharp drops in any run, most stable |
| gemma4-e4b | 95 / 96 / 92 | Alternative for resource-constrained settings |

## Evaluation System

Same pipeline as experimental/04.

- Evaluator: `ollama:qwen3.6`
- 5 criteria × 20 points = 100 points total
- Aggregation: median of 3 evaluations

## Trials

| Trial | threshold | Result |
|---|:---:|---|
| [tr/](tr/) | 10 | gemma4-26b: 95/96/97, gemma4-e4b: 95/95/94 |

## Comparison Results

Comparison against experimental/04 (terms extracted per run) — the only difference is whether the term dictionary is shared:

| Model | experimental/04 | experimental/05 |
|---|:---:|:---:|
| gemma4-26b run 1 | 96 | 95 |
| gemma4-26b run 2 | 96 | 96 |
| gemma4-26b run 3 | 99 | 97 |
| gemma4-e4b run 1 | 95 | 95 |
| gemma4-e4b run 2 | 96 | 95 |
| gemma4-e4b run 3 | **92** (sharp drop) | 94 |

**Observations:**

- **gemma4-e4b's sharp drop is resolved**: 92 → 94 points, no sharp drop. This confirms the effect of eliminating run-to-run terminology drift via the shared term dictionary
- **gemma4-26b**: the ceiling dipped slightly, 99 → 97, but it remains stable in the 95–97 range
- **Overall**: both models converge into the 94–97 range. Given the practical ceiling of the qwen3.6 evaluator (97 points), the proofread shared term dictionary is contributing to improved stability

## Deduction Analysis

Analysis of all 18 evaluation logs (9 per model).

### gemma4-26b (9 logs)

| Criterion | Average | Minimum |
|---|:---:|:---:|
| information_completeness | 19.89 | 19 |
| contextual_adaptation | 19.22 | 19 |
| terminology | 19.44 | 18 |
| readability | 18.89 | 18 |
| fluency | 18.67 | 17 |

**Deduction patterns:**
- The translation of `antisèche` ("cheat sheet") as `acordeón` — understood in some regions but not universal (`chuleta` is recommended). Since this is not in the term dictionary, it varies between runs
- The -3 fluency deduction (run 1, eval-2) came from a combination of `acordeón` and slightly unnatural phrasing
- No structural defects

### gemma4-e4b (9 logs)

| Criterion | Average | Minimum |
|---|:---:|:---:|
| terminology | 19.11 | 18 |
| readability | 18.78 | 18 |
| fluency | 18.33 | 17 |
| contextual_adaptation | 18.78 | 17 |
| information_completeness | 19.44 | 18 |

**Deduction patterns:**
- **Run 2**: inconsistent formal register (`Vean más bien: usted no le enseñaría...` — the plural "ustedes" imperative and the singular "usted" form appear mixed within a single sentence). Without specifying the regional variant (Latin American vs. Spain), the model drifts
- **Run 3**: a dropped speaker label (`Camille: Elle oublie tout.` → `Olvida todo.`) combined with a mistranslation of `antisèche → sinopsis` ("summary/synopsis") caused one evaluator to deduct a total of 7 points across the readability, contextual_adaptation, and information_completeness criteria. However, 2 of the 3 evaluations (eval-1, eval-3) missed this (scoring 93–94)

### Summary

For gemma4-26b, deductions almost entirely trace back to a single stylistic choice — the translation of `antisèche` — with no structural defects. gemma4-e4b is treated as a fallback for resource-constrained environments, where occasional minor structural issues such as dropped speakers or inconsistent formal register are considered acceptable trade-offs. gemma4-26b remains the primary recommendation whenever it is available.
