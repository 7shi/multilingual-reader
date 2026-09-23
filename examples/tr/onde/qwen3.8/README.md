# examples/tr/onde/qwen3.8/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: qwen3.8
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.2 | Minor subtle idiomatic variations |
| French | 90.5 | Pronoun inconsistency |
| Chinese | 90.3 | Subtle phrasing choices slightly less idiomatic |
| Arabic | 87.7 | Awkward phrasing and stiffness |
| Romanian | 87.0 | Minor gender agreement errors |
| Catalan | 86.3 | Awkward literal phrasing detracts from fluency |
| Portuguese | 84.5 | Mechanical fluency |
| Vietnamese | 84.1 | Lack of natural fluency |
| Malay | 83.8 | Lacks fluency and naturalness |
| German | 82.3 | Stiff literal phrasing and awkward collocations |
| Italian | 82.2 | Lacks polish and precise terminology |
| Ukrainian | 82.0 | Over-literal syntax and grammar errors |
| Turkish | 81.8 | Awkward phrasing and literal translations |
| Polish | 79.6 | Grammatical and stylistic flaws |
| Swedish | 79.0 | Mechanical stiffness and awkward phrasing |
| Russian | 78.5 | Contextual inconsistency between formal and informal address |
| Croatian | 77.7 | Significant grammatical and lexical errors |
| Bulgarian | 77.5 | Grammatical inaccuracies and unnatural phrasing |
| Galician | 77.4 | Orthographic inconsistency and translation errors |
| Danish | 77.2 | Literal phrasing and grammatical errors |
| Dutch | 77.1 | Untranslated English word and stiff phrasing |
| Finnish | 76.1 | Significant mistranslations and grammatical flaws |
| Indonesian | 75.3 | Chinese character intrusion |
| Norwegian | 75.2 | Grammatical errors and mixed-language artifact |
| Japanese | 75.1 | Language leakage with untranslated text |
| Afrikaans | 74.9 | Inconsistent orthography and calqued phrasing |
| Czech | 74.8 | Severe grammatical breakdown and non-Latin artifacts at the end |
| Persian | 73.8 | Language intrusion issues |
| Lithuanian | 73.3 | Terminological inaccuracies and hallucinations |
| Macedonian | 73.2 | Significant fluency and grammatical issues |
| Serbian | 73.0 | Severe grammatical errors and Chinese character intrusion |
| Albanian | 71.7 | Significant linguistic unnaturalness and grammatical errors |
| Slovak | 70.5 | Pervasive grammatical errors and awkward phrasing |
| Hindi | 69.8 | Poor fluency and unnatural phrasing |
| Hungarian | 67.3 | Critical technical terminology errors |
| Urdu | 66.7 | Over-reliance on phonetic transliteration |
| Belarusian | 65.5 | Awkward phrasing and unnatural dialogue |
| Slovene | 65.1 | Severe physics terminology errors |
| Interlingua | 64.1 | Poor fluency and awkward phrasing |
| Nepali | 63.6 | Severe fidelity issues with Chinese chars |
| Bengali | 62.6 | Critical scientific terminology errors |
| Azerbaijani | 62.2 | Critical errors and mistranslations |
| Latvian | 58.9 | Severe grammatical errors and incorrect terminology |
| Esperanto | 57.9 | Severe lexical errors and grammatical breakdown |
| Hebrew | 57.3 | Severe linguistic degradation and gibberish |
| Korean | 57.0 | Contains untranslated Chinese characters and severe truncation |
| Marathi | 56.6 | Poor fluency and frequent grammatical errors |
| Swahili | 56.2 | Severe terminology errors and poor fluency |
| Khmer | 55.8 | Severe speaker misattribution and major translation errors |
| Estonian | 55.5 | Untranslated English fragments and nonsensical terms |
| Tagalog | 55.5 | Pervasive incorrect vocabulary and technical errors |
| Basque | 53.8 | Catastrophic text repetition |
| Greek | 51.9 | Significant fragmentation and mixed language |
| Tamil | 51.8 | Severe linguistic contamination |
| Telugu | 49.6 | Severe lexical and grammatical errors |
| Thai | 49.5 | Severely flawed with incomplete text |
| Lao | 49.3 | Severe mistranslations and gibberish |
| Irish | 47.3 | Machine-generated gibberish |
| Sinhala | 45.5 | Severe lexical errors and hallucinated words |
| Armenian | 45.1 | Severe grammatical errors and mixed languages |
| Georgian | 44.6 | Severe semantic errors and nonsensical terms |
| Icelandic | 41.9 | Severe terminology errors and hallucinations |
| Kannada | 40.8 | Korean character intrusion |
| Burmese | 40.8 | Severe semantic errors and hallucinations |
| Welsh | 39.8 | Chaotic mixture of English and pseudo-Welsh |
| Mongolian | 38.7 | Severe grammatical errors and lexical hallucinations |
| Malayalam | 38.0 | Chaotic mix of broken Malayalam and transliterated English |
