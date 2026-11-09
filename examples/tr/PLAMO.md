# Plan for Evaluating PLaMo 3 Translate

[PLaMo 3 Translate](https://huggingface.co/pfnet/plamo-3-translate-0.8b) (Preferred Networks) is a translation-only model with its own way of use: its chat template skips system messages, reads every user/assistant pair as a source/translation example, and takes the target language, glossary and other options as template variables. `trtools translate`, which translates line by line with injected instructions, cannot drive it, so it is translated by `trtools plamo` instead: the whole text in one request per language, with the target language's whole column of the term TSV as its glossary (see [trtools/README.md](../../trtools/README.md#plamo)).

The first run, of 0.8B over every corpus language, is kept in [experimental/16](../../experimental/16/README.md). Outside the supported languages the output mostly came out in another language, so the runs below are limited to the supported ones.

## Conditions Shared by Every Run

- **Languages**: `PLAMO_LANGS` in [common.mk](common.mk), every language the model card lists as supported except the source English. It includes some languages the corpus lacks (`zh-hant ceb gu jv kk pa uz`). The corpus's `zh` is sent as `zh-hans`.
- **Context**: `llama-server -c 32768 --jinja --no-prefill-assistant`. 32,768 tokens is the model card's training length for input and output combined; going past it is not done, since the model is not known to work there. Splitting the text in two, for a model or server that cannot hold that much, is on hold.
- **Line alignment**: PLaMo is not meant to translate line by line, so dropped, repeated or split lines and runaway repetition are kept as they are, as part of its performance. They are not fixed, retranslated or excluded.
- **Glossary**: the target language's whole column of [terms/onde-en.tsv](terms/onde-en.tsv). The columns for the languages the corpus lacks were added for PLaMo (`make plamo` in [terms/](terms/)), translated by gpt-6-luna and proofread.

## 1. Every Size of PLaMo 3 Translate

Evaluate each size the model is published in (0.8B, 2B, 8B and 31B), each as its own directory under [plamo/](plamo/) like [plamo/plamo-3-translate-0.8b/](plamo/plamo-3-translate-0.8b/). The languages and the translation command are shared through [plamo/common.mk](plamo/common.mk), so each `Makefile` only names its `TRANSLATOR`. Other than that, adding each size follows [ADD_MODEL.md](ADD_MODEL.md).

## 2. Kept Apart from the Other Models

PLaMo's languages differ from the corpus's: put side by side with the other models in [onde/](onde/), the 22 corpus languages it does not support would count as 0 and pull it far below models it matches on its own languages. So the results under [plamo/](plamo/) are not part of the main comparison in [README.md](README.md), and are compared only with each other, on PLaMo's languages, in its own section there ([PLaMo 3 Translate](README.md#plamo-3-translate-plamo)).

## 3. General Models under PLaMo's Conditions

A comparison of PLaMo with the general models in onde/ would mix the model with the method: those translate line by line, with a summary and instructions, while PLaMo translates the whole text at once. To separate the two, translate PLaMo's languages with general models under PLaMo's conditions, as further directories under [plamo/](plamo/) named like their onde/ counterparts, the whole text in one request with the whole glossary column, and compare the results with both PLaMo and the same models' line-by-line results.

- **gpt-6-luna**: as a ceiling. Among the API models it differs little from the top ones on PLaMo's languages, so the cheaper one stands for them.
- **Gemma 4**: as local models with open weights, run with llama.cpp like PLaMo, in every size: the dense E2B, E4B, 12B and 31B (`gemma4-e2b`, `gemma4-e4b`, `gemma4-12b`, `gemma4-31b`), and the MoE 26B-A4B (`gemma4`) for reference. Lining up the dense sizes against PLaMo's shows whether dropped lines and repetition in one request come from PLaMo or from small models in general; the MoE, with few active parameters in a large model, shows whether that depends on the total or the active size.

This needs a whole-text translation path for general models, since `trtools plamo` relies on PLaMo's template variables; its design comes first. The same line-alignment rule as PLaMo's applies to these runs.
