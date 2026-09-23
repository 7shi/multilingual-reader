# examples/tr/onde/qwen3.6/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6. The comparison with gpt-oss:120b as evaluator is in `gpt-oss-120b/`.

- Translation model: qwen3.6
- Evaluation model: jev-1.13.0 (qwen3.6 before it, gpt-oss:120b for comparison)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.0 | Minor idiomatic flow issues |
| Portuguese | 87.0 | Minor literal phrasing and stiff transitions |
| Romanian | 86.9 | Lexical errors and awkward phrasing |
| Galician | 86.5 | Residual stiffness and minor awkwardness |
| Polish | 86.5 | Grammatical errors and awkward phrasing |
| German | 86.1 | Inconsistent register mixing formal and informal address |
| Ukrainian | 84.7 | Mechanical translation artifacts and grammatical errors |
| Croatian | 84.6 | Grammatical errors and awkward phrasing |
| Swedish | 83.1 | Notable lack of fluency and naturalness |
| Persian | 82.7 | Noticeable linguistic awkwardness |
| Russian | 82.2 | Inconsistent pronouns and awkward phrasing |
| Serbian | 81.9 | Grammatical inconsistencies break conversational flow |
| Afrikaans | 81.7 | Awkward literalisms and grammatical inconsistencies |
| Chinese | 81.7 | Notable grammatical errors and awkward phrasing |
| Dutch | 80.9 | Poor handling of math notation causes clunky phrasing |
| Catalan | 80.8 | Presence of anglicisms and literal translations |
| Italian | 79.7 | Retention of untranslated foreign word |
| Norwegian | 79.6 | Significant grammatical and syntax issues |
| Albanian | 79.3 | Frequent inaccurate lexical choices |
| French | 78.9 | Notable lexical inaccuracies and anglicisms break immersion |
| Czech | 78.8 | Literal and awkward phrasing |
| Lithuanian | 78.3 | Stylistic and idiomatic issues |
| Slovak | 77.5 | Severe grammatical errors and unnatural phrasing |
| Bulgarian | 77.4 | Prominent Russian intrusion and terminology errors |
| Danish | 77.4 | Language leakage and unnatural phrasing |
| Vietnamese | 77.2 | Awkward idiomatic flow |
| Belarusian | 77.0 | Grammatical errors and non-standard terminology |
| Hungarian | 76.5 | Grammatical errors and awkward phrasing |
| Finnish | 75.7 | Presence of English fragment |
| Estonian | 74.8 | Persistent grammatical and lexical errors |
| Japanese | 74.4 | Mixed language and register inconsistencies |
| Indonesian | 72.8 | Code-switching error with Chinese characters |
| Korean | 71.6 | Mixed-language error and inconsistent terminology |
| Lao | 71.5 | Severe terminology and fluency issues |
| Turkish | 71.5 | Critical literalism and terminology errors |
| Azerbaijani | 71.4 | Pervasive misspellings and grammatical errors |
| Latvian | 71.4 | Frequent grammatical errors and unnatural phrasing |
| Hebrew | 71.2 | Phonetic spelling and nonsensical fragments |
| Malay | 70.5 | Major mistranslations and unnatural phrasing |
| Macedonian | 69.2 | Numerous critical linguistic errors and mistranslations |
| Icelandic | 68.8 | Severe grammatical and lexical errors |
| Arabic | 67.1 | Untranslated Chinese characters disrupt text |
| Armenian | 66.8 | Frequent spelling errors and lexical inaccuracies |
| Swahili | 65.9 | Severe grammatical errors and mistranslations |
| Mongolian | 65.6 | Critical mistranslation and poor fluency |
| Georgian | 64.0 | Critical semantic errors and nonsensical phrasing |
| Slovene | 63.9 | Excessive literal translation and grammatical errors |
| Urdu | 61.8 | Mixed language artifacts |
| Esperanto | 61.7 | Critical contamination by Chinese characters |
| Interlingua | 61.2 | Severe code-switching and structural defects |
| Khmer | 60.5 | Severely flawed terminology and unnatural fluency |
| Bengali | 60.0 | Extensive grammatical and syntactic errors |
| Sinhala | 57.5 | Severe grammatical errors and technical inaccuracies |
| Tagalog | 57.5 | Mixed language errors and poor grammar |
| Greek | 57.0 | Critical terminology errors and unnatural fluency |
| Thai | 56.6 | Severe typos and non-standard spelling |
| Nepali | 53.8 | Severe character corruption and typos |
| Welsh | 52.6 | Severe grammar and vocabulary failures |
| Basque | 52.6 | Severe lexical inaccuracies and grammatical errors |
| Marathi | 51.8 | Severe quality issues |
| Kannada | 50.1 | Severe lexical and grammatical errors |
| Irish | 49.6 | Severe grammatical breakdowns and vocabulary errors |
| Telugu | 48.2 | Severe OCR/Garbled Artifacts |
| Hindi | 47.0 | Severe orthographic errors and script mixing |
| Burmese | 42.2 | Infinite repetition loop and untranslated terms |
| Malayalam | 42.1 | Severe linguistic degradation and hallucination |
| Tamil | 42.1 | Extensive text corruption and structural failure |

## Past Experiment: Comparison with Evaluation by gpt-oss:120b

In addition to evaluation by `qwen3.6` (`evals/`), evaluation by `gpt-oss:120b` was also carried out for comparative verification. The results are stored in the `gpt-oss-120b/` directory (evaluations in `gpt-oss-120b/evals/`, scores in `gpt-oss-120b/SCORES.txt`).

| Language | qwen3.6 | gpt-oss |
| :--- | :--- | :--- |
| Estonian | 53 | 84 |
| Serbian | 85 | 79 |
| Turkish | 63 | 77 |
| Korean | 75 | 74 |
| Kannada | 38 | 73 |
| Esperanto | 27 | 64 |
| Telugu | 39 | 62 |
| Hindi | 29 | 43 |
※ Only the 8 languages used at the time are covered.

Comparing these evaluation logs showed that **both models function very well, and equally, at "the ability to accurately detect and point out errors in the translated text (prompt contamination, Han-character hallucination, critical mistranslation, etc.)"**.

However, there was an **extreme difference between the two in "how they score those errors (the scoring criteria)"**, and as a result an interesting phenomenon was confirmed: "self-evaluation is overwhelmingly stricter."

1. **qwen3.6's (self-evaluation) tendency: a merciless deduction method (the grammar police)**
   Having accurately detected "grammar errors, incorrect inflection, spelling mistakes, unnatural literal translation" in its own generated translation, `qwen3.6` mercilessly criticized itself as needing "a fundamental rewrite" or being "completely broken," giving itself **extremely low scores (20s to 40s)**.

2. **gpt-oss:120b's (third-party evaluation) tendency: a meaning-focused, credit-giving approach (leniency)**
   In contrast, even while correctly listing and pointing out critical errors like Han-character contamination or mistranslation in its log, `gpt-oss:120b` tended to rate the overall gestalt of the context highly — "the scientific content comes through overall" — and give **relatively higher scores (60s to 80s)**.
