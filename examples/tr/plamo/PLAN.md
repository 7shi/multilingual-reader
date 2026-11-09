# Plan for Evaluating PLaMo 3 Translate

[PLaMo 3 Translate](https://huggingface.co/pfnet/plamo-3-translate-0.8b) (Preferred Networks) is a translation-only model with its own way of use: its chat template skips system messages, reads every user/assistant pair as a source/translation example, and takes the target language, glossary and other options as template variables. `trtools translate`, which translates line by line with injected instructions, cannot drive it, so it is translated by `trtools plamo` instead: the whole text in one request per language, with the target language's whole column of the term TSV as its glossary (see [trtools/README.md](../../../trtools/README.md#plamo)).

The first run, of 0.8B over every corpus language, is kept in [experimental/16](../../../experimental/16/README.md). Outside the supported languages the output mostly came out in another language, so the runs under [plamo/](./) are limited to the supported ones.

## Conditions Shared by Every Run

- **Languages**: `PLAMO_LANGS` in [../common.mk](../common.mk), every language the model card lists as supported except the source English. It includes some languages the corpus lacks (`zh-hant ceb gu jv kk pa uz`). The corpus's `zh` is sent as `zh-hans`.
- **Context**: `llama-server -c 32768 --jinja --no-prefill-assistant`. 32,768 tokens is the model card's training length for input and output combined; going past it is not done, since the model is not known to work there. Splitting the text in two, for a model or server that cannot hold that much, is on hold.
- **Line alignment**: PLaMo is not meant to translate line by line, so dropped, repeated or split lines and runaway repetition are kept as they are, as part of its performance. They are not fixed, retranslated or excluded.
- **Glossary**: the target language's whole column of [terms/onde-en.tsv](../terms/onde-en.tsv). The columns for the languages the corpus lacks were added for PLaMo (`make plamo` in [terms/](../terms/)), translated by gpt-6-luna and proofread.

## Kept Apart from the Other Models

PLaMo's languages differ from the corpus's: put side by side with the other models in [onde/](../onde/), the 22 corpus languages it does not support would count as 0 and pull it far below models it matches on its own languages. So the results under [plamo/](./) are not part of the main comparison in [../README.md](../README.md), and are compared only with each other, on PLaMo's languages, in [README.md](README.md).

## On Hold

Splitting the text in two for a model or server that cannot hold 32,768 tokens, and detecting a stop at the length limit (`finish_reason=length`) in llm7shi.
