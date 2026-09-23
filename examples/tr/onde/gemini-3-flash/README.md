# examples/tr/onde/gemini-3-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-3-flash-preview
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Japanese | 79.3 | Stiff dialogue phrasing |
| Czech | 78.1 | Severe structural formatting errors |
| Croatian | 77.3 | Missing speaker labels |
| Finnish | 76.9 | Awkward conversational tone |
| Serbian | 76.0 | missing speaker labels |
| Swedish | 75.8 | Lack of proper dialogue formatting |
| Ukrainian | 75.5 | Severe structural and formatting errors |
| Georgian | 75.2 | Missing speaker attributions disrupt dialogue clarity |
| Hebrew | 75.0 | Pronoun agreement errors |
| Welsh | 74.9 | Frequent typos and unnatural phrasing |
| Catalan | 74.8 | Speaker attribution failures |
| Vietnamese | 74.2 | Noticeable flaws in fluency and naturalness |
| Arabic | 74.1 | Speaker attribution errors and line duplication |
| Khmer | 73.9 | Inconsistent terminology and unnatural phrasing |
| Chinese | 73.9 | Repeated sentences and incorrect speaker tags |
| Slovene | 73.8 | Missing speaker labels and typos |
| Tamil | 73.8 | Translationese and awkward phrasing |
| Spanish | 73.7 | Chinese character intrusion |
| Romanian | 73.5 | Poor dialogue structure and formatting |
| French | 73.2 | Structural and formatting defects |
| Marathi | 73.1 | Inconsistent pronoun usage disrupts naturalness |
| Thai | 73.1 | Inconsistent politeness particles and repetition |
| Armenian | 73.0 | Significant mechanical error and repetition |
| Korean | 73.0 | Duplicate text segments disrupt flow |
| Portuguese | 72.2 | Missing speaker lines |
| Russian | 72.0 | Missing speaker tags |
| Turkish | 72.0 | missing speaker tags and typos |
| Indonesian | 71.8 | Missing speaker labels disrupt flow |
| Albanian | 71.4 | Missing speaker labels and formatting inconsistencies |
| Basque | 71.1 | Inconsistent dialogue attribution markers |
| Sinhala | 71.1 | Mechanical tone and unnatural phrasing |
| Bulgarian | 70.3 | Missing speaker tags |
| Dutch | 70.1 | Severely broken dialogue format and speaker attribution |
| Azerbaijani | 69.9 | Structural glitches and linguistic awkwardness |
| Danish | 69.7 | Severe structural integrity issues and stray Chinese character |
| Kannada | 69.5 | Structural speaker attribution errors |
| Malayalam | 69.5 | Missing speaker tag and copy-paste repetition |
| Macedonian | 69.4 | Persistent formatting and missing speaker labels |
| Slovak | 69.3 | Broken structure with JSON fragment |
| Lithuanian | 69.2 | Complete collapse of dialogue structure |
| Mongolian | 69.2 | Severe formatting and grammar errors |
| Belarusian | 69.1 | Significant grammatical and syntactic errors |
| Polish | 69.0 | Inconsistent speaker attributions and dialogue fragmentation |
| German | 68.3 | Missing speaker attributions |
| Estonian | 68.2 | Severe mechanical errors and formatting defects |
| Burmese | 68.0 | Notable editing errors and awkward phrasing |
| Persian | 67.8 | Breakdown of dialogue structure |
| Telugu | 67.8 | Severe lack of naturalness and fluency |
| Malay | 67.6 | Major structural defects and text glitches |
| Urdu | 67.3 | Mixed-language fragments and formatting errors |
| Italian | 66.9 | Mixed language artifacts and malformed syntax |
| Norwegian | 66.9 | Critical structural defects and missing content |
| Icelandic | 66.8 | Untranslated English text artifacts |
| Hindi | 66.5 | Structural breakdown and missing speaker tags |
| Latvian | 66.5 | Severe formatting and attribution errors |
| Hungarian | 66.1 | Missing lines and mixed English |
| Irish | 66.0 | Critical language mixing and duplication error |
| Afrikaans | 65.8 | Inconsistent speaker labeling and structural defects |
| Galician | 64.3 | Missing speaker tags and non-Latin character |
| Nepali | 64.0 | Severe duplication and structural errors |
| Greek | 61.0 | Severe lexical errors in physics terminology |
| Esperanto | 59.2 | Broken coherence due to garbled mixed-language duplication |
| Swahili | 57.8 | Severe formatting error with repeated Chinese characters |
| Interlingua | 55.7 | Pervasive formatting and structural errors |
| Bengali | 55.1 | Severe structural defects with numerical noise |
| Tagalog | 54.1 | Critical structural defects with artifacts |
| Lao | 50.8 | Repetitive block and poor language quality |
