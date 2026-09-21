# Experiment 11: which variant, taking one evaluator as reference

Reference evaluator: `gpt-5.6-terra`. Variants: `evals/`, `evals-nt/`, `evals-ne/`.

Every figure below is a median of 3 runs. The reference is assumed correct; the report measures how far each variant moves the other evaluators toward or away from it, and what the variant does to the reference itself.

## 1. The reference under each variant

If the reference itself moved between variants, nothing further could be compared. Its own per-target scores:

| Target | evals | evals-nt | evals-ne | Spread |
| --- | ---: | ---: | ---: | ---: |
| gpt-5.6-terra / pl | 79 | 77 | 72 | 7 |
| gpt-oss / ia | 50 | 51 | 50 | 1 |
| qwen3.8 / ja | 69 | 71 | 75 | 6 |
| gemini-3.5-flash-lite / kn | 71 | 66 | 64 | 7 |
| ox-alpha / ga | 61 | 61 | 61 | 0 |
| qwen3.6-27b / ko | 69 | 74 | 78 | 9 |
| gemini-2.5-flash / ru | 93 | 90 | 90 | 3 |
| gemini-3-flash / hi | 81 | 82 | 68 | 14 |
| **Mean score** | 71.6 | 71.5 | 69.8 | |
| **Mean run-to-run range** | 7.1 | 4.9 | 7.1 | |
| **Mean call time** | 43s | 39s | 34s | |

- `evals` vs `evals-nt`: 60/400 of the reference's item medians differ (15.0%).
- `evals` vs `evals-ne`: 67/400 of the reference's item medians differ (16.8%).
- `evals-nt` vs `evals-ne`: 42/400 of the reference's item medians differ (10.5%).

## 2. Ground truth on a01_speaker_label_present

Unlabeled lines are counted from the translations, and the rubric's bands (0 = yes, 1-3 = partial, 4+ = no) turn the count into the correct verdict. This is the one item that does not depend on the reference assumption.

- gpt-5.6-terra / pl: 2 unlabeled lines -> partial
- gpt-oss / ia: 13 unlabeled lines -> no
- qwen3.8 / ja: 0 unlabeled lines -> yes
- gemini-3.5-flash-lite / kn: 0 unlabeled lines -> yes
- ox-alpha / ga: 1 unlabeled lines -> partial
- qwen3.6-27b / ko: 0 unlabeled lines -> yes
- gemini-2.5-flash / ru: 15 unlabeled lines -> no
- gemini-3-flash / hi: 5 unlabeled lines -> no

| Evaluator | evals exact | evals bias | evals-nt exact | evals-nt bias | evals-ne exact | evals-ne bias |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `gemma4-31b` | 5/8 | +0.50 | 6/8 | -0.25 | 6/8 | +0.25 |
| `gpt-5.6-luna` | 8/8 | +0.00 | 7/8 | -0.12 | 7/8 | +0.12 |
| `gpt-5.6-terra` | 8/8 | +0.00 | 8/8 | +0.00 | 7/8 | -0.12 |
| `gpt-oss-120b` | 4/8 | +0.38 | 3/8 | +0.62 | 5/8 | +0.62 |
| `qwen3.6` | 5/8 | -0.25 | 5/8 | +0.50 | 6/8 | +0.00 |

Bias is the mean signed error with yes=2, partial=1, no=0; positive means scoring higher than the count warrants.

## 3. Distance from the reference, per variant

MAD is the mean absolute difference in total score. Recall and precision are over the reference's non-yes item medians: recall is how many of its defects the evaluator also reports, precision is how many of the evaluator's own reports the reference shares. False alarms are the non-yes verdicts the reference scores yes. Agreement is over all 50 item medians, defects and clean verdicts alike.

### evals

| Evaluator | Mean score | MAD | Pearson | Spearman | Kendall | Recall | Precision | False alarms | Item agreement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-5.6-terra` | 71.6 | 0.0 | - | - | - | - | - | - | - |
| `gemma4-31b` | 90.1 | 20.8 | -0.05 | 0.23 | 0.08 | 23.3% | 84.1% | 7 | 63.5% |
| `gpt-5.6-luna` | 74.9 | 5.0 | 0.89 | 0.86 | 0.78 | 81.1% | 86.0% | 21 | 80.5% |
| `gpt-oss-120b` | 88.4 | 22.2 | 0.11 | 0.10 | 0.04 | 22.6% | 63.2% | 21 | 61.8% |
| `qwen3.6` | 88.9 | 18.5 | 0.34 | 0.43 | 0.26 | 35.8% | 90.5% | 6 | 65.5% |

### evals-nt

| Evaluator | Mean score | MAD | Pearson | Spearman | Kendall | Recall | Precision | False alarms | Item agreement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-5.6-terra` | 71.5 | 0.0 | - | - | - | - | - | - | - |
| `gemma4-31b` | 89.8 | 18.5 | 0.11 | 0.19 | 0.14 | 26.0% | 88.0% | 6 | 61.0% |
| `gpt-5.6-luna` | 73.1 | 6.1 | 0.83 | 0.83 | 0.63 | 81.1% | 87.3% | 20 | 80.5% |
| `gpt-oss-120b` | 87.9 | 19.9 | 0.36 | 0.68 | 0.56 | 30.2% | 69.9% | 22 | 61.0% |
| `qwen3.6` | 74.0 | 8.0 | 0.61 | 0.69 | 0.50 | 66.9% | 72.9% | 42 | 66.2% |

### evals-ne

| Evaluator | Mean score | MAD | Pearson | Spearman | Kendall | Recall | Precision | False alarms | Item agreement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-5.6-terra` | 69.8 | 0.0 | - | - | - | - | - | - | - |
| `gemma4-31b` | 94.5 | 24.8 | 0.13 | 0.19 | 0.15 | 12.4% | 91.7% | 2 | 58.2% |
| `gpt-5.6-luna` | 73.4 | 6.9 | 0.76 | 0.67 | 0.36 | 82.5% | 86.9% | 22 | 81.2% |
| `gpt-oss-120b` | 87.2 | 24.2 | 0.28 | 0.43 | 0.33 | 27.1% | 73.8% | 17 | 56.8% |
| `qwen3.6` | 90.1 | 20.4 | 0.32 | 0.40 | 0.29 | 35.6% | 88.7% | 8 | 62.3% |

## 4. Verdict distribution and evidence fill

| Evaluator | Variant | yes | partial | no | Evidence filled |
| --- | --- | ---: | ---: | ---: | ---: |
| `gemma4-31b` | evals | 88.2% | 2.2% | 9.6% | 12.1% |
| `gemma4-31b` | evals-nt | 88.1% | 4.2% | 7.7% | 0.0% |
| `gemma4-31b` | evals-ne | 93.1% | 1.2% | 5.8% | 0.0% |
| `gpt-5.6-luna` | evals | 60.4% | 25.0% | 14.6% | 39.9% |
| `gpt-5.6-luna` | evals-nt | 59.6% | 26.2% | 14.2% | 0.0% |
| `gpt-5.6-luna` | evals-ne | 58.2% | 29.8% | 12.1% | 0.0% |
| `gpt-5.6-terra` | evals | 59.8% | 23.2% | 17.0% | 40.2% |
| `gpt-5.6-terra` | evals-nt | 58.2% | 26.8% | 15.0% | 0.0% |
| `gpt-5.6-terra` | evals-ne | 55.7% | 27.8% | 16.6% | 0.0% |
| `gpt-oss-120b` | evals | 83.6% | 5.4% | 11.0% | 15.7% |
| `gpt-oss-120b` | evals-nt | 78.3% | 14.5% | 7.2% | 0.0% |
| `gpt-oss-120b` | evals-ne | 82.1% | 7.7% | 10.2% | 0.0% |
| `qwen3.6` | evals | 84.1% | 8.3% | 7.6% | 15.9% |
| `qwen3.6` | evals-nt | 61.3% | 21.8% | 17.0% | 0.0% |
| `qwen3.6` | evals-ne | 81.3% | 14.6% | 4.1% | 0.0% |

## 5. Group subtotals, per variant

Out of 20 per group, meaned over the targets.

| Evaluator | Variant | A | B | C | D | E |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `gemma4-31b` | evals | 17.2 | 16.8 | 18.0 | 19.4 | 18.8 |
| `gemma4-31b` | evals-nt | 15.9 | 16.0 | 18.4 | 20.0 | 19.5 |
| `gemma4-31b` | evals-ne | 17.4 | 17.8 | 19.6 | 19.8 | 20.0 |
| `gpt-5.6-luna` | evals | 15.9 | 15.5 | 15.1 | 16.0 | 12.4 |
| `gpt-5.6-luna` | evals-nt | 15.9 | 13.9 | 15.0 | 16.0 | 12.4 |
| `gpt-5.6-luna` | evals-ne | 16.4 | 15.5 | 14.2 | 15.5 | 11.8 |
| `gpt-5.6-terra` | evals | 16.5 | 13.2 | 14.0 | 15.6 | 12.2 |
| `gpt-5.6-terra` | evals-nt | 16.2 | 14.5 | 14.1 | 15.5 | 11.1 |
| `gpt-5.6-terra` | evals-ne | 15.8 | 13.8 | 14.0 | 15.0 | 11.2 |
| `gpt-oss-120b` | evals | 17.2 | 18.1 | 16.9 | 18.2 | 17.9 |
| `gpt-oss-120b` | evals-nt | 18.0 | 16.6 | 18.8 | 18.2 | 16.2 |
| `gpt-oss-120b` | evals-ne | 16.6 | 18.1 | 17.1 | 18.1 | 17.2 |
| `qwen3.6` | evals | 16.2 | 16.8 | 18.4 | 18.8 | 18.8 |
| `qwen3.6` | evals-nt | 14.1 | 16.6 | 14.6 | 14.8 | 13.9 |
| `qwen3.6` | evals-ne | 17.4 | 16.6 | 18.8 | 19.0 | 18.4 |

## 6. Correlation with the old scheme's per-language corpus mean

An independent reference: each language's old-scheme mean over every translator in examples/tr/onde/, which README's provisional position treats as the better-verified of the two old-scheme references. It does not depend on the reference evaluator assumption either.

| Language | pl | ia | ja | kn | ga | ko | ru | hi |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Old corpus mean | 83.7 | 47.2 | 85.6 | 58.2 | 37.8 | 75.9 | 85.2 | 70.4 |

| Evaluator | Variant | Pearson | Spearman | Kendall |
| --- | --- | ---: | ---: | ---: |
| `gemma4-31b` | evals | -0.35 | -0.16 | -0.19 |
| `gemma4-31b` | evals-nt | -0.03 | 0.36 | 0.21 |
| `gemma4-31b` | evals-ne | -0.17 | 0.19 | 0.08 |
| `gpt-5.6-luna` | evals | 0.68 | 0.64 | 0.43 |
| `gpt-5.6-luna` | evals-nt | 0.65 | 0.71 | 0.48 |
| `gpt-5.6-luna` | evals-ne | 0.78 | 0.69 | 0.50 |
| `gpt-5.6-terra` | evals | 0.72 | 0.54 | 0.41 |
| `gpt-5.6-terra` | evals-nt | 0.79 | 0.67 | 0.50 |
| `gpt-5.6-terra` | evals-ne | 0.82 | 0.86 | 0.71 |
| `gpt-oss-120b` | evals | 0.24 | 0.31 | 0.31 |
| `gpt-oss-120b` | evals-nt | 0.38 | 0.68 | 0.48 |
| `gpt-oss-120b` | evals-ne | 0.22 | 0.35 | 0.19 |
| `qwen3.6` | evals | 0.07 | 0.12 | 0.07 |
| `qwen3.6` | evals-nt | 0.67 | 0.48 | 0.29 |
| `qwen3.6` | evals-ne | 0.07 | 0.07 | 0.14 |

## 7. Call time, per variant

| Evaluator | evals | evals-nt | evals-ne |
| --- | ---: | ---: | ---: |
| `gemma4-31b` | 798s | 110s | 382s |
| `gpt-5.6-luna` | 42s | 43s | 39s |
| `gpt-5.6-terra` | 43s | 39s | 34s |
| `gpt-oss-120b` | 160s | 160s | 124s |
| `qwen3.6` | 245s | 23s | 156s |
