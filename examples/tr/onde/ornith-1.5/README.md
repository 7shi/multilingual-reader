# examples/tr/onde/ornith-1.5/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: ornith-1.5:122b (122B-A10B MoE, tuned from Qwen3.5 122B-A10B)
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Portuguese | 91.7 | Slight stiffness in transitional phrases |
| Russian | 91.6 | Inconsistent pronoun register |
| Vietnamese | 88.8 | Minor stylistic stiffness from literalness |
| Chinese | 88.4 | Minor syntactic stiffness |
| Galician | 88.0 | Occasional translationese and literal adherence to English syntax |
| Italian | 87.8 | Grammar error and awkward phrasing |
| Arabic | 87.4 | Significant translationese and awkward phrasing |
| Latvian | 86.6 | Notably literal translationese and stiff fluency |
| Dutch | 86.2 | Translationese and literal calques |
| Romanian | 86.0 | Frequent typos and unnatural phrasing |
| Malay | 84.5 | Stylistically rough phrasing |
| Lithuanian | 83.8 | Grammatical errors and unnatural phrasing |
| Polish | 82.8 | Lacks naturalness due to awkward phrasing |
| Slovak | 82.8 | Direct calques from English |
| Czech | 81.5 | Awkward phrasing and inconsistent register |
| Bulgarian | 81.2 | Inconsistent name localization |
| Turkish | 80.8 | Lacks natural idiomatic flow |
| Hebrew | 80.6 | Unnatural literalness in interjections and phrasing |
| Armenian | 80.6 | Noticeable lack of fluency and naturalness |
| Persian | 80.5 | Retains English interjections |
| French | 80.0 | Significant speaker attribution error |
| Ukrainian | 79.8 | Inconsistent register and terminology |
| Spanish | 78.9 | Misattribution of speaker tags |
| Finnish | 77.0 | Critical role-switching and fluency errors |
| Macedonian | 76.9 | Grammatical errors and awkward phrasing |
| Afrikaans | 76.2 | Critical omission of dialogue line |
| Thai | 76.0 | Vietnamese word insert and mechanical errors |
| Serbian | 75.7 | Role reversal between Camille and Luc |
| Esperanto | 75.6 | Systematic mistranslation of fillers as "or" |
| German | 75.5 | Frequent grammatical errors |
| Japanese | 74.5 | Inclusion of untranslated Chinese characters |
| Albanian | 74.2 | Grammatical errors and unnatural phrasing |
| Danish | 74.0 | Glitch: 'No response requested' pasted as dialogue |
| Mongolian | 72.6 | Rigid literal translation lacking naturalness |
| Icelandic | 72.4 | Inconsistent capitalization of common nouns |
| Khmer | 72.4 | Untranslated Vietnamese/Chinese artifacts present |
| Korean | 71.4 | Presence of Chinese/English intrusions |
| Urdu | 69.9 | Lacks fluency and naturalness |
| Slovene | 69.7 | Severe grammatical errors and scientific mistranslations |
| Georgian | 69.2 | Overuse of awkward filler words |
| Norwegian | 68.9 | Severe mistranslation of "clever" as "clown" |
| Indonesian | 68.6 | Rigid adherence to English structure causing unnatural phrasing |
| Hindi | 68.1 | Severe grammatical and script inconsistencies |
| Hungarian | 66.1 | Unnatural phrasing and a few dropped speaker labels |
| Belarusian | 65.5 | Poor fluency and lexical inconsistency |
| Swedish | 64.1 | Severe speaker misattribution and dialogue disruption |
| Croatian | 63.9 | Speaker labels dropped and swapped near the end |
| Basque | 63.8 | Major defects with mixed languages and broken syntax |
| Lao | 63.8 | Inconsistent terminology and untranslated English terms |
| Interlingua | 62.4 | Severe speaker misattribution and mixed-language interference |
| Bengali | 62.1 | Incomplete translation with English remnants |
| Sinhala | 61.8 | Severe mistranslations and garbled output |
| Catalan | 61.1 | Back-channels replaced by invented monologues |
| Marathi | 60.7 | Significant linguistic and technical defects |
| Estonian | 59.8 | Severe fidelity and terminology errors |
| Swahili | 58.9 | Inaccurate physics terminology and notation |
| Nepali | 58.6 | Severely flawed literal machine translation |
| Welsh | 57.8 | Catastrophic speaker misattribution and severe grammatical errors |
| Tagalog | 57.1 | Severe linguistic unnaturalness and inconsistent code-switching |
| Kannada | 56.6 | Inconsistent script and terminology errors |
| Greek | 56.2 | Severe mistranslation errors |
| Telugu | 55.8 | Severe grammatical errors |
| Azerbaijani | 55.0 | Speaker labels lost after line 63 |
| Malayalam | 52.7 | Pervasive nonsensical terms and structures |
| Tamil | 52.0 | Severe grammatical and scientific errors |
| Burmese | 47.7 | Catastrophic phonetic substitution and semantic drift |
| Irish | 6.0 | Repeats a "no text provided" notice after line 4 |
