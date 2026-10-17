# examples/tr/onde/gemini-3.5-flash-lite/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-3.5-flash-lite
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 92.7 | Slightly rigid conversational tone |
| Italian | 86.3 | Terminological errors and unnatural phrasing |
| Korean | 85.3 | Stiff formal tone stilted syntax |
| Basque | 85.2 | Awkward calques and non-standard terms |
| Slovene | 82.9 | Grammatical errors and stylistic inconsistency |
| Galician | 82.0 | Scattered spelling and grammatical errors |
| French | 81.9 | Inconsistent mixing of tu and vous |
| Hebrew | 81.9 | Notable technical glitch in text |
| Esperanto | 81.7 | Unnatural phrasing and literal calques |
| Japanese | 80.9 | untranslated English text |
| Armenian | 80.6 | Linguistic fluency and naturalness |
| Thai | 78.6 | Untranslated English sentence present |
| German | 78.5 | Fluency issues and grammatical awkwardness |
| Russian | 78.4 | Presence of mixed-language fragments |
| Afrikaans | 78.3 | Occasional stiffness and structural awkwardness |
| Polish | 78.2 | Speaker misattribution error |
| Swedish | 78.0 | Severe structural errors due to wrong speaker attributions |
| Ukrainian | 77.8 | Incomplete translation with untranslated English lines |
| Czech | 77.2 | Grammatical errors and unnatural phrasing |
| Malayalam | 76.9 | Awkward phrasing and stiff register |
| Vietnamese | 76.9 | Awkward phrasing and literalism |
| Arabic | 76.2 | Untranslated English sentences present |
| Khmer | 75.8 | Inclusion of Chinese characters |
| Romanian | 75.8 | Significant grammatical errors and unnatural phrasing |
| Hungarian | 75.2 | Typographical errors and mechanical flaws |
| Chinese | 75.0 | Untranslated English segments mixed with Chinese text |
| Portuguese | 74.9 | Speaker misattribution and literalisms |
| Dutch | 74.8 | Speaker attribution errors disrupt dialogue structure |
| Norwegian | 74.5 | Meta-commentary and missing content |
| Persian | 73.9 | Incomplete localization with English remnants |
| Bulgarian | 73.7 | Untranslated English segments and inconsistent naming |
| Burmese | 73.5 | Unnatural phrasing and tone issues |
| Croatian | 72.3 | Untranslated English text insertion |
| Icelandic | 72.0 | Contextual errors and missing dialogue |
| Hindi | 71.3 | Formatting errors and awkward phrasing |
| Serbian | 71.3 | Recurring grammatical errors and register inconsistency |
| Macedonian | 71.2 | Missing English segments |
| Latvian | 71.1 | Severe grammatical errors |
| Indonesian | 71.0 | Inclusion of untranslated English source text |
| Georgian | 71.0 | Glitchy text and stiff style |
| Azerbaijani | 70.5 | Inconsistent dialogue formatting breaks conversational flow |
| Marathi | 70.5 | Mixed-language fragmentation and structural defects |
| Urdu | 70.2 | Glaring inconsistency in speaker tags |
| Turkish | 70.0 | Untranslated English segment and unnatural phrasing |
| Malay | 69.7 | Untranslated speaker labels and meta-text artifacts |
| Kannada | 69.6 | Mixed language fragments and anglicisms |
| Lao | 69.3 | Untranslated English text and Chinese character typos |
| Nepali | 69.2 | Mixed language and incomplete translation |
| Belarusian | 69.1 | Mixed English language segments |
| Finnish | 69.1 | Terminology errors and awkward phrasing |
| Tagalog | 68.8 | Unnatural and overly literal phrasing |
| Estonian | 68.7 | Severe mixed-language intrusions |
| Danish | 67.5 | Critical speaker role reversals and hallucinated labels |
| Catalan | 67.2 | Speaker attribution errors and unidiomatic phrasing |
| Albanian | 66.5 | Pervasive lack of grammatical correctness |
| Tamil | 65.7 | Severe mixing with Georgian and Chinese scripts |
| Swahili | 64.5 | Pervasive code-switching errors |
| Bengali | 64.3 | Mixed language and corrupted formatting |
| Telugu | 63.2 | Incomplete sentences, formatting errors, and mixed language artifacts |
| Greek | 61.8 | Untranslated English segments |
| Interlingua | 61.2 | Severe structural defect mixing languages |
| Slovak | 60.9 | Severe grammatical incoherence and incorrect case usage |
| Sinhala | 60.6 | Severe code-switching to Bengali and Tamil |
| Welsh | 60.5 | Inconsistent language usage and incomplete translation |
| Mongolian | 59.2 | Major language mixing defects |
| Irish | 59.0 | Severe terminology and structural failures |
| Lithuanian | 56.9 | Severe grammatical errors |
