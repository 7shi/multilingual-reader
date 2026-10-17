# examples/tr/onde/qwen3.5-9b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: qwen3.5:9b
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Chinese | 89.5 | Translationese and stiff phrasing |
| Italian | 88.5 | Minor grammatical inconsistencies |
| Indonesian | 85.3 | Severe fluency issues and awkward lexical choices |
| Portuguese | 85.3 | Significant issues with naturalness and lexical choice |
| Spanish | 79.8 | Unnatural literal translations |
| Russian | 79.1 | Lacks natural fluency and idiomatic correctness |
| Vietnamese | 77.5 | Random insertion of Chinese characters |
| Swedish | 77.4 | Unnatural phrasing and grammatical errors |
| French | 77.3 | Glaring typos and awkward phrasing |
| Romanian | 77.3 | Significant issues in fluency and naturalness |
| German | 77.2 | Critical errors like "Allez" and garbled text |
| Dutch | 73.5 | Grammatical errors |
| Ukrainian | 73.2 | Lexical error changing meaning |
| Japanese | 71.5 | Untranslated Chinese characters appear in text |
| Persian | 71.2 | Critical scientific terminology errors and phonetic artifacts |
| Arabic | 71.0 | Severe mistranslation and inconsistent terminology |
| Catalan | 71.0 | Non-Catalan characters disrupt readability |
| Serbian | 71.0 | Inconsistent dialect mixing |
| Afrikaans | 70.8 | Frequent English interference and grammatical errors |
| Danish | 70.8 | Grammatical errors and non-Danish words |
| Lithuanian | 70.7 | Severe grammatical and terminology errors |
| Croatian | 70.5 | Severe grammatical errors and awkward phrasing |
| Malay | 70.3 | Poor fluency and lexical errors |
| Polish | 68.8 | Mixed-language artifacts and severe grammatical errors |
| Thai | 67.5 | Contains untranslated Chinese fragments |
| Galician | 66.9 | Translation is Portuguese, not Galician |
| Hungarian | 66.5 | Critical lexical errors and mistranslation of physics terms |
| Macedonian | 65.5 | Severe Chinese character encoding errors |
| Bulgarian | 65.4 | Pervasive grammatical errors and awkward syntax |
| Interlingua | 64.2 | Fundamentally flawed and non-standard |
| Slovene | 63.8 | Severe grammatical and terminology errors |
| Czech | 62.8 | Significant language contamination with Russian |
| Korean | 61.6 | Mixed-language errors |
| Hebrew | 60.5 | Severe terminology and grammar errors |
| Esperanto | 60.2 | Severe lexical and grammatical errors |
| Slovak | 60.0 | Severe linguistic and structural failures |
| Marathi | 59.7 | Heavy use of untranslated English words |
| Latvian | 59.5 | Severe mechanical and grammatical failures |
| Turkish | 58.1 | Severe mistranslations and flawed terminology |
| Bengali | 57.0 | Severe lexical errors and poor fluency |
| Hindi | 56.8 | Contains untranslated text and foreign fragments |
| Norwegian | 56.6 | Pervasive grammatical errors and unnatural phrasing |
| Belarusian | 55.8 | Severe linguistic corruption |
| Nepali | 55.5 | Severe mistranslations and hallucinations |
| Greek | 54.5 | Severe grammatical errors and nonsensical phrases |
| Estonian | 53.9 | Severe vocabulary and grammar errors |
| Finnish | 52.5 | Severe grammatical errors |
| Azerbaijani | 52.0 | Systematic mechanical errors and typos |
| Urdu | 51.3 | Written entirely in Roman script |
| Albanian | 50.4 | severe grammatical and lexical errors |
| Tamil | 48.8 | Severe translation errors and hallucinations |
| Malayalam | 45.3 | Severe semantic errors and hallucinations |
| Icelandic | 44.6 | Catastrophic quality and unintelligibility |
| Tagalog | 43.1 | Severe linguistic inaccuracies and mistranslations |
| Swahili | 42.7 | Nonsensical syntax and severe terminology errors |
| Georgian | 42.0 | Severe lexical hallucinations and gibberish |
| Basque | 41.9 | Nonsense words and gibberish |
| Sinhala | 40.1 | Severe grammatical errors and random Chinese character insertions |
| Telugu | 39.2 | Severe terminology distortion and nonsensical phrasing |
| Mongolian | 38.1 | Catastrophic mistranslations and hallucinations |
| Khmer | 38.0 | Severe terminology errors and broken syntax |
| Lao | 38.0 | Severe grammatical breakdown and inaccurate terminology |
| Burmese | 36.8 | Severe machine-translation artifacts and broken syntax |
| Welsh | 35.2 | Syntactically broken nonsense |
| Kannada | 34.5 | Severe lexical errors and nonsense words |
| Irish | 32.5 | Severe lexical hallucination and nonsense |
| Armenian | 32.5 | Nonsensical terminology and grammatical incoherence |
