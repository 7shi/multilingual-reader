# examples/tr/onde/union-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: union-alpha
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.6 | Minor stylistic nuance and regional interjection choice |
| Catalan | 94.5 | Handles minor calques and style preferences |
| French | 94.4 | No shortcomings noted; virtually perfect |
| Italian | 94.0 | No defects found; flawless execution |
| Romanian | 93.2 | Slightly literal phrasing feels unnatural |
| Swedish | 93.0 | Slightly stiff idiomatic expressions |
| Russian | 92.8 | Subtle stylistic friction points |
| Slovak | 92.7 | Slightly formal tone |
| Albanian | 91.9 | slight stiffness in transitions |
| Serbian | 91.3 | minor stylistic awkwardness |
| Latvian | 91.2 | Minor phrasing stiffness in fluency |
| Estonian | 91.0 | Slightly stiff phrasing |
| Slovene | 91.0 | Slightly rigid phrases and unnatural interjections |
| Bulgarian | 90.9 | Inconsistent localization of proper names |
| Croatian | 90.8 | Minor fluency issues |
| Belarusian | 90.5 | Minor stylistic issues affect fluency |
| Ukrainian | 90.5 | Minor syntactic rigidness and calques |
| Chinese | 90.5 | Minor stylistic rigidity |
| Dutch | 89.7 | Literal phrasing |
| Polish | 89.6 | Translationese causes stiff phrasing |
| Galician | 89.5 | Occasional stiffness from source text |
| Arabic | 89.4 | Slight traces of English syntax |
| Finnish | 89.4 | Stiff conversational flow |
| Malay | 89.3 | Slight rigidity and formal phrasing |
| German | 89.2 | Slightly translated feel |
| Georgian | 89.1 | Stiff phrasing and overly literal idioms |
| Macedonian | 89.1 | Minor stylistic stiffness |
| Hungarian | 88.8 | Slightly formal tone and stiff phrasing |
| Persian | 88.4 | Slightly literal and stiff phrasing |
| Japanese | 88.2 | Slight stiffness in conversational flow |
| Thai | 88.1 | Stilted phrasing and unnatural connectors |
| Basque | 88.0 | Slightly rigid tone |
| Vietnamese | 87.7 | Calques and stiff phrasing |
| Turkish | 87.6 | Retains filler words and unnatural phrasing |
| Hebrew | 87.5 | Slightly unnatural expression and stylistic rigidity |
| Malayalam | 87.4 | Occasionally unnatural phrasing and rigid syntax |
| Czech | 87.3 | Awkward and unnatural dialogue tone |
| Danish | 87.1 | Literal/Clunky Phrasing |
| Esperanto | 87.0 | Slightly stiff flow and awkward calques |
| Hindi | 87.0 | Terminology inconsistencies |
| Norwegian | 86.7 | Retains a somewhat "translated" feel |
| Azerbaijani | 86.6 | Slightly stiff fluency |
| Korean | 86.2 | Slightly stiff fluency |
| Afrikaans | 86.0 | Slight "translated" feel and mechanical dialogue flow |
| Welsh | 85.7 | Persistent grammatical errors regarding mutations and articles |
| Indonesian | 85.7 | Occasional literal phrasing reduces fluency |
| Armenian | 85.6 | Phrasing occasionally feels stiff or influenced by English syntax |
| Icelandic | 85.4 | Literal rendering with stiff academic tone |
| Lithuanian | 84.9 | Lack of naturalness in syntax and register |
| Swahili | 84.8 | Linguistic awkwardness from literal translations |
| Bengali | 84.2 | Lack of linguistic naturalness |
| Marathi | 84.2 | Minor literal phrasing and rigid connectors reduce naturalness |
| Urdu | 84.1 | Noticeable fluency issues and awkward phrasing |
| Portuguese | 84.0 | Slight sense of "translationese" |
| Khmer | 83.5 | Rigid sentence structures hinder natural flow |
| Tamil | 83.0 | Lacks naturalness and fluency |
| Mongolian | 82.7 | Significant stylistic and idiomatic issues |
| Tagalog | 82.0 | Poor naturalness due to literal translation |
| Kannada | 81.3 | Literal phrasing and awkward flow |
| Lao | 81.2 | Slightly rigid and awkward casual phrasing |
| Burmese | 81.1 | Inconsistent technical terminology and transliteration |
| Nepali | 76.1 | Literal translations of idioms |
| Telugu | 75.6 | Noticeable flaws in fluency and naturalness |
| Sinhala | 75.2 | Literal syntax and unnatural phrasing |
| Interlingua | 75.1 | Written in Latin instead of Interlingua |
| Greek | 73.8 | Notable terminology inaccuracies |
| Irish | 71.7 | Glaring mixed language error |
