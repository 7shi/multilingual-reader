# examples/tr/onde/gemini-3.7-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-3.7-flash
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.5 | Sound translation with minor stylistic deductions |
| Italian | 94.5 | No structural defects, omissions, or major errors |
| Catalan | 93.8 | Minor stylistic awkwardness in transitions |
| French | 93.0 | Occasional non-idiomatic phrasing and filler words |
| Galician | 92.0 | Slightly literal phrasing and stiff terminology |
| Polish | 91.6 | Slightly stiff transitional phrases and colloquialisms |
| Ukrainian | 91.6 | Minor literal translations reduce naturalness |
| Czech | 91.0 | Slight structural rigidities affecting fluency |
| Hungarian | 90.8 | Unnatural filler word usage |
| Arabic | 90.1 | Occasionally rigid phrasing |
| Georgian | 90.1 | Retains English syntax and fillers |
| Latvian | 90.1 | Minor stiffness in colloquial dialogue fluency |
| Albanian | 90.1 | Some sentences feel slightly less idiomatic |
| Swedish | 89.8 | Slightly literal phrasing |
| Macedonian | 89.7 | Slightly rigid sentence structures |
| Japanese | 89.5 | Slightly abrupt speaker transitions |
| Danish | 89.4 | Minor lack of native fluency |
| Serbian | 89.4 | Slightly stiff phrasing in specific scientific contexts |
| Slovak | 89.2 | Slightly rigid and literal tone |
| Vietnamese | 89.0 | Occasionally rigid tone |
| Estonian | 88.2 | Translationese and awkward idioms |
| Bulgarian | 88.1 | Minor stiffness in dialogue markers |
| Croatian | 88.0 | Noticeable linguistic awkwardness |
| Indonesian | 87.9 | Slightly formal phrasing and syntax |
| Dutch | 87.3 | Slightly stiff phrasing |
| Azerbaijani | 86.5 | Stiff literal phrasing and non-standard terms |
| Turkish | 86.5 | Overuse of calques and ellipses |
| Belarusian | 86.4 | Significant typo in superposition term and awkward phrasing |
| Esperanto | 86.2 | Slightly rigid conversational flow |
| Icelandic | 85.8 | Lacks fluency and naturalness |
| Persian | 85.6 | Tonal inconsistency due to casual language |
| Portuguese | 83.7 | Lacks fluency and naturalness |
| Armenian | 82.8 | Notable awkwardness and literalism |
| Marathi | 82.7 | Awkward literal syntax and rigid fluency |
| Malay | 82.4 | Pervasive incorrect diacritics |
| Tagalog | 82.2 | Slightly stiff and literal phrasing |
| Mongolian | 81.5 | Awkward phrasing and literalism |
| Malayalam | 81.2 | Literal syntax reduces fluency |
| Welsh | 80.5 | Lacks fluency and naturalness |
| Lao | 80.5 | Awkward literal phrasing |
| Burmese | 80.4 | Unnatural terminology and phrasing |
| Bengali | 80.3 | Severe Unicode character corruption |
| Hebrew | 79.8 | Literal phrasing and minor punctuation errors |
| Lithuanian | 79.8 | Significant issues with fluency and naturalness |
| Slovene | 79.2 | Notable mechanical and grammatical errors |
| Chinese | 78.8 | Stiff phrasing and dialogue formatting errors |
| German | 78.7 | Mechanically translated with awkward phrasing |
| Finnish | 78.5 | Translationese and minor inconsistencies |
| Romanian | 77.7 | Speaker attribution error and awkward phrasing |
| Norwegian | 77.5 | Systematic scientific terminology errors |
| Russian | 77.5 | Missing speaker tags breaks dialogue format |
| Hindi | 77.2 | Stiff phrasing due to literal translation |
| Telugu | 76.9 | Noticeable fluency issues and literal phrasing |
| Korean | 75.7 | Stiff and unnatural phrasing detracts from fluency |
| Khmer | 75.5 | Rigid and unnatural phrasing |
| Kannada | 75.2 | Rigid literal phrasing disrupting natural flow |
| Afrikaans | 73.8 | Noticeable fluency issues |
| Sinhala | 73.8 | Noticeable fluency and naturalness issues |
| Nepali | 73.0 | Unnatural conversational tone and rigid literal structure |
| Basque | 72.8 | Inconsistent speaker attribution and missing labels |
| Urdu | 71.3 | Inconsistent scientific terminology and awkward phrasing |
| Thai | 70.9 | Inconsistent tone and awkward phrasing |
| Irish | 69.3 | Major language mixing and errors |
| Swahili | 69.2 | Inconsistent terminology and awkward syntax |
| Greek | 68.0 | Literal phrasing and terminological errors |
| Tamil | 67.0 | Inconsistent English-Tamil mixing and formatting errors |
| Interlingua | 64.8 | Severe code-switching and text corruption |
