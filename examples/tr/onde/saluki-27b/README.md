# examples/tr/onde/saluki-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: Underdog Saluki 27B 1.0 (quantized Qwen 3.8 27B)
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 87.9 | Slightly stiff and unnatural phrasing |
| Spanish | 87.4 | French word intrusion and stiff phrasing |
| Indonesian | 83.4 | Literal translation artifacts and awkward phrasing |
| French | 80.5 | Needs editing for natural flow |
| Malay | 72.5 | Glaring terminology errors and code-mixing |
| Arabic | 71.9 | Frequent linguistic inaccuracies and awkward phrasing |
| Russian | 70.8 | Untranslated English words and inconsistent formality |
| Portuguese | 70.1 | Ambiguous speaker attribution |
| Vietnamese | 69.8 | Mixed-language intrusion and poor fluency |
| Polish | 69.7 | Significant linguistic flaws and mixed-language error |
| Norwegian | 68.8 | Severe English intrusion and corrupted terms |
| Swedish | 66.8 | Severe linguistic and mechanical defects |
| Japanese | 66.2 | Inconsistent Kansai dialect and mixed languages |
| Korean | 66.2 | Inconsistent tone and unnatural phrasing |
| Macedonian | 62.0 | Severe linguistic degradation |
| Danish | 59.0 | Severe lack of fluency and unnatural phrasing |
| Urdu | 57.9 | Inconsistent script mixing Urdu and Latin |
| Afrikaans | 55.9 | Severe language mixing and errors |
| Nepali | 54.9 | Severe grammar errors and nonsensical vocabulary |
| Bengali | 54.1 | Critical structural defects and pervasive lexical errors |
| Bulgarian | 49.1 | Severe truncation and numerous errors |
| Slovak | 47.1 | Not in valid Slovak |
| Lithuanian | 44.0 | Severe grammatical and semantic errors |
| Esperanto | 43.2 | Catastrophic grammatical errors and neologisms |
| Hungarian | 42.6 | Severe mixed language and broken grammar |
| Catalan | 41.5 | Severe incompleteness due to abrupt cutoff |
| Turkish | 41.1 | Critical incompleteness and formatting errors |
| Romanian | 40.3 | Severe truncation and structural breakdown |
| Slovene | 39.0 | Abrupt termination leaving half untranslated |
| Dutch | 37.9 | Severe incompleteness and linguistic errors |
| German | 37.5 | Catastrophic truncation and gibberish |
| Interlingua | 34.9 | Incomplete and grammatically flawed |
| Latvian | 34.4 | Catastrophic lexical hallucination |
| Greek | 33.9 | Catastrophic mixed-language contamination |
| Galician | 33.1 | Severe loss of content and truncation |
| Chinese | 33.1 | Catastrophic failure with massive content loss and mixed language |
| Finnish | 31.9 | Catastrophic truncation and fragmentation |
| Ukrainian | 31.2 | Severe data corruption and fragmentation |
| Belarusian | 30.8 | Severe degradation and gibberish throughout |
| Persian | 30.6 | Severe structural breakdown and severe incompleteness |
| Azerbaijani | 30.4 | Repetitive name loops and structural corruption |
| Hindi | 27.6 | Severe truncation and corruption into gibberish |
| Tamil | 27.1 | Unusable: broken, fragmented, and incomplete |
| Telugu | 26.5 | Severe nonsense and truncation |
| Hebrew | 26.1 | Catastrophic structural failure and missing text |
| Albanian | 25.8 | Severe collapse into gibberish and repetition |
| Thai | 23.3 | Severe information loss and gibberish |
| Icelandic | 22.4 | Severe truncation and data loss |
| Estonian | 21.9 | Complete failure due to severe grammatical and structural collapse |
| Marathi | 21.4 | Complete structural failure with repetitive name loops |
| Kannada | 20.2 | Repetitive nonsensical loop and gibberish |
| Georgian | 20.1 | Complete failure due to broken grammar and loss of meaning |
| Basque | 19.2 | Catastrophic failure with missing dialogue |
| Khmer | 17.0 | Severe structural corruption and meaningless repetition |
| Tagalog | 15.4 | Complete dialogue truncation resulting in empty lines |
| Swahili | 13.6 | Infinite loop and missing content |
| Serbian | 13.0 | Severe truncation and missing content |
| Lao | 9.8 | Catastrophic structural collapse into gibberish |
| Croatian | 9.2 | Severely incomplete and structurally broken |
| Malayalam | 7.3 | Complete breakdown into corrupted data |
| Sinhala | 6.6 | Severe incomprehensibility and meaningless repetitions |
| Czech | 5.8 | Severe truncation and repetitive speaker name loops |
| Welsh | 5.8 | Catastrophic failure and information loss |
| Armenian | 5.0 | Severe structural failure and nonsensical repetition |
| Mongolian | 4.9 | Severe content degradation and missing text |
| Burmese | 4.2 | Catastrophic quality; unintelligible gibberish |
| Irish | 3.1 | Severe structural defect with empty placeholders |
