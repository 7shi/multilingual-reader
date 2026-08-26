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
| Portuguese | 96 | Minor typo and filler word retention |
| Spanish | 95 | Minor phrasing and gender agreement issues |
| Italian | 95 | Minor terminology variations for strict academic standards |
| Vietnamese | 93 | Excellent technical accuracy with minor conversational phrasing issues |
| Japanese | 92 | Minor phrasing and nuance issues |
| Chinese | 91 | Minor fluency and terminology issues |
| Catalan | 89 | Lexical mistranslations and anglicisms |
| Macedonian | 89 | Notable calques and awkward phrasing |
| Dutch | 89 | Minor stylistic and grammatical inaccuracies |
| Polish | 89 | Minor terminology inaccuracies and fluency issues |
| Bulgarian | 86 | Technical accuracy hindered by unnatural filler words |
| Persian | 86 | Notable fluency issues and untranslated 'ripple' |
| French | 85 | Grammatical errors and 'rideau' mistranslation |
| Turkish | 85 | Minor fluency issues from literal calques |
| Danish | 84 | Minor grammatical and terminology errors |
| Galician | 82 | Minor errors and Portuguese/Spanish interference |
| Korean | 82 | Mixed-language typo and non-standard terminology |
| Urdu | 82 | Inconsistent terminology and unnatural phrasing |
| Afrikaans | 80 | Untranslated English terms and typos |
| Lithuanian | 79 | Notable grammatical errors and non-standard calques |
| Slovak | 78 | Good accuracy with grammatical and fluency issues |
| Ukrainian | 78 | Direct calques and a textual duplication error |
| Malay | 76 | Terminology precision issues and Anglicisms |
| Romanian | 76 | Grammatical inconsistencies and loanwords |
| Arabic | 75 | Systematic grammatical and fluency issues |
| Croatian | 75 | Frequent grammatical errors and terminology issues |
| German | 74 | Grammar and phrasing issues |
| Swedish | 74 | Notable grammatical awkwardness and duplication error |
| Armenian | 73 | Notable machine-translation artifacts and literal calques |
| Serbian | 72 | Persistent grammatical errors and specific term mistranslations |
| Czech | 71 | Frequent Czech grammatical errors and case governance issues |
| Hungarian | 71 | Severe fluency and mechanical errors |
| Slovene | 71 | Grammatical errors and literal calques |
| Indonesian | 67 | Repetitive dialogue lines and terminology errors |
| Hebrew | 65 | Severe linguistic issues and terminology errors |
| Estonian | 64 | Persistent grammatical errors and non-standard terminology |
| Azerbaijani | 63 | Obvious machine translation artifacts |
| Norwegian | 63 | Grammatical errors and duplicated lines |
| Basque | 62 | Major grammatical errors and language mix-ups |
| Swahili | 62 | Significant literal calques and inaccurate physics terminology |
| Mongolian | 60 | Pervasive fluency and grammatical issues |
| Belarusian | 59 | Numerous MT artifacts and errors |
| Georgian | 57 | Critical mistranslations and mixed-language artifacts |
| Finnish | 56 | Severe grammatical errors and literal phrasing |
| Latvian | 53 | Pervasive grammatical and terminology errors |
| Icelandic | 51 | Significant mathematical and terminology errors |
| Welsh | 50 | Pervasive spelling and grammatical errors with mistranslated technical terms |
| Tagalog | 50 | Severe linguistic and grammatical flaws |
| Russian | 48 | Pervasive grammatical errors and structural repetitions |
| Greek | 45 | Critical terminology errors and grammatical flaws |
| Irish | 43 | Severe grammatical errors and awkward phrasing |
| Albanian | 43 | Severe grammatical and morphological errors |
| Telugu | 42 | Severe grammatical and terminology defects |
| Bengali | 41 | Severe orthographical and grammatical errors |
| Tamil | 40 | Pervasive typographical errors |
| Thai | 39 | Severe typographical and orthographic errors |
| Hindi | 38 | Pervasive typographical errors and inconsistent rendering |
| Esperanto | 36 | Systematic technical and grammatical defects |
| Kannada | 35 | Pervasive grammatical errors and critical semantic mistranslations |
| Marathi | 35 | Severe grammatical errors and unnatural syntax |
| Malayalam | 34 | Severe grammatical and syntactic errors |
| Nepali | 34 | Severe machine-translation artifacts and grammatical errors |
| Lao | 32 | Systematic terminology errors and pervasive typos |
| Interlingua | 27 | Severe structural defects and mixed-language contamination |
| Sinhala | 23 | Severe grammatical and technical errors make it incomprehensible |
| Burmese | 17 | Severe encoding corruption and structural breakdown |
| Khmer | 16 | Catastrophic character corruption and gibberish |
