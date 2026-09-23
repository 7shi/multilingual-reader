# examples/tr/onde/gemma4-31b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemma4:31b-it-qat
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 94.7 | Excellent terminology and flow |
| Spanish | 94.5 | Mistranslation of "ingenuity" as "ingenuidad" |
| Russian | 92.8 | Slight deviations in colloquialism |
| Swedish | 92.7 | Minor literal phrasing and English cadence |
| Italian | 92.3 | Stiff phrasing and literal English interjections |
| Ukrainian | 91.4 | Minor grammatical awkwardness |
| German | 91.0 | Slightly rigid dialogue flow |
| Romanian | 90.8 | Lacks naturalness and idiomatic flow |
| Thai | 90.8 | Slightly translated sentence structures |
| Dutch | 90.2 | Occasional literal phrasing and repetition |
| Galician | 90.0 | Retains slight structural shadow of English syntax |
| Serbian | 89.8 | Retains English prepositional logic |
| Chinese | 89.2 | slight stiffness or overly literal phrasing |
| Korean | 88.9 | Sentence structure too close to English |
| Danish | 88.6 | Literal phrasing and stiffness |
| Bulgarian | 88.4 | Slightly literal translations |
| Turkish | 88.3 | Slightly stiff and literal phrasing |
| Polish | 88.2 | Occasional stiffness and literal phrasing |
| Persian | 88.1 | Slightly literal phrasing disrupts naturalness |
| Finnish | 88.0 | Stiff phrasing and unnatural transitions |
| Vietnamese | 87.0 | Slight translational rhythm and minor inconsistency |
| Norwegian | 86.5 | Retains an English rhythm and literal phrasing |
| Croatian | 86.0 | Translationese quality and stiff dialogue |
| Indonesian | 86.0 | Overspecific word choice "rumbai" for fringes |
| Portuguese | 85.5 | Mistranslation of ingenuity as naivety |
| Esperanto | 84.1 | Unnatural phrasing and syntactic stiffness |
| Bengali | 83.1 | Severe character encoding errors |
| Japanese | 83.0 | Punctuation errors and stiff dialogue naturalness |
| Hindi | 82.9 | Slightly rigid phrasing reduces natural flow |
| Swahili | 82.6 | Notable fluency issues and awkward phrasing |
| Hebrew | 82.3 | Notable terminology errors and awkward phrasing |
| Afrikaans | 81.0 | Potgooi and kruiesaal errors |
| Arabic | 80.9 | awkward phrasing and literal translations |
| Malay | 80.6 | Noticeable mechanical and stylistic flaws |
| Czech | 80.5 | Awkward fluency and naturalness |
| Slovak | 79.3 | Pervasive grammatical mistakes and unnatural phrasing |
| Tagalog | 78.1 | Translationese and inconsistent terminology |
| Azerbaijani | 77.4 | Unnatural phrasing and terminology errors |
| Tamil | 77.2 | Glaring Vietnamese code-switching error |
| Albanian | 77.1 | Careless retention of English words |
| Marathi | 76.7 | Inconsistent register and localization errors |
| Urdu | 76.2 | Excessive reliance on transliterated English terms |
| Nepali | 74.8 | Language code-switching to English |
| Telugu | 74.2 | Occasional inconsistencies and awkward phrasing |
| Catalan | 73.2 | Untranslated Chinese character and gender agreement errors |
| Belarusian | 69.5 | Severe text corruption and garbled words |
| Armenian | 69.3 | Severe language mixing and untranslated fragments |
| Icelandic | 67.2 | Inconsistent mathematical notation formatting |
| Sinhala | 66.2 | Contaminated by Tamil and Chinese text |
| Mongolian | 65.5 | Severe mistranslations and grammatical errors |
| Slovene | 65.0 | Severe grammatical and terminology errors with nonsensical phrases |
| Burmese | 64.0 | Severe mixed-language fragmentation |
| Macedonian | 63.7 | Mixed-language artifacts and inaccurate terminology |
| Hungarian | 62.9 | Untranslated English words and nonsense phrases |
| Kannada | 60.6 | Hybrid defects and mixed-language intrusions |
| Greek | 59.5 | Severe terminology and typographical errors |
| Latvian | 57.3 | Severe grammatical errors and mixed languages |
| Malayalam | 57.0 | Severe language mixing and structural defects |
| Lao | 56.2 | Severe code-switching and language mixing |
| Khmer | 52.7 | Severe mixed-language corruption |
| Lithuanian | 51.1 | Critical failure with mixed languages and severe grammatical errors |
| Georgian | 50.4 | Severe structural defect with mixed script intrusions |
| Estonian | 48.3 | Severe language pollution |
| Interlingua | 45.0 | Fails to meet basic grammar requirements |
| Basque | 44.5 | Pervasive code-mixing with foreign languages |
| Welsh | 37.2 | Severe grammar errors and gibberish |
| Irish | 27.5 | Severe hallucination and code-switching |
