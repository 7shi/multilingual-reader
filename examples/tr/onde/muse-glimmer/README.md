# examples/tr/onde/muse-glimmer/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: muse-glimmer
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 93.1 | Incomplete rendering of filler word "Okay" |
| Polish | 90.8 | Slightly stiff phrasing |
| Spanish | 90.6 | Minor native phrasing nuances slightly lower fluency score |
| Romanian | 88.8 | Minor fluency and gender agreement issues |
| Vietnamese | 87.7 | Retains degree of translationese |
| Dutch | 87.6 | Slight translationese and forced transitions |
| Macedonian | 86.2 | Stilted phrasing and minor grammatical inconsistencies |
| Portuguese | 85.3 | Slightly literal phrasing and unnatural fillers |
| Chinese | 85.3 | Translationese and awkward syntax |
| Galician | 84.8 | Minor typos and inconsistencies |
| Danish | 84.4 | Slightly literal phrasing and minor grammatical issues |
| Estonian | 83.9 | Literal calques and minor lexical errors |
| Turkish | 81.9 | Inconsistent tone and awkward phrasing |
| Bulgarian | 81.5 | Literal calques and unnatural phrasing |
| Slovak | 81.5 | Lacks fluency and naturalness due to literal syntax |
| Croatian | 81.3 | Fluency and grammatical accuracy issues |
| Arabic | 81.2 | Awkward phrasing and grammatical inconsistencies |
| Japanese | 79.9 | Stiff and unnatural dialogue |
| Hebrew | 79.8 | Unidiomatic and syntactically awkward |
| Czech | 78.5 | Significant grammatical agreement errors |
| German | 78.5 | Persistent grammatical errors |
| Afrikaans | 78.3 | Fluency issues and unnatural phrasing |
| Catalan | 76.4 | Glaring linguistic inaccuracies and unnatural syntax |
| Persian | 76.0 | Inconsistent scientific terminology transliteration |
| Ukrainian | 75.7 | Notable repetition error |
| Malay | 75.5 | Poor scientific terminology and unnatural phrasing |
| Swedish | 74.9 | Repeated line disrupts flow |
| Icelandic | 74.8 | Awkward phrasing and terminology errors |
| Lithuanian | 74.8 | Pervasive grammatical and syntactic errors |
| Norwegian | 74.8 | Mechanical and unnatural phrasing |
| Finnish | 74.6 | Severe grammatical and terminological errors |
| French | 74.6 | Lack of fluency and naturalness |
| Slovene | 74.2 | Grammatical errors and awkward phrasing |
| Latvian | 74.1 | Significant linguistic unnaturalness and grammatical inconsistencies |
| Swahili | 73.8 | Severe terminology and scientific accuracy errors |
| Hungarian | 73.5 | Clear editing error and diacritic issues |
| Esperanto | 73.0 | Critical terminology errors |
| Serbian | 71.9 | Mechanical sentence duplication and poor grammar |
| Armenian | 71.7 | Poor transliteration and grammar |
| Korean | 71.4 | Significant fluency issues and script errors |
| Azerbaijani | 71.2 | Severe linguistic and structural defects |
| Indonesian | 71.0 | Content redundancy from pasted drafts |
| Tagalog | 70.8 | Poor physics terminology and unnatural phrasing |
| Basque | 70.0 | Severe grammatical and lexical errors |
| Welsh | 69.4 | Grammatical errors and non-existent words |
| Urdu | 69.3 | Inconsistent terminology and unnatural mix of scripts |
| Georgian | 68.8 | Unnatural calques and technical inaccuracies |
| Albanian | 66.2 | Pervasive grammatical errors in gender and definiteness |
| Belarusian | 65.1 | Repetition error and mechanical flaws |
| Mongolian | 65.0 | Severe linguistic deficiencies and terminology errors |
| Interlingua | 63.8 | Structurally broken gibberish with technical artifacts |
| Irish | 62.1 | Significant linguistic and stylistic flaws |
| Tamil | 60.0 | Severe grammatical and spelling errors |
| Russian | 58.8 | Severe grammatical errors and text duplication |
| Greek | 58.1 | Severe lexical and grammatical errors |
| Malayalam | 58.1 | Severe grammatical errors and unnatural phrasing |
| Telugu | 57.0 | Inconsistent script mixing and poor fluency |
| Thai | 54.8 | Severe character corruption rendering text unreadable |
| Marathi | 53.8 | severe linguistic errors |
| Kannada | 51.3 | Severe grammatical and dialectal inconsistency |
| Hindi | 50.8 | Severe formatting collapse |
| Bengali | 50.7 | Severe orthographic errors |
| Lao | 50.0 | Severe lexical errors and hallucinations |
| Nepali | 45.5 | Severe OCR-like corruption and typos |
| Khmer | 40.6 | Severe lexical hallucination and garbled text |
| Sinhala | 38.1 | Catastrophic quality with non-existent vocabulary |
| Burmese | 22.5 | Severe OCR errors and garbled text |
