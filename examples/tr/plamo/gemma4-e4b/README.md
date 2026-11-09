# examples/tr/plamo/gemma4-e4b/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gemma4-e4b/](../../onde/gemma4-e4b/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:e4b on Ollama, its context set to 32,768 tokens (`OLLAMA_CONTEXT_LENGTH=32768`), as for PLaMo, since the whole text and its translation go in one request
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), no CoT (`--no-think`) and Ollama's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/gemma4-e4b/](../../onde/gemma4-e4b/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language and kept the source's 99 lines in every one, with no line skipped, repeated, split or joined.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 91.7 | Minor stylistic nuances affect fluency |
| Italian | 89.7 | Stiff and literal prose |
| German | 88.1 | Awkward calques and rigid syntax |
| Indonesian | 87.9 | Occasionally stiff and overly literal phrasing |
| Russian | 87.7 | Translationese style |
| Thai | 87.7 | Some stiff sentence flow due to literal phrasing |
| Dutch | 87.5 | Lacks idiomatic fluency |
| Japanese | 87.0 | Stiff sentence structures |
| Vietnamese | 87.0 | Stylistic issues detract from polish |
| Malay | 86.4 | Awkward literal translations and unnatural filler usage |
| Korean | 84.2 | Tone and register inconsistencies |
| Arabic | 82.3 | Translationese and stiff dialogue flow |
| Polish | 82.2 | Fluency and naturalness issues |
| Chinese (Traditional) | 81.7 | Awkward phrasing and lack of naturalness |
| Persian | 79.5 | Stiff translationese and lack of naturalness |
| French | 78.5 | Untranslated English word and grammatical error |
| Nepali | 78.5 | Awkward literal syntax and poor fluency |
| Chinese | 77.7 | Awkward phrasing and grammatical errors |
| Marathi | 77.0 | Rigidly literal and unnatural phrasing |
| Gujarati | 76.9 | Lacks casual nuance |
| Swahili | 76.8 | Significant fluency issues and awkward phrasings |
| Urdu | 75.2 | Severe phonetic transliteration errors and poor terminology |
| Bengali | 75.1 | Significant stylistic inconsistencies and grammatical errors |
| Burmese | 74.2 | Inconsistent speaker names |
| Hindi | 74.0 | Awkward and stilted phrasing |
| Serbian | 73.9 | Poor fluency and terminology |
| Uzbek | 73.6 | Significant lexical and fluency errors |
| Croatian | 73.3 | Pervasive grammatical errors and unnatural phrasing |
| Hebrew | 73.2 | Translationese with terminology errors |
| Azerbaijani | 72.9 | Grammatical errors and unnatural phrasing |
| Malayalam | 72.1 | Chinese character intrusion and rigid syntax |
| Telugu | 71.7 | Unnatural literal translation |
| Sinhala | 71.4 | Major Indonesian language intrusion |
| Bulgarian | 71.3 | Severe grammatical and morphological errors |
| Cebuano | 70.5 | Stiff syntax and inaccurate terminology |
| Tagalog | 68.7 | Severe terminology and fluency issues |
| Kazakh | 67.8 | Severe linguistic and stylistic errors |
| Catalan | 67.4 | Confused French grammar with Catalan vocabulary |
| Armenian | 67.2 | Korean text intrusion and stiffness |
| Georgian | 67.2 | Egregious MT artifacts and language mixing |
| Javanese | 66.1 | Severe lexical and grammatical errors |
| Khmer | 65.8 | Severe mixed-language artifacts and technical inaccuracies |
| Punjabi | 63.9 | Non-existent vocabulary and gibberish |
| Slovak | 63.5 | Severe systemic errors and poor grammar |
| Slovene | 62.5 | Severe grammatical errors and incorrect word choices |
| Hungarian | 59.2 | Severe grammatical and lexical errors |
| Tamil | 58.6 | Mixed languages and stray characters |
| Lithuanian | 46.3 | Nonsense vocabulary and broken syntax |
| Estonian | 43.3 | Unintelligible gibberish and broken grammar |
| Belarusian | 42.9 | Severe grammatical and lexical errors |
| Latvian | 37.6 | Catastrophic failure with non-existent language and gibberish |
| Basque | 30.4 | Severe mixed-language corruption |
