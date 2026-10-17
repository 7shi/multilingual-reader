# examples/tr/onde/qwen3.8/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: qwen3.8
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.6 | Minor subtle idiomatic variations |
| French | 91.9 | Pronoun inconsistency |
| Italian | 90.2 | Lacks polish and precise terminology |
| Chinese | 89.4 | Subtle phrasing choices slightly less idiomatic |
| Portuguese | 87.6 | Mechanical fluency |
| Arabic | 87.2 | Awkward phrasing and stiffness |
| Catalan | 85.3 | Awkward literal phrasing detracts from fluency |
| Vietnamese | 85.2 | Lack of natural fluency |
| Turkish | 85.1 | Awkward phrasing and literal translations |
| Romanian | 83.8 | Minor gender agreement errors |
| Polish | 82.2 | Grammatical and stylistic flaws |
| German | 82.0 | Stiff literal phrasing and awkward collocations |
| Malay | 82.0 | Lacks fluency and naturalness |
| Danish | 81.7 | Literal phrasing and grammatical errors |
| Ukrainian | 81.4 | Over-literal syntax and grammar errors |
| Galician | 80.9 | Orthographic inconsistency and translation errors |
| Bulgarian | 80.2 | Grammatical inaccuracies and unnatural phrasing |
| Dutch | 79.0 | Untranslated English word and stiff phrasing |
| Russian | 78.9 | Contextual inconsistency between formal and informal address |
| Afrikaans | 78.6 | Inconsistent orthography and calqued phrasing |
| Swedish | 78.3 | Mechanical stiffness and awkward phrasing |
| Croatian | 77.8 | Significant grammatical and lexical errors |
| Indonesian | 77.2 | Chinese character intrusion |
| Persian | 76.6 | Language intrusion issues |
| Czech | 76.5 | Severe grammatical breakdown and non-Latin artifacts at the end |
| Norwegian | 76.3 | Grammatical errors and mixed-language artifact |
| Japanese | 75.1 | Language leakage with untranslated text |
| Lithuanian | 74.3 | Terminological inaccuracies and hallucinations |
| Finnish | 74.1 | Significant mistranslations and grammatical flaws |
| Serbian | 74.0 | Severe grammatical errors and Chinese character intrusion |
| Macedonian | 73.2 | Significant fluency and grammatical issues |
| Albanian | 72.5 | Significant linguistic unnaturalness and grammatical errors |
| Slovak | 72.2 | Pervasive grammatical errors and awkward phrasing |
| Hindi | 69.9 | Poor fluency and unnatural phrasing |
| Urdu | 68.7 | Over-reliance on phonetic transliteration |
| Slovene | 68.4 | Severe physics terminology errors |
| Hungarian | 66.7 | Critical technical terminology errors |
| Belarusian | 66.2 | Awkward phrasing and unnatural dialogue |
| Nepali | 65.5 | Severe fidelity issues with Chinese chars |
| Bengali | 63.4 | Critical scientific terminology errors |
| Interlingua | 62.9 | Poor fluency and awkward phrasing |
| Latvian | 61.4 | Severe grammatical errors and incorrect terminology |
| Azerbaijani | 61.0 | Critical errors and mistranslations |
| Korean | 59.4 | Contains untranslated Chinese characters and severe truncation |
| Hebrew | 58.7 | Severe linguistic degradation and gibberish |
| Esperanto | 58.5 | Severe lexical errors and grammatical breakdown |
| Estonian | 57.8 | Untranslated English fragments and nonsensical terms |
| Marathi | 57.7 | Poor fluency and frequent grammatical errors |
| Swahili | 57.2 | Severe terminology errors and poor fluency |
| Tamil | 56.2 | Severe linguistic contamination |
| Khmer | 55.7 | Severe speaker misattribution and major translation errors |
| Basque | 55.4 | Catastrophic text repetition |
| Tagalog | 54.5 | Pervasive incorrect vocabulary and technical errors |
| Greek | 53.5 | Significant fragmentation and mixed language |
| Thai | 52.0 | Severely flawed with incomplete text |
| Telugu | 49.5 | Severe lexical and grammatical errors |
| Georgian | 49.1 | Severe semantic errors and nonsensical terms |
| Lao | 49.0 | Severe mistranslations and gibberish |
| Armenian | 48.4 | Severe grammatical errors and mixed languages |
| Irish | 47.5 | Machine-generated gibberish |
| Icelandic | 44.8 | Severe terminology errors and hallucinations |
| Sinhala | 44.2 | Severe lexical errors and hallucinated words |
| Mongolian | 43.4 | Severe grammatical errors and lexical hallucinations |
| Burmese | 42.9 | Severe semantic errors and hallucinations |
| Kannada | 42.7 | Korean character intrusion |
| Malayalam | 40.7 | Chaotic mix of broken Malayalam and transliterated English |
| Welsh | 40.5 | Chaotic mixture of English and pseudo-Welsh |
