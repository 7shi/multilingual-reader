# examples/tr/onde/qwen3.6-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: qwen3.6-27b
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 99 | Minor stylistic literalness |
| Spanish | 96 | Minor register inconsistencies |
| French | 96 | Minor grammatical typo noted across all evaluations |
| Portuguese | 96 | Minor tense inconsistency |
| Japanese | 95 | Minor inconsistencies in notation conventions |
| Dutch | 95 | Minor typo 'betweten' and rigid phrasing |
| Russian | 94 | Minor lexical calques and nuances |
| Chinese | 94 | Excellent accuracy with minor terminology tweaks |
| Italian | 92 | Minor typos and gender agreement errors |
| Vietnamese | 92 | Minor terminology and fluency issues |
| Galician | 89 | Minor grammatical and typographical errors |
| German | 84 | Critical semantic reversal of 'irrefutable' to 'widerlegbar' |
| Polish | 83 | Minor grammatical and typographical errors |
| Ukrainian | 83 | Repeated typos disrupt fluency |
| Slovak | 79 | Grammatical inconsistencies and awkward phrasing |
| Arabic | 78 | Technical accuracy marred by typos and calques |
| Danish | 78 | Semantic mistranslations compromise scientific precision |
| Afrikaans | 77 | Recurring typos and awkward phrasing |
| Hindi | 77 | Excessive literalness hinders fluency |
| Korean | 77 | Mixed-language artifacts and terminology inconsistencies |
| Persian | 75 | Literal phrasing and tone issues |
| Croatian | 74 | Typos and physics terminology errors |
| Romanian | 74 | Grammatical errors and typos |
| Serbian | 74 | Erratic speaker names and terminology errors |
| Turkish | 74 | Significant scientific inaccuracies and errors |
| Swedish | 73 | Critical negation errors and semantic mistranslations |
| Thai | 72 | Mixed Chinese characters disrupt readability |
| Kannada | 71 | Lacks native fluency and technical accuracy |
| Slovene | 71 | Grammatical errors and unnatural phrasing |
| Hungarian | 70 | Severe typos and unnatural literal translations |
| Lithuanian | 69 | Lexical errors and unnatural phrasing |
| Norwegian | 69 | Lexical errors and awkward math phrasing |
| Urdu | 69 | Recurring terminology and filler word errors |
| Latvian | 68 | Severe lexical and grammatical flaws |
| Macedonian | 67 | Anglicized syntax and semantic errors |
| Marathi | 67 | Persistent literalism and unnatural phrasing |
| Bulgarian | 66 | Noticeable MT artifacts and terminology errors |
| Czech | 66 | Grammatical errors and typos |
| Indonesian | 66 | Critical mixed-language glitch (Chinese) |
| Azerbaijani | 62 | Grammatical errors and unnatural phrasing |
| Belarusian | 62 | Multiple mistranslations and unnatural phrasing |
| Nepali | 60 | Literal phrasing and semantic errors |
| Greek | 55 | Severe technical terminology errors |
| Albanian | 55 | Significant semantic errors and lexical inaccuracies |
| Swahili | 55 | Pervasive literal calques and unedited MT artifacts |
| Bengali | 53 | Mixed-language artifacts and poor linguistic quality |
| Esperanto | 48 | Significant scientific terminology errors |
| Armenian | 45 | Hallucinations and mistranslations |
| Georgian | 42 | Severe grammatical errors and unnatural phrasing |
| Finnish | 41 | Pervasive grammatical and lexical errors |
| Interlingua | 38 | Pervasive lexical interference and untranslated terms |
| Mongolian | 38 | Severe machine-translation artifacts and structural defects |
| Malay | 38 | Major terminology errors and code-mixing |
| Hebrew | 37 | Severe MT artifacts and mixed-language errors |
| Welsh | 34 | Pervasive grammatical errors and poor phrasing |
| Sinhala | 34 | Severe linguistic and technical flaws typical of unedited MT |
| Telugu | 34 | Pervasive major defects and mistranslations |
| Icelandic | 33 | P pervasive grammatical and terminology errors |
| Tamil | 33 | Pivotal technical mistranslations and pervasive terminology errors |
| Estonian | 32 | Major defects: severe lexical errors, grammatical breakdowns, and corrupted scientific terminology |
| Khmer | 32 | Severe scientific terminology errors and unnatural syntax |
| Basque | 31 | Severe mistranslation of scientific meaning and syntax |
| Tagalog | 31 | Severe lexical and meaning-inverting errors |
| Burmese | 29 | Severe technical inaccuracies and mistranslation of physics concepts |
| Irish | 28 | Pervasive grammatical errors and incorrect physics terminology |
| Lao | 25 | Severe machine-translation artifacts and terminology errors |
| Malayalam | 25 | Severe mixed-script artifacts and structural defects |
