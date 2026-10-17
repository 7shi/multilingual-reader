# examples/tr/onde/gemma4-31b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemma4:31b-it-qat
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.2 | Mistranslation of "ingenuity" as "ingenuidad" |
| French | 93.4 | Excellent terminology and flow |
| Swedish | 92.0 | Minor literal phrasing and English cadence |
| Italian | 91.9 | Stiff phrasing and literal English interjections |
| German | 91.2 | Slightly rigid dialogue flow |
| Portuguese | 90.9 | Mistranslation of ingenuity as naivety |
| Russian | 90.8 | Slight deviations in colloquialism |
| Danish | 90.2 | Literal phrasing and stiffness |
| Dutch | 90.1 | Occasional literal phrasing and repetition |
| Thai | 90.1 | Slightly translated sentence structures |
| Galician | 89.7 | Retains slight structural shadow of English syntax |
| Korean | 89.4 | Sentence structure too close to English |
| Ukrainian | 89.2 | Minor grammatical awkwardness |
| Persian | 88.8 | Slightly literal phrasing disrupts naturalness |
| Norwegian | 88.7 | Retains an English rhythm and literal phrasing |
| Bulgarian | 88.4 | Slightly literal translations |
| Chinese | 87.8 | slight stiffness or overly literal phrasing |
| Romanian | 87.5 | Lacks naturalness and idiomatic flow |
| Turkish | 87.5 | Slightly stiff and literal phrasing |
| Japanese | 87.3 | Punctuation errors and stiff dialogue naturalness |
| Polish | 87.0 | Occasional stiffness and literal phrasing |
| Vietnamese | 87.0 | Slight translational rhythm and minor inconsistency |
| Serbian | 86.6 | Retains English prepositional logic |
| Finnish | 86.4 | Stiff phrasing and unnatural transitions |
| Hindi | 85.2 | Slightly rigid phrasing reduces natural flow |
| Croatian | 84.8 | Translationese quality and stiff dialogue |
| Indonesian | 84.4 | Overspecific word choice "rumbai" for fringes |
| Afrikaans | 84.1 | Potgooi and kruiesaal errors |
| Arabic | 82.5 | awkward phrasing and literal translations |
| Bengali | 82.5 | Severe character encoding errors |
| Malay | 81.9 | Noticeable mechanical and stylistic flaws |
| Czech | 81.7 | Awkward fluency and naturalness |
| Azerbaijani | 81.3 | Unnatural phrasing and terminology errors |
| Swahili | 81.1 | Notable fluency issues and awkward phrasing |
| Urdu | 80.2 | Excessive reliance on transliterated English terms |
| Esperanto | 79.8 | Unnatural phrasing and syntactic stiffness |
| Hebrew | 79.3 | Notable terminology errors and awkward phrasing |
| Tamil | 78.3 | Glaring Vietnamese code-switching error |
| Slovak | 78.0 | Pervasive grammatical mistakes and unnatural phrasing |
| Albanian | 77.4 | Careless retention of English words |
| Nepali | 76.7 | Language code-switching to English |
| Tagalog | 76.4 | Translationese and inconsistent terminology |
| Marathi | 76.2 | Inconsistent register and localization errors |
| Catalan | 75.9 | Untranslated Chinese character and gender agreement errors |
| Sinhala | 73.0 | Contaminated by Tamil and Chinese text |
| Belarusian | 70.5 | Severe text corruption and garbled words |
| Armenian | 70.0 | Severe language mixing and untranslated fragments |
| Telugu | 69.4 | Occasional inconsistencies and awkward phrasing |
| Burmese | 69.0 | Severe mixed-language fragmentation |
| Icelandic | 67.8 | Inconsistent mathematical notation formatting |
| Hungarian | 67.5 | Untranslated English words and nonsense phrases |
| Macedonian | 66.8 | Mixed-language artifacts and inaccurate terminology |
| Slovene | 66.3 | Severe grammatical and terminology errors with nonsensical phrases |
| Mongolian | 64.5 | Severe mistranslations and grammatical errors |
| Kannada | 64.4 | Hybrid defects and mixed-language intrusions |
| Latvian | 63.5 | Severe grammatical errors and mixed languages |
| Lao | 60.9 | Severe code-switching and language mixing |
| Malayalam | 60.0 | Severe language mixing and structural defects |
| Greek | 59.9 | Severe terminology and typographical errors |
| Khmer | 56.5 | Severe mixed-language corruption |
| Lithuanian | 53.6 | Critical failure with mixed languages and severe grammatical errors |
| Georgian | 53.0 | Severe structural defect with mixed script intrusions |
| Interlingua | 50.5 | Fails to meet basic grammar requirements |
| Estonian | 50.3 | Severe language pollution |
| Basque | 50.2 | Pervasive code-mixing with foreign languages |
| Welsh | 38.5 | Severe grammar errors and gibberish |
| Irish | 28.7 | Severe hallucination and code-switching |
