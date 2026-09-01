# examples/tr/onde/gemini-3.7-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemini-3.7-flash
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 98 | Minor stylistic padding in conversational fillers |
| Catalan | 97 | High quality with minor stylistic variations |
| Danish | 97 | Near-perfect academic quality |
| Spanish | 97 | High quality with minor stylistic adjustments needed |
| Persian | 97 | Minor fillers and notation inaccuracies |
| Japanese | 97 | Minor terminology refinement needed |
| Polish | 97 | Flawless professional grade with minor stylistic notes |
| Portuguese | 97 | High quality with minor cadence nuances |
| Vietnamese | 97 | Exceptional scientific accuracy and naturalness |
| Afrikaans | 96 | Minor stylistic preferences and terminology alignment needed |
| Galician | 96 | Minor lexical and terminology refinements needed |
| Italian | 96 | Exceptional quality ready for publication |
| Romanian | 96 | Excellent quality with minor stylistic variations |
| Swedish | 96 | Minor colloquial phrasing in math notation |
| Chinese | 96 | Minor terminology preferences |
| Arabic | 95 | Minor typographical artifacts and phrasing adjustments needed |
| Bulgarian | 95 | Minor formatting and terminology preferences |
| Czech | 95 | Minor calques and terminology localization issues |
| Hungarian | 95 | Minor literalisms and filler words |
| Georgian | 95 | Excellent professional quality with negligible stylistic variations |
| Lithuanian | 95 | Minor terminology inconsistencies and stylistic refinements needed |
| Dutch | 95 | High quality with minor typographical errors |
| Russian | 95 | Minor fluency and formatting issues |
| Ukrainian | 95 | Minor stylistic inconsistencies in scientific terminology |
| German | 94 | Minor phrasing issues but high quality |
| Korean | 94 | Non-standard Greek letter transliteration |
| Macedonian | 94 | High quality with minor stylistic refinements needed |
| Telugu | 94 | Minor stylistic issues with formal transitions |
| Hebrew | 92 | Minor stylistic calques and minor terminology inconsistencies |
| Finnish | 91 | Minor typos and non-standard physics terminology |
| Malayalam | 91 | Minor terminology and fluency issues |
| Malay | 91 | Minor stylistic stiffness and non-standard terminology |
| Albanian | 91 | Minor stylistic imperfections requiring polishing |
| Serbian | 91 | Minor terminology and grammatical errors |
| Armenian | 90 | Minor stylistic stiffness and terminology adjustments needed |
| Norwegian | 90 | Minor terminology and formatting issues |
| Turkish | 90 | Minor typographical and phrasing adjustments needed |
| Belarusian | 89 | Minor terminology inaccuracies |
| Khmer | 89 | Minor terminology inaccuracies |
| Indonesian | 88 | Minor terminology inconsistencies and literal phrasing |
| Latvian | 88 | Minor technical and stylistic flaws |
| Mongolian | 88 | Minor terminology and fluency issues |
| Nepali | 88 | High quality with minor phrasing and typo issues |
| Thai | 87 | Minor typos and rigid fluency |
| Azerbaijani | 86 | Minor spelling errors and terminology inconsistencies |
| Marathi | 86 | Minor terminology and fluency issues |
| Esperanto | 84 | Non-standard terminology and calques |
| Hindi | 84 | Minor fluency nits and literal calques |
| Estonian | 83 | Minor technical terminology errors and typos |
| Greek | 82 | Terminology inaccuracies and literal phrasing |
| Basque | 81 | Minor terminology and fluency imperfections |
| Croatian | 81 | Minor calques and syntax issues |
| Kannada | 81 | Significant terminology inaccuracies and fluency issues |
| Burmese | 81 | Minor terminology non-standardization and literal phrasing |
| Sinhala | 81 | Grammatical awkwardness and inconsistent terminology |
| Slovak | 81 | Grammatical errors and terminological inaccuracies |
| Icelandic | 80 | Recurring technical mistranslations |
| Urdu | 80 | Minor fluency issues and notable terminology error |
| Slovene | 76 | Machine-translation artifacts and literal notation |
| Tamil | 73 | Mixed-script artifacts and non-standard terminology |
| Swahili | 70 | Terminology and unnatural phrasing |
| Lao | 69 | Inaccurate physics terminology and stiff phrasing |
| Bengali | 66 | Severe encoding corruption impairs readability |
| Tagalog | 65 | Literal syntax and non-standard terminology |
| Irish | 64 | Technical terminology errors |
| Welsh | 63 | Pervasive lexical and idiomatic errors |
| Interlingua | 52 | Severe foreign-language contamination and code-switching |
