# examples/tr/onde/ox-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: ox-alpha (glm-5.3-flash stealth)
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 97 | Flawless high-quality scientific localization |
| Spanish | 97 | Near-perfect professional quality with minor stylistic nuances |
| French | 97 | Minor tu/vous inconsistency |
| Italian | 97 | Exceptionally high quality with minor stylistic flaws |
| Polish | 97 | Minor fluency issues and calques |
| Portuguese | 97 | Nearly flawless professional quality |
| Swedish | 97 | Exceptional quality and accuracy with no critical defects |
| Ukrainian | 97 | Professional grade with minor issues |
| German | 96 | Minor stylistic literalness and stiffness |
| Dutch | 96 | Minor phrasing adjustments needed for fluency |
| Russian | 96 | Professional and accurate with minor stylistic polish needed |
| Danish | 95 | Minor lexical and grammatical imperfections |
| Norwegian | 95 | Exceptional quality with minor terminology refinement suggested |
| Slovak | 95 | Minor typos and literal phrasing |
| Albanian | 95 | High quality, minor literalisms |
| Serbian | 95 | Minor transliteration and phrasing issues |
| Vietnamese | 95 | Excellent scientific accuracy and fluency |
| Persian | 94 | Minor stylistic refinements needed for flow |
| Macedonian | 94 | Minor literal phrasing and stylistic adjustments needed |
| Thai | 94 | Minor literalism and standardization issues |
| Galician | 93 | Minor lexical inaccuracies and Portuguese interference |
| Croatian | 93 | Minor terminology issues and stylistic calques |
| Japanese | 93 | High-quality with one minor flaw |
| Romanian | 93 | Minor stylistic issues including unnatural word choices |
| Chinese | 93 | Excellent scientific accuracy with minor stylistic imperfections |
| Bulgarian | 92 | Minor stylistic and grammatical inconsistencies |
| Czech | 92 | Minor grammatical and stylistic issues |
| Finnish | 92 | Minor phrasing stiffness and literal artifacts reduce absolute fluency |
| Hebrew | 92 | Minor terminology and fluency tweaks needed |
| Georgian | 92 | Minor stylistic adjustments and one typo |
| Slovene | 92 | Minor fluency and grammatical issues |
| Turkish | 92 | Minor literal phrasing issues |
| Bengali | 91 | Minor awkwardness prevents native fluency despite high accuracy |
| Hindi | 91 | Minor stylistic and phrasing issues only |
| Telugu | 91 | Minor terminology refinements needed for perfect accuracy |
| Arabic | 90 | Minor refinements in phrasing and terminology needed for native-level polish |
| Basque | 90 | Minor terminology and expression calques |
| Lithuanian | 90 | Minor stylistic and typographical issues present |
| Korean | 88 | Minor terminology inconsistency for 'psi' |
| Latvian | 87 | Minor terminology inconsistencies and literal phrasing |
| Afrikaans | 85 | Prominent lexical mistranslation: 'podcast' as 'potgooi' |
| Belarusian | 85 | Technical terminology errors and Russianisms |
| Estonian | 85 | Terminology inaccuracies and minor phrasing issues |
| Indonesian | 84 | Minor terminology precision and phrasing issues |
| Tamil | 84 | Minor stylistic and terminology issues |
| Greek | 82 | Minor technical inaccuracies and grammatical slips |
| Mongolian | 81 | High quality with minor lexical calques |
| Marathi | 81 | Fluency suffers from literal calques and rigid syntax |
| Hungarian | 80 | Missing speaker tags and terminology issues |
| Armenian | 80 | Minor errors and literal phrasing |
| Kannada | 80 | Minor terminology and fluency issues |
| Swahili | 80 | Non-standard physics terminology and literal phrasing |
| Burmese | 78 | Significant terminology errors |
| Nepali | 78 | Over-literal translation patterns reduce fluency |
| Urdu | 78 | Literal phrasing and awkward syntax |
| Esperanto | 77 | Lexical inaccuracies and awkward calques |
| Khmer | 73 | Mistranslated technical physics terminology |
| Azerbaijani | 72 | Non-standard terminology and noticeable translationese |
| Interlingua | 71 | Severe non-standard vocabulary and morphology |
| Malayalam | 71 | Noticeable literal phrasing and stiffness |
| Malay | 71 | Significant terminology errors and awkward phrasing |
| Irish | 68 | Significant terminology errors and Anglicized phrasing |
| Icelandic | 66 | Significant technical terminology errors |
| Tagalog | 66 | Literal translation and non-standard terminology |
| Sinhala | 62 | Significant lexical inaccuracies and rigid syntax |
| Lao | 51 | Severe machine-translation artifacts and technical inaccuracies |
| Welsh | 43 | Systematic vocabulary errors and grammatical defects |
