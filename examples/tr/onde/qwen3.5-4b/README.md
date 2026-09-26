# examples/tr/onde/qwen3.5-4b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: qwen3.5:4b
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Chinese | 74.2 | Missing speaker labels and semantic errors |
| Spanish | 72.8 | Severe formatting errors and unnatural syntax |
| Italian | 71.5 | Severe mistranslation of dialogue cues |
| Portuguese | 65.4 | Significant mechanical and semantic errors |
| Indonesian | 65.1 | Severe lexical errors and unnatural phrasing |
| Thai | 64.0 | Severe grammatical errors and Chinese character intrusion |
| German | 63.7 | Severe grammatical and idiomatic errors |
| French | 63.7 | Loss of speaker labels |
| Ukrainian | 63.5 | Grammatical errors and language mixing |
| Vietnamese | 63.2 | Awkward phrasing and literal translations |
| Russian | 62.9 | Mixed-language artifacts and major defects |
| Serbian | 61.3 | Major contextual misinterpretation and hallucination |
| Catalan | 60.2 | Severe structural and grammatical flaws |
| Japanese | 56.4 | Severe mixed-language contamination |
| Bulgarian | 55.7 | Severe grammatical and terminology errors |
| Dutch | 55.5 | Complete collapse of dialogue structure |
| Galician | 54.6 | Mixed-language errors and non-standard forms |
| Romanian | 54.4 | Severe grammatical and syntactic errors |
| Polish | 53.4 | Presence of French words and nonsense Polish |
| Persian | 52.1 | Pervasive OCR errors and hallucinations |
| Malay | 51.6 | Pervasive grammatical and lexical errors |
| Interlingua | 50.8 | Severe mixed Romance language usage |
| Danish | 49.4 | Code-switching to Chinese and severe grammatical errors |
| Czech | 49.2 | Severe grammatical breakdown and gibberish |
| Slovak | 48.6 | Failed with severe grammatical and semantic errors |
| Norwegian | 46.7 | Catastrophic linguistic failures |
| Arabic | 44.8 | Severe grammatical errors and broken dialogue attribution |
| Swedish | 44.3 | Severe grammatical errors and inaccurate terminology |
| Croatian | 43.8 | Mixed language text (German) |
| Turkish | 43.7 | Severe semantic errors and nonsense phrases |
| Macedonian | 43.5 | Severe hallucinations and broken syntax |
| Afrikaans | 42.0 | Severe structural and linguistic errors |
| Esperanto | 41.6 | Catastrophic grammar and vocabulary errors |
| Hindi | 41.5 | Catastrophic mixed-language contamination |
| Albanian | 41.0 | Severe grammatical and lexical errors |
| Korean | 40.9 | Contains large chunks of untranslated Russian text |
| Slovene | 39.8 | Severe linguistic incomprehensibility |
| Bengali | 39.6 | severe linguistic degradation and technical inaccuracies |
| Urdu | 39.2 | Severe grammatical and syntax errors |
| Latvian | 38.1 | Catastrophic lexical and grammatical errors |
| Lithuanian | 37.4 | Severe lexical errors and hallucinations |
| Hungarian | 36.7 | Catastrophic mistranslations and broken syntax |
| Belarusian | 36.5 | Severe lexical corruption and nonsense |
| Nepali | 35.9 | Massive hallucinations and nonsensical phrases |
| Estonian | 35.5 | Catastrophic grammatical errors and mistranslated terminology |
| Finnish | 35.4 | Mixed-language structure and severe grammar errors |
| Marathi | 33.6 | Severe grammatical and terminology errors |
| Icelandic | 33.5 | Severe grammatical and lexical errors |
| Hebrew | 32.3 | Severe generation glitches including Chinese text |
| Telugu | 31.6 | Severe mixed-language errors and nonsense syntax |
| Greek | 31.4 | Severe language mixing with Chinese and English |
| Lao | 30.2 | Extreme hallucination and lexical errors |
| Khmer | 29.8 | Severe hallucination and incoherence |
| Tamil | 29.7 | Major semantic and grammatical defects |
| Tagalog | 29.6 | Nonsensical and unintelligible gibberish |
| Azerbaijani | 29.4 | Severe linguistic errors |
| Swahili | 27.7 | Severe linguistic breakdown and nonsensical output |
| Kannada | 25.2 | Extremely poor quality and unintelligible |
| Malayalam | 24.4 | Lack of linguistic validity and coherence |
| Armenian | 24.0 | Completely nonsensical and unintelligible |
| Basque | 23.7 | Severe grammatical and syntactic breakdown |
| Irish | 23.2 | Completely incomprehensible |
| Burmese | 22.9 | Severe lack of accuracy and coherence |
| Mongolian | 22.3 | Severe semantic errors and nonsensical output |
| Welsh | 21.8 | Severely defective and unintelligible |
| Georgian | 21.4 | Completely unusable and broken |
| Sinhala | 20.8 | Complete linguistic nonsense and incoherence |
