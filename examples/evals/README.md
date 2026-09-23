# examples/evals/

Evaluations of the reference translations in [examples/](../), the `{topic}-{lang}.txt` files the site is built from. Each translation is evaluated against the text it was translated from: English and Spanish against the French original, German, Japanese and Chinese against the English one.

## Files

| File | Evaluator | Contents |
| --- | --- | --- |
| `jev-{topic}-{src}.jsonl` | TypeSafe Jev (`jev-1.13.0`), one run per language | One record per target language, for the topic's `{src}` original |
| `SCORES-jev.txt` | Jev | Totals out of 100, one decimal, named `{topic}-{src}-{target}` |
| `{topic}-{src}-{target}-{run}.json` | `ollama:qwen3.6`, three runs | The previous evaluator's record; no longer written |
| `SCORES.txt` | qwen3.6 | The median of the three runs, as integers |
| `batch.sh` | Jev | Evaluates and aggregates |

A Jev record names only its target language, so each topic and source has a file of its own, and the source goes into the aggregated name through `trtools agg --jev --prefix {topic}-{src}`.

## Running

```bash
cd examples/evals
bash batch.sh
```

Languages a `jev-*.jsonl` already holds are skipped, so the script resumes after an interruption. It ends by printing the per-language average over the four topics, which is the table in the top-level [README.md](../../README.md).

## History

- **2026-04-27**: The reference translations' evaluations were collected here from an earlier experiment directory, with `batch.sh` to rerun them. Each pair was evaluated three times by `ollama:qwen3.6` with `trtools eval`, and the median was taken. The same day, the pairs were settled as they are now: English and Spanish are translated from French, and German, Japanese and Chinese from English, so each is evaluated against its own source. The file names took the `{topic}-{src}-{target}` form.
- **2026-04-28**: The Spanish, German and Chinese references were replaced with gemma4:26b translations, proofread, and re-evaluated. English (Gemini, reviewed by Claude) and Japanese were kept. Esperanto and Hindi were removed for their low scores.
- **2026-09-23**: Moved to Jev along with the translation corpus in [examples/tr/](../tr/README.md), whose evaluator had been replaced after [experimental/13](../../experimental/13/README.md). The qwen3.6 record is kept beside Jev's rather than replaced.

## Comparing the Two Evaluators

The same 20 translations, unchanged between the two runs.

| Topic | Pair | qwen3.6 | Jev | Difference |
| --- | --- | ---: | ---: | ---: |
| finetuning | en→de | 95 | 93.2 | -1.8 |
| finetuning | en→ja | 99 | 90.4 | -8.6 |
| finetuning | en→zh | 95 | 89.5 | -5.5 |
| finetuning | fr→en | 100 | 91.2 | -8.8 |
| finetuning | fr→es | 97 | 90.7 | -6.3 |
| momentum | en→de | 97 | 89.2 | -7.8 |
| momentum | en→ja | 97 | 83.0 | -14.0 |
| momentum | en→zh | 96 | 92.3 | -3.7 |
| momentum | fr→en | 100 | 95.4 | -4.6 |
| momentum | fr→es | 97 | 90.6 | -6.4 |
| onde | en→de | 97 | 92.5 | -4.5 |
| onde | en→ja | 97 | 90.3 | -6.7 |
| onde | en→zh | 98 | 88.6 | -9.4 |
| onde | fr→en | 96 | 87.5 | -8.5 |
| onde | fr→es | 97 | 93.5 | -3.5 |
| transformer | en→de | 96 | 91.5 | -4.5 |
| transformer | en→ja | 95 | 87.7 | -7.3 |
| transformer | en→zh | 97 | 91.8 | -5.2 |
| transformer | fr→en | 97 | 93.1 | -3.9 |
| transformer | fr→es | 96 | 88.0 | -8.0 |

Averaged over the four topics:

| Language | qwen3.6 | Rank | Jev | Rank |
| --- | ---: | ---: | ---: | ---: |
| English | 98.25 | 1 | 91.80 | 1 |
| German | 96.25 | 5 | 91.60 | 2 |
| Spanish | 96.75 | 3 | 90.70 | 3 |
| Chinese | 96.50 | 4 | 90.55 | 4 |
| Japanese | 97.00 | 2 | 87.85 | 5 |

- **The old scale was at its ceiling.** qwen3.6 put all 20 between 95 and 100, with 9 of them at 97, so it said little about their order. Jev spreads them over 83.0–95.4, lower on every one; the two rank the 20 almost independently (Spearman 0.21). This is the compression at the top that [experimental/13](../../experimental/13/README.md) measured on the corpus, and the numbers are not converted between the scales.
- **English stays first; the rest reorder.** German moves from last to second and Japanese from second to last. Between German, Spanish and Chinese the averages are within about a point on either scale, so their order is not read as meaningful.
- **Fluency is the lowest criterion** for 16 of the 20, as it is across the corpus.
- **momentum en→ja is the one outlier**, 83.0 against 87.7–90.4 for Japanese's other topics, with information completeness at 15.6 of 20, the lowest of any criterion here. Its speaker labels and line correspondence are intact, which rules out the usual cause of that deduction (see [examples/tr/README.md](../tr/README.md)). Reading it line by line against [momentum-en.txt](../momentum-en.txt) turns up one real omission, in the episode's key point, and two smaller departures:
  - **Omission**, [momentum-ja.txt](../momentum-ja.txt) line 60: the generalized measurement "translates the information you want—the momentum—into a different kind of information that's easier to measure, like position", but the Japanese drops both "the momentum" and "like position", leaving only "converts the information you want into other, easier information". Without them, the line no longer ties back to the half-turn experiment just before it.
  - **Addition**, line 15: "I see its position change. Simple." gains "and you know its speed" (速さがわかる).
  - **Changed meaning**, line 37: "You have no idea." becomes "Nowhere." (どこにも。), which reads as the particle being nowhere rather than its position being unknown.

  Jev gives no reasons, so these are not confirmed as what it deducted for, but the omission fits a low information completeness. The reference translation is left as it is: it is the site's source text, and changing it is a separate decision.
