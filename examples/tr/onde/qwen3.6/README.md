# examples/tr/onde/qwen3.6/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6. The comparison with gpt-oss:120b as evaluator is in `gpt-oss-120b/`.

- Translation model: qwen3.6
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it, gpt-oss:120b for comparison)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 92.3 | Minor idiomatic flow issues |
| Portuguese | 90.2 | Minor literal phrasing and stiff transitions |
| Galician | 88.4 | Residual stiffness and minor awkwardness |
| Chinese | 86.9 | Notable grammatical errors and awkward phrasing |
| Romanian | 86.2 | Lexical errors and awkward phrasing |
| Persian | 85.9 | Noticeable linguistic awkwardness |
| Ukrainian | 85.3 | Mechanical translation artifacts and grammatical errors |
| German | 84.5 | Inconsistent register mixing formal and informal address |
| Polish | 84.5 | Grammatical errors and awkward phrasing |
| Swedish | 83.9 | Notable lack of fluency and naturalness |
| Afrikaans | 82.5 | Awkward literalisms and grammatical inconsistencies |
| Croatian | 82.1 | Grammatical errors and awkward phrasing |
| Catalan | 82.0 | Presence of anglicisms and literal translations |
| Danish | 80.4 | Language leakage and unnatural phrasing |
| Norwegian | 80.4 | Significant grammatical and syntax issues |
| Russian | 80.4 | Inconsistent pronouns and awkward phrasing |
| Serbian | 80.3 | Grammatical inconsistencies break conversational flow |
| French | 80.2 | Notable lexical inaccuracies and anglicisms break immersion |
| Dutch | 80.2 | Poor handling of math notation causes clunky phrasing |
| Slovak | 79.9 | Severe grammatical errors and unnatural phrasing |
| Bulgarian | 79.3 | Prominent Russian intrusion and terminology errors |
| Vietnamese | 79.0 | Awkward idiomatic flow |
| Lithuanian | 78.3 | Stylistic and idiomatic issues |
| Czech | 78.2 | Literal and awkward phrasing |
| Italian | 77.5 | Retention of untranslated foreign word |
| Albanian | 76.5 | Frequent inaccurate lexical choices |
| Hungarian | 76.4 | Grammatical errors and awkward phrasing |
| Estonian | 75.8 | Persistent grammatical and lexical errors |
| Belarusian | 75.5 | Grammatical errors and non-standard terminology |
| Hebrew | 75.3 | Phonetic spelling and nonsensical fragments |
| Finnish | 74.8 | Presence of English fragment |
| Indonesian | 74.8 | Code-switching error with Chinese characters |
| Japanese | 74.8 | Mixed language and register inconsistencies |
| Korean | 73.8 | Mixed-language error and inconsistent terminology |
| Malay | 72.8 | Major mistranslations and unnatural phrasing |
| Macedonian | 72.2 | Numerous critical linguistic errors and mistranslations |
| Latvian | 72.0 | Frequent grammatical errors and unnatural phrasing |
| Turkish | 71.3 | Critical literalism and terminology errors |
| Lao | 70.2 | Severe terminology and fluency issues |
| Icelandic | 69.9 | Severe grammatical and lexical errors |
| Azerbaijani | 69.0 | Pervasive misspellings and grammatical errors |
| Arabic | 68.8 | Untranslated Chinese characters disrupt text |
| Swahili | 67.0 | Severe grammatical errors and mistranslations |
| Armenian | 66.7 | Frequent spelling errors and lexical inaccuracies |
| Urdu | 66.2 | Mixed language artifacts |
| Mongolian | 65.8 | Critical mistranslation and poor fluency |
| Interlingua | 65.4 | Severe code-switching and structural defects |
| Slovene | 64.3 | Excessive literal translation and grammatical errors |
| Esperanto | 64.2 | Critical contamination by Chinese characters |
| Georgian | 61.8 | Critical semantic errors and nonsensical phrasing |
| Bengali | 61.7 | Extensive grammatical and syntactic errors |
| Khmer | 60.9 | Severely flawed terminology and unnatural fluency |
| Thai | 60.7 | Severe typos and non-standard spelling |
| Marathi | 58.9 | Severe quality issues |
| Sinhala | 58.8 | Severe grammatical errors and technical inaccuracies |
| Nepali | 57.8 | Severe character corruption and typos |
| Tagalog | 55.1 | Mixed language errors and poor grammar |
| Greek | 55.0 | Critical terminology errors and unnatural fluency |
| Welsh | 53.8 | Severe grammar and vocabulary failures |
| Basque | 53.2 | Severe lexical inaccuracies and grammatical errors |
| Hindi | 52.8 | Severe orthographic errors and script mixing |
| Kannada | 51.5 | Severe lexical and grammatical errors |
| Irish | 48.8 | Severe grammatical breakdowns and vocabulary errors |
| Telugu | 48.2 | Severe OCR/Garbled Artifacts |
| Tamil | 48.0 | Extensive text corruption and structural failure |
| Malayalam | 46.6 | Severe linguistic degradation and hallucination |
| Burmese | 44.1 | Infinite repetition loop and untranslated terms |

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
