# examples/tr/onde/union-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: union-alpha
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 98 | Exceptional quality with minor stylistic variations |
| Slovak | 98 | Minor typos and non-standard terms |
| Bulgarian | 97 | Minor stylistic polish needed for idiomatic flow |
| Czech | 97 | Excellent quality with minor stylistic improvements needed |
| German | 97 | Minor phrasing and flow imperfections |
| Spanish | 97 | Excellent quality with minor stylistic variations |
| French | 97 | Near-perfect professional grade |
| Italian | 97 | High-quality professional translation |
| Japanese | 97 | Flawless quality with minor stylistic nuances noted |
| Russian | 97 | Minor stylistic adjustments |
| Danish | 96 | Near-flawless execution with only minor stylistic nuances |
| Macedonian | 96 | Minor stylistic and typo issues only |
| Polish | 96 | Minor filler word and typo issues |
| Portuguese | 96 | Minor conversational and idiomatic polishing needed |
| Hebrew | 95 | High quality with minor terminology/stylistic nuances |
| Hungarian | 95 | High quality with minor typographical errors |
| Dutch | 95 | Minor stylistic calques in mathematical notation |
| Norwegian | 95 | Non-standard notation for squared quantities |
| Romanian | 95 | Minor typos and literal phrasing |
| Slovene | 95 | High quality, minor stylistic issues |
| Albanian | 95 | High quality with minor typos and non-standard terms |
| Serbian | 95 | Minor technical inaccuracies and fluency quirks |
| Swedish | 95 | Minor terminology tweaks needed |
| Galician | 94 | High quality with minor typos and style choices |
| Korean | 94 | Minor terminology variations |
| Ukrainian | 94 | Minor register inconsistencies and minor calques |
| Afrikaans | 93 | Minor lexical errors including 'potgooi' for podcast |
| Finnish | 93 | Minor terminology and typo issues |
| Indonesian | 93 | Minor terminology standardization needed |
| Georgian | 93 | Minor stylistic refinements needed for metaphorical phrasing and physics terms |
| Arabic | 92 | Minor stylistic quirks and artifacts |
| Belarusian | 92 | Minor non-standard terminology artifacts |
| Basque | 92 | Minor terminology inconsistencies and anglicisms |
| Persian | 92 | Minor stylistic stiffness in phrasing |
| Hindi | 92 | Minor literal phrasing and fluency issues |
| Bengali | 91 | Minor grammatical imperfections and loanword issues |
| Welsh | 91 | Minor fluency issues and lexical calques |
| Croatian | 91 | Minor technical terminology inaccuracies |
| Armenian | 91 | Minor literal calques and unnatural fillers reduce fluency |
| Lithuanian | 91 | Minor terminology and orthographic errors |
| Latvian | 91 | Minor terminology and spelling errors |
| Nepali | 91 | High quality with minor formatting issues |
| Thai | 91 | High technical accuracy with occasional fluency stiffness |
| Turkish | 91 | Minor stylistic stiffness and literal syntax |
| Vietnamese | 91 | Minor stylistic and terminology adjustments needed |
| Chinese | 91 | Minor terminology preferences for minor flaws |
| Estonian | 90 | Minor terminology inaccuracies and slight literalness |
| Telugu | 90 | Minor literal calques and transliteration inconsistencies |
| Marathi | 89 | Minor flow and phrasing issues persist |
| Esperanto | 88 | Terminology errors and unnatural calques |
| Kannada | 88 | Minor fluency and stylistic stiffness |
| Malayalam | 88 | Minor fluency and phrasing issues |
| Mongolian | 88 | Minor terminology and literal phrasing issues |
| Tamil | 88 | Minor terminology adjustments needed |
| Azerbaijani | 87 | Minor typo and incomplete ending with English text |
| Burmese | 87 | Moderate stiffness in conversational flow |
| Icelandic | 86 | Minor terminology inaccuracies and calques |
| Greek | 85 | Repetitive phrasing and literal terminology |
| Urdu | 85 | Heavy reliance on transliterated technical terms |
| Khmer | 82 | Systematic orthographic errors and technical mistranslations |
| Sinhala | 81 | Scientific terminology errors |
| Interlingua | 80 | Anglicisms and mixed lexicon |
| Malay | 80 | Technical terminology errors |
| Lao | 78 | Inconsistent physics terminology |
| Swahili | 78 | Terminological inaccuracies and literal calques |
| Tagalog | 69 | Non-standard terminology and literal calques |
| Irish | 29 | Foreign character intrusions and lexical errors |
