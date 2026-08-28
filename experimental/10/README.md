# Experiment 10: Verifying the operation of trtools review

After integrating the third-party evaluation approach (`review.py`) established in Experiments 07 and 09 as a subcommand of `trtools`, this experiment verifies the full translate → eval → review → eval pipeline for the 5 languages (bg, eu, et, sl, hu) where revision was most effective in Experiment 09.

## Purpose

- Verify the implementation of the `trtools review` subcommand
- Confirm the integrated display of `StatusLine` (Rich progress bar) across `translate`, `eval`, and `review`
- Compare scores before and after revision

## Flow

1. **Translation**: `trtools translate` (gemma4:26b, `--threshold 20`, with terminology injection) → `tr/onde-{lang}.txt`
2. **Translation evaluation × 3**: `trtools eval` (qwen3.6) → `evals/onde-{lang}-{1,2,3}.json`
3. **Revision**: `trtools review` (qwen3.6, `--no-think`) → `tr-rev/onde-{lang}.txt`
4. **Post-revision evaluation × 3**: `trtools eval` (qwen3.6) → `evals-rev/onde-{lang}-{1,2,3}.json`

## Results

| Language | Base translation | Post-revision | Diff |
|---|---|---|---|
| bg: Bulgarian | 88 | 87 | -1 |
| et: Estonian  | 30 | 51 | +21 |
| eu: Basque    | 17 | 59 | +42 |
| hu: Hungarian | 26 | 89 | +63 |
| sl: Slovene   | 56 | 83 | +27 |

Execution time: about 3.5 hours (bg: 37m57.938s; eu, et, sl, hu: 172m9.014s)

## Discussion

Experiment 10's base scores are overall lower than Experiment 09's. Whereas Experiment 09 selected the optimal model per language, Experiment 10 uniformly used gemma4:26b, so translation quality is lower for medium-resource languages.

Revision produced large improvements for eu (+42), hu (+63), sl (+27), and et (+21), confirming that revision works effectively even when the base score is low. However, the final post-revision scores did not reach those of Experiment 09 (eu: 87, hu: 96, sl: 95, et: 82).

bg had a high base score of 88, so revision resulted in a slight decrease (-1). This is consistent with Experiment 09's finding that, for languages with a high pre-revision score, the revision model tends to make unnecessary changes that degrade quality.

We confirmed that the `trtools review` subcommand and the progress bar integration work correctly.
