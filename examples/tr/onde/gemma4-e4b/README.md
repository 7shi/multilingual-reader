# examples/tr/onde/gemma4-e4b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:e4b
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 92.4 | Slight translationese stiffness |
| Russian | 91.2 | Occasional stiffness and non-idiomatic phrasing |
| Swedish | 90.2 | Slightly stiff and literal phrasing |
| Italian | 89.4 | Slightly stiff phrasing and incorrect word usage |
| Arabic | 88.7 | Slightly stiff phrasing |
| Indonesian | 88.0 | Slightly unnatural phrasing |
| Malay | 88.0 | Inconsistent terminology and awkward phrasing |
| Chinese | 87.2 | awkward phrasing and literal translations |
| Vietnamese | 86.5 | Lacks natural spoken flow |
| Spanish | 86.2 | Minor awkwardness and stiffness |
| Serbian | 84.5 | Significant fluency issues and grammatical inaccuracies |
| Norwegian | 84.2 | Noticeable mechanical stiffness |
| Portuguese | 84.1 | Slightly literal phrasing and terminology inconsistencies |
| Turkish | 83.9 | Unnatural phrasing and literalism detract from fluency |
| Thai | 83.8 | Lacks natural flow |
| Dutch | 82.0 | Unnatural handling of mathematical notation |
| German | 81.9 | Unnatural phrasing |
| Ukrainian | 81.1 | Literal phrasing lacks fluency |
| Korean | 80.4 | Slightly stiff or overly literal phrasing |
| Polish | 80.3 | Noticeable mechanical errors and awkward phrasing |
| Persian | 79.5 | Literalism and awkward phrasing |
| Japanese | 79.2 | Slightly unnatural hesitation replication |
| Tagalog | 79.0 | Unnatural and awkward phrasing |
| Hindi | 78.5 | Unnatural phrasing and lack of fluency |
| Nepali | 77.4 | Severe grammatical inconsistencies and awkward phrasing |
| Danish | 76.3 | Inconsistent technical terminology and stiff phrasing |
| Hebrew | 75.8 | Inconsistent technical terminology |
| Finnish | 75.6 | Frequent grammatical errors and awkward phrasing |
| Swahili | 75.5 | Inconsistent terminology and unnatural phrasing |
| Azerbaijani | 72.6 | Significant linguistic issues |
| Afrikaans | 71.3 | Severe lexical and grammatical errors |
| Burmese | 71.1 | Severe generation glitch with Chinese characters |
| Lao | 70.4 | Linguistic awkwardness and poor fluency |
| Czech | 69.2 | Severe grammatical and lexical errors |
| Telugu | 68.9 | Severe language mixing with Thai script |
| Romanian | 68.1 | Severe language mixing and terminology errors |
| Croatian | 67.8 | Severe MT errors and non-existent words |
| Bulgarian | 66.6 | Severe lack of linguistic competence |
| Marathi | 66.6 | Significant mechanical errors and language leakage |
| Bengali | 66.1 | Severe code-switching with Russian and Hindi |
| Tamil | 65.3 | Mixed scripts throughout |
| Georgian | 64.5 | Injected foreign characters and words |
| Galician | 64.3 | Poor fluency and naturalness due to foreign syntax |
| Catalan | 62.4 | Mixed languages and severe grammatical errors |
| Khmer | 62.0 | Encoding errors and language mixing |
| Urdu | 61.6 | Mixed Chinese characters in Urdu text |
| Mongolian | 57.4 | Severe retention of untranslated English text |
| Malayalam | 56.9 | Severe code-switching with Chinese and Korean text |
| Macedonian | 56.8 | Severe mixed language and terminology errors |
| Sinhala | 56.4 | Intrusive foreign language fragments |
| Slovak | 53.2 | Severe linguistic degradation and nonsense vocabulary |
| Albanian | 53.0 | Severe grammatical errors and poor terminology |
| Kannada | 50.9 | Foreign script artifacts and severe errors |
| Greek | 48.5 | Severe mixed-language corruption |
| Slovene | 48.5 | Complete gibberish, not valid Slovene |
| Interlingua | 44.4 | Malformed Latin-English hybrid |
| Hungarian | 43.8 | Severe linguistic errors and nonsensical content |
| Esperanto | 42.7 | Riddled with nonsense vocabulary |
| Belarusian | 40.4 | Severe mechanical corruption and gibberish |
| Armenian | 38.4 | Severe hybrid-language contamination |
| Lithuanian | 37.6 | Severe linguistic errors and gibberish |
| Icelandic | 36.6 | Hallucinated vocabulary and syntax collapse |
| Estonian | 34.7 | Lexical hallucinations and nonsense |
| Latvian | 31.4 | Catastrophic lexical and grammatical failures |
| Basque | 25.0 | Completely unintelligible and broken grammar |
| Welsh | 20.4 | Nonsensical mixture of broken Welsh and random characters |
| Irish | 18.9 | Nonsensical pseudo-Gaelic gibberish |
