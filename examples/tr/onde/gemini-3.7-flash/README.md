# examples/tr/onde/gemini-3.7-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-3.7-flash
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.8 | Sound translation with minor stylistic deductions |
| Catalan | 93.2 | Minor stylistic awkwardness in transitions |
| French | 93.1 | Occasional non-idiomatic phrasing and filler words |
| Portuguese | 93.0 | Lacks fluency and naturalness |
| Italian | 92.7 | No structural defects, omissions, or major errors |
| Galician | 91.9 | Slightly literal phrasing and stiff terminology |
| Hungarian | 90.4 | Unnatural filler word usage |
| Ukrainian | 90.1 | Minor literal translations reduce naturalness |
| Macedonian | 89.8 | Slightly rigid sentence structures |
| Arabic | 89.1 | Occasionally rigid phrasing |
| Czech | 88.9 | Slight structural rigidities affecting fluency |
| Bulgarian | 88.4 | Minor stiffness in dialogue markers |
| Danish | 88.4 | Minor lack of native fluency |
| Indonesian | 88.4 | Slightly formal phrasing and syntax |
| Polish | 88.3 | Slightly stiff transitional phrases and colloquialisms |
| Dutch | 88.2 | Slightly stiff phrasing |
| Vietnamese | 88.2 | Occasionally rigid tone |
| Japanese | 88.1 | Slightly abrupt speaker transitions |
| Georgian | 88.0 | Retains English syntax and fillers |
| Latvian | 87.8 | Minor stiffness in colloquial dialogue fluency |
| Turkish | 87.3 | Overuse of calques and ellipses |
| Albanian | 87.2 | Some sentences feel slightly less idiomatic |
| Slovak | 87.1 | Slightly rigid and literal tone |
| Serbian | 87.1 | Slightly stiff phrasing in specific scientific contexts |
| Swedish | 87.1 | Slightly literal phrasing |
| Icelandic | 86.7 | Lacks fluency and naturalness |
| Croatian | 86.3 | Noticeable linguistic awkwardness |
| Estonian | 85.5 | Translationese and awkward idioms |
| Armenian | 85.5 | Notable awkwardness and literalism |
| Persian | 85.1 | Tonal inconsistency due to casual language |
| Azerbaijani | 84.9 | Stiff literal phrasing and non-standard terms |
| Esperanto | 83.9 | Slightly rigid conversational flow |
| Belarusian | 83.5 | Significant typo in superposition term and awkward phrasing |
| Marathi | 82.1 | Awkward literal syntax and rigid fluency |
| Mongolian | 81.8 | Awkward phrasing and literalism |
| Malayalam | 81.3 | Literal syntax reduces fluency |
| Bengali | 81.0 | Severe Unicode character corruption |
| Slovene | 79.8 | Notable mechanical and grammatical errors |
| Romanian | 79.5 | Speaker attribution error and awkward phrasing |
| Korean | 79.3 | Stiff and unnatural phrasing detracts from fluency |
| German | 79.0 | Mechanically translated with awkward phrasing |
| Lithuanian | 78.9 | Significant issues with fluency and naturalness |
| Tagalog | 78.8 | Slightly stiff and literal phrasing |
| Malay | 78.7 | Pervasive incorrect diacritics |
| Russian | 78.3 | Missing speaker tags breaks dialogue format |
| Burmese | 78.2 | Unnatural terminology and phrasing |
| Chinese | 78.1 | Stiff phrasing and dialogue formatting errors |
| Welsh | 77.8 | Lacks fluency and naturalness |
| Norwegian | 77.7 | Systematic scientific terminology errors |
| Kannada | 77.5 | Rigid literal phrasing disrupting natural flow |
| Hebrew | 76.9 | Literal phrasing and minor punctuation errors |
| Afrikaans | 76.6 | Noticeable fluency issues |
| Lao | 76.3 | Awkward literal phrasing |
| Finnish | 76.2 | Translationese and minor inconsistencies |
| Khmer | 76.2 | Rigid and unnatural phrasing |
| Hindi | 74.8 | Stiff phrasing due to literal translation |
| Sinhala | 74.4 | Noticeable fluency and naturalness issues |
| Basque | 73.8 | Inconsistent speaker attribution and missing labels |
| Thai | 73.7 | Inconsistent tone and awkward phrasing |
| Urdu | 73.6 | Inconsistent scientific terminology and awkward phrasing |
| Nepali | 73.5 | Unnatural conversational tone and rigid literal structure |
| Swahili | 73.0 | Inconsistent terminology and awkward syntax |
| Greek | 72.3 | Literal phrasing and terminological errors |
| Interlingua | 71.9 | Severe code-switching and text corruption |
| Irish | 71.8 | Major language mixing and errors |
| Telugu | 70.6 | Noticeable fluency issues and literal phrasing |
| Tamil | 68.3 | Inconsistent English-Tamil mixing and formatting errors |
