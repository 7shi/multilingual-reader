# examples/tr/onde/qwen3.5-9b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: qwen3.5:9b
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Chinese | 90.5 | Translationese and stiff phrasing |
| Indonesian | 85.0 | Severe fluency issues and awkward lexical choices |
| Italian | 85.0 | Minor grammatical inconsistencies |
| Portuguese | 82.0 | Significant issues with naturalness and lexical choice |
| Swedish | 80.2 | Unnatural phrasing and grammatical errors |
| Russian | 79.9 | Lacks natural fluency and idiomatic correctness |
| Spanish | 79.0 | Unnatural literal translations |
| Romanian | 78.5 | Significant issues in fluency and naturalness |
| French | 77.2 | Glaring typos and awkward phrasing |
| German | 75.8 | Critical errors like "Allez" and garbled text |
| Vietnamese | 75.1 | Random insertion of Chinese characters |
| Dutch | 74.5 | Grammatical errors |
| Ukrainian | 73.2 | Lexical error changing meaning |
| Catalan | 72.0 | Non-Catalan characters disrupt readability |
| Serbian | 70.2 | Inconsistent dialect mixing |
| Japanese | 69.3 | Untranslated Chinese characters appear in text |
| Galician | 69.1 | Translation is Portuguese, not Galician |
| Lithuanian | 68.9 | Severe grammatical and terminology errors |
| Danish | 68.2 | Grammatical errors and non-Danish words |
| Persian | 67.8 | Critical scientific terminology errors and phonetic artifacts |
| Malay | 67.8 | Poor fluency and lexical errors |
| Croatian | 67.4 | Severe grammatical errors and awkward phrasing |
| Arabic | 67.0 | Severe mistranslation and inconsistent terminology |
| Polish | 66.8 | Mixed-language artifacts and severe grammatical errors |
| Afrikaans | 64.5 | Frequent English interference and grammatical errors |
| Thai | 64.5 | Contains untranslated Chinese fragments |
| Macedonian | 64.1 | Severe Chinese character encoding errors |
| Bulgarian | 63.5 | Pervasive grammatical errors and awkward syntax |
| Hungarian | 63.4 | Critical lexical errors and mistranslation of physics terms |
| Slovene | 62.2 | Severe grammatical and terminology errors |
| Korean | 61.8 | Mixed-language errors |
| Marathi | 61.8 | Heavy use of untranslated English words |
| Czech | 61.1 | Significant language contamination with Russian |
| Slovak | 60.6 | Severe linguistic and structural failures |
| Interlingua | 60.3 | Fundamentally flawed and non-standard |
| Latvian | 58.5 | Severe mechanical and grammatical failures |
| Esperanto | 58.0 | Severe lexical and grammatical errors |
| Hebrew | 57.7 | Severe terminology and grammar errors |
| Norwegian | 55.9 | Pervasive grammatical errors and unnatural phrasing |
| Bengali | 55.8 | Severe lexical errors and poor fluency |
| Belarusian | 55.1 | Severe linguistic corruption |
| Hindi | 54.8 | Contains untranslated text and foreign fragments |
| Turkish | 54.8 | Severe mistranslations and flawed terminology |
| Finnish | 53.2 | Severe grammatical errors |
| Nepali | 52.0 | Severe mistranslations and hallucinations |
| Estonian | 50.2 | Severe vocabulary and grammar errors |
| Albanian | 50.1 | severe grammatical and lexical errors |
| Greek | 49.4 | Severe grammatical errors and nonsensical phrases |
| Azerbaijani | 48.3 | Systematic mechanical errors and typos |
| Urdu | 48.0 | Written entirely in Roman script |
| Tagalog | 46.1 | Severe linguistic inaccuracies and mistranslations |
| Tamil | 44.2 | Severe translation errors and hallucinations |
| Malayalam | 43.6 | Severe semantic errors and hallucinations |
| Basque | 43.2 | Nonsense words and gibberish |
| Swahili | 42.5 | Nonsensical syntax and severe terminology errors |
| Icelandic | 40.5 | Catastrophic quality and unintelligibility |
| Sinhala | 39.7 | Severe grammatical errors and random Chinese character insertions |
| Georgian | 37.9 | Severe lexical hallucinations and gibberish |
| Telugu | 37.7 | Severe terminology distortion and nonsensical phrasing |
| Khmer | 35.9 | Severe terminology errors and broken syntax |
| Lao | 35.9 | Severe grammatical breakdown and inaccurate terminology |
| Mongolian | 35.5 | Catastrophic mistranslations and hallucinations |
| Burmese | 34.9 | Severe machine-translation artifacts and broken syntax |
| Irish | 33.4 | Severe lexical hallucination and nonsense |
| Welsh | 31.5 | Syntactically broken nonsense |
| Armenian | 31.0 | Nonsensical terminology and grammatical incoherence |
| Kannada | 30.0 | Severe lexical errors and nonsense words |
