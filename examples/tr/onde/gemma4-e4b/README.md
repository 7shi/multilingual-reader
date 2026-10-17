# examples/tr/onde/gemma4-e4b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: gemma4:e4b
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 90.8 | Slight translationese stiffness |
| Swedish | 90.3 | Slightly stiff and literal phrasing |
| Spanish | 89.5 | Minor awkwardness and stiffness |
| Russian | 89.5 | Occasional stiffness and non-idiomatic phrasing |
| Malay | 88.6 | Inconsistent terminology and awkward phrasing |
| Portuguese | 88.0 | Slightly literal phrasing and terminology inconsistencies |
| Indonesian | 87.4 | Slightly unnatural phrasing |
| Arabic | 87.0 | Slightly stiff phrasing |
| Chinese | 86.3 | awkward phrasing and literal translations |
| Turkish | 85.8 | Unnatural phrasing and literalism detract from fluency |
| Vietnamese | 85.4 | Lacks natural spoken flow |
| Italian | 85.2 | Slightly stiff phrasing and incorrect word usage |
| Thai | 84.7 | Lacks natural flow |
| German | 83.8 | Unnatural phrasing |
| Dutch | 83.8 | Unnatural handling of mathematical notation |
| Serbian | 83.3 | Significant fluency issues and grammatical inaccuracies |
| Ukrainian | 83.0 | Literal phrasing lacks fluency |
| Norwegian | 81.9 | Noticeable mechanical stiffness |
| Japanese | 81.3 | Slightly unnatural hesitation replication |
| Persian | 80.6 | Literalism and awkward phrasing |
| Danish | 78.3 | Inconsistent technical terminology and stiff phrasing |
| Nepali | 78.3 | Severe grammatical inconsistencies and awkward phrasing |
| Polish | 78.0 | Noticeable mechanical errors and awkward phrasing |
| Korean | 77.8 | Slightly stiff or overly literal phrasing |
| Hindi | 77.2 | Unnatural phrasing and lack of fluency |
| Hebrew | 76.7 | Inconsistent technical terminology |
| Finnish | 74.7 | Frequent grammatical errors and awkward phrasing |
| Tagalog | 74.5 | Unnatural and awkward phrasing |
| Swahili | 73.4 | Inconsistent terminology and unnatural phrasing |
| Afrikaans | 73.0 | Severe lexical and grammatical errors |
| Azerbaijani | 71.7 | Significant linguistic issues |
| Burmese | 70.3 | Severe generation glitch with Chinese characters |
| Tamil | 70.3 | Mixed scripts throughout |
| Lao | 69.8 | Linguistic awkwardness and poor fluency |
| Czech | 69.4 | Severe grammatical and lexical errors |
| Romanian | 68.7 | Severe language mixing and terminology errors |
| Bulgarian | 68.6 | Severe lack of linguistic competence |
| Bengali | 67.6 | Severe code-switching with Russian and Hindi |
| Croatian | 67.4 | Severe MT errors and non-existent words |
| Khmer | 67.2 | Encoding errors and language mixing |
| Galician | 66.7 | Poor fluency and naturalness due to foreign syntax |
| Telugu | 65.8 | Severe language mixing with Thai script |
| Catalan | 65.2 | Mixed languages and severe grammatical errors |
| Marathi | 64.4 | Significant mechanical errors and language leakage |
| Georgian | 63.8 | Injected foreign characters and words |
| Urdu | 61.7 | Mixed Chinese characters in Urdu text |
| Sinhala | 60.1 | Intrusive foreign language fragments |
| Malayalam | 59.5 | Severe code-switching with Chinese and Korean text |
| Macedonian | 59.0 | Severe mixed language and terminology errors |
| Mongolian | 58.8 | Severe retention of untranslated English text |
| Slovak | 55.0 | Severe linguistic degradation and nonsense vocabulary |
| Albanian | 53.4 | Severe grammatical errors and poor terminology |
| Kannada | 53.3 | Foreign script artifacts and severe errors |
| Greek | 52.2 | Severe mixed-language corruption |
| Slovene | 51.2 | Complete gibberish, not valid Slovene |
| Armenian | 46.2 | Severe hybrid-language contamination |
| Esperanto | 45.2 | Riddled with nonsense vocabulary |
| Hungarian | 45.2 | Severe linguistic errors and nonsensical content |
| Belarusian | 44.8 | Severe mechanical corruption and gibberish |
| Interlingua | 44.7 | Malformed Latin-English hybrid |
| Lithuanian | 39.5 | Severe linguistic errors and gibberish |
| Estonian | 37.6 | Lexical hallucinations and nonsense |
| Icelandic | 35.6 | Hallucinated vocabulary and syntax collapse |
| Latvian | 35.3 | Catastrophic lexical and grammatical failures |
| Basque | 27.3 | Completely unintelligible and broken grammar |
| Welsh | 21.9 | Nonsensical mixture of broken Welsh and random characters |
| Irish | 20.2 | Nonsensical pseudo-Gaelic gibberish |
