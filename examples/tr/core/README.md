# examples/tr/core/

Translates and evaluates the English source text into the core languages (French, Spanish, German, Japanese, Chinese).

## Running

`make` runs translation, evaluation, and aggregation all at once. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemma4:26b
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term-file injection (`../../terms/*-en.{json,tsv}`)
- Existing files are skipped, so it can be resumed partway through

## Translation Quality Overview

The quality trends for each language, based on the evaluation results (`SCORES.txt`) and content review, are as follows.

| Language | finetuning | transformer | momentum | Average |
| --- | ---: | ---: | ---: | ---: |
| Japanese (ja) | 95 | 97 | 95 | 95.67 |
| Chinese (zh) | 95 | 97 | 96 | 96.00 |
| Spanish (es) | 96 | 97 | 93 | 95.33 |
| French (fr) | 96 | 100 | 82 | 92.67 |
| German (de) | 96 | 99 | 88 | 94.33 |

For core languages with abundant training resources, stable, high-quality translations are produced.

- **Contextual adaptation**: perfectly reproduces the podcast's characteristic "casual, easy-to-follow conversational tone".
- **Native-level fluency**: back-channel responses and sentence flow feel natural, with almost none of the awkwardness typical of translations ("translationese").

Reasons for the lower French and German scores on the momentum topic:

- German (88): content accuracy and logical flow are perfect, but literal English calques and anglicisms occasionally appear, such as "Pitcher-Hügel" (pitcher's mound) or "Peak" (peak) or "neu verdrahten" (a literal translation of "rewire"), leading to a minor deduction in the "fluency" category from a native speaker's perspective. There's no practical issue.
- French (82): the explanations of physics terminology and concepts are accurate, but a structural flaw occurs frequently where speaker labels (`Luc:`, `Camille:`, etc.) drop out from short back-channel responses (e.g. "Oh ?", "D'accord"), breaking the dialogue format and making it hard to read — this drew a large deduction. Minor grammar mistakes such as "Son nature" (should be "Sa nature") and some remaining awkward literal-translation phrasing also contributed.
