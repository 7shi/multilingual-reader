# examples/tr/onde/space-bunny-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: space-bunny-alpha
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Ukrainian | 74.1 | Missing speaker attributions |
| Turkish | 72.3 | Frequent separation of speaker names and missing tags |
| Russian | 72.0 | Leftover English word and formatting errors |
| Romanian | 70.9 | Severe formatting errors and literal calques |
| Hindi | 70.6 | Inconsistent formatting and mechanical errors |
| Portuguese | 69.5 | Stray Chinese characters and mixed dialects |
| Polish | 69.1 | Severe formatting and dialogue tag errors |
| Vietnamese | 68.7 | Structural glitches and unnatural phrasing |
| Slovak | 67.9 | Significant mechanical and grammatical errors |
| French | 67.6 | Glaring untranslated errors and garbled text |
| Bulgarian | 67.5 | Mixed language and missing speaker attributions |
| Nepali | 67.4 | Inconsistent speaker labeling |
| Persian | 67.0 | Inconsistent tone and mixed-language defects |
| Belarusian | 65.9 | Severe grammatical and structural errors |
| Bengali | 65.8 | Speaker confusion disrupts dialogue |
| Thai | 65.5 | Missing speaker tags and garbled text |
| Swedish | 65.4 | Severe structural and formatting errors |
| Croatian | 65.2 | Untranslated English and swapped speaker labels |
| Slovene | 65.0 | Speaker attribution breakdown |
| Danish | 64.8 | Inconsistent speaker labels and formatting defects |
| Finnish | 64.8 | Formatting and accuracy errors |
| Chinese | 64.7 | Jarring mixed-language error |
| Norwegian | 64.4 | Speaker labels missing and misattributed |
| Hungarian | 64.1 | Inclusion of untranslated English segments |
| Hebrew | 64.0 | Severe structural disorganization and untranslated segments |
| Macedonian | 63.9 | Severe loss of speaker attribution tags |
| Italian | 63.8 | Major formatting and mixed-language errors |
| Dutch | 63.7 | Repeated grammatical errors in math notation phrasing |
| Catalan | 63.0 | Significant language mixing and structural errors |
| Azerbaijani | 62.9 | Orphaned markers and mixed English terms |
| German | 62.8 | Critical loss of speaker labels |
| Serbian | 62.5 | Stiff and unnatural phrasing |
| Korean | 62.1 | Severe mixed-language contamination |
| Afrikaans | 62.0 | Severe structural and content errors |
| Marathi | 60.7 | Pervasive grammatical and terminology errors |
| Spanish | 60.6 | Lost speaker attribution and mixed-language errors |
| Greek | 60.5 | Severe scientific terminology errors |
| Latvian | 60.5 | Severe grammatical and structural errors |
| Galician | 60.3 | Mixed language artifacts and missing dialogue tags |
| Czech | 59.6 | Multiple missing speaker labels |
| Urdu | 55.9 | Severe structural fragmentation and grammatical errors |
| Indonesian | 55.5 | Foreign language intrusion and meta-commentary leakage |
| Esperanto | 55.0 | Broken formatting with English artifacts |
| Icelandic | 54.0 | Severe grammatical and syntactical errors |
| Estonian | 53.9 | Severe structural breakdown of dialogue attribution |
| Mongolian | 53.0 | Severe linguistic and mechanical failures |
| Albanian | 52.7 | Severe structural breakdown and speaker attribution errors |
| Armenian | 50.4 | Severe mechanical and grammatical errors |
| Telugu | 50.4 | Severe semantic errors and nonsense |
| Lithuanian | 49.5 | Severe OCR artifacts and terminology errors |
| Tamil | 49.5 | Foreign language intrusion |
| Basque | 48.6 | Major structural and linguistic errors |
| Swahili | 48.4 | Severe mixed-language errors and grammatical nonsense |
| Kannada | 47.3 | Severe linguistic contamination and mechanical errors |
| Tagalog | 45.9 | Contains untranslated Chinese characters |
| Georgian | 45.4 | Severe mechanical and OCR corruption |
| Interlingua | 45.0 | Hybrid of Italian, Spanish, and English |
| Arabic | 44.4 | Massive code-switching errors |
| Lao | 42.9 | Pervasive mechanical errors and unintelligibility |
| Malayalam | 42.8 | Severe grammatical and vocabulary errors |
| Khmer | 41.2 | Completely broken and incomprehensible |
| Malay | 40.9 | Severe language mixing and chaotic output |
| Burmese | 37.8 | Catastrophic semantic failure and hallucination |
| Japanese | 36.9 | Mixed-language corruption |
| Welsh | 35.6 | Hybrid language and Chinese character insertions |
| Sinhala | 35.2 | Severe structural and linguistic defects |
| Irish | 32.1 | Nonsensical mix of English and fake Irish |
