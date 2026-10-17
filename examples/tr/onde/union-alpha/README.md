# examples/tr/onde/union-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: union-alpha (Pareto 26.9 by The Unbiased Co., stealth listing). By its maker's announcement it is a router, not a single set of weights: several open and frontier models work the task, and a harness checks the work and calls in a stronger model when needed. Which model translated each language is not known.
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.4 | Minor stylistic nuance and regional interjection choice |
| French | 93.8 | No shortcomings noted; virtually perfect |
| Catalan | 93.0 | Handles minor calques and style preferences |
| Italian | 92.5 | No defects found; flawless execution |
| Russian | 92.3 | Subtle stylistic friction points |
| Swedish | 91.7 | Slightly stiff idiomatic expressions |
| Romanian | 91.2 | Slightly literal phrasing feels unnatural |
| Chinese | 91.2 | Minor stylistic rigidity |
| Slovak | 90.8 | Slightly formal tone |
| Serbian | 90.8 | minor stylistic awkwardness |
| German | 90.2 | Slightly translated feel |
| Bulgarian | 89.9 | Inconsistent localization of proper names |
| Dutch | 89.9 | Literal phrasing |
| Polish | 89.8 | Translationese causes stiff phrasing |
| Galician | 89.5 | Occasional stiffness from source text |
| Lithuanian | 89.5 | Lack of naturalness in syntax and register |
| Slovene | 89.5 | Slightly rigid phrases and unnatural interjections |
| Albanian | 89.2 | slight stiffness in transitions |
| Macedonian | 89.0 | Minor stylistic stiffness |
| Danish | 88.9 | Literal/Clunky Phrasing |
| Malay | 88.9 | Slight rigidity and formal phrasing |
| Estonian | 88.8 | Slightly stiff phrasing |
| Japanese | 88.8 | Slight stiffness in conversational flow |
| Latvian | 88.8 | Minor phrasing stiffness in fluency |
| Hungarian | 88.7 | Slightly formal tone and stiff phrasing |
| Ukrainian | 88.4 | Minor syntactic rigidness and calques |
| Finnish | 88.0 | Stiff conversational flow |
| Turkish | 88.0 | Retains filler words and unnatural phrasing |
| Vietnamese | 88.0 | Calques and stiff phrasing |
| Persian | 87.8 | Slightly literal and stiff phrasing |
| Hindi | 87.8 | Terminology inconsistencies |
| Indonesian | 87.6 | Occasional literal phrasing reduces fluency |
| Afrikaans | 87.3 | Slight "translated" feel and mechanical dialogue flow |
| Arabic | 87.3 | Slight traces of English syntax |
| Thai | 87.3 | Stilted phrasing and unnatural connectors |
| Belarusian | 87.0 | Minor stylistic issues affect fluency |
| Portuguese | 87.0 | Slight sense of "translationese" |
| Basque | 86.9 | Slightly rigid tone |
| Norwegian | 86.5 | Retains a somewhat "translated" feel |
| Czech | 86.2 | Awkward and unnatural dialogue tone |
| Croatian | 86.2 | Minor fluency issues |
| Georgian | 86.1 | Stiff phrasing and overly literal idioms |
| Malayalam | 86.1 | Occasionally unnatural phrasing and rigid syntax |
| Icelandic | 85.8 | Literal rendering with stiff academic tone |
| Korean | 85.8 | Slightly stiff fluency |
| Esperanto | 85.5 | Slightly stiff flow and awkward calques |
| Urdu | 85.5 | Noticeable fluency issues and awkward phrasing |
| Azerbaijani | 84.8 | Slightly stiff fluency |
| Armenian | 84.8 | Phrasing occasionally feels stiff or influenced by English syntax |
| Marathi | 84.0 | Minor literal phrasing and rigid connectors reduce naturalness |
| Swahili | 84.0 | Linguistic awkwardness from literal translations |
| Hebrew | 83.9 | Slightly unnatural expression and stylistic rigidity |
| Tamil | 83.7 | Lacks naturalness and fluency |
| Mongolian | 83.6 | Significant stylistic and idiomatic issues |
| Welsh | 83.4 | Persistent grammatical errors regarding mutations and articles |
| Khmer | 82.8 | Rigid sentence structures hinder natural flow |
| Bengali | 81.9 | Lack of linguistic naturalness |
| Sinhala | 81.9 | Literal syntax and unnatural phrasing |
| Kannada | 81.6 | Literal phrasing and awkward flow |
| Tagalog | 81.0 | Poor naturalness due to literal translation |
| Lao | 79.5 | Slightly rigid and awkward casual phrasing |
| Burmese | 78.7 | Inconsistent technical terminology and transliteration |
| Interlingua | 78.1 | Written in Latin instead of Interlingua |
| Greek | 75.3 | Notable terminology inaccuracies |
| Nepali | 74.7 | Literal translations of idioms |
| Irish | 72.6 | Glaring mixed language error |
| Telugu | 70.5 | Noticeable flaws in fluency and naturalness |
