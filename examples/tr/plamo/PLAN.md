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

This needs a whole-text translation path for general models, since `trtools plamo` relies on PLaMo's template variables. Its design follows; it is implemented as `trtools whole`. The same line-alignment rule as PLaMo's applies to these runs.

### Design of the Whole-Text Path

The aim is to change only the method from each model's onde/ run, and to give the model only what PLaMo gets.

- **Command**: a new `trtools whole`, with the same arguments as `trtools plamo` plus `--no-think`. The two share one loop, split out of `plamo.py`: the languages, the output files and skipping of existing ones, the glossary column, the warnings on line count and on a stop, and the save through a temporary file. They differ only in the client and in the license note, which only `plamo` prints. The shared loop also shows and records each language's usage, and shows a status line per language, both as `trtools translate` does. It is not an option of `trtools translate`, whose line-by-line machinery (summary compression, per-line glossary, resuming) has nothing to share with one request.
- **Prompt**: what PLaMo's template variables carry, the source and target languages and the glossary, and nothing else (no summary, no surrounding context).
  - The system message is `trtools translate`'s, without its wording on consistency between lines: translate the following {source} text into {target}, and give only the translation without explanations or commentary.
  - The glossary, the target language's whole column, follows in the system message as `term => translation` lines, the format of `trtools translate`'s glossary messages.
  - The user message is the source text alone, so that the instructions are neither translated nor read as part of the text.
  - Languages are named by `LANG_NAMES`, as in onde/; `zh` is `Chinese`, not PLaMo's `zh-hans`.
  - Line alignment is not asked for, since PLaMo is not asked either. Dropped, repeated or split lines count as for PLaMo.
- **Generation**: the model and thinking setting of the onde/ counterpart (`TRANSLATOR` and `OPTIONS`: `--no-think` for the Gemma 4 sizes, thinking for gpt-6-luna), and the provider's default temperature as in onde/, not PLaMo's 0. The runaway guard is `plamo`'s: output stopped at five times the source's length plus 100 characters or on repetition, with no retry; a stop is warned about and the output saved. The output is only stripped of surrounding whitespace and, when the source has no blank lines, of blank lines: gpt-6-luna set every line apart with one in some languages and not in others, which is layout rather than translation (PLaMo's outputs have none). A preamble or a code fence is warned about and kept, as part of the performance.
- **Running Gemma 4**: on Ollama with the same models as onde/ (the QAT builds for 31B and 12B), since moving to llama.cpp would change the quantization along with the method. Ollama's default context is too short for the whole text and its translation, so the server is run with `OLLAMA_CONTEXT_LENGTH=32768`, the length PLaMo runs with; no code change is needed for it.
- **Directories**: `plamo/<model>/`, named like onde/ (`plamo/gemma4-31b/`), each `Makefile` with the onde/ counterpart's `TRANSLATOR` and `OPTIONS`. [common.mk](common.mk) defines both commands and makes the whole-text one the default; the PLaMo sizes' Makefiles set `TRANSLATE_CMD = $(PLAMO_TRANSLATE)` after the include. The general models join `MODELS` in [Makefile](Makefile).
- **Aggregation**: `generate_compare_rows.py` names the per-language columns by model, shortening only the PLaMo sizes (`0.8B`), and orders the languages by PLaMo's largest size; and the stats table and chart tell the general models from their onde/ results by the model cell (e.g. `gemma4-31b (whole text)`). The comparison with the same models' line-by-line results is on the 45 corpus languages among PLaMo's; whether it goes in a table or only in the text is decided once the results are in.

## 4. Schedule

1. **gpt-6-luna** ([gpt-6-luna/](gpt-6-luna/)), done: once its translation and evaluation are done ([ADD_PLAMO.md](../ADD_PLAMO.md)'s section 3):
   - check the line counts, settle the language check's reviews, and check the scores and trends, adding the facts to its README;
   - compare it with the PLaMo sizes on PLaMo's 52 languages, and with [onde/gpt-6-luna/](../onde/gpt-6-luna/) on the 45 corpus languages among them, the comparison of the method alone; on the seven languages outside the corpus it was given a glossary it wrote;
   - run `make sync` and `make compare` in `examples/tr/`, and write its Notes and the text in [README.md](README.md).

   It kept the source's 99 lines in all 52 languages without being asked to, and is above the 31B in 51 of them (mean 87.48 against 78.92), so losing one's place is not a cost of the whole-text request itself. On the 45 corpus languages it is above its own line-by-line translation (mean 88.0 against 86.0, above in 33, p = 0.002), the line-by-line run having lost points in a few languages to typos, a missing speaker label and fragments ([README.md](README.md)).
2. **Procedure and plan**, done: drop from [ADD_PLAMO.md](../ADD_PLAMO.md) the note that only PLaMo can be added, and add the steps for a general model (the onde/ counterpart's `TRANSLATOR` and `OPTIONS` in its `Makefile`; blank lines dropped and usage recorded by `trtools whole`); record here what gpt-6-luna showed.
3. **Gemma 4**: the dense E2B, E4B, 12B and 31B, and the MoE 26B-A4B for reference, each as `plamo/<model>/` with the onde/ counterpart's `TRANSLATOR` (no `OPTIONS`, so `--no-think`). The user runs Ollama with `OLLAMA_CONTEXT_LENGTH=32768` before `make`, or the whole text and its translation may not fit. Then:
   - compare each size with PLaMo's sizes, to see whether dropped lines and repetition in one request come from PLaMo or from small models in general, and, with the MoE, whether that depends on the total or the active size;
   - compare each with its onde/ counterpart, for the method;
   - write the conclusions on whole-text translation in [README.md](README.md).

On hold: splitting the text in two for a model or server that cannot hold 32,768 tokens, and detecting a stop at the length limit (`finish_reason=length`) in llm7shi.
