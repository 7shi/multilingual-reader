# examples/tr/onde/gemini-3.5-flash-lite/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-3.5-flash-lite
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 92.8 | Slightly rigid conversational tone |
| Italian | 84.5 | Terminological errors and unnatural phrasing |
| Basque | 83.5 | Awkward calques and non-standard terms |
| Korean | 82.7 | Stiff formal tone stilted syntax |
| Slovene | 82.7 | Grammatical errors and stylistic inconsistency |
| Hebrew | 82.3 | Notable technical glitch in text |
| Esperanto | 82.0 | Unnatural phrasing and literal calques |
| Armenian | 79.8 | Linguistic fluency and naturalness |
| Japanese | 79.8 | untranslated English text |
| French | 79.2 | Inconsistent mixing of tu and vous |
| Swedish | 78.5 | Severe structural errors due to wrong speaker attributions |
| Russian | 77.7 | Presence of mixed-language fragments |
| Polish | 77.2 | Speaker misattribution error |
| Khmer | 77.1 | Inclusion of Chinese characters |
| Thai | 77.0 | Untranslated English sentence present |
| German | 76.6 | Fluency issues and grammatical awkwardness |
| Galician | 76.5 | Scattered spelling and grammatical errors |
| Czech | 76.3 | Grammatical errors and unnatural phrasing |
| Afrikaans | 76.0 | Occasional stiffness and structural awkwardness |
| Croatian | 75.2 | Untranslated English text insertion |
| Hindi | 74.6 | Formatting errors and awkward phrasing |
| Malayalam | 74.5 | Awkward phrasing and stiff register |
| Romanian | 73.5 | Significant grammatical errors and unnatural phrasing |
| Arabic | 73.4 | Untranslated English sentences present |
| Hungarian | 73.3 | Typographical errors and mechanical flaws |
| Bulgarian | 72.6 | Untranslated English segments and inconsistent naming |
| Burmese | 72.2 | Unnatural phrasing and tone issues |
| Ukrainian | 72.2 | Incomplete translation with untranslated English lines |
| Norwegian | 72.0 | Meta-commentary and missing content |
| Azerbaijani | 71.9 | Inconsistent dialogue formatting breaks conversational flow |
| Dutch | 71.8 | Speaker attribution errors disrupt dialogue structure |
| Finnish | 71.4 | Terminology errors and awkward phrasing |
| Portuguese | 71.4 | Speaker misattribution and literalisms |
| Persian | 71.3 | Incomplete localization with English remnants |
| Georgian | 71.2 | Glitchy text and stiff style |
| Vietnamese | 70.2 | Awkward phrasing and literalism |
| Macedonian | 70.1 | Missing English segments |
| Icelandic | 70.0 | Contextual errors and missing dialogue |
| Malay | 69.2 | Untranslated speaker labels and meta-text artifacts |
| Serbian | 69.1 | Recurring grammatical errors and register inconsistency |
| Marathi | 69.0 | Mixed-language fragmentation and structural defects |
| Turkish | 69.0 | Untranslated English segment and unnatural phrasing |
| Chinese | 69.0 | Untranslated English segments mixed with Chinese text |
| Catalan | 68.8 | Speaker attribution errors and unidiomatic phrasing |
| Indonesian | 68.6 | Inclusion of untranslated English source text |
| Nepali | 68.6 | Mixed language and incomplete translation |
| Urdu | 68.3 | Glaring inconsistency in speaker tags |
| Belarusian | 68.0 | Mixed English language segments |
| Lao | 67.6 | Untranslated English text and Chinese character typos |
| Tagalog | 67.6 | Unnatural and overly literal phrasing |
| Latvian | 67.3 | Severe grammatical errors |
| Estonian | 67.2 | Severe mixed-language intrusions |
| Kannada | 66.8 | Mixed language fragments and anglicisms |
| Tamil | 64.2 | Severe mixing with Georgian and Chinese scripts |
| Bengali | 64.0 | Mixed language and corrupted formatting |
| Danish | 63.8 | Critical speaker role reversals and hallucinated labels |
| Albanian | 63.5 | Pervasive lack of grammatical correctness |
| Telugu | 63.0 | Incomplete sentences, formatting errors, and mixed language artifacts |
| Swahili | 62.8 | Pervasive code-switching errors |
| Greek | 60.8 | Untranslated English segments |
| Sinhala | 59.8 | Severe code-switching to Bengali and Tamil |
| Welsh | 59.5 | Inconsistent language usage and incomplete translation |
| Interlingua | 59.5 | Severe structural defect mixing languages |
| Mongolian | 59.1 | Major language mixing defects |
| Irish | 56.3 | Severe terminology and structural failures |
| Lithuanian | 54.2 | Severe grammatical errors |
| Slovak | 53.7 | Severe grammatical incoherence and incorrect case usage |
