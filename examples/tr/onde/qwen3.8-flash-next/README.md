# examples/tr/onde/qwen3.8-flash-next/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S (125B-A6B MoE with 51B of n-gram embeddings, GSQ-RCO quantized, run with Strata)
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.1 | Polished and professional |
| Catalan | 93.7 | Minor stylistic nuances adapted to Catalan |
| Chinese | 91.2 | Slight translationese stiffness in dialogue |
| Japanese | 90.3 | Minor stiff phrasings and direct calques |
| Russian | 90.1 | Slight literalness over idiomatic phrasing |
| Portuguese | 89.9 | Excessive literalness and stiffness |
| Lithuanian | 89.6 | Retains some stiffness from direct translation |
| Galician | 89.5 | Scattered fluency issues |
| Polish | 89.5 | Slightly awkward phrasing from literal translation |
| Ukrainian | 88.9 | Slightly literal phrasing lacks naturalness |
| Indonesian | 88.4 | Overly literal phrasing |
| German | 88.0 | Inconsistent pronoun usage and awkward phrasing |
| Swedish | 87.8 | Literal translations of idioms and fillers |
| Turkish | 87.8 | occasional stiffness in sentence structure |
| Afrikaans | 87.5 | Translationese and rigid phrasing |
| Korean | 87.4 | Preserved English sounds like "psi" |
| Dutch | 87.2 | awkward phrasing of mathematical concepts |
| Arabic | 86.5 | Slightly stiff or overly literal phrasing |
| Danish | 86.3 | Retains source language syntax artifacts |
| Slovak | 86.3 | Slightly stiff phrasing |
| Romanian | 86.2 | Slightly rigid syntax |
| Malay | 84.7 | Disjointed code-switching between Malay and English |
| Vietnamese | 83.9 | Literal word-for-word phrasing |
| Welsh | 83.6 | Slight awkwardness from Calque Syndrome |
| Hindi | 83.4 | Awkward phrasing and literalism |
| Hebrew | 83.2 | Inconsistent ellipsis punctuation |
| Norwegian | 83.2 | Awkward phrasing |
| Thai | 83.0 | Inconsistent gendered polite particles |
| Latvian | 82.8 | Pervasive grammatical errors |
| Esperanto | 82.4 | Inconsistent orthography and spelling |
| Armenian | 82.2 | Significant fluency issues |
| Marathi | 81.9 | Translationese quality |
| Georgian | 81.7 | Literal and awkward phrasing |
| Belarusian | 81.6 | Rigid literal calques from English syntax |
| Swahili | 81.6 | Rigid phrasing lacks natural conversational fluency |
| Finnish | 81.4 | Glaring mechanical errors and identity inconsistencies |
| Malayalam | 81.2 | Inconsistent technical terminology handling |
| Albanian | 81.2 | Reads as literal rather than natural speech |
| Azerbaijani | 81.0 | Awkward phrasing and literal translations |
| Bengali | 80.6 | Unnatural phrasing and stiff tone |
| Khmer | 80.6 | Inconsistent repetition of Yes/Sir |
| Icelandic | 80.2 | Inconsistent terminology usage |
| Bulgarian | 80.0 | English word intrusion |
| Estonian | 80.0 | Occasional stiffness in phrasing and minor errors |
| Macedonian | 77.6 | Language switch to English |
| Slovene | 77.3 | Lacks idiomatic polish |
| Serbian | 77.2 | Noticeable mechanical imperfections disrupt speech flow |
| Persian | 76.6 | Literal rendering lacks naturalness |
| Burmese | 76.2 | Terminological inconsistency and literalism |
| Croatian | 76.0 | Significant fluency and structural issues |
| Czech | 75.9 | Severe loss of coherence in speaker attribution |
| Irish | 74.2 | Inconsistent linguistic execution and mixed language |
| Tagalog | 73.8 | Severe translationese hindering fluency |
| Urdu | 73.7 | Inconsistent scientific terminology |
| Lao | 73.1 | Register inconsistency due to interjection errors |
| Interlingua | 73.0 | Not in Interlingua |
| Nepali | 72.2 | Severe structural and formatting flaws |
| Sinhala | 72.1 | Awkward phrasing and literal translation artifacts |
| Mongolian | 71.1 | Significant grammatical errors and unnatural phrasing |
| Tamil | 71.1 | Awkward phrasing and lack of fluency |
| Hungarian | 70.8 | Severe code-switching with English |
| Basque | 69.8 | Significant mistranslations alter meaning |
| French | 68.8 | Missing speaker labels |
| Italian | 68.6 | Missing speaker labels breaks dialogue |
| Kannada | 68.5 | Inconsistent speaker labels |
| Telugu | 67.8 | Contains untranslated English artifacts |
| Greek | 66.6 | Severe terminology errors |

- **Interlingua**: the trend phrase "Not in Interlingua" overstates it. The translation is written in Interlingua throughout; what Jev deducts for is mainly fluency, with scattered non-Interlingua forms such as the English `pattern` and `fringes` (line 22) or the Spanish/Portuguese spelling `localizar` (line 58, Interlingua `localisar`). Interlingua scores low in every model (see [Scope of the Comparison](../../README.md#scope-of-the-comparison)).
- **Greek**: no obvious breakdown was found on reading the translation; speaker labels are intact and there is no other-language contamination, so the cause of its lowest score could not be identified. Greek scores low in every model (see [Scope of the Comparison](../../README.md#scope-of-the-comparison)), so this is not read as a failure specific to this model.
