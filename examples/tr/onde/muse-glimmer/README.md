# examples/tr/onde/muse-glimmer/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: muse-glimmer
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 91.4 | Minor native phrasing nuances slightly lower fluency score |
| Italian | 90.9 | Incomplete rendering of filler word "Okay" |
| Portuguese | 90.9 | Slightly literal phrasing and unnatural fillers |
| Polish | 88.4 | Slightly stiff phrasing |
| Dutch | 87.5 | Slight translationese and forced transitions |
| Romanian | 87.0 | Minor fluency and gender agreement issues |
| Vietnamese | 86.2 | Retains degree of translationese |
| Danish | 85.2 | Slightly literal phrasing and minor grammatical issues |
| Macedonian | 85.1 | Stilted phrasing and minor grammatical inconsistencies |
| Galician | 84.9 | Minor typos and inconsistencies |
| Japanese | 84.5 | Stiff and unnatural dialogue |
| Turkish | 83.0 | Inconsistent tone and awkward phrasing |
| Chinese | 82.6 | Translationese and awkward syntax |
| Estonian | 82.4 | Literal calques and minor lexical errors |
| Slovak | 82.1 | Lacks fluency and naturalness due to literal syntax |
| Arabic | 81.9 | Awkward phrasing and grammatical inconsistencies |
| French | 81.1 | Lack of fluency and naturalness |
| German | 80.6 | Persistent grammatical errors |
| Croatian | 80.3 | Fluency and grammatical accuracy issues |
| Bulgarian | 80.0 | Literal calques and unnatural phrasing |
| Malay | 79.0 | Poor scientific terminology and unnatural phrasing |
| Afrikaans | 78.7 | Fluency issues and unnatural phrasing |
| Persian | 78.7 | Inconsistent scientific terminology transliteration |
| Czech | 78.6 | Significant grammatical agreement errors |
| Lithuanian | 78.6 | Pervasive grammatical and syntactic errors |
| Ukrainian | 77.0 | Notable repetition error |
| Icelandic | 76.9 | Awkward phrasing and terminology errors |
| Hebrew | 76.7 | Unidiomatic and syntactically awkward |
| Swedish | 76.3 | Repeated line disrupts flow |
| Catalan | 76.1 | Glaring linguistic inaccuracies and unnatural syntax |
| Urdu | 76.1 | Inconsistent terminology and unnatural mix of scripts |
| Armenian | 74.7 | Poor transliteration and grammar |
| Indonesian | 74.7 | Content redundancy from pasted drafts |
| Norwegian | 73.7 | Mechanical and unnatural phrasing |
| Swahili | 73.5 | Severe terminology and scientific accuracy errors |
| Korean | 73.3 | Significant fluency issues and script errors |
| Serbian | 73.3 | Mechanical sentence duplication and poor grammar |
| Hungarian | 73.2 | Clear editing error and diacritic issues |
| Slovene | 73.2 | Grammatical errors and awkward phrasing |
| Finnish | 72.5 | Severe grammatical and terminological errors |
| Albanian | 71.7 | Pervasive grammatical errors in gender and definiteness |
| Azerbaijani | 71.3 | Severe linguistic and structural defects |
| Basque | 71.1 | Severe grammatical and lexical errors |
| Latvian | 71.0 | Significant linguistic unnaturalness and grammatical inconsistencies |
| Esperanto | 70.1 | Critical terminology errors |
| Georgian | 69.9 | Unnatural calques and technical inaccuracies |
| Welsh | 68.9 | Grammatical errors and non-existent words |
| Interlingua | 66.7 | Structurally broken gibberish with technical artifacts |
| Tagalog | 66.2 | Poor physics terminology and unnatural phrasing |
| Mongolian | 65.8 | Severe linguistic deficiencies and terminology errors |
| Belarusian | 65.3 | Repetition error and mechanical flaws |
| Tamil | 63.9 | Severe grammatical and spelling errors |
| Irish | 62.9 | Significant linguistic and stylistic flaws |
| Thai | 62.5 | Severe character corruption rendering text unreadable |
| Greek | 61.2 | Severe lexical and grammatical errors |
| Russian | 60.9 | Severe grammatical errors and text duplication |
| Malayalam | 59.9 | Severe grammatical errors and unnatural phrasing |
| Kannada | 58.0 | Severe grammatical and dialectal inconsistency |
| Marathi | 57.8 | severe linguistic errors |
| Bengali | 55.7 | Severe orthographic errors |
| Hindi | 55.7 | Severe formatting collapse |
| Telugu | 54.5 | Inconsistent script mixing and poor fluency |
| Lao | 52.5 | Severe lexical errors and hallucinations |
| Nepali | 48.9 | Severe OCR-like corruption and typos |
| Khmer | 45.5 | Severe lexical hallucination and garbled text |
| Sinhala | 43.6 | Catastrophic quality with non-existent vocabulary |
| Burmese | 25.7 | Severe OCR errors and garbled text |
