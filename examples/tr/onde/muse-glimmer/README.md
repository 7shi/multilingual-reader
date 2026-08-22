# examples/tr/onde/muse-glimmer/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: muse-glimmer
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Portuguese | 96 | Minor grammar and filler word issues |
| Spanish | 95 | Minor lexical and idiomatic improvements needed |
| Italian | 95 | Minor terminology conventions and minor stylistic adjustments |
| Vietnamese | 93 | Excellent accuracy and natural flow |
| Japanese | 92 | Excellent quality with minor phrasing adjustments needed |
| Chinese | 91 | Minor literal phrasing affecting fluency |
| Catalan | 89 | Lexical mistranslations ('rosseca', 'ressecca') |
| Macedonian | 89 | Minor calques and stiff phrasing |
| Dutch | 89 | Minor stylistic and phrasing issues |
| Polish | 89 | Minor grammatical and fluency issues |
| Bulgarian | 86 | Literal conversational fillers disrupt fluency |
| Persian | 86 | Noticeable fluency issues and mixed-language defects |
| French | 85 | Grammatical errors and inconsistent register |
| Turkish | 85 | Minor fluency issues from literal calques |
| Danish | 84 | Minor grammatical errors and terminology issues |
| Galician | 82 | Notable lexical and morphological errors requiring proofreading |
| Korean | 82 | Non-standard terminology and code-switching detract from fluency |
| Urdu | 82 | Minor issues with terminology consistency and naturalness |
| Afrikaans | 80 | Untranslated English terms and typos |
| Lithuanian | 79 | Technical errors and unnatural phrasing |
| Arabic | 78 | Grammatical errors and duplicate line glitches hinder fluency |
| Slovak | 78 | Grammatical errors and lack of fluency |
| Ukrainian | 78 | Grammatical inconsistencies and literal calques |
| Malay | 76 | Terminology precision issues and Anglicisms |
| Romanian | 76 | Grammatical inconsistencies and lack of polish |
| Croatian | 75 | Recurring grammatical errors and mistranslations |
| German | 74 | Noticeable grammatical inaccuracies |
| Swedish | 74 | Noticeable grammatical awkwardness and duplication errors |
| Armenian | 73 | Calques and lack of natural flow |
| Serbian | 72 | Persistent grammatical errors and terminology mistranslations |
| Czech | 71 | Grammatical errors and awkward calques |
| Hungarian | 71 | Severe fluency issues and typos |
| Slovene | 71 | Grammatical errors and unnatural phrasing |
| Indonesian | 67 | Repetition of dialogue lines and terminology errors |
| Hebrew | 65 | Severe linguistic and terminology errors |
| Estonian | 64 | Numerous typos and technical errors |
| Azerbaijani | 63 | Literal calques and stiff syntax |
| Norwegian | 63 | Grammatical errors, unidiomatic math phrasing, and duplication artifacts |
| Basque | 62 | Mixed language errors and duplication artifacts |
| Swahili | 62 | Significant literal translation artifacts and terminology errors |
| Mongolian | 60 | Pervasive fluency issues and literal phrasing |
| Belarusian | 59 | Multiple machine-translation artifacts and errors |
| Georgian | 57 | Mixed-language artifact and key mistranslations |
| Finnish | 56 | Pervasive grammatical errors and unnatural phrasing |
| Latvian | 53 | Pervasive grammatical and terminology errors |
| Icelandic | 51 | Grammar and terminology errors |
| Welsh | 50 | Pervasive lexical and grammatical errors |
| Tagalog | 50 | Severe machine-translation artifacts and unnatural phrasing |
| Russian | 48 | Grammatical errors and repetition artifacts |
| Greek | 45 | Critical physics terminology errors and unnatural phrasing |
| Irish | 43 | Pervasive grammatical errors and unnatural phrasing |
| Albanian | 43 | Severe grammatical and syntactic defects |
| Telugu | 42 | Severe grammar and terminology flaws |
| Bengali | 41 | Severe orthographical and grammatical errors |
| Thai | 39 | Severe typographical and orthographic corruption |
| Hindi | 38 | Pervasive typographical and formatting errors |
| Esperanto | 36 | Critical terminology errors and grammatical defects |
| Marathi | 35 | Pervasive grammatical errors and unnatural syntax |
| Malayalam | 34 | Pervasive grammatical errors and unnatural syntax |
| Nepali | 34 | Severe machine-translation artifacts and broken syntax |
| Lao | 32 | Severe errors in technical terminology and fluency |
| Kannada | 29 | Severe technical and linguistic defects |
| Interlingua | 27 | Severe linguistic and structural flaws including code artifacts |
| Khmer | 24 | Severe corruption and unintelligibility |
| Sinhala | 23 | Severe grammatical and linguistic errors |
| Tamil | 21 | Pervasive repetitive loops and broken syntax |
| Burmese | 12 | Severe character corruption and structural breakdown |
