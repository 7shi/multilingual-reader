# threshold=20 trial

A trial run with summary interval `--threshold 20` (default) and reorganization at `--keep 5`.

3 translation runs × 3 evaluation runs (median of each run).

## Verifying KV cache behavior

Verified each model's KV cache effect via the `prompt_eval_duration` in the execution log.

| Model | KV cache | Representative prefill tps |
|---|:---:|---|
| gemma4-26b | **active** | line 2 onward: 992→1379→2174→3641 tps |
| gemma4-e4b | **active** | line 2 onward: 3340→4592→6673→9131 tps |
| qwen3.6-27b | **inactive** | all lines: 200-235 tps (constant) |

The gemma4-series models show a rapid rise in prefill tps from line 2 onward, indicating the KV cache is working. qwen3.6 appears to use internal tags (like `/think`) to switch between think/no-think modes, which slightly changes the token sequence Ollama receives each time, breaking prefix matching and preventing the cache from working. This doesn't affect translation quality, but it does lengthen processing time.

gemma4-26b is a MoE (Mixture of Experts) model with roughly 3B active parameters (A3B), so its generation speed (eval tps) is not much different from gemma4-e4b (both around 49-51 tps). Meanwhile, prefill tps is higher for e4b (since a smaller total parameter count means lower prefill cost). On all three dimensions — KV cache efficiency, generation speed, and translation quality — the gemma4 series pairs well with hybrid mode.

### Cold start right after the summary

When the summary is removed from history right after generation and translation continues, a cold start occurs for just the one line right after. This is because Ollama's previous cache is for the "sequence including the summary," and the prefix no longer matches the sequence with the summary removed.

| Model | Cold start right after the summary | Cache recovery 2 lines later |
|---|---|---|
| gemma4-e4b | 1.24s, 1501 tps | 0.07s, 30001 tps |
| gemma4-26b | (not measured) | (recovered) |
| qwen3.6-27b | 2.06s, 912 tps | 0.23s, 8475 tps |

The cold start occurs for **only 1 line** right after the summary; the cache recovers from there on.

This is an inherent design cost. Keeping the long CoT-generated summary text (1000+ tokens) in history risks pulling the model toward the summary's style and phrasing. Removing it from history isolates the summary's influence from subsequent translations, stabilizing the translation style. The 1-line cold start is an acceptable price for that.

## Experimental results

Translation input: [examples/finetuning-fr.txt](../../../examples/finetuning-fr.txt) (43 lines, French podcast)
Target language: Spanish (3 translation runs × 3 evaluation runs, median of each run)

### Score summary

| Model | tr-1 | tr-2 | tr-3 |
|---|:---:|:---:|:---:|
| qwen3.6-27b | 95 | 94 | **87** |
| gemma4-26b | 96 | 96 | **100** |
| gemma4-e4b | 96 | **68** | 94 |

Reference: the reference translation (Gemini 2.5 Pro) scored 97 points (measured in experimental/02)

Individual scores of the 3 evaluation runs for each run:

| Model | run | eval-1 | eval-2 | eval-3 | Median |
|---|:---:|:---:|:---:|:---:|:---:|
| qwen3.6-27b | 1 | 95 | 96 | 94 | **95** |
| qwen3.6-27b | 2 | 95 | 93 | 94 | **94** |
| qwen3.6-27b | 3 | 87 | 90 | 83 | **87** |
| gemma4-26b | 1 | 95 | 96 | 97 | **96** |
| gemma4-26b | 2 | 97 | 95 | 96 | **96** |
| gemma4-26b | 3 | 100 | 100 | 97 | **100** |
| gemma4-e4b | 1 | 95 | 97 | 96 | **96** |
| gemma4-e4b | 2 | 84 | 68 | 62 | **68** |
| gemma4-e4b | 3 | 93 | 95 | 94 | **94** |

### Main issues and observations

**gemma4-26b-3: 100 points**

Perfect score on all 5 categories. experimental/02 had found "97 points is effectively the ceiling for this evaluator (qwen3.6)," but this run exceeded it. Two of the three evaluations were perfect (eval-1, eval-2), and eval-3 was 97, with very little evaluation variance. The idiomatic localization of `bachoter` was also rated highly.

**gemma4-e4b-2: dropped to 68**

The main cause was two terminology mistranslations:
- `grounding` → `puesta a tierra` (electrical-engineering "grounding"; the correct AI term would be `anclaje` or `vinculación contextual`)
- `bachoter` → `hacer trampas` ("cheating"; the correct meaning is "cramming for an exam")

These jointly dragged down fluency, terminology, and contextual_adaptation. Since tr-1/tr-3 didn't show similar mistranslations, this appears to be a temporary collapse from variance in initial glossary accumulation.

**qwen3.6-27b-3: dropped to 87**

The main cause was `prompt` → `indicio` (Spanish for "clue/trace"). In an AI context, `prompt` should either stay as-is or be `instrucción`/`entrada`; all 3 evaluations flagged this. Since it didn't appear in tr-1/tr-2, the mistranslation appears to have gotten locked in and reinforced through run-3's initial glossary accumulation.

While the glossary method improves terminology consistency, these two cases show the risk that **early mistranslations can get locked in and reinforced**.

### Overall assessment

- **gemma4-26b** was the most stable. Its median across the 3 runs (96, 96, 100) showed the least translation variance. A run exceeded the reference translation's score (97 points), earning it the highest practical rating.
- **qwen3.6-27b** doesn't benefit from the KV cache, so processing time is long, and it also had a terminology-mistranslation-driven plunge in tr-3, leaving reliability concerns.
- **gemma4-e4b** scored well (94-96 points) in tr-1/tr-3, but the plunge in tr-2 (68 points) raises questions about reliability. Results can swing heavily depending on the glossary's initial accumulation.
- Hybrid mode's (CoT summary) positive effect on translation quality is shown by gemma4-26b's 100-point run, while a summary without CoT also carries the risk of locking in early mistranslations — an issue that remains for future work.
