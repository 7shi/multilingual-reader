# examples/tr/onde/haiku-5.5/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: Claude Haiku 5.5
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.1 | Minor stylistic rigidities |
| French | 93.1 | Professional-grade and virtually error-free |
| Portuguese | 92.5 | Feels like a literal word-for-word conversion |
| Dutch | 92.4 | Minor stylistic idiosyncrasies |
| German | 91.3 | Few slightly literal phrasings |
| Hungarian | 91.0 | Minor stylistic rigidities and anglicized cadence |
| Ukrainian | 90.2 | Slight stiffness in phrasing |
| Romanian | 90.1 | Occasional stiff phrasing |
| Polish | 90.0 | Slightly literal and rigid phrasing |
| Croatian | 89.9 | Phrasing feels slightly literal |
| Lithuanian | 89.7 | Minor tonal inconsistencies |
| Finnish | 89.6 | Slight literal phrasing reducing naturalness |
| Catalan | 89.5 | Minor stylistic rigidities and calques from English |
| Slovak | 89.4 | minor stiffness in flow and idioms |
| Czech | 89.1 | Minor stylistic choices are slightly less idiomatic |
| Vietnamese | 88.9 | Rigid and unnatural phrasing |
| Russian | 88.5 | Slight translationese and fragmented flow |
| Indonesian | 88.0 | Minor literal syntax and punctuation |
| Galician | 87.8 | Slightly formal tone and minor lexical choices |
| Japanese | 87.2 | Artificially hesitant dialogue flow |
| Latvian | 87.2 | Slightly stiff and literal phrasing |
| Malay | 87.2 | Notable calques and stiff phrasing |
| Korean | 86.7 | Inconsistent speech particles and unnatural flow |
| Norwegian | 86.6 | Awkward literal translations of idioms and fillers |
| Swedish | 86.5 | Slightly rigid phrasing |
| Italian | 85.8 | Grammatical agreement errors |
| Turkish | 85.5 | Occasional translationese disrupts natural flow |
| Afrikaans | 84.7 | Stiff phrasing and literal translations hinder natural flow |
| Estonian | 84.7 | Lexical errors and stiff phrasing |
| Welsh | 83.5 | Persistent typo of Helo instead of Helo |
| Thai | 83.5 | Stiff and unnatural conversational tone |
| Icelandic | 83.4 | Awkward fluency and phrasing |
| Danish | 83.0 | Occasional Anglicized sentence structure |
| Esperanto | 83.0 | Translationese tendencies and missing accusative markers |
| Chinese | 83.0 | Inconsistent terminology and translationese |
| Urdu | 82.7 | Presence of unexpected Chinese characters |
| Slovene | 82.2 | Translationese phrasing and lexical error 'znameno' |
| Albanian | 82.1 | Minor phrasing issues and literal sentence structures |
| Swahili | 81.9 | Unnatural and overly literal phrasing |
| Bengali | 81.1 | Lacks polish and has pronoun inconsistencies |
| Macedonian | 80.6 | Inconsistent code-switching and awkward phrasing |
| Serbian | 80.5 | Inconsistent diacritics and poor math terminology |
| Azerbaijani | 80.2 | Stilted, unnatural phrasing |
| Marathi | 80.2 | Rigid syntax and awkward connectors |
| Basque | 80.1 | Code-switching disrupts fluency |
| Greek | 79.2 | Persistent misuse of character names |
| Hebrew | 79.2 | Gloring typo in line 98 |
| Tagalog | 79.0 | Poor lexical choices and unnatural phrasing |
| Sinhala | 78.9 | Rigid sentence structures and stiff dialogue flow |
| Mongolian | 78.4 | Translationese fluency issues |
| Malayalam | 78.3 | Occasionally stiff phrasing disrupts natural flow |
| Tamil | 77.7 | Inconsistent tone and register |
| Khmer | 77.5 | Terminological inconsistency |
| Georgian | 77.0 | Terminological inaccuracy |
| Lao | 77.0 | Inconsistent terminology |
| Persian | 76.2 | Missing speaker labels |
| Hindi | 76.0 | Structural glitch breaking flow |
| Bulgarian | 75.8 | Mixed-language editing artifact in dialogue |
| Arabic | 75.0 | Occasional awkward phrasing and stiffness |
| Burmese | 71.6 | Inconsistent terminology and non-standard phrasing |
| Irish | 70.5 | Unnatural syntax due to heavy calques from English |
| Armenian | 70.1 | Code-switching into English |
| Belarusian | 69.7 | Missing speaker tags |
| Interlingua | 69.5 | Grammatical errors |
| Kannada | 65.3 | Severe structural fragmentation and omissions |
| Nepali | 64.0 | Awkward literal translation style |
| Telugu | 63.7 | Inconsistent formatting and minor grammatical awkwardness |
