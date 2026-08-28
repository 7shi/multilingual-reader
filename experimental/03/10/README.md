# threshold=10 trial

A trial run with summary interval `--threshold 10`, reorganization at `--keep 5`, and summary CoT **enabled**.

3 translation runs × 3 evaluation runs (median of each run).

## Experimental results

Translation input: [examples/finetuning-fr.txt](../../../examples/finetuning-fr.txt) (43 lines, French podcast)
Target language: Spanish (3 translation runs × 3 evaluation runs, median of each run)

### Score summary

| Model | tr-1 | tr-2 | tr-3 |
|---|:---:|:---:|:---:|
| qwen3.6-27b | 95 | 94 | 95 |
| gemma4-26b | **97** | 94 | **97** |
| gemma4-e4b | 88 | 87 | 92 |

Reference: the reference translation (Gemini 2.5 Pro) scored 97 points (measured in experimental/02)

Individual scores of the 3 evaluation runs for each run:

| Model | run | eval-1 | eval-2 | eval-3 | Median |
|---|:---:|:---:|:---:|:---:|:---:|
| qwen3.6-27b | 1 | 95 | 95 | 100 | **95** |
| qwen3.6-27b | 2 | 94 | 96 | 94 | **94** |
| qwen3.6-27b | 3 | 95 | 93 | 96 | **95** |
| gemma4-26b | 1 | 98 | 97 | 95 | **97** |
| gemma4-26b | 2 | 92 | 94 | 98 | **94** |
| gemma4-26b | 3 | 95 | 100 | 97 | **97** |
| gemma4-e4b | 1 | 94 | 86 | 88 | **88** |
| gemma4-e4b | 2 | 93 | 87 | 87 | **87** |
| gemma4-e4b | 3 | 92 | 92 | 92 | **92** |

### Main issues and observations

**gemma4-26b: stable, consistently high quality**

All 3 runs scored 94-97. This matches the quality level of 20/, showing no degradation from switching to threshold=10. tr-1/tr-3 matched the reference translation's level (97 points). Evaluation variance was also small, indicating high stability.

**qwen3.6-27b: the plunge risk is resolved**

In 20/, tr-3 plunged to 87 points, but with threshold=10 it stabilized at 94-95 points. The plunge in 20/ was caused by the `prompt` → `indicio` mistranslation getting locked into the glossary; increasing summary frequency with threshold=10 appears to have suppressed the fixation/reinforcement of mistranslations.

**gemma4-e4b: consistently low across all runs (87-92 points)**

In 20/, there was a plunge run (tr-2: 68 points), but tr-1/tr-3 scored 94-96 points, quite high. With threshold=10, the plunge disappeared but overall scores dropped. Main causes of deduction:

- **tr-1 (88 points)**: fluency=16. The second-person pronouns `tú` and `vosotros` are mixed, disrupting the natural flow. Also, `sinopsis` (translation of antisèche) skews too much toward "summary," losing the "crib sheet/cheat notes" nuance.
- **tr-2 (87 points)**: terminology=16. Two mistranslations: `grounding` → `conexión a tierra` (electrical-engineering "grounding"), and `bachoter` → `hacer trampas` ("cheating"). Same pattern as 20/'s tr-2, likely due to initial glossary accumulation.
- **tr-3 (92 points)**: terminology=16 (consistent across all 3 evaluations). The `grounding` → `puesta a tierra` mistranslation got locked in. Since fluency and readability improved, the terminology mistranslation was the sole major cause of deduction.

gemma4-e4b continued to show recurring terminology mistranslations (grounding/bachoter patterns) even at threshold=10, indicating it remains susceptible to the influence of initial glossary accumulation.

### Overall assessment

- **gemma4-26b** was the most stable, maintaining high quality in the 94-97 range across all 3 runs, matching threshold=20's results.
- **qwen3.6-27b** had its 20/ plunge resolved by shortening the threshold, stabilizing at 94-95 points.
- **gemma4-e4b** no longer had the plunge (68 points), but overall performance stayed low (87-92 points). Terminology mistranslations occurred across multiple runs, leaving room for improvement in how this model handles the glossary.
- Compared with 20/, threshold=10 is effective at reducing plunge risk, but it didn't resolve gemma4-e4b's low performance, and gemma4-26b's top score (100 points) didn't appear either.
