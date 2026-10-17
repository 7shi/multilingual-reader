# examples/tr/onde/gemma4-e2b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: gemma4:e2b
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Dutch | 87.5 | Inconsistent mathematical phrasing |
| Serbian | 75.9 | Significant grammatical errors and unnatural phrasing |
| Khmer | 73.8 | Severe encoding artifacts present |
| Indonesian | 73.1 | Missing speaker labels and mixed-language terms |
| Portuguese | 72.0 | Critical structural defects and terminology error |
| Japanese | 71.8 | Severe lack of formatting fidelity to speaker tags |
| Malay | 71.8 | Awkward phrasing and code-switching |
| Spanish | 71.5 | Breakdown of speaker attribution |
| Thai | 71.5 | Severe formatting and segmentation errors |
| Vietnamese | 71.1 | Missing content in translation |
| Polish | 70.8 | Frequent grammatical errors and unnatural phrasing |
| Swedish | 70.2 | Severe grammatical errors and unnatural syntax |
| Burmese | 70.0 | Poor terminology and unnatural syntax |
| Italian | 69.6 | Dialogue attribution errors |
| Nepali | 69.4 | Grammar errors and awkward phrasing |
| French | 69.2 | Missing speaker labels and disconnected dialogue |
| Ukrainian | 69.2 | Severe grammar and terminology errors |
| Turkish | 68.8 | Severe structural and syntactic defects |
| Korean | 68.2 | Inconsistent and incorrect terminology for physics concepts |
| Hindi | 67.8 | Poor fluency and naturalness due to awkward syntax |
| Chinese | 67.2 | Missing speaker labels and unnatural phrasing |
| Norwegian | 66.9 | Severe structural and grammatical inconsistencies |
| Tamil | 66.6 | Mixed languages and non-Tamil characters |
| Russian | 66.4 | Broken dialogue structure and speaker attribution |
| Tagalog | 65.5 | Severe awkwardness and unnatural phrasing |
| Marathi | 65.3 | Disorganized speaker attributions |
| Persian | 65.2 | Severe formatting errors and rigid tone |
| Danish | 64.6 | Missing speaker labels |
| Afrikaans | 63.9 | Missing speaker labels and content |
| Arabic | 63.5 | Missing speaker labels |
| Croatian | 63.2 | Pervasive translationese and major errors |
| German | 62.5 | Unnatural fluency and grammar |
| Urdu | 60.9 | Severe syntax and terminology flaws |
| Lao | 60.2 | Severe mixed script errors |
| Sinhala | 59.7 | Severe grammatical errors and typos |
| Galician | 59.3 | Corrupted mix of languages and Chinese characters |
| Finnish | 59.2 | Severe grammatical breakdowns and mistranslations |
| Bengali | 57.9 | Severe translationese and unnatural phrasing |
| Czech | 57.2 | Severe structural and linguistic failures |
| Romanian | 56.6 | Severe mistranslation and grammatical errors |
| Georgian | 56.5 | Severe corruption and mixed languages |
| Hebrew | 56.0 | Severe structural and grammatical errors |
| Telugu | 56.0 | Inconsistent scientific transliteration |
| Swahili | 54.5 | Severe fluency and grammatical errors |
| Malayalam | 54.1 | Severe structural and formatting errors with mixed-language contamination |
| Macedonian | 52.2 | Fundamentally flawed and largely unintelligible |
| Azerbaijani | 51.9 | Severe machine translation errors |
| Armenian | 50.9 | Severe multilingual contamination |
| Catalan | 50.5 | Pervasive errors and nonsense words |
| Mongolian | 49.8 | Severe terminology and grammar issues |
| Albanian | 49.7 | Severe mistranslations and grammatical errors |
| Bulgarian | 48.5 | Severe structural integrity failures and mixed language contamination |
| Slovak | 48.2 | Severe grammatical and syntactic flaws |
| Kannada | 47.4 | Severe mechanical errors and code injection |
| Interlingua | 42.5 | Not genuine Interlingua |
| Hungarian | 41.2 | Nonsensical and invented vocabulary |
| Slovene | 40.3 | Fundamentally flawed and largely unintelligible |
| Belarusian | 40.0 | Severe grammatical errors and nonsense |
| Esperanto | 37.1 | Severe grammatical and semantic errors |
| Greek | 35.3 | Severe code-switching with multiple foreign languages |
| Icelandic | 33.8 | Complete gibberish and non-existent words |
| Lithuanian | 29.1 | Foreign intrusions and code artifacts |
| Estonian | 28.9 | Severe mixed-language artifacts and broken grammar |
| Latvian | 25.9 | Severe corruption and foreign language contamination |
| Basque | 22.7 | Severe structural and lexical defects |
| Welsh | 19.3 | Catastrophic failure with mixed-language garbling |
| Irish | 15.0 | Nonsensical and grammatically broken |
