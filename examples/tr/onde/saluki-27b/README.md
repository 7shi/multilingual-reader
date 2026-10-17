# examples/tr/onde/saluki-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: Underdog Saluki 27B 1.0 (quantized Qwen 3.8 27B)
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 87.9 | Slightly stiff and unnatural phrasing |
| French | 86.6 | Needs editing for natural flow |
| Spanish | 85.0 | French word intrusion and stiff phrasing |
| Indonesian | 83.2 | Literal translation artifacts and awkward phrasing |
| Portuguese | 74.2 | Ambiguous speaker attribution |
| Russian | 73.2 | Untranslated English words and inconsistent formality |
| Arabic | 73.0 | Frequent linguistic inaccuracies and awkward phrasing |
| Malay | 73.0 | Glaring terminology errors and code-mixing |
| Vietnamese | 71.9 | Mixed-language intrusion and poor fluency |
| Polish | 71.2 | Significant linguistic flaws and mixed-language error |
| Norwegian | 70.8 | Severe English intrusion and corrupted terms |
| Japanese | 69.9 | Inconsistent Kansai dialect and mixed languages |
| Korean | 68.8 | Inconsistent tone and unnatural phrasing |
| Swedish | 67.1 | Severe linguistic and mechanical defects |
| Macedonian | 62.2 | Severe linguistic degradation |
| Danish | 60.7 | Severe lack of fluency and unnatural phrasing |
| Urdu | 60.0 | Inconsistent script mixing Urdu and Latin |
| Afrikaans | 58.8 | Severe language mixing and errors |
| Bengali | 55.5 | Critical structural defects and pervasive lexical errors |
| Nepali | 55.5 | Severe grammar errors and nonsensical vocabulary |
| Bulgarian | 49.7 | Severe truncation and numerous errors |
| Slovak | 49.6 | Not in valid Slovak |
| Esperanto | 48.8 | Catastrophic grammatical errors and neologisms |
| Lithuanian | 46.8 | Severe grammatical and semantic errors |
| Hungarian | 46.1 | Severe mixed language and broken grammar |
| Catalan | 43.6 | Severe incompleteness due to abrupt cutoff |
| Turkish | 43.6 | Critical incompleteness and formatting errors |
| Romanian | 43.0 | Severe truncation and structural breakdown |
| German | 42.6 | Catastrophic truncation and gibberish |
| Greek | 39.5 | Catastrophic mixed-language contamination |
| Latvian | 38.5 | Catastrophic lexical hallucination |
| Slovene | 38.4 | Abrupt termination leaving half untranslated |
| Dutch | 38.1 | Severe incompleteness and linguistic errors |
| Interlingua | 37.6 | Incomplete and grammatically flawed |
| Galician | 33.8 | Severe loss of content and truncation |
| Finnish | 33.3 | Catastrophic truncation and fragmentation |
| Chinese | 33.1 | Catastrophic failure with massive content loss and mixed language |
| Persian | 33.0 | Severe structural breakdown and severe incompleteness |
| Belarusian | 32.9 | Severe degradation and gibberish throughout |
| Ukrainian | 32.5 | Severe data corruption and fragmentation |
| Azerbaijani | 30.6 | Repetitive name loops and structural corruption |
| Hindi | 29.6 | Severe truncation and corruption into gibberish |
| Hebrew | 29.3 | Catastrophic structural failure and missing text |
| Tamil | 29.3 | Unusable: broken, fragmented, and incomplete |
| Albanian | 28.4 | Severe collapse into gibberish and repetition |
| Telugu | 26.2 | Severe nonsense and truncation |
| Icelandic | 25.3 | Severe truncation and data loss |
| Marathi | 24.1 | Complete structural failure with repetitive name loops |
| Thai | 23.3 | Severe information loss and gibberish |
| Estonian | 22.3 | Complete failure due to severe grammatical and structural collapse |
| Kannada | 22.2 | Repetitive nonsensical loop and gibberish |
| Basque | 21.9 | Catastrophic failure with missing dialogue |
| Khmer | 19.6 | Severe structural corruption and meaningless repetition |
| Georgian | 19.0 | Complete failure due to broken grammar and loss of meaning |
| Tagalog | 15.5 | Complete dialogue truncation resulting in empty lines |
| Serbian | 15.3 | Severe truncation and missing content |
| Swahili | 13.8 | Infinite loop and missing content |
| Croatian | 13.7 | Severely incomplete and structurally broken |
| Lao | 11.7 | Catastrophic structural collapse into gibberish |
| Malayalam | 8.5 | Complete breakdown into corrupted data |
| Welsh | 7.5 | Catastrophic failure and information loss |
| Sinhala | 6.8 | Severe incomprehensibility and meaningless repetitions |
| Mongolian | 6.7 | Severe content degradation and missing text |
| Czech | 6.5 | Severe truncation and repetitive speaker name loops |
| Armenian | 6.2 | Severe structural failure and nonsensical repetition |
| Burmese | 4.8 | Catastrophic quality; unintelligible gibberish |
| Irish | 4.5 | Severe structural defect with empty placeholders |
