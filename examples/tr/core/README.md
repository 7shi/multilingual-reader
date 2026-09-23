# examples/tr/core/

Translates and evaluates the English source text into the core languages (French, Spanish, German, Japanese, Chinese).

## Running

`make` runs translation, evaluation, and aggregation all at once. Translations go to `tr/`, evaluations to `jev-{topic}.jsonl` (one per topic, since a record names only its language), and scores to `SCORES-jev.txt`.

- Translation model: gemma4:26b
- Evaluation model: TypeSafe Jev (`jev-1.13.0`, one run per language)
- Settings: threshold=20, keep=5, no CoT, term-file injection (`../../terms/*-en.{json,tsv}`)
- Existing files are skipped, so it can be resumed partway through

`evals/` and `SCORES.txt` are the previous evaluator's record (qwen3.6, median of three runs). They are no longer written; `make scores` re-aggregates them.

## Translation Quality Overview

The quality trends for each language, based on the evaluation results (`SCORES-jev.txt`) and content review, are as follows.

| Language | finetuning | transformer | momentum | Average |
| --- | ---: | ---: | ---: | ---: |
| Japanese (ja) | 85.2 | 90.2 | 86.1 | 87.17 |
| Chinese (zh) | 92.6 | 86.9 | 78.0 | 85.83 |
| Spanish (es) | 87.1 | 82.6 | 75.7 | 81.80 |
| French (fr) | 92.2 | 86.8 | 77.6 | 85.53 |
| German (de) | 92.2 | 89.5 | 88.6 | 90.10 |

For core languages with abundant training resources, the translations are practical on every topic.

- **Content**: terminology is the most consistently scored criterion, and the explanations carry over accurately.
- **Fluency**: fluency is the lowest criterion on average. The conversational tone comes through, but literal renderings of the English remain.

Reasons for the lower Spanish, French and Chinese scores on the momentum topic:

- Speaker labels (`Luc:`, `Camille:`) drop out, mostly on short lines such as the back-channel "Oh?" or "Sure.", on 23 of 73 lines in Spanish, 24 in French and 9 in Chinese. This breaks the dialogue format, and Jev deducts for it under information completeness, the lowest criterion for all three. The same labels are kept on every line in finetuning, and on all but one line in transformer.
- German (88.6) keeps every label and sits close to its other topics. Its lowest criterion is fluency: literal English calques and anglicisms such as "Pitcher-Hügel" (pitcher's mound), "Peak" (peak) and "neu verdrahten" (a literal translation of "rewire") remain.
