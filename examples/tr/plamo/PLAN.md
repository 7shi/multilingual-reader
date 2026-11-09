# Plan for Evaluating PLaMo 3 Translate

[PLaMo 3 Translate](https://huggingface.co/pfnet/plamo-3-translate-0.8b) (Preferred Networks) is a translation-only model with its own way of use: its chat template skips system messages, reads every user/assistant pair as a source/translation example, and takes the target language, glossary and other options as template variables. `trtools translate`, which translates line by line with injected instructions, cannot drive it, so it is translated by `trtools plamo` instead: the whole text in one request per language, with the target language's whole column of the term TSV as its glossary (see [trtools/README.md](../../../trtools/README.md#plamo)).

The first run, of 0.8B over every corpus language, is kept in [experimental/16](../../../experimental/16/README.md). Outside the supported languages the output mostly came out in another language, so the runs below are limited to the supported ones.

## Conditions Shared by Every Run

- **Languages**: `PLAMO_LANGS` in [../common.mk](../common.mk), every language the model card lists as supported except the source English. It includes some languages the corpus lacks (`zh-hant ceb gu jv kk pa uz`). The corpus's `zh` is sent as `zh-hans`.
- **Context**: `llama-server -c 32768 --jinja --no-prefill-assistant`. 32,768 tokens is the model card's training length for input and output combined; going past it is not done, since the model is not known to work there. Splitting the text in two, for a model or server that cannot hold that much, is on hold.
- **Line alignment**: PLaMo is not meant to translate line by line, so dropped, repeated or split lines and runaway repetition are kept as they are, as part of its performance. They are not fixed, retranslated or excluded.
- **Glossary**: the target language's whole column of [terms/onde-en.tsv](../terms/onde-en.tsv). The columns for the languages the corpus lacks were added for PLaMo (`make plamo` in [terms/](../terms/)), translated by gpt-6-luna and proofread.

## 1. Every Size of PLaMo 3 Translate

Evaluate each size the model is published in (0.8B, 2B, 8B and 31B), each as its own directory under [plamo/](./) like [plamo-3-translate-0.8b/](plamo-3-translate-0.8b/). The languages and the translation command are shared through [common.mk](common.mk), so each `Makefile` only names its `TRANSLATOR`. Adding each size follows [ADD_PLAMO.md](../ADD_PLAMO.md).

## 2. Kept Apart from the Other Models

PLaMo's languages differ from the corpus's: put side by side with the other models in [onde/](../onde/), the 22 corpus languages it does not support would count as 0 and pull it far below models it matches on its own languages. So the results under [plamo/](./) are not part of the main comparison in [../README.md](../README.md), and are compared only with each other, on PLaMo's languages, in [README.md](README.md).

## 3. General Models under PLaMo's Conditions

A comparison of PLaMo with the general models in onde/ would mix the model with the method: those translate line by line, with a summary and instructions, while PLaMo translates the whole text at once. To separate the two, translate PLaMo's languages with general models under PLaMo's conditions, as further directories under [plamo/](./) named like their onde/ counterparts, the whole text in one request with the whole glossary column, and compare the results with both PLaMo and the same models' line-by-line results.

- **gpt-6-luna**: as a ceiling. Among the API models it differs little from the top ones on PLaMo's languages, so the cheaper one stands for them.
- **Gemma 4**: as local models with open weights, in every size: the dense E2B, E4B, 12B and 31B (`gemma4-e2b`, `gemma4-e4b`, `gemma4-12b`, `gemma4-31b`), and the MoE 26B-A4B (`gemma4`) for reference. Lining up the dense sizes against PLaMo's shows whether dropped lines and repetition in one request come from PLaMo or from small models in general; the MoE, with few active parameters in a large model, shows whether that depends on the total or the active size.

This needs a whole-text translation path for general models, since `trtools plamo` relies on PLaMo's template variables. Its design follows; it is not implemented yet. The same line-alignment rule as PLaMo's applies to these runs.

### Design of the Whole-Text Path

The aim is to change only the method from each model's onde/ run, and to give the model only what PLaMo gets.

- **Command**: a new `trtools whole`, with the same arguments as `trtools plamo` plus `--no-think`. The two share one loop, split out of `plamo.py`: the languages, the output files and skipping of existing ones, the glossary column, the warnings on line count and on a stop, and the save through a temporary file. They differ only in the client and in the license note, which only `plamo` prints. It is not an option of `trtools translate`, whose line-by-line machinery (summary compression, per-line glossary, resuming) has nothing to share with one request.
- **Prompt**: what PLaMo's template variables carry, the source and target languages and the glossary, and nothing else (no summary, no surrounding context).
  - The system message is `trtools translate`'s, without its wording on consistency between lines: translate the following {source} text into {target}, and give only the translation without explanations or commentary.
  - The glossary, the target language's whole column, follows in the system message as `term => translation` lines, the format of `trtools translate`'s glossary messages.
  - The user message is the source text alone, so that the instructions are neither translated nor read as part of the text.
  - Languages are named by `LANG_NAMES`, as in onde/; `zh` is `Chinese`, not PLaMo's `zh-hans`.
  - Line alignment is not asked for, since PLaMo is not asked either. Dropped, repeated or split lines count as for PLaMo.
- **Generation**: the model and thinking setting of the onde/ counterpart (`TRANSLATOR` and `OPTIONS`: `--no-think` for the Gemma 4 sizes, thinking for gpt-6-luna), and the provider's default temperature as in onde/, not PLaMo's 0. The runaway guard is `plamo`'s: output stopped at five times the source's length plus 100 characters or on repetition, with no retry; a stop is warned about and the output saved. The output is only stripped of surrounding whitespace; a preamble or a code fence is warned about and kept, as part of the performance.
- **Running Gemma 4**: on Ollama with the same models as onde/ (the QAT builds for 31B and 12B), since moving to llama.cpp would change the quantization along with the method. Ollama's default context is too short for the whole text and its translation, so the server is run with `OLLAMA_CONTEXT_LENGTH=32768`, the length PLaMo runs with; no code change is needed for it.
- **Directories**: `plamo/<model>/`, named like onde/ (`plamo/gemma4-31b/`), each `Makefile` with the onde/ counterpart's `TRANSLATOR` and `OPTIONS`. [common.mk](common.mk) defines both commands and makes the whole-text one the default; the PLaMo sizes' Makefiles set `TRANSLATE_CMD = $(PLAMO_TRANSLATE)` after the include. The general models join `MODELS` in [Makefile](Makefile).
- **Aggregation**: `generate_compare_rows.py` takes every model in `plamo/Makefile` for a PLaMo size, naming the per-language columns by the size. It is to name them by model and shorten only the PLaMo sizes, and the stats table and chart tell the general models from their onde/ results by the model cell (e.g. `gemma4-31b (whole text)`). The comparison with the same models' line-by-line results is on the 45 corpus languages among PLaMo's; whether it goes in a table or only in the text is decided once the results are in.
