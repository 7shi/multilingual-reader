# examples/tr/onde/gemma4/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemma4:26b
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The quality trend for each language, based on the evaluation results (`SCORES.txt`) and manual content verification, is as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 100 | Flawless scientific accuracy and natural flow |
| Japanese | 97 | Perfect professional-grade translation |
| Russian | 97 | Minor typos and inconsistent pronouns |
| Vietnamese | 97 | Exceptional quality, nearly perfect |
| Arabic | 96 | Near-perfect execution with minor stylistic literalness |
| Persian | 96 | High professional accuracy with minor tone inconsistencies |
| Chinese | 96 | Near-perfect, professional-quality translation with minor quibbles |
| Finnish | 95 | Minor typographical and phrasing imperfections |
| Korean | 95 | Minor phrasing and fluency issues |
| German | 94 | Near-perfect with minor stylistic polishing needed |
| Spanish | 93 | Mistranslation of ingenuity as ingenuidad |
| Serbian | 93 | Accurate yet requires minor terminology polishing |
| Ukrainian | 93 | High quality with minor physics term standardization needed |
| Danish | 92 | Minor typos and slight literalness |
| Italian | 92 | Minor lexical and grammatical tweaks needed |
| Portuguese | 92 | Minor typo 'Constantes' instead of 'Constantemente' |
| Armenian | 91 | Minor stylistic and typographical errors |
| Polish | 91 | Minor stylistic and idiomatic imperfections |
| Turkish | 91 | Minor phrasing and formatting issues |
| Hebrew | 89 | Major grammatical, terminology, and formatting defects |
| Croatian | 89 | Minor grammatical and terminology issues |
| Norwegian | 89 | Minor terminology inconsistencies in mathematical notation |
| Swedish | 88 | Minor fluency and idiomatic issues |
| Indonesian | 86 | Minor terminology and phrasing adjustments needed |
| Malay | 86 | Minor technical terminology errors and calques |
| Albanian | 83 | Minor terminology and phrasing issues |
| Afrikaans | 82 | 'potgooi' lexical error for podcast |
| Swahili | 82 | Minor typos and terminology issues |
| Bulgarian | 80 | Minor technical and grammatical errors |
| Azerbaijani | 78 | Multiple typographical and spelling errors |
| Czech | 78 | Minor grammatical and fluency issues with some artifacts |
| Galician | 78 | Portuguese/Spanish lexical interference and orthographic errors |
| Dutch | 78 | Minor fluency and idiomatic phrasing issues |
| Macedonian | 76 | Significant typographical and grammatical errors |
| Mongolian | 76 | Minor lexical and grammatical artifacts |
| Hindi | 75 | Grammatical errors and typographical issues |
| Catalan | 74 | Numerous typos and grammatical errors |
| Urdu | 72 | Critical terminology error and inconsistent phrasing |
| Tagalog | 70 | Major lexical inaccuracies and non-standard terminology |
| Lao | 68 | Terminology errors and awkward phrasing |
| Marathi | 67 | Systemic orthographic and grammatical errors undermine fluency |
| Slovak | 66 | Typographical errors, grammatical inconsistencies, and awkward phrasing |
| Romanian | 64 | Multiple grammatical errors and unnatural phrasing |
| Telugu | 64 | Inconsistent terminology and anglicized syntax |
| Georgian | 60 | Foreign language artifacts and grammatical errors |
| Nepali | 60 | Widespread typos and poor fluency |
| Slovene | 58 | Pervasive typos, grammar errors, and untranslated English |
| Bengali | 54 | Systematic typographical and terminology errors |
| Khmer | 54 | Severe orthographic and spelling errors |
| Greek | 53 | Critical terminology errors and text corruption |
| Kannada | 50 | Severe orthographic and grammatical errors |
| Malayalam | 49 | Pervasive orthographic and grammatical errors |
| Thai | 46 | Pervasive spelling and orthographic errors |
| Tamil | 43 | Severe orthographic and grammatical errors |
| Belarusian | 35 | Severe mixed-language artifacts and terminology errors |
| Hungarian | 35 | Severe code-switching with mixed languages |
| Burmese | 34 | Pervasive orthographic corruption |
| Sinhala | 32 | Systematic orthographic and grammatical errors |
| Esperanto | 31 | Severe mixed-language contamination |
| Icelandic | 23 | Severe grammatical errors and incorrect terminology |
| Lithuanian | 23 | Severe structural defects and pervasive grammatical errors |
| Estonian | 22 | Severe structural defects and mixed languages |
| Interlingua | 20 | Severe contamination with multiple foreign languages and mixed scripts |
| Latvian | 20 | Severe mixed-language contamination and structural defects |
| Welsh | 16 | Severe lexical hallucination and grammatical corruption |
| Basque | 15 | Pervasive language mixing and severe grammatical errors |
| Irish | 9 | Catastrophic linguistic breakdown and artifacts |
