# Inter-Evaluator Comparison Analysis Tools

This directory contains tools for comparing and analyzing the evaluation results of three translation evaluators (Gemini-2.5-flash, gpt-oss-20b, and gpt-oss-120b).

## 📁 File List

### Execution Scripts (4)

#### 1. `compare_evaluators.py`
**Statistical analysis script**

**Functionality**:
- Reads the SCORES.txt files of the three evaluators
- Computes basic statistics (mean, median, standard deviation)
- Correlation analysis (Pearson, Spearman rank correlation)
- Agreement analysis (MAE, RMSE, agreement rate within ±5/10 points)
- Detects systematic bias by model family, reasoning level, and temperature
- Extracts problem cases (top 30 discrepancies, zero-point evaluations, reversal cases)
- Automatically runs the migration decision

**Input**:
- `../gemini-2.5-flash/SCORES.txt` (716 entries)
- `../gpt-oss-20b/SCORES.txt` (716 entries)
- `../gpt-oss-120b/SCORES.txt` (716 entries)

**Output**:
- `stats.json` - Detailed statistical data (JSON format)

**How to run**:
```bash
cd evaluator_comparison
uv run compare_evaluators.py
```

#### 2. `generate_evaluator_report.py`
**Report generation script**

**Functionality**:
- Generates a Markdown report from stats.json
- Includes an executive summary, detailed statistics, migration decision, and recommendations

**Output**:
- `REPORT.md` - Comprehensive analysis report (244 lines, 13 sections)

**How to run**:
```bash
uv run generate_evaluator_report.py
```

#### 3. `compute_euclidean_distances.py`
**Distance matrix generation script**

**Functionality**:
- Reads the SCORES.txt files of the three evaluators
- Computes the Euclidean distance and per-dimension RMSE for each evaluator pair
- Generates `DISTANCES.md` as a lower-triangular matrix with the upper triangle left blank

**Output**:
- `DISTANCES.md` - Euclidean distance & RMSE matrix

**How to run**:
```bash
uv run compute_euclidean_distances.py
```

#### 4. `analyze_eval_variance.py`
**Evaluation variance analysis script**

**Functionality**:
- Quantifies the variance across three evaluation runs for each evaluator
- Computes the average range, sigma statistics, and variance by criterion

**How to run**:
```bash
cd evaluator_comparison
python analyze_eval_variance.py [evaluator ID ...]
# Example: python analyze_eval_variance.py gpt-oss-120b gemma-4-31b gemini-2.5-flash
```

### Auto-Generated Data

#### 3. `stats.json`
**Detailed statistical data (JSON format)**

**Contents**:
- Metadata (716 entries, 3 evaluators, generation timestamp)
- Basic statistics (mean, median, standard deviation, and score-range distribution for each evaluator)
- Correlation analysis (Pearson r, Spearman ρ, p-values)
- Agreement metrics (MAE, RMSE, agreement rate within ±5/10 points, top-10% agreement rate)
- Systematic bias (by model family, reasoning level, temperature)
- Problem cases (top 30 discrepancies, list of zero-point evaluations, reversal cases)
- Migration decision result (verdict, score, reasoning)

**Size**: approx. 50KB

**Purpose**:
- Source data for report generation
- Raw data for detailed analysis

#### 4. `REPORT.md`
**Comprehensive analysis report (auto-generated)**

- Automatically generated from `stats.json` by `generate_evaluator_report.py`
- Includes an executive summary, basic statistics, correlation analysis, agreement analysis, systematic bias, problem cases, and migration decision

For the background on evaluator selection, see [memo/evaluators.md](../memo/evaluators.md).

## 🚀 Execution Steps

### One-Time Setup

```bash
# Move to the directory
cd experimental/01/evaluator_comparison

# Install dependencies
uv add numpy scipy
```

### Running the Full Analysis

```bash
# 1. Statistical analysis
uv run compare_evaluators.py

# 2. Report generation
uv run generate_evaluator_report.py
```

### Checking the Results

```bash
# Main report
cat REPORT.md

# Statistical data
jq '.' stats.json
```

## 📊 Final Results

### Conclusion of Evaluator Selection

**qwen3.6 was adopted as the official evaluator (used on its own)**.

| Evaluator | Conclusion |
|--------|------|
| **qwen3.6** | **Adopted as the official evaluator. Ranks all 716 entries by median** |
| gemma-4-31b | Unnecessary even as a first-pass filter. Discontinued |
| gpt-oss-120b | Exhibits a ceiling effect. Discontinued |
| gemini-2.5-flash | Unstable. Discontinued |

### Score Distribution by Evaluator (at the time qwen3.6 was adopted)

| Metric | GPT-OSS 120B | gemma-4-31b | qwen3.6 |
|------|-------------|-------------|---------|
| Mean | 78.61 | 76.28 | 66.92 |
| Standard deviation | 16.90 | 24.30 | 25.98 |
| Highest score | 92 | 100 | 98 |
| 90+ | 0% | 37.6% | 23.7% |
| 95+ | 0% | 27.2% | 8.1% |
| 100 | 0 | 13 | 0 |

### Characteristics of Each Evaluator

| Evaluator | Strength | Weakness |
|--------|------|------|
| gemma-4-31b | Reliably detects broken text | Misses mistranslated/untranslated proper nouns and terminology errors |
| gpt-oss-120b | Moderate content checking | Cannot disable CoT (→ see "Characteristics and usage policy for GPT-OSS 120B" in [memo/README.md](../memo/README.md)) |
| gemini-2.5-flash | High detection power for content errors | Evaluations of the same translation vary greatly across 3 runs |
| qwen3.6 | Logical defect identification through CoT | Average range of 14.11 points (largest), but mostly isolated outliers that don't affect the median |

### Stability and Accuracy

| Evaluator | Stability | Accuracy |
|--------|:------:|:----:|
| gemma-4-31b | ◎ | △ (misses content errors) |
| GPT-OSS 120B | ○ | △ (ceiling effect, MoE judgment ability) |
| gemini-2.5-flash | ✕ | ○ (high detection power for content errors) |

### Highest-Score Ranking by Model (qwen3.6, mid-to-large models)

| Rank | Model | Highest score | Best setting | Notes |
|--------|--------|------:|---------|------|
| 1 | gemma3-27b | 98 | setting 0 | Also 97 on tr4/tr5 — very stable |
| 1 | gpt-oss-120b | 98 | setting 0 | 96 on multiple settings — most stable |
| 3 | aya-expanse-32b | 97 | tr4 | 95 on setting 0 |
| 4 | command-r-35b | 96 | tr4 | 93 on setting 0 |
| 4 | ministral-3-8b | 96 | setting 0 | 95 on setting 2 |
| 4 | mistral-small3.2 | 96 | tr4 | 94-95 on multiple settings — stable |
| 4 | qwen3-30b | 96 | setting 1, 1-nt | tr series (unstructured) all score 0 |
| 4 | qwen3-32b | 96 | tr4 | 95 on setting 3-nt/4 |
| 9 | gpt-oss-20b | 95 | settings 1,4 | Stable on multiple settings |
| 9 | gemma3-12b | 95 | setting 0 | Collapses on setting 1 (11 points) |
| 9 | llama3.3 | 95 | setting 0, tr4 | 94 on tr6 |
| 9 | llama4-scout | 95 | setting 0 | 94 on tr5, low from setting 2 onward |
| 9 | ministral-3-14b | 95 | setting 0, tr5 | Unstable from setting 1 onward |
| 9 | qwen3-14b | 95 | settings 4, 3 | Large variance across settings |

### Score Statistics by Setting Type

| Setting | Count | Median | Highest | Assessment |
|------|-----:|------:|-----:|------|
| Setting 0 (tr0) | 123 | 83.0 | 98 | ◎ Most stable as the basic setting |
| Setting 2-nt | 18 | 83.5 | 95 | ◎ |
| Setting 0-nt | 23 | 78.0 | 95 | ○ |
| tr4 | 96 | 78.5 | 97 | ○ High scores for top-tier models |
| Setting 2 | 98 | 77.0 | 96 | ○ |
| tr5 | 72 | 75.0 | 97 | △ High variance |
| tr6 | 72 | 71.5 | 96 | △ High variance |
| Setting 1 (structured with reasoning) | 98 | 59.0 | 96 | ✗ Counterproductive for most models |

For the background of the analysis, see [memo/evaluators.md](../memo/evaluators.md).

## 🔧 Technical Specifications

### Dependencies
- `numpy`: numerical computation, statistical processing
- `scipy`: correlation coefficient computation (stats.pearsonr, stats.spearmanr)

### Data Format

#### SCORES.txt format
```
aya-expanse-8b-0-05: 88
aya-expanse-8b-0-10: 70
...
```

#### stats.json format
```json
{
  "metadata": {
    "num_entries": 716,
    "evaluators": ["gemini-2.5-flash", "gpt-oss-20b", "gpt-oss-120b"],
    "generated_at": "2026-01-07 15:21:16"
  },
  "basic_stats": { ... },
  "correlations": { ... },
  "agreement": { ... },
  "systematic_bias": { ... },
  "problem_cases": { ... },
  "migration_decision": { ... }
}
```

## 📚 Related Documents

- [../README.md](../README.md) - Overview of the whole experiment
- [REPORT.md](REPORT.md) - Comprehensive analysis report
- [stats.json](stats.json) - Detailed statistical data

## Troubleshooting

### Error: ModuleNotFoundError
```bash
# Solution: install dependencies
uv add numpy scipy
```

### Error: FileNotFoundError (SCORES.txt)
```bash
# Solution: run from the correct directory
cd experimental/01/evaluator_comparison
uv run compare_evaluators.py
```
