# examples/tr/onde/qwen3.8-flash-next/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S (125B-A6B MoE with 51B of n-gram embeddings, GSQ-RCO quantized, run with Strata)
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 95.5 | Polished and professional |
| Catalan | 93.8 | Minor stylistic nuances adapted to Catalan |
| Russian | 91.9 | Slight literalness over idiomatic phrasing |
| Romanian | 90.8 | Slightly rigid syntax |
| Swedish | 90.8 | Literal translations of idioms and fillers |
| Lithuanian | 90.5 | Retains some stiffness from direct translation |
| Japanese | 90.1 | Minor stiff phrasings and direct calques |
| Chinese | 90.0 | Slight translationese stiffness in dialogue |
| Polish | 89.8 | Slightly awkward phrasing from literal translation |
| German | 88.9 | Inconsistent pronoun usage and awkward phrasing |
| Galician | 88.8 | Scattered fluency issues |
| Ukrainian | 88.8 | Slightly literal phrasing lacks naturalness |
| Indonesian | 88.5 | Overly literal phrasing |
| Slovak | 88.4 | Slightly stiff phrasing |
| Danish | 87.7 | Retains source language syntax artifacts |
| Korean | 87.3 | Preserved English sounds like "psi" |
| Dutch | 87.1 | awkward phrasing of mathematical concepts |
| Malay | 86.4 | Disjointed code-switching between Malay and English |
| Turkish | 86.2 | occasional stiffness in sentence structure |
| Arabic | 85.4 | Slightly stiff or overly literal phrasing |
| Albanian | 85.2 | Reads as literal rather than natural speech |
| Afrikaans | 85.0 | Translationese and rigid phrasing |
| Belarusian | 85.0 | Rigid literal calques from English syntax |
| Swahili | 84.5 | Rigid phrasing lacks natural conversational fluency |
| Welsh | 84.1 | Slight awkwardness from Calque Syndrome |
| Thai | 83.8 | Inconsistent gendered polite particles |
| Hebrew | 83.7 | Inconsistent ellipsis punctuation |
| Esperanto | 83.6 | Inconsistent orthography and spelling |
| Hindi | 83.3 | Awkward phrasing and literalism |
| Armenian | 82.8 | Significant fluency issues |
| Azerbaijani | 82.6 | Awkward phrasing and literal translations |
| Vietnamese | 82.6 | Literal word-for-word phrasing |
| Latvian | 82.5 | Pervasive grammatical errors |
| Norwegian | 82.5 | Awkward phrasing |
| Portuguese | 82.5 | Excessive literalness and stiffness |
| Bengali | 82.3 | Unnatural phrasing and stiff tone |
| Khmer | 81.4 | Inconsistent repetition of Yes/Sir |
| Marathi | 81.3 | Translationese quality |
| Estonian | 80.0 | Occasional stiffness in phrasing and minor errors |
| Georgian | 79.8 | Literal and awkward phrasing |
| Bulgarian | 78.6 | English word intrusion |
| Finnish | 77.8 | Glaring mechanical errors and identity inconsistencies |
| Persian | 77.5 | Literal rendering lacks naturalness |
| Serbian | 77.5 | Noticeable mechanical imperfections disrupt speech flow |
| Malayalam | 77.0 | Inconsistent technical terminology handling |
| Croatian | 76.8 | Significant fluency and structural issues |
| Slovene | 76.3 | Lacks idiomatic polish |
| Tagalog | 75.7 | Severe translationese hindering fluency |
| Czech | 75.5 | Severe loss of coherence in speaker attribution |
| Lao | 75.3 | Register inconsistency due to interjection errors |
| Urdu | 75.0 | Inconsistent scientific terminology |
| Macedonian | 74.2 | Language switch to English |
| Icelandic | 74.0 | Inconsistent terminology usage |
| Irish | 73.8 | Inconsistent linguistic execution and mixed language |
| Burmese | 73.8 | Terminological inconsistency and literalism |
| Sinhala | 73.8 | Awkward phrasing and literal translation artifacts |
| Hungarian | 73.3 | Severe code-switching with English |
| Nepali | 72.8 | Severe structural and formatting flaws |
| Telugu | 72.5 | Contains untranslated English artifacts |
| Italian | 72.4 | Missing speaker labels breaks dialogue |
| Mongolian | 72.0 | Significant grammatical errors and unnatural phrasing |
| Interlingua | 71.4 | Not in Interlingua |
| French | 71.2 | Missing speaker labels |
| Kannada | 70.3 | Inconsistent speaker labels |
| Tamil | 69.9 | Awkward phrasing and lack of fluency |
| Basque | 69.0 | Significant mistranslations alter meaning |
| Greek | 66.2 | Severe terminology errors |

- **Interlingua**: the trend phrase "Not in Interlingua" overstates it. The translation is written in Interlingua throughout; what Jev deducts for is mainly fluency, with scattered non-Interlingua forms such as the English `pattern` and `fringes` (line 22) or the Spanish/Portuguese spelling `localizar` (line 58, Interlingua `localisar`). Interlingua scores low in every model (see [Scope of the Comparison](../../README.md#scope-of-the-comparison)).
- **Greek**: no obvious breakdown was found on reading the translation; speaker labels are intact and there is no other-language contamination, so the cause of its lowest score could not be identified. Greek scores low in every model (see [Scope of the Comparison](../../README.md#scope-of-the-comparison)), so this is not read as a failure specific to this model.
