# examples/tr/onde/space-bunny-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: space-bunny-alpha
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Ukrainian | 77.6 | Missing speaker attributions |
| Romanian | 71.3 | Severe formatting errors and literal calques |
| Turkish | 70.5 | Frequent separation of speaker names and missing tags |
| Finnish | 70.3 | Formatting and accuracy errors |
| Polish | 70.2 | Severe formatting and dialogue tag errors |
| Russian | 69.8 | Leftover English word and formatting errors |
| Chinese | 69.6 | Jarring mixed-language error |
| Slovak | 69.5 | Significant mechanical and grammatical errors |
| Hindi | 69.4 | Inconsistent formatting and mechanical errors |
| Danish | 68.7 | Inconsistent speaker labels and formatting defects |
| Croatian | 68.0 | Untranslated English and swapped speaker labels |
| Vietnamese | 68.0 | Structural glitches and unnatural phrasing |
| Dutch | 67.4 | Repeated grammatical errors in math notation phrasing |
| French | 66.3 | Glaring untranslated errors and garbled text |
| Hungarian | 66.2 | Inclusion of untranslated English segments |
| Persian | 65.8 | Inconsistent tone and mixed-language defects |
| Hebrew | 65.8 | Severe structural disorganization and untranslated segments |
| Nepali | 65.7 | Inconsistent speaker labeling |
| Bulgarian | 65.3 | Mixed language and missing speaker attributions |
| Belarusian | 65.1 | Severe grammatical and structural errors |
| Bengali | 64.8 | Speaker confusion disrupts dialogue |
| German | 64.5 | Critical loss of speaker labels |
| Thai | 64.2 | Missing speaker tags and garbled text |
| Portuguese | 63.8 | Stray Chinese characters and mixed dialects |
| Serbian | 63.7 | Stiff and unnatural phrasing |
| Norwegian | 63.4 | Speaker labels missing and misattributed |
| Swedish | 63.4 | Severe structural and formatting errors |
| Spanish | 63.0 | Lost speaker attribution and mixed-language errors |
| Italian | 62.4 | Major formatting and mixed-language errors |
| Macedonian | 61.6 | Severe loss of speaker attribution tags |
| Slovene | 61.2 | Speaker attribution breakdown |
| Catalan | 60.9 | Significant language mixing and structural errors |
| Afrikaans | 60.1 | Severe structural and content errors |
| Czech | 60.0 | Multiple missing speaker labels |
| Greek | 60.0 | Severe scientific terminology errors |
| Galician | 59.3 | Mixed language artifacts and missing dialogue tags |
| Azerbaijani | 58.4 | Orphaned markers and mixed English terms |
| Latvian | 58.2 | Severe grammatical and structural errors |
| Marathi | 58.0 | Pervasive grammatical and terminology errors |
| Korean | 55.9 | Severe mixed-language contamination |
| Albanian | 54.8 | Severe structural breakdown and speaker attribution errors |
| Telugu | 54.5 | Severe semantic errors and nonsense |
| Urdu | 54.4 | Severe structural fragmentation and grammatical errors |
| Estonian | 54.3 | Severe structural breakdown of dialogue attribution |
| Icelandic | 53.8 | Severe grammatical and syntactical errors |
| Esperanto | 52.7 | Broken formatting with English artifacts |
| Mongolian | 51.6 | Severe linguistic and mechanical failures |
| Swahili | 51.2 | Severe mixed-language errors and grammatical nonsense |
| Indonesian | 51.0 | Foreign language intrusion and meta-commentary leakage |
| Tamil | 49.5 | Foreign language intrusion |
| Armenian | 49.2 | Severe mechanical and grammatical errors |
| Lithuanian | 47.9 | Severe OCR artifacts and terminology errors |
| Tagalog | 46.3 | Contains untranslated Chinese characters |
| Basque | 46.2 | Major structural and linguistic errors |
| Kannada | 45.2 | Severe linguistic contamination and mechanical errors |
| Interlingua | 42.7 | Hybrid of Italian, Spanish, and English |
| Georgian | 41.7 | Severe mechanical and OCR corruption |
| Arabic | 41.1 | Massive code-switching errors |
| Malayalam | 39.8 | Severe grammatical and vocabulary errors |
| Khmer | 39.2 | Completely broken and incomprehensible |
| Lao | 38.1 | Pervasive mechanical errors and unintelligibility |
| Burmese | 37.1 | Catastrophic semantic failure and hallucination |
| Welsh | 35.4 | Hybrid language and Chinese character insertions |
| Sinhala | 33.6 | Severe structural and linguistic defects |
| Malay | 33.4 | Severe language mixing and chaotic output |
| Irish | 30.2 | Nonsensical mix of English and fake Irish |
| Japanese | 28.0 | Mixed-language corruption |
