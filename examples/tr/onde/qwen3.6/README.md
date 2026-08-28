# examples/tr/onde/qwen3.6/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals*/`, and scores to `SCORES*.txt`.

- Translation model: qwen3.6
- Evaluation model: qwen3.6 (gpt-oss:120b for comparison)
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The quality trend for each language, based on the evaluation results (`SCORES.txt`) and manual content verification (evaluator: `qwen3.6`), is as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 97 | Exceptional quality with minor stylistic nuances |
| French | 97 | Retention of English word 'ripple' |
| Portuguese | 97 | Flawless high-quality work |
| Italian | 96 | Retained English word 'perplexing' |
| Romanian | 92 | High quality with minor typos and slips |
| Dutch | 91 | Minor calques and terminology errors |
| Russian | 91 | Minor typos and stiff phrasing |
| Vietnamese | 91 | Minor code-switching and fluency issues requiring light proofreading |
| German | 89 | Minor grammatical and terminology imperfections |
| Persian | 89 | Minor stylistic calques and transliterations |
| Galician | 89 | Portuguese lexical interference |
| Norwegian | 86 | Minor grammatical errors and awkward technical phrasing |
| Chinese | 86 | Accurate terminology hindered by literal phrasing |
| Serbian | 85 | Minor terminology errors like 'Abov limit' and typo 'divirira' |
| Croatian | 83 | Minor grammatical and terminology errors |
| Hungarian | 83 | Numerous typographical errors |
| Swedish | 80 | Clear signs of machine translation and literal phrasing |
| Afrikaans | 78 | Pervasive Dutch interference and typographical errors |
| Catalan | 78 | Multiple major grammatical errors |
| Lithuanian | 77 | Lexical errors and grammatical imperfections |
| Danish | 76 | Mixed-language artifact ('actually kender, faktum') |
| Japanese | 76 | Critical mixed-language artifacts disrupt fluency |
| Korean | 75 | Untranslated English words and technical inconsistencies |
| Ukrainian | 73 | Notable grammatical errors and awkward phrasing |
| Polish | 72 | Grammatical and typographical errors |
| Albanian | 71 | Grammatical errors and non-idiomatic phrasing |
| Hebrew | 70 | Severe typos and grammar errors |
| Czech | 68 | Grammatical errors and unnatural literal translations |
| Belarusian | 66 | High density of grammatical errors and unnatural phrasing |
| Latvian | 65 | Pervasive MT artifacts and grammatical errors |
| Turkish | 63 | Prominent mistranslations and fluency issues |
| Slovak | 62 | High frequency of grammatical and typographical errors |
| Greek | 61 | Critical terminology errors and unnatural phrasing |
| Indonesian | 55 | Mixed-language Chinese fragment and terminology errors |
| Malay | 55 | Technical terminology errors and unnatural phrasing |
| Estonian | 53 | Frequent terminology errors and typos |
| Bulgarian | 50 | Severe machine-translation artifacts and lexical errors |
| Urdu | 50 | Major lexical errors including Russian intrusion and mistranslations |
| Finnish | 49 | Severe grammatical errors and mixed-language artifacts |
| Slovene | 48 | Pervasive untranslated English fragments and grammatical errors |
| Azerbaijani | 46 | Severe terminology errors and unnatural phrasing |
| Armenian | 46 | Significant fluency and accuracy issues |
| Macedonian | 46 | Severe linguistic and technical inaccuracies |
| Lao | 45 | Severe physics terminology errors and poor fluency |
| Bengali | 42 | Extensive orthographic and mechanical errors |
| Mongolian | 42 | Severe lexical and grammatical errors impair readability |
| Telugu | 39 | Severe terminology inconsistency and pervasive grammatical errors |
| Marathi | 38 | Major linguistic flaws and spelling errors |
| Nepali | 37 | Pervasive typos and poor linguistic quality |
| Georgian | 36 | Severe systemic errors and major defects |
| Arabic | 33 | Intrusion of Chinese characters |
| Icelandic | 33 | Severe grammar errors and pervasive mistranslations |
| Interlingua | 32 | Severe mixed-language contamination and structural defects |
| Malayalam | 32 | Severe orthographic and grammatical defects |
| Sinhala | 32 | Pervasive systematic character corruption and grammatical defects |
| Swahili | 32 | Severe machine translation artifacts and linguistic flaws |
| Irish | 30 | Severe grammatical errors and incorrect scientific terminology |
| Khmer | 30 | Severe typos and terminology errors |
| Hindi | 29 | Severe typographical and systematic errors |
| Welsh | 27 | Severe machine-translation artifacts |
| Esperanto | 27 | Critical structural and lexical failures with mixed languages |
| Kannada | 26 | Severe terminology mistranslation and structural defects |
| Thai | 26 | Pervasive spelling and orthographic errors |
| Tagalog | 25 | Severe machine-translation artifacts and lexical errors |
| Basque | 23 | Severe lexical and grammatical defects |
| Burmese | 19 | Massive text-generation loop causes corruption |
| Tamil | 18 | Severe orthographic corruption and spelling errors |

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
