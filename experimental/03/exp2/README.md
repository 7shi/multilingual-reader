# Comparison trial using experimental/02 settings

A trial run using the same settings as [experimental/02](../../02/) (`--summary glossary --no-think`, threshold=10, keep=5), with 3 translation runs × 3 evaluation runs. The purpose is a fair comparison against each trial in experimental/03.

## Experimental results

Translation input: [examples/finetuning-fr.txt](../../../examples/finetuning-fr.txt) (43 lines, French podcast)
Target language: Spanish (3 translation runs × 3 evaluation runs, median of each run)

### Score summary

| Model | tr-1 | tr-2 | tr-3 |
|---|:---:|:---:|:---:|
| qwen3.6-27b | **84** | 96 | 95 |
| gemma4-26b | 96 | **98** | 96 |
| gemma4-e4b | 95 | **83** | 94 |

Reference: the reference translation (Gemini 2.5 Pro) scored 97 points (measured in experimental/02)

Individual scores of the 3 evaluation runs for each run:

| Model | run | eval-1 | eval-2 | eval-3 | Median |
|---|:---:|:---:|:---:|:---:|:---:|
| qwen3.6-27b | 1 | 84 | 80 | 93 | **84** |
| qwen3.6-27b | 2 | 96 | 96 | 96 | **96** |
| qwen3.6-27b | 3 | 95 | 95 | 96 | **95** |
| gemma4-26b | 1 | 97 | 95 | 96 | **96** |
| gemma4-26b | 2 | 97 | 98 | 100 | **98** |
| gemma4-26b | 3 | 96 | 98 | 96 | **96** |
| gemma4-e4b | 1 | 88 | 95 | 96 | **95** |
| gemma4-e4b | 2 | 68 | 83 | 93 | **83** |
| gemma4-e4b | 3 | 83 | 95 | 94 | **94** |

### Main observations

**qwen3.6-27b-1: dropped to 84**

Deductions across multiple categories: readability=16, fluency=15, terminology=17. Since tr-2/tr-3 were stable at 95-96 points, this looks like a temporary collapse due to variance in tr-1's initial glossary accumulation.

**gemma4-e4b-2: dropped to 83**

Includes an eval-1 score of 68 (the same score as experimental/03/20/'s tr-2 plunge); standard deviation was 5.80, the largest of any trial. The main deduction factor was terminology=15 (11, 15, 18 — also high evaluation variance). The same kind of plunge occurred at threshold=15 as at threshold=20, suggesting the probabilistic variance in initial glossary accumulation dominates over differences in threshold value.

**gemma4-26b: stable across all runs**

Scored 96, 98, 96 with no plunges. Matches the level of the other experimental/03 trials, showing stable quality regardless of the setting differences.
