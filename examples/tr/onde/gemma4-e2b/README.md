# examples/tr/onde/gemma4-e2b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:e2b
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Dutch | 88.3 | Inconsistent mathematical phrasing |
| Spanish | 76.1 | Breakdown of speaker attribution |
| Serbian | 74.5 | Significant grammatical errors and unnatural phrasing |
| Khmer | 74.2 | Severe encoding artifacts present |
| Thai | 73.5 | Severe formatting and segmentation errors |
| French | 72.6 | Missing speaker labels and disconnected dialogue |
| Hindi | 72.1 | Poor fluency and naturalness due to awkward syntax |
| Indonesian | 71.3 | Missing speaker labels and mixed-language terms |
| Malay | 71.3 | Awkward phrasing and code-switching |
| Vietnamese | 71.1 | Missing content in translation |
| Italian | 70.3 | Dialogue attribution errors |
| Swedish | 69.8 | Severe grammatical errors and unnatural syntax |
| Nepali | 69.5 | Grammar errors and awkward phrasing |
| Marathi | 69.2 | Disorganized speaker attributions |
| Tagalog | 68.4 | Severe awkwardness and unnatural phrasing |
| Chinese | 68.3 | Missing speaker labels and unnatural phrasing |
| Arabic | 68.2 | Missing speaker labels |
| Norwegian | 68.2 | Severe structural and grammatical inconsistencies |
| Ukrainian | 68.1 | Severe grammar and terminology errors |
| Burmese | 68.0 | Poor terminology and unnatural syntax |
| Portuguese | 68.0 | Critical structural defects and terminology error |
| Polish | 67.7 | Frequent grammatical errors and unnatural phrasing |
| Japanese | 67.0 | Severe lack of formatting fidelity to speaker tags |
| Tamil | 66.9 | Mixed languages and non-Tamil characters |
| Turkish | 66.4 | Severe structural and syntactic defects |
| Persian | 66.2 | Severe formatting errors and rigid tone |
| Danish | 64.9 | Missing speaker labels |
| Russian | 64.8 | Broken dialogue structure and speaker attribution |
| Afrikaans | 64.4 | Missing speaker labels and content |
| Korean | 64.0 | Inconsistent and incorrect terminology for physics concepts |
| German | 63.5 | Unnatural fluency and grammar |
| Croatian | 63.0 | Pervasive translationese and major errors |
| Urdu | 63.0 | Severe syntax and terminology flaws |
| Bengali | 62.3 | Severe translationese and unnatural phrasing |
| Lao | 61.2 | Severe mixed script errors |
| Sinhala | 60.7 | Severe grammatical errors and typos |
| Telugu | 57.9 | Inconsistent scientific transliteration |
| Czech | 54.6 | Severe structural and linguistic failures |
| Swahili | 54.6 | Severe fluency and grammatical errors |
| Hebrew | 54.0 | Severe structural and grammatical errors |
| Romanian | 53.5 | Severe mistranslation and grammatical errors |
| Georgian | 53.4 | Severe corruption and mixed languages |
| Galician | 53.0 | Corrupted mix of languages and Chinese characters |
| Finnish | 51.6 | Severe grammatical breakdowns and mistranslations |
| Malayalam | 51.3 | Severe structural and formatting errors with mixed-language contamination |
| Azerbaijani | 50.1 | Severe machine translation errors |
| Macedonian | 49.3 | Fundamentally flawed and largely unintelligible |
| Armenian | 49.1 | Severe multilingual contamination |
| Albanian | 49.1 | Severe mistranslations and grammatical errors |
| Bulgarian | 45.7 | Severe structural integrity failures and mixed language contamination |
| Catalan | 45.7 | Pervasive errors and nonsense words |
| Mongolian | 44.9 | Severe terminology and grammar issues |
| Kannada | 44.0 | Severe mechanical errors and code injection |
| Slovak | 43.8 | Severe grammatical and syntactic flaws |
| Interlingua | 41.7 | Not genuine Interlingua |
| Hungarian | 38.6 | Nonsensical and invented vocabulary |
| Belarusian | 38.1 | Severe grammatical errors and nonsense |
| Slovene | 38.0 | Fundamentally flawed and largely unintelligible |
| Esperanto | 35.0 | Severe grammatical and semantic errors |
| Greek | 31.7 | Severe code-switching with multiple foreign languages |
| Icelandic | 30.6 | Complete gibberish and non-existent words |
| Estonian | 26.4 | Severe mixed-language artifacts and broken grammar |
| Lithuanian | 25.8 | Foreign intrusions and code artifacts |
| Latvian | 24.0 | Severe corruption and foreign language contamination |
| Basque | 21.7 | Severe structural and lexical defects |
| Welsh | 20.3 | Catastrophic failure with mixed-language garbling |
| Irish | 15.5 | Nonsensical and grammatically broken |
