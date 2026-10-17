# examples/tr/core/

Translates and evaluates the English source text into the core languages (French, Spanish, German, Japanese, Chinese).

## Running

`make` runs translation, evaluation, and aggregation all at once. Translations go to `tr/`, evaluations to `jev-{topic}.jsonl` (one per topic, since a record names only its language), and scores to `SCORES-jev.txt`.

- Translation model: gemma4:26b
- Evaluation model: TypeSafe Jev (`jev-1.14.0`, one run per language; `jev-1.13.0/` keeps jev-1.13.0's files, frozen)
- Settings: threshold=20, keep=5, no CoT, term-file injection (`../../terms/*-en.{json,tsv}`)
- Existing files are skipped, so it can be resumed partway through

`evals/` and `SCORES.txt` are the previous evaluator's record (qwen3.6, median of three runs). They are no longer written; `make scores` re-aggregates them.

## Translation Quality Overview

The quality trends for each language, based on the evaluation results (`SCORES-jev.txt`) and content review, are as follows.

| Language | finetuning | transformer | momentum | Average |
| --- | ---: | ---: | ---: | ---: |
| Japanese (ja) | 86.0 | 90.4 | 86.2 | 87.53 |
| Chinese (zh) | 92.4 | 88.0 | 78.1 | 86.17 |
| Spanish (es) | 87.6 | 85.5 | 78.6 | 83.90 |
| French (fr) | 90.8 | 87.0 | 76.2 | 84.67 |
| German (de) | 91.8 | 90.8 | 89.9 | 90.83 |

For core languages with abundant training resources, the translations are practical on every topic.

- **Content**: terminology is the most consistently scored criterion, and the explanations carry over accurately.
- **Fluency**: fluency is the lowest criterion on average. The conversational tone comes through, but literal renderings of the English remain.

Reasons for the lower Spanish, French and Chinese scores on the momentum topic:

- Speaker labels (`Luc:`, `Camille:`) drop out, mostly on short lines such as the back-channel "Oh?" or "Sure.", on 23 of 73 lines in Spanish, 24 in French and 9 in Chinese. This breaks the dialogue format, and Jev deducts for it under information completeness, the lowest criterion for French and, tied with fluency, for Spanish; for Chinese it is a tenth of a point above fluency. The same labels are kept on every line in finetuning, and on all but one line in transformer.
- German (89.9) keeps every label and sits close to its other topics. Its lowest criterion is fluency: literal English calques and anglicisms such as "Pitcher-Hügel" (pitcher's mound), "Peak" (peak) and "neu verdrahten" (a literal translation of "rewire") remain.
