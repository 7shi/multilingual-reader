# Inter-Evaluator Comparison Analysis Report

Generated: 2026-04-23 23:33:41

## Executive Summary

- **Scope of analysis**: 716 translation evaluation results
- **Evaluators**: gemini-2.5-flash, gpt-oss-20b, gpt-oss-120b, qwen3.6, gemma-4-31b
- **Migration decision**: ❌ Migration not viable

### Main Conclusion

Migrating from Gemini-2.5-flash to gpt-oss-120b **cannot be recommended**.
The difference in evaluation tendencies is too large, so a different evaluation approach should be considered.

### Key Metrics

| Metric | Value | Threshold | Verdict |
|------|-----|------|------|
| Spearman rank correlation coefficient | 0.784 | ≥0.85 (pass), ≥0.70 (conditional) | ⚠️ |
| Top-10% model agreement rate | 37.2% | ≥75% (pass), ≥60% (conditional) | ❌ |
| Agreement rate within ±10 points | 55.0% | ≥70% (pass), ≥60% (conditional) | ❌ |
| Maximum bias by model family | 25.4 points | ≤15 points (easily correctable) | ⚠️ |

## Basic Statistics

### Basic Statistics per Evaluator

| Evaluator | Mean | Median | Std. dev. | Min | Max | Q25 | Q75 |
|--------|------|--------|----------|--------|--------|-----|-----|
| gemini-2.5-flash | 69.35 | 75.00 | 22.97 | 0 | 100 | 57.00 | 88.00 |
| gpt-oss-20b | 78.00 | 83.00 | 16.09 | 0 | 92 | 76.00 | 87.00 |
| gpt-oss-120b | 78.61 | 84.00 | 16.90 | 0 | 92 | 76.00 | 88.00 |
| qwen3.6 | 66.92 | 74.00 | 25.98 | 0 | 98 | 53.00 | 89.00 |
| gemma-4-31b | 76.28 | 83.00 | 24.30 | 0 | 100 | 68.00 | 95.00 |

### Distribution by Score Range

| Evaluator | 0-20 | 21-40 | 41-60 | 61-80 | 81-100 |
|--------|--------|---------|---------|---------|----------|
| gemini-2.5-flash | 45 | 36 | 129 | 214 | 292 |
| gpt-oss-20b | 15 | 21 | 29 | 196 | 455 |
| gpt-oss-120b | 17 | 23 | 18 | 207 | 451 |
| qwen3.6 | 53 | 80 | 109 | 184 | 290 |
| gemma-4-31b | 39 | 26 | 64 | 197 | 390 |

### Distribution in the High-Score Range (95 and above)

| Evaluator | 95+ | 96+ | 97+ | 98+ | 99+ | 100 |
|--------|----------|----------|----------|----------|----------|-------|
| gemini-2.5-flash | 48 | 38 | 24 | 11 | 5 | 2 |
| gpt-oss-20b | 0 | 0 | 0 | 0 | 0 | 0 |
| gpt-oss-120b | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3.6 | 58 | 28 | 8 | 2 | 0 | 0 |
| gemma-4-31b | 195 | 162 | 132 | 90 | 37 | 13 |

## Correlation Analysis

### Correlation Coefficients Between Evaluators

| Pair | Common entries | Pearson r | p-value | Spearman ρ | p-value |
|------|-----------|----------|-----|-------------|-----|
| gemini25flash_vs_gptoss20b | 716 | 0.621 | 1.94e-77 | 0.699 | 2.87e-106 |
| gemini25flash_vs_gptoss120b | 716 | 0.683 | 1.90e-99 | 0.784 | 4.36e-150 |
| gemini25flash_vs_qwen36 | 716 | 0.824 | 2.23e-178 | 0.835 | 1.32e-187 |
| gemini25flash_vs_gemma431b | 716 | 0.842 | 2.31e-193 | 0.853 | 3.24e-204 |
| gptoss20b_vs_gptoss120b | 716 | 0.901 | 4.33e-261 | 0.742 | 2.66e-126 |
| gptoss20b_vs_qwen36 | 716 | 0.757 | 4.87e-134 | 0.717 | 8.78e-114 |
| gptoss20b_vs_gemma431b | 716 | 0.835 | 3.02e-187 | 0.753 | 4.54e-132 |
| gptoss120b_vs_qwen36 | 716 | 0.804 | 3.42e-163 | 0.819 | 1.99e-174 |
| gptoss120b_vs_gemma431b | 716 | 0.882 | 3.24e-235 | 0.837 | 8.93e-189 |
| qwen36_vs_gemma431b | 716 | 0.895 | 6.23e-253 | 0.877 | 1.45e-229 |

### Interpretation of the Correlation Coefficients

- **gpt-oss-20b vs gpt-oss-120b**: a very high correlation (ρ≈0.91), with nearly identical evaluation tendencies
- **gemini vs gpt-oss series**: a moderate correlation (ρ≈0.67), indicating a systematic difference

## Agreement Analysis

### Agreement Metrics Between Evaluators

| Pair | MAE | RMSE | Within ±5 | Within ±10 | Top-10% agreement | Mean diff. | Std. dev. |
|------|-----|------|----------|-----------|---------------|--------|----------|
| gemini25flash_vs_gptoss20b | 14.15 | 20.05 | 32.3% | 54.6% | 21.3% | -8.65 | 18.10 |
| gemini25flash_vs_gptoss120b | 13.54 | 19.19 | 34.6% | 55.0% | 37.2% | -9.26 | 16.82 |
| gemini25flash_vs_qwen36 | 9.57 | 14.99 | 45.7% | 68.9% | 49.1% | +2.43 | 14.80 |
| gemini25flash_vs_gemma431b | 10.64 | 15.04 | 35.8% | 61.5% | 49.3% | -6.93 | 13.36 |
| gptoss20b_vs_gptoss120b | 4.87 | 7.40 | 67.5% | 89.9% | 26.6% | -0.61 | 7.38 |
| gptoss20b_vs_qwen36 | 15.23 | 20.57 | 28.5% | 50.3% | 20.0% | +11.08 | 17.35 |
| gptoss20b_vs_gemma431b | 10.36 | 14.12 | 30.2% | 64.0% | 20.2% | +1.72 | 14.02 |
| gptoss120b_vs_qwen36 | 14.41 | 19.77 | 33.4% | 53.6% | 40.7% | +11.69 | 15.96 |
| gptoss120b_vs_gemma431b | 9.35 | 12.54 | 33.1% | 70.3% | 36.9% | +2.33 | 12.33 |
| qwen36_vs_gemma431b | 11.17 | 14.91 | 34.9% | 56.8% | 55.1% | -9.36 | 11.62 |

## Systematic Bias Analysis

### Bias by Model Family

| Model family | Gemini mean | GPT-OSS-120B mean | Diff. (Gemini-GPT120B) |
|-----------------|-----------|-----------------|---------------------|
| command-r7b | 47.71 | 73.08 | -25.37 |
| gemma2 | 63.96 | 80.04 | -16.08 |
| ministral-3 | 56.74 | 71.93 | -15.19 |
| mixtral | 57.42 | 71.50 | -14.08 |
| llama4-scout | 61.12 | 74.67 | -13.54 |
| gemma3n-e4b | 68.83 | 82.25 | -13.42 |
| aya-expanse | 69.92 | 83.10 | -13.19 |
| command-r | 71.00 | 83.12 | -12.12 |
| phi4 | 76.67 | 84.92 | -8.25 |
| gemma3 | 72.67 | 79.83 | -7.17 |
| qwen3 | 70.15 | 76.71 | -6.56 |
| llama3.3 | 81.88 | 83.67 | -1.79 |
| mistral-small3.2 | 84.38 | 85.83 | -1.46 |
| gpt-oss | 90.35 | 89.35 | +1.00 |

### Effect of Reasoning Level

| Reasoning level | Gemini mean | GPT-OSS-120B mean | Diff. |
|-----------|-----------|-----------------|------|
| 0 | 78.75 | 85.79 | -7.04 |
| 1 | 55.88 | 70.54 | -14.67 |
| 2 | 69.42 | 80.21 | -10.79 |
| 3 | 61.17 | 77.62 | -16.46 |
| 4 | 53.62 | 71.00 | -17.38 |
| tr4 | 76.49 | 79.13 | -2.64 |
| tr5 | 66.52 | 73.87 | -7.35 |
| tr6 | 66.75 | 75.95 | -9.20 |

### Effect of Temperature Setting

| Temperature | Gemini mean | GPT-OSS-120B mean | Diff. |
|------|-----------|-----------------|------|
| 05 | 69.95 | 78.32 | -8.37 |
| 10 | 70.29 | 78.31 | -8.02 |
| 15 | 61.42 | 78.00 | -16.58 |
| 20 | 71.43 | 79.79 | -8.36 |
| 25 | 59.00 | 75.25 | -16.25 |

## Details of Problem Cases

### Top 30 Cases with the Largest Discrepancy

| Rank | Model name | Gemini score | GPT-OSS-120B score | Diff. |
|------|----------|-------------|-------------------|------|
| 1 | qwen3-30b-tr4-nt-05 | 93 | 0 | +93 |
| 2 | qwen3-30b-tr6-nt-10 | 91 | 0 | +91 |
| 3 | qwen3-30b-tr4-nt-10 | 84 | 0 | +84 |
| 4 | qwen3-30b-tr6-nt-05 | 82 | 0 | +82 |
| 5 | qwen3-30b-tr5-nt-20 | 81 | 0 | +81 |
| 6 | qwen3-30b-tr6-nt-20 | 80 | 0 | +80 |
| 7 | qwen3-30b-tr4-nt-20 | 70 | 0 | +70 |
| 8 | phi4-1-05 | 8 | 72 | +64 |
| 9 | qwen3-30b-tr5-nt-10 | 63 | 0 | +63 |
| 10 | qwen3-30b-tr5-nt-05 | 63 | 0 | +63 |
| 11 | command-r-35b-1-20 | 10 | 67 | +57 |
| 12 | gemma3-4b-tr4-05 | 25 | 75 | +50 |
| 13 | ministral-3-3b-2-20 | 13 | 62 | +49 |
| 14 | gemma3n-e4b-1 | 17 | 66 | +49 |
| 15 | ministral-3-3b-2-10 | 20 | 69 | +49 |
| 16 | aya-expanse-8b-4 | 20 | 67 | +47 |
| 17 | qwen3-32b-1-nt-20 | 19 | 66 | +47 |
| 18 | command-r7b-tr6-10 | 28 | 75 | +47 |
| 19 | qwen3-4b-tr5-nt-20 | 5 | 50 | +45 |
| 20 | ministral-3-3b-tr5-20 | 34 | 78 | +44 |
| 21 | phi4-1-10 | 15 | 59 | +44 |
| 22 | ministral-3-3b-2-05 | 25 | 68 | +43 |
| 23 | ministral-3-8b-tr5-05 | 40 | 83 | +43 |
| 24 | mixtral-8x7b-3 | 23 | 66 | +43 |
| 25 | aya-expanse-8b-3 | 36 | 78 | +42 |
| 26 | mixtral-8x7b-1-10 | 16 | 58 | +42 |
| 27 | command-r7b-2-05 | 31 | 72 | +41 |
| 28 | command-r7b-1-10 | 23 | 64 | +41 |
| 29 | gemma2-9b-1 | 30 | 71 | +41 |
| 30 | command-r7b-tr6-20 | 25 | 65 | +40 |

### Zero-Point Evaluation Cases

| Model name | Evaluator |
|----------|--------|
| qwen3-30b-tr6-10 | gemini-2.5-flash |
| qwen3-30b-tr6-20 | gemini-2.5-flash |
| qwen3-30b-tr4-nt-05 | gpt-oss-20b |
| qwen3-30b-tr4-nt-10 | gpt-oss-20b |
| qwen3-30b-tr4-nt-20 | gpt-oss-20b |
| qwen3-30b-tr5-nt-05 | gpt-oss-20b |
| qwen3-30b-tr5-nt-10 | gpt-oss-20b |
| qwen3-30b-tr5-nt-20 | gpt-oss-20b |
| qwen3-30b-tr6-nt-05 | gpt-oss-20b |
| qwen3-30b-tr6-nt-10 | gpt-oss-20b |
| qwen3-30b-tr6-nt-20 | gpt-oss-20b |
| qwen3-30b-tr4-nt-05 | gpt-oss-120b |
| qwen3-30b-tr4-nt-10 | gpt-oss-120b |
| qwen3-30b-tr4-nt-20 | gpt-oss-120b |
| qwen3-30b-tr5-nt-05 | gpt-oss-120b |
| qwen3-30b-tr5-nt-10 | gpt-oss-120b |
| qwen3-30b-tr5-nt-20 | gpt-oss-120b |
| qwen3-30b-tr6-nt-05 | gpt-oss-120b |
| qwen3-30b-tr6-nt-10 | gpt-oss-120b |
| qwen3-30b-tr6-nt-20 | gpt-oss-120b |
| ministral-3-14b-4 | qwen3.6 |
| ministral-3-3b-1 | qwen3.6 |
| gemma3-12b-1-05 | qwen3.6 |
| qwen3-30b-tr4-nt-05 | qwen3.6 |
| qwen3-30b-tr4-nt-10 | qwen3.6 |
| qwen3-30b-tr4-nt-20 | qwen3.6 |
| mixtral-8x7b-tr5-05 | qwen3.6 |
| mixtral-8x7b-tr5-10 | qwen3.6 |
| qwen3-30b-tr5-10 | qwen3.6 |
| qwen3-30b-tr5-nt-05 | qwen3.6 |
| qwen3-30b-tr5-nt-10 | qwen3.6 |
| qwen3-30b-tr5-nt-20 | qwen3.6 |
| qwen3-30b-tr6-05 | qwen3.6 |
| qwen3-30b-tr6-20 | qwen3.6 |
| qwen3-30b-tr6-nt-05 | qwen3.6 |
| qwen3-30b-tr6-nt-10 | qwen3.6 |
| qwen3-30b-tr6-nt-20 | qwen3.6 |
| ministral-3-14b-4 | gemma-4-31b |
| ministral-3-3b-1 | gemma-4-31b |
| ministral-3-8b-1 | gemma-4-31b |
| gemma3-12b-1-05 | gemma-4-31b |
| gemma3-12b-1-10 | gemma-4-31b |
| gemma3-12b-1-20 | gemma-4-31b |
| ministral-3-3b-1-05 | gemma-4-31b |
| ministral-3-3b-1-10 | gemma-4-31b |
| ministral-3-3b-1-20 | gemma-4-31b |
| qwen3-30b-tr4-nt-05 | gemma-4-31b |
| qwen3-30b-tr4-nt-10 | gemma-4-31b |
| qwen3-30b-tr4-nt-20 | gemma-4-31b |
| mixtral-8x7b-tr5-10 | gemma-4-31b |
| qwen3-30b-tr5-05 | gemma-4-31b |
| qwen3-30b-tr5-10 | gemma-4-31b |
| qwen3-30b-tr5-20 | gemma-4-31b |
| qwen3-30b-tr5-nt-05 | gemma-4-31b |
| qwen3-30b-tr5-nt-10 | gemma-4-31b |
| qwen3-30b-tr5-nt-20 | gemma-4-31b |
| mixtral-8x7b-tr6-20 | gemma-4-31b |
| qwen3-30b-tr6-05 | gemma-4-31b |
| qwen3-30b-tr6-10 | gemma-4-31b |
| qwen3-30b-tr6-20 | gemma-4-31b |
| qwen3-30b-tr6-nt-10 | gemma-4-31b |
| qwen3-30b-tr6-nt-20 | gemma-4-31b |

**Note**: it is particularly notable that the qwen3-30b-nt series receives zero-point evaluations from the gpt-oss series.

### Reversal Cases (opposite evaluations)

| Model name | Gemini score | GPT-OSS-120B score | Diff. |
|----------|-------------|-------------------|------|
| qwen3-30b-tr6-nt-05 | 82 | 0 | +82 |
| qwen3-4b-1-nt-05 | 50 | 81 | -31 |
| qwen3-30b-tr5-nt-20 | 81 | 0 | +81 |
| qwen3-30b-tr6-nt-20 | 80 | 0 | +80 |
| qwen3-30b-tr4-nt-10 | 84 | 0 | +84 |
| ministral-3-3b-tr6-20 | 49 | 85 | -36 |
| aya-expanse-8b-tr6-05 | 41 | 80 | -39 |
| qwen3-30b-tr4-nt-05 | 93 | 0 | +93 |
| ministral-3-8b-tr5-05 | 40 | 83 | -43 |
| ministral-3-14b-1 | 50 | 80 | -30 |
| gemma3-4b-tr6-20 | 48 | 85 | -37 |
| mixtral-8x7b-0-05 | 48 | 81 | -33 |
| qwen3-30b-tr6-nt-10 | 91 | 0 | +91 |
| aya-expanse-8b-1 | 45 | 83 | -38 |
| gemma2-9b-tr6-05 | 48 | 80 | -32 |
| qwen3-4b-3 | 50 | 83 | -33 |
| qwen3-4b-1-t-10 | 49 | 80 | -31 |
| qwen3-4b-tr4-20 | 42 | 81 | -39 |
| ministral-3-3b-tr5-10 | 48 | 80 | -32 |

## Migration Decision

### Verdict: **❌ Migration not viable**

### Comparison Against the Decision Criteria

- ⚠️ Spearman rank correlation coefficient: 0.784 (in the 0.70-0.85 range)
- ❌ Top-10% agreement rate: 0.372 < 0.60 (fail)
- ❌ Agreement rate within ±10 points: 0.550 < 0.60 (fail)
- ⚠️ Maximum bias by model family: 25.4 points (correction needed)

### Recommendations

gpt-oss-120b cannot be recommended as a replacement for Gemini-2.5-flash.

**Alternatives**:
1. Try a larger-scale gpt-oss model (if available)
2. Use the average of multiple evaluators (gpt-oss-20b, gpt-oss-120b)
3. Continue using Gemini-2.5-flash and pursue cost optimization through other means

## Detailed Data

- Statistical data: [stats.json](stats.json)

---

Generated: 2026-04-23T23:33:28.616692
