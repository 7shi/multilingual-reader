# examples/tr/onde/flint/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: flint (40B-A2.5B MoE)
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 79.0 | Awkward literal calques and formatting errors |
| French | 73.2 | Persistent grammatical errors |
| Portuguese | 71.7 | Dropped speaker labels and literal calques |
| Spanish | 69.5 | Lost speaker labels and grammar errors |
| Danish | 68.4 | Severe grammatical and lexical errors |
| Dutch | 67.0 | Significant grammatical errors and unnatural phrasing |
| Vietnamese | 66.3 | Egregious mistranslations and tonal inconsistency |
| Russian | 65.7 | Frequent mistranslations and awkward phrasing |
| Chinese | 64.8 | Severe structural and coherence failures |
| Swedish | 61.8 | Severe structural and linguistic failures |
| Indonesian | 60.4 | Severe grammatical and terminology errors |
| Galician | 60.2 | Severe corruption with Portuguese lexical items |
| Japanese | 60.1 | Missing dialogue and wrong speaker tags |
| Turkish | 59.6 | Severe syntactic breakdowns |
| Nepali | 59.5 | Pervasive structural and linguistic errors |
| Korean | 59.3 | Inconsistent politeness levels and awkward syntax |
| Norwegian | 58.7 | Severe language contamination and structural corruption |
| German | 58.3 | Severe structural and formatting errors |
| Arabic | 58.2 | Grammatical gender inconsistencies and incorrect terminology |
| Malay | 57.9 | Severe dialogue attribution errors |
| Persian | 57.3 | Severe structural degradation and chaotic formatting |
| Catalan | 56.2 | Severe terminology and factual errors |
| Ukrainian | 55.6 | Severe grammatical and terminological errors |
| Hungarian | 55.0 | Severe grammatical errors and nonsensical vocabulary |
| Czech | 54.8 | Fundamentally flawed and unusable |
| Croatian | 53.4 | Pervasive grammatical and terminology errors |
| Tamil | 52.7 | Severe grammatical and terminology errors |
| Polish | 52.4 | Missing speaker tags and mechanical errors |
| Greek | 50.9 | Severe grammatical and lexical errors |
| Hindi | 49.9 | Severe structural and grammatical failures |
| Marathi | 48.5 | Severe grammatical and syntactic errors |
| Serbian | 48.1 | Severe grammatical and vocabulary errors |
| Interlingua | 47.9 | Major mixed-language defect |
| Afrikaans | 47.0 | Comprehensively unintelligible due to severe linguistic breakdowns |
| Thai | 46.9 | Severe orthographic and grammatical errors |
| Bulgarian | 46.4 | Severe grammatical and terminology errors |
| Swahili | 46.2 | Critical structural and grammatical failures |
| Sinhala | 45.9 | Severe linguistic errors and nonsense |
| Finnish | 45.7 | Severe linguistic and grammatical failures |
| Tagalog | 45.6 | Severe linguistic errors and unnatural phrasing |
| Hebrew | 45.5 | Severe linguistic and terminology errors |
| Slovene | 45.3 | Severe grammatical and lexical errors |
| Telugu | 44.4 | Severe terminology and grammar errors |
| Bengali | 44.2 | Severe grammar errors and incorrect physics terminology |
| Slovak | 42.8 | Heavily corrupted Czech with severe errors |
| Kannada | 41.3 | Catastrophic errors violating basic language principles |
| Esperanto | 41.2 | Severe lexical and grammatical failures |
| Urdu | 40.9 | Severe grammatical and terminology failures |
| Lithuanian | 40.8 | Catastrophic grammatical errors |
| Malayalam | 39.6 | Severe mistranslations and nonsensical phrasing |
| Macedonian | 37.9 | Severe grammatical errors and inaccurate terminology |
| Romanian | 37.9 | Catastrophic failures in grammar and syntax |
| Basque | 36.6 | Severe grammatical errors and nonsensical phrasing |
| Irish | 35.2 | Severe grammatical errors and invented vocabulary |
| Estonian | 33.8 | Incoherent and unintelligible |
| Icelandic | 32.5 | Catastrophic grammatical collapse and hallucination |
| Belarusian | 32.0 | Unintelligible gibberish and severe errors |
| Albanian | 31.4 | Systematic misuse of vocabulary and grammar renders text incomprehensible |
| Azerbaijani | 30.8 | Severe grammatical and vocabulary errors |
| Lao | 29.8 | Severe hallucination and nonsensical phrasing |
| Khmer | 28.6 | Severe hallucination and nonsense |
| Burmese | 28.1 | Severe loss of meaning and coherence |
| Georgian | 27.4 | Complete gibberish and hallucinated text |
| Mongolian | 26.8 | Completely unintelligible gibberish |
| Latvian | 26.3 | Severely garbled and nonsensical output |
| Welsh | 24.1 | Complete linguistic and structural collapse |
| Armenian | 16.1 | Complete nonsense gibberish |
