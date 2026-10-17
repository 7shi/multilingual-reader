# examples/tr/onde/gemini-3-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-3-flash-preview
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Czech | 79.9 | Severe structural formatting errors |
| Japanese | 79.0 | Stiff dialogue phrasing |
| Catalan | 77.4 | Speaker attribution failures |
| Vietnamese | 76.9 | Noticeable flaws in fluency and naturalness |
| Portuguese | 76.7 | Missing speaker lines |
| Finnish | 76.4 | Awkward conversational tone |
| Ukrainian | 75.5 | Severe structural and formatting errors |
| Swedish | 75.3 | Lack of proper dialogue formatting |
| Hebrew | 74.9 | Pronoun agreement errors |
| Russian | 74.8 | Missing speaker tags |
| Basque | 74.5 | Inconsistent dialogue attribution markers |
| Serbian | 74.5 | missing speaker labels |
| Arabic | 74.4 | Speaker attribution errors and line duplication |
| Thai | 74.3 | Inconsistent politeness particles and repetition |
| French | 74.2 | Structural and formatting defects |
| Slovene | 74.1 | Missing speaker labels and typos |
| Turkish | 74.1 | missing speaker tags and typos |
| Romanian | 73.8 | Poor dialogue structure and formatting |
| Chinese | 73.6 | Repeated sentences and incorrect speaker tags |
| Bulgarian | 73.2 | Missing speaker tags |
| Khmer | 73.2 | Inconsistent terminology and unnatural phrasing |
| Croatian | 73.1 | Missing speaker labels |
| Indonesian | 73.1 | Missing speaker labels disrupt flow |
| Malayalam | 73.1 | Missing speaker tag and copy-paste repetition |
| Tamil | 72.8 | Translationese and awkward phrasing |
| Spanish | 72.7 | Chinese character intrusion |
| Marathi | 72.7 | Inconsistent pronoun usage disrupts naturalness |
| Armenian | 72.5 | Significant mechanical error and repetition |
| Burmese | 72.3 | Notable editing errors and awkward phrasing |
| Macedonian | 72.0 | Persistent formatting and missing speaker labels |
| Polish | 72.0 | Inconsistent speaker attributions and dialogue fragmentation |
| Welsh | 71.9 | Frequent typos and unnatural phrasing |
| Georgian | 71.8 | Missing speaker attributions disrupt dialogue clarity |
| Korean | 71.8 | Duplicate text segments disrupt flow |
| Afrikaans | 71.7 | Inconsistent speaker labeling and structural defects |
| Danish | 71.3 | Severe structural integrity issues and stray Chinese character |
| Persian | 71.3 | Breakdown of dialogue structure |
| Albanian | 71.2 | Missing speaker labels and formatting inconsistencies |
| Lithuanian | 71.0 | Complete collapse of dialogue structure |
| Sinhala | 70.8 | Mechanical tone and unnatural phrasing |
| Slovak | 70.8 | Broken structure with JSON fragment |
| Belarusian | 70.6 | Significant grammatical and syntactic errors |
| Malay | 70.5 | Major structural defects and text glitches |
| Hindi | 69.8 | Structural breakdown and missing speaker tags |
| Latvian | 69.5 | Severe formatting and attribution errors |
| Dutch | 69.3 | Severely broken dialogue format and speaker attribution |
| Estonian | 69.1 | Severe mechanical errors and formatting defects |
| Mongolian | 68.7 | Severe formatting and grammar errors |
| Norwegian | 68.7 | Critical structural defects and missing content |
| Azerbaijani | 68.6 | Structural glitches and linguistic awkwardness |
| Kannada | 68.0 | Structural speaker attribution errors |
| Hungarian | 67.1 | Missing lines and mixed English |
| German | 67.0 | Missing speaker attributions |
| Galician | 66.8 | Missing speaker tags and non-Latin character |
| Icelandic | 66.8 | Untranslated English text artifacts |
| Irish | 66.2 | Critical language mixing and duplication error |
| Urdu | 66.2 | Mixed-language fragments and formatting errors |
| Italian | 65.6 | Mixed language artifacts and malformed syntax |
| Nepali | 65.4 | Severe duplication and structural errors |
| Telugu | 63.9 | Severe lack of naturalness and fluency |
| Greek | 63.2 | Severe lexical errors in physics terminology |
| Esperanto | 62.0 | Broken coherence due to garbled mixed-language duplication |
| Swahili | 60.9 | Severe formatting error with repeated Chinese characters |
| Bengali | 58.8 | Severe structural defects with numerical noise |
| Tagalog | 56.8 | Critical structural defects with artifacts |
| Lao | 56.2 | Repetitive block and poor language quality |
| Interlingua | 56.0 | Pervasive formatting and structural errors |
