# examples/tr/onde/qwen3.5-4b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: qwen3.5:4b
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Chinese | 73.6 | Missing speaker labels and semantic errors |
| Italian | 71.8 | Severe mistranslation of dialogue cues |
| Spanish | 70.2 | Severe formatting errors and unnatural syntax |
| Portuguese | 68.6 | Significant mechanical and semantic errors |
| Vietnamese | 67.0 | Awkward phrasing and literal translations |
| Russian | 65.8 | Mixed-language artifacts and major defects |
| Ukrainian | 65.8 | Grammatical errors and language mixing |
| Indonesian | 63.2 | Severe lexical errors and unnatural phrasing |
| Serbian | 62.5 | Major contextual misinterpretation and hallucination |
| Thai | 62.1 | Severe grammatical errors and Chinese character intrusion |
| German | 61.8 | Severe grammatical and idiomatic errors |
| French | 61.8 | Loss of speaker labels |
| Galician | 60.2 | Mixed-language errors and non-standard forms |
| Catalan | 59.3 | Severe structural and grammatical flaws |
| Japanese | 56.1 | Severe mixed-language contamination |
| Polish | 55.9 | Presence of French words and nonsense Polish |
| Bulgarian | 55.5 | Severe grammatical and terminology errors |
| Dutch | 54.6 | Complete collapse of dialogue structure |
| Persian | 54.2 | Pervasive OCR errors and hallucinations |
| Romanian | 53.5 | Severe grammatical and syntactic errors |
| Danish | 52.6 | Code-switching to Chinese and severe grammatical errors |
| Malay | 52.4 | Pervasive grammatical and lexical errors |
| Norwegian | 52.2 | Catastrophic linguistic failures |
| Czech | 51.8 | Severe grammatical breakdown and gibberish |
| Interlingua | 51.8 | Severe mixed Romance language usage |
| Slovak | 51.0 | Failed with severe grammatical and semantic errors |
| Swedish | 48.4 | Severe grammatical errors and inaccurate terminology |
| Turkish | 46.4 | Severe semantic errors and nonsense phrases |
| Esperanto | 46.1 | Catastrophic grammar and vocabulary errors |
| Croatian | 46.0 | Mixed language text (German) |
| Macedonian | 45.4 | Severe hallucinations and broken syntax |
| Arabic | 45.3 | Severe grammatical errors and broken dialogue attribution |
| Afrikaans | 45.1 | Severe structural and linguistic errors |
| Korean | 45.1 | Contains large chunks of untranslated Russian text |
| Albanian | 44.1 | Severe grammatical and lexical errors |
| Slovene | 43.3 | Severe linguistic incomprehensibility |
| Urdu | 43.0 | Severe grammatical and syntax errors |
| Hindi | 42.0 | Catastrophic mixed-language contamination |
| Latvian | 42.0 | Catastrophic lexical and grammatical errors |
| Bengali | 41.1 | severe linguistic degradation and technical inaccuracies |
| Estonian | 40.9 | Catastrophic grammatical errors and mistranslated terminology |
| Hungarian | 40.9 | Catastrophic mistranslations and broken syntax |
| Lithuanian | 40.4 | Severe lexical errors and hallucinations |
| Belarusian | 39.1 | Severe lexical corruption and nonsense |
| Nepali | 38.8 | Massive hallucinations and nonsensical phrases |
| Finnish | 38.0 | Mixed-language structure and severe grammar errors |
| Greek | 37.2 | Severe language mixing with Chinese and English |
| Marathi | 37.2 | Severe grammatical and terminology errors |
| Icelandic | 35.8 | Severe grammatical and lexical errors |
| Hebrew | 35.5 | Severe generation glitches including Chinese text |
| Telugu | 33.3 | Severe mixed-language errors and nonsense syntax |
| Lao | 32.2 | Extreme hallucination and lexical errors |
| Azerbaijani | 31.4 | Severe linguistic errors |
| Tamil | 30.3 | Major semantic and grammatical defects |
| Khmer | 30.0 | Severe hallucination and incoherence |
| Tagalog | 29.8 | Nonsensical and unintelligible gibberish |
| Kannada | 27.1 | Extremely poor quality and unintelligible |
| Swahili | 26.2 | Severe linguistic breakdown and nonsensical output |
| Malayalam | 26.1 | Lack of linguistic validity and coherence |
| Basque | 25.2 | Severe grammatical and syntactic breakdown |
| Mongolian | 25.1 | Severe semantic errors and nonsensical output |
| Irish | 25.0 | Completely incomprehensible |
| Armenian | 24.4 | Completely nonsensical and unintelligible |
| Burmese | 23.5 | Severe lack of accuracy and coherence |
| Welsh | 22.8 | Severely defective and unintelligible |
| Georgian | 22.3 | Completely unusable and broken |
| Sinhala | 22.1 | Complete linguistic nonsense and incoherence |
