# examples/

The reference texts the reader site is built from, and the work that produces and checks them.

## Files

| File | Contents |
| --- | --- |
| `{topic}-{lang}.txt` | The source of truth: one podcast dialogue per topic, in each language. One utterance per line, `speaker: text` (a full-width colon `：` is also accepted), with the same number of lines in every language. [templates/build.py](../templates/build.py) builds the site's pages from them. |
| `{topic}-summary.jsonl` | The English summary of each topic's English original, a cache that `trtools translate` reads (see [trtools/README.md](../trtools/README.md)). |
| `Makefile` | Generates the `{topic}-summary.jsonl` files with `trtools summary`. Existing summaries are skipped. |

The topics are `finetuning`, `momentum`, `onde` and `transformer`. French is the original language: English and Spanish are translated from French, and German, Japanese and Chinese from English. Which model translated and proofread each language is in the top-level [README.md](../README.md).

## Subdirectories

- [evals/](evals/README.md): evaluations of the reference translations above
- [tr/](tr/README.md): machine translations into many languages, used to update the reference translations and to compare translation models
