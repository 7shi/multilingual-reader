# examples/tr/plamo/gemma4-26b/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model, the mixture-of-experts Gemma 4 (26B total, 4B active), for reference beside the dense sizes.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gemma4/](../../onde/gemma4/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:26b-a4b-it-qat (QAT, Q4_0) on Ollama, its context set to 32,768 tokens (`OLLAMA_CONTEXT_LENGTH=32768`), as for PLaMo, since the whole text and its translation go in one request
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), no CoT (`--no-think`) and Ollama's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Besides the quantization (onde/gemma4 ran `gemma4:26b`, Q4_K_M; here the QAT build, as onde/ runs for the 12B and 31B), only the method differs from [onde/gemma4/](../../onde/gemma4/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

In 3 of the 52 languages the model does not translate into the target language, and those score 0 by the language check. In Malay it returns the English source unchanged, byte for byte. In Catalan and German it translates into French instead, leaving a few of the glossary's terms in the target language (`Ponts en la Física`, `une físic teòric`; `Brücken in der Physik`, `un Experimentalphysiker`).

Where it does translate, four languages lose their place:

- **Khmer**: mixes in Thai, Bengali, Arabic, Chinese and Latin script from the first lines, Camille's label among them (`ក gamle`), and breaks off in the middle of line 20 ("When we perform the double-slit experiment…"), 79 lines short.
- **Japanese**: folds Camille's `Hmm.` on line 89 into line 91 ("Absolutely. And that leaves us with a final question…") and drops Luc's "The world is really... coherent." on line 90, two lines short.
- **Urdu**: puts Luc's question on line 94 ("…does that mean that probability is not just a simple calculating tool?") into Camille's line 93 and drops Camille's `Yes...` on line 95, two lines short.
- **Estonian**: breaks line 58 in the middle of a word (`kohal` / `ta asukohta`), one line over.

The trend column's phrase for Estonian, written as "Massive untranslated English text", was rewritten by hand to what the translation shows: only interjections such as `Hmm.` are as in the source, and the low score comes from misspellings, broken words and stray symbols.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 92.3 | Pronoun inconsistency and typo |
| Spanish | 91.3 | Subtle phrasing slightly less colloquial than ideal |
| Japanese | 89.7 | Minor stiffness and filler word repetition |
| Chinese (Traditional) | 88.9 | Pronounced translationese style reduces fluency and naturalness |
| Italian | 88.7 | Slightly stiff phrasing from English syntax |
| Indonesian | 88.6 | Slightly literal phrasing affecting naturalness |
| Dutch | 88.0 | Grammatical errors and unidiomatic phrasing |
| Chinese | 87.8 | Slight translationese stiffness and awkward phrasing |
| Vietnamese | 86.6 | Pronoun usage slightly inconsistent |
| Hindi | 85.1 | Distinct translated quality impacting fluency |
| Arabic | 84.8 | Stiff dialogue flow |
| Thai | 83.7 | Slightly stiff phrasing and translationese |
| Persian | 83.5 | Inconsistent speaker labeling |
| Polish | 83.4 | Persistent anglicisms and awkward syntax |
| Russian | 79.7 | Translationese and mixed languages |
| Korean | 78.8 | Inconsistent honorifics and stiff phrasing |
| Urdu | 78.2 | Unnatural phrasing and lack of fluency |
| Bengali | 77.9 | Scattered Chinese characters |
| Nepali | 76.6 | Inconsistent character naming and awkward syntax |
| Javanese | 76.2 | Frequent English intrusions |
| Marathi | 74.7 | Luc's name inconsistency to Kamel |
| Tagalog | 74.3 | Severe terminology errors like 'pisiko' for physicist |
| Croatian | 72.8 | Mixed language sentences and typos |
| Tamil | 72.8 | Significant mixed-language defects |
| Cebuano | 71.5 | Severe scientific terminology errors |
| Bulgarian | 71.1 | Significant mechanical errors and transcription artifacts |
| Serbian | 71.1 | Corrupted LaTeX code and frequent typos |
| Punjabi | 69.5 | Severe mixed-language character defects |
| Burmese | 69.2 | Mixed language artifacts and gibberish |
| Uzbek | 68.7 | Lack of technical precision and naturalness |
| Gujarati | 68.5 | Untranslated English and garbled text |
| Telugu | 68.1 | Severe code-switching and poor localization |
| Azerbaijani | 67.2 | Severe lexical errors and awkward phrasing |
| Hebrew | 62.7 | Mixed languages and untranslated text |
| Swahili | 62.4 | Non-English script glitch and severe linguistic errors |
| Slovak | 62.3 | Severe lexical and grammatical defects with mixed languages |
| Slovene | 60.0 | Severe linguistic defects |
| Kazakh | 55.4 | Severe linguistic breakage and foreign character intrusion |
| Belarusian | 54.2 | Severe text corruption and gibberish |
| Malayalam | 51.9 | Severe mixed-language formatting |
| Hungarian | 51.3 | Severe linguistic incoherence and mixed-language artifacts |
| Armenian | 46.7 | Severe mixed-language and garbled output |
| Georgian | 46.1 | Severe mixed-language artifacts |
| Latvian | 44.9 | Severe grammatical and lexical failures with vulgarity |
| Lithuanian | 43.8 | Pervasive mixed language and structural defects |
| Sinhala | 42.6 | Severe mixed-language intrusion |
| Estonian | 40.9 | Pervasive misspellings, broken words and stray symbols |
| Basque | 37.3 | Severe grammatical and syntactical breakdown |
| Khmer | 27.9 | Severe multi-language contamination and truncation |
| Catalan | 0.0 | Not in the target language (detected: French) |
| German | 0.0 | Not in the target language (detected: French) |
| Malay | 0.0 | Not in the target language (detected: English) |
