# examples/tr/plamo/gemma4-12b/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gemma4-12b/](../../onde/gemma4-12b/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:12b-it-qat on Ollama, its context set to 32,768 tokens (`OLLAMA_CONTEXT_LENGTH=32768`), as for PLaMo, since the whole text and its translation go in one request
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), no CoT (`--no-think`) and Ollama's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/gemma4-12b/](../../onde/gemma4-12b/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language and kept the source's 99 lines in every one, with no line skipped, repeated, split or joined. Within the lines, though, words from other languages and scripts break in: Chinese characters, Hangul, Cyrillic or Arabic in the middle of a sentence (`ez千 göndítés`, `Ber 있기ra`), in 27 of the 48 languages not written in Chinese characters or Hangul, 74 lines in all, where each other Gemma 4 size has them in 5 to 11 languages. Its line-by-line run in [onde/gemma4-12b/](../../onde/gemma4-12b/) has them in as many (31 languages), so they come with this model rather than with the method, and the trend column names them in most of its languages below 70.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses one simplified character (`通过` on line 87, where `過` is used elsewhere). From line 79 on, Camille's label turns into `卡米 Starr`.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 91.2 | slightly literal phrasing |
| French | 90.8 | Negligible stylistic tweaks needed |
| Indonesian | 87.4 | Awkward literal phrasing |
| Korean | 87.0 | Slight stiffness and literalness |
| Polish | 86.9 | Occasional stiff and literal phrasing |
| Thai | 83.7 | Inconsistent honorifics and mixed-script name |
| Arabic | 83.0 | Unnatural phrasing and anglicisms |
| Chinese | 77.3 | Name inconsistency and untranslated fragments |
| Serbian | 77.2 | Significant grammatical and lexical errors |
| Vietnamese | 76.7 | Untranslated English verb in Vietnamese sentence |
| Dutch | 76.6 | Russian text intrusion breaks language consistency |
| Malay | 75.7 | Incorrect scientific terminology and unnatural phrasing |
| Italian | 75.1 | Poor fluency and grammar |
| Russian | 74.0 | Unlocalized English and broken math notation |
| Hindi | 73.8 | Grammatical roughness and stiffness |
| German | 71.2 | Mixed languages within sentences |
| Japanese | 70.5 | Significant text artifacts |
| Nepali | 69.7 | Script mixing and code-switching |
| Chinese (Traditional) | 68.2 | Severe structural corruption with name errors and mixed-language artifacts |
| Swahili | 66.6 | Mixed languages and code-switching errors |
| Telugu | 66.2 | Inconsistent mixed-language artifacts |
| Persian | 65.9 | Severe structural defects and mixed-language glitches |
| Tagalog | 64.5 | Severe linguistic and grammatical errors |
| Croatian | 64.2 | Severe fluency and grammatical issues |
| Burmese | 63.0 | Mixed Chinese and Russian characters |
| Uzbek | 62.3 | Severe machine-translation errors and hallucinations |
| Javanese | 61.6 | Severe mixed-language defect and non-standard terminology |
| Urdu | 60.3 | Frequent Chinese character insertions |
| Bulgarian | 59.9 | Severe language mixing and corruption |
| Gujarati | 59.1 | Heavy code-switching and untranslated fragments |
| Khmer | 58.7 | Catastrophic language mixing artifacts and severe inaccuracies |
| Bengali | 56.6 | Severe code-switching and typos |
| Catalan | 56.5 | Severe mixed-language errors and lexical inaccuracies |
| Azerbaijani | 55.8 | Presence of Chinese characters |
| Cebuano | 55.8 | Severe corruption by random Chinese and English text fragments |
| Hebrew | 55.5 | Severe mixed-language corruption |
| Marathi | 55.0 | Severe mixed-language intrusions |
| Punjabi | 53.9 | Severe code-switching with untranslated English |
| Sinhala | 52.9 | Severe code-switching and mixed language errors |
| Tamil | 52.0 | Severe language mixing renders text unreadable |
| Kazakh | 50.9 | Severe structural defects with mixed languages |
| Malayalam | 50.8 | Severe mixed-language contamination |
| Slovene | 45.9 | Total failure; unreadable and unintelligible output |
| Slovak | 45.0 | Severe corruption with untranslated Chinese characters |
| Armenian | 41.7 | Severe structural defects mixed with gibberish |
| Hungarian | 38.2 | Corrupted by Chinese/Japanese characters and nonsense |
| Estonian | 38.1 | Catastrophic linguistic breakdown and nonsense |
| Georgian | 36.5 | Severe mixed-language pollution renders text unintelligible |
| Latvian | 36.0 | Severe mixed-language artifacts |
| Belarusian | 35.2 | Complete unintelligibility due to mixed scripts and nonsense |
| Lithuanian | 32.0 | Contains corrupted foreign language artifacts |
| Basque | 29.1 | Unintelligible gibberish with Korean intrusions |
