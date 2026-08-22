# examples/tr/onde/ox-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: ox-alpha
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 97 | Nearly perfect high-quality scientific localization |
| French | 97 | Minor tu/vous mixing |
| Italian | 97 | Exceptional quality and accuracy with minor stylistic deviations |
| Polish | 97 | Highly accurate and professional with minor stylistic tweaks needed |
| Portuguese | 97 | Flawless scientific and stylistic quality |
| Swedish | 97 | Exceptional scientific and linguistic quality |
| Dutch | 96 | Minor phrasing adjustments regarding 'squared' would elevate fluency further |
| Russian | 96 | High quality with minor stylistic polish needed |
| Spanish | 95 | Minor dialogue formatting error at end |
| Vietnamese | 95 | High technical accuracy with minor stylistic issues |
| Persian | 94 | Minor terminology standardization needed |
| Japanese | 93 | Professional grade with minor grammatical flaws |
| Romanian | 93 | Minor stylistic and lexical issues |
| Bulgarian | 92 | Minor grammatical and stylistic flaws |
| Czech | 92 | Minor grammatical and phrasing inconsistencies |
| Hebrew | 92 | Minor terminology and fluency tweaks needed |
| Turkish | 92 | High quality with minor fluency issues |
| Telugu | 91 | Minor terminology refinements needed |
| Galician | 90 | Portuguese-influenced orthographic inconsistencies |
| Lithuanian | 90 | Minor typos and machine-translation artifacts |
| Albanian | 90 | Minor lexical calques in mathematical phrasing |
| Belarusian | 89 | Minor lexical inaccuracies and non-standard technical terminology |
| German | 89 | Minor stylistic and grammatical issues |
| Macedonian | 88 | Minor dialogue omission and slightly stiff phrasing |
| Norwegian | 88 | Minor terminology stiffness and literal math verbalization |
| Slovene | 88 | Minor literal calques and phrasing quirks |
| Basque | 87 | Conversational filler inaccuracies |
| Hindi | 87 | Minor fluency hiccups and artifacts impact natural flow |
| Latvian | 87 | Minor terminology and grammatical slips |
| Bengali | 86 | Minor fluency and one dialogue omission |
| Croatian | 86 | Minor errors and glitches |
| Slovak | 86 | Minor errors and calques |
| Azerbaijani | 85 | Minor terminology errors and literal phrasing |
| Mongolian | 85 | Minor fluency issues and terminology refinements needed |
| Indonesian | 84 | Minor terminology precision issues |
| Serbian | 84 | Typographical errors and content omissions |
| Tamil | 84 | Minor terminology inconsistencies and calques |
| Nepali | 83 | Literal phrasing hinders fluency |
| Thai | 83 | Minor phrasing stiffness and formatting inconsistencies |
| Interlingua | 82 | Truncated ending and minor grammatical/calque issues |
| Burmese | 82 | Typographical errors and inconsistent formatting |
| Armenian | 80 | Minor typos and awkward phrasing |
| Marathi | 80 | Needs proofreading for typos and fluency |
| Urdu | 78 | Unnatural phrasing due to literal translation and heavy transliteration |
| Esperanto | 77 | Lexical inaccuracies and awkward phrasing |
| Swahili | 77 | Excessive literalism and non-standard terminology |
| Arabic | 74 | Dialogue omissions and literal phrasing |
| Danish | 74 | Structural flaws and dialogue attribution errors |
| Ukrainian | 74 | Critical structural defect with mixed-language meta-commentary |
| Chinese | 74 | Excellent terminology but missing dialogue lines and speaker tags |
| Icelandic | 73 | Grammar errors and non-standard terminology |
| Kannada | 73 | Notable terminology inaccuracies |
| Malayalam | 71 | Literal phrasing and terminology inconsistencies |
| Sinhala | 70 | Unnatural phrasing and terminology errors |
| Malay | 69 | Terminology errors and omissions |
| Hungarian | 68 | Major omissions and structural flaws |
| Korean | 65 | Significant omissions and structural defects |
| Tagalog | 64 | Inconsistent and incorrect technical terminology |
| Finnish | 62 | Severe omissions and structural defects |
| Estonian | 60 | Major omissions and structural defects |
| Greek | 56 | Severe structural flaw: mixed-language intrusions and meta-commentary present in the final output |
| Afrikaans | 42 | Unremoved English meta-commentary |
| Khmer | 42 | Significant technical terminology errors and unnatural phrasing |
| Irish | 41 | Omission of critical content and mistranslation of key terms |
| Welsh | 40 | Major grammatical errors and inaccurate terminology |
| Lao | 34 | Severe technical terminology and MT artifacts |
| Georgian | 28 | Unremoved English meta-commentary |
