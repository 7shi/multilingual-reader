# threshold=10, summary CoT disabled trial

A trial run with summary interval `--threshold 10`, reorganization at `--keep 5`, and summary CoT **disabled** (`--no-think`).

3 translation runs × 3 evaluation runs (median of each run).

## Experimental results

Translation input: [examples/finetuning-fr.txt](../../../examples/finetuning-fr.txt) (43 lines, French podcast)
Target language: Spanish (3 translation runs × 3 evaluation runs, median of each run)

### Score summary

| Model | tr-1 | tr-2 | tr-3 |
|---|:---:|:---:|:---:|
| qwen3.6-27b | 96 | **86** | 94 |
| gemma4-26b | 95 | **99** | 96 |
| gemma4-e4b | 95 | 96 | **84** |

Reference: the reference translation (Gemini 2.5 Pro) scored 97 points (measured in experimental/02)

Individual scores of the 3 evaluation runs for each run:

| Model | run | eval-1 | eval-2 | eval-3 | Median |
|---|:---:|:---:|:---:|:---:|:---:|
| qwen3.6-27b | 1 | 98 | 96 | 95 | **96** |
| qwen3.6-27b | 2 | 90 | 86 | 84 | **86** |
| qwen3.6-27b | 3 | 94 | 92 | 95 | **94** |
| gemma4-26b | 1 | 95 | 94 | 96 | **95** |
| gemma4-26b | 2 | 100 | 97 | 99 | **99** |
| gemma4-26b | 3 | 96 | 95 | 97 | **96** |
| gemma4-e4b | 1 | 92 | 96 | 95 | **95** |
| gemma4-e4b | 2 | 94 | 96 | 98 | **96** |
| gemma4-e4b | 3 | 84 | 82 | 87 | **84** |

### Main issues and observations

**gemma4-26b-2: 99 points (near-perfect)**

All 5 categories were very close to 20 points. eval-1 was a perfect score (100), and eval-2/eval-3 were 97 and 99 with minimal evaluation variance. This is the second-highest score after 20/'s tr-3 (100 points), further demonstrating gemma4-26b's stable, high quality.

**qwen3.6-27b-2: dropped to 86**

Large deductions across multiple items: fluency=16, terminology=16, readability=17. Main issues:

- Grammar errors: `las informaciónes` ("information" is an uncountable noun with no plural), `partías` (incorrect verb conjugation)
- Terminology drift: `afinado` (non-standard translation of fine-tuning; `ajuste fino` is correct), `bachotage` → `aprendizaje de memoria` ("rote learning," lacking the "cramming for an exam" nuance)

All three evaluation scores (90, 86, 84) were consistently low, indicating an actual translation-quality problem (not evaluation variance). Since CoT only applies to the summary, it's not a direct cause of the terminology drift; this appears to be drift from this run's initial glossary accumulation.

**gemma4-e4b-3: dropped to 84**

terminology=14 was consistent across all 3 evaluations (the most reliable issue). Main mistranslations:

- `bachotage` → `atracón` (means "binge eating" or "binge-watching," unrelated to "cramming for an exam")
- `grounding` (NLP/AI context) → mistranslated as an electrical-engineering "grounding/earthing" term

contextual_adaptation=17 (16, 17, 18) also declined. This terminology mistranslation also negatively affected contextual coherence. tr-1/tr-2 (95, 96 points) didn't show this issue, suggesting the mistranslation got locked in through tr-3's initial glossary accumulation.

### Overall assessment

- **gemma4-26b** performed best. All 3 runs scored 95-99, maintaining high quality even with a no-CoT summary. tr-2's 99 points exceeds experimental/02 Phase B's reference level (97 points).
- **qwen3.6-27b** was good (94-96 points) in tr-1/tr-3, but the drop to 86 in tr-2 undermines reliability. The grammar errors show the difficulty of maintaining terminology/style consistency with a no-CoT summary.
- **gemma4-e4b** scored well (95-96 points) in tr-1/tr-2, but dropped to 84 in tr-3. Since the terminology mistranslation was consistent across all 3 evaluations, this reflects an actual translation-quality issue — the risk of glossary mistranslations getting locked in became apparent.
- Since CoT only applies to summary generation and not to translation itself, it's more reasonable to interpret the score gap between 10-nt and 10/ as run-to-run variance (differences in initial glossary accumulation) rather than a definitive effect of CoT presence.
