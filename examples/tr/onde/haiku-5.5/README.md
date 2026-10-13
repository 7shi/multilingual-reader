# examples/tr/onde/haiku-5.5/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: Claude Haiku 5.5
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 95.1 | Professional-grade and virtually error-free |
| Spanish | 93.7 | Minor stylistic rigidities |
| Romanian | 93.0 | Occasional stiff phrasing |
| Croatian | 92.8 | Phrasing feels slightly literal |
| Ukrainian | 92.2 | Slight stiffness in phrasing |
| Czech | 92.1 | Minor stylistic choices are slightly less idiomatic |
| German | 91.8 | Few slightly literal phrasings |
| Hungarian | 90.9 | Minor stylistic rigidities and anglicized cadence |
| Dutch | 90.7 | Minor stylistic idiosyncrasies |
| Finnish | 90.5 | Slight literal phrasing reducing naturalness |
| Lithuanian | 90.5 | Minor tonal inconsistencies |
| Slovak | 90.4 | minor stiffness in flow and idioms |
| Polish | 90.2 | Slightly literal and rigid phrasing |
| Russian | 89.8 | Slight translationese and fragmented flow |
| Latvian | 89.4 | Slightly stiff and literal phrasing |
| Catalan | 88.0 | Minor stylistic rigidities and calques from English |
| Danish | 88.0 | Occasional Anglicized sentence structure |
| Indonesian | 88.0 | Minor literal syntax and punctuation |
| Norwegian | 87.4 | Awkward literal translations of idioms and fillers |
| Galician | 87.2 | Slightly formal tone and minor lexical choices |
| Swedish | 86.8 | Slightly rigid phrasing |
| Korean | 86.4 | Inconsistent speech particles and unnatural flow |
| Turkish | 85.8 | Occasional translationese disrupts natural flow |
| Vietnamese | 85.8 | Rigid and unnatural phrasing |
| Swahili | 85.5 | Unnatural and overly literal phrasing |
| Japanese | 85.3 | Artificially hesitant dialogue flow |
| Esperanto | 85.2 | Translationese tendencies and missing accusative markers |
| Estonian | 85.1 | Lexical errors and stiff phrasing |
| Malay | 85.0 | Notable calques and stiff phrasing |
| Welsh | 84.9 | Persistent typo of Helo instead of Helo |
| Slovene | 84.8 | Translationese phrasing and lexical error 'znameno' |
| Albanian | 84.6 | Minor phrasing issues and literal sentence structures |
| Portuguese | 84.3 | Feels like a literal word-for-word conversion |
| Icelandic | 83.0 | Awkward fluency and phrasing |
| Marathi | 82.5 | Rigid syntax and awkward connectors |
| Thai | 81.9 | Stiff and unnatural conversational tone |
| Hebrew | 81.8 | Gloring typo in line 98 |
| Serbian | 81.8 | Inconsistent diacritics and poor math terminology |
| Tagalog | 81.3 | Poor lexical choices and unnatural phrasing |
| Afrikaans | 80.2 | Stiff phrasing and literal translations hinder natural flow |
| Khmer | 79.9 | Terminological inconsistency |
| Italian | 79.8 | Grammatical agreement errors |
| Chinese | 79.5 | Inconsistent terminology and translationese |
| Azerbaijani | 79.2 | Stilted, unnatural phrasing |
| Macedonian | 78.9 | Inconsistent code-switching and awkward phrasing |
| Urdu | 78.9 | Presence of unexpected Chinese characters |
| Basque | 78.5 | Code-switching disrupts fluency |
| Mongolian | 78.5 | Translationese fluency issues |
| Malayalam | 78.2 | Occasionally stiff phrasing disrupts natural flow |
| Bengali | 78.0 | Lacks polish and has pronoun inconsistencies |
| Sinhala | 78.0 | Rigid sentence structures and stiff dialogue flow |
| Lao | 77.6 | Inconsistent terminology |
| Persian | 76.8 | Missing speaker labels |
| Arabic | 76.5 | Occasional awkward phrasing and stiffness |
| Georgian | 76.2 | Terminological inaccuracy |
| Tamil | 76.2 | Inconsistent tone and register |
| Greek | 76.1 | Persistent misuse of character names |
| Hindi | 75.5 | Structural glitch breaking flow |
| Bulgarian | 73.2 | Mixed-language editing artifact in dialogue |
| Belarusian | 71.8 | Missing speaker tags |
| Telugu | 71.0 | Inconsistent formatting and minor grammatical awkwardness |
| Irish | 70.0 | Unnatural syntax due to heavy calques from English |
| Burmese | 69.5 | Inconsistent terminology and non-standard phrasing |
| Interlingua | 69.1 | Grammatical errors |
| Armenian | 68.9 | Code-switching into English |
| Nepali | 66.9 | Awkward literal translation style |
| Kannada | 60.6 | Severe structural fragmentation and omissions |
