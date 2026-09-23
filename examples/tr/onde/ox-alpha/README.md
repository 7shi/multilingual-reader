# examples/tr/onde/ox-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: ox-alpha (glm-5.3-flash stealth)
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 95.9 | Professional grade, no significant corrections |
| Spanish | 94.1 | No shortcomings identified |
| Croatian | 93.4 | Minor stylistic fluency issues |
| Catalan | 92.8 | Minor stylistic rough spots in long sentences |
| Russian | 92.8 | Slight informal/pronoun inconsistency |
| Swedish | 92.8 | Minor stylistic choices do not detract from clarity |
| Serbian | 92.2 | Overuse of filler words like "Uh" and "Aha" |
| German | 91.5 | Minor grammatical error and slight stiffness |
| Slovak | 91.2 | Slight awkwardness in phrasing |
| Polish | 91.1 | Slightly rigid phrasing compared to native speech |
| Romanian | 91.0 | Minor fluency and tone issues |
| Galician | 90.9 | Inxenuidade mistranslated for ingenuity |
| Albanian | 90.7 | Occasional stiff phrasing |
| Slovene | 90.3 | Overly literal phrasing causes slight stiffness |
| Dutch | 89.8 | Slightly stiff Dutch phrasing |
| Arabic | 89.7 | Literal phrasing feels slightly unnatural |
| Macedonian | 89.7 | minor stylistic tweaks needed for native elegance |
| Bulgarian | 89.1 | minor phrasing stiffness and grammatical errors |
| Ukrainian | 89.0 | Slight awkwardness in idiomatic transitions |
| Belarusian | 88.9 | Slightly stiff phrasing from source structure |
| Danish | 88.4 | Adjective inflection and phrasing issues |
| Indonesian | 88.4 | Inconsistent use of pronouns |
| Thai | 88.4 | Slightly rigid phrasing disrupts natural flow |
| Persian | 88.2 | Minor stylistic and punctuation issues |
| Czech | 88.1 | Awkward conversational phrasing |
| Lithuanian | 87.9 | Literal calques disrupting natural rhythm |
| Japanese | 87.3 | Slight stiffness in conversational connectors |
| Turkish | 87.3 | Slightly rigid syntax lacks fluency |
| Hindi | 87.1 | Structural rigidity |
| Norwegian | 87.1 | Minor stylistic choices on mathematical notation |
| Esperanto | 87.0 | Literal phrasing reduces naturalness |
| Hebrew | 86.8 | Phrasing feels slightly literal or translation-heavy |
| Malay | 86.4 | Pervasive typographical errors and non-standard spellings |
| Vietnamese | 86.4 | Retains structural artifacts from English source |
| Azerbaijani | 86.3 | Rigid syntax and unnatural phrasing |
| Latvian | 86.2 | Slight stiffness in phrasing |
| Portuguese | 85.8 | Minor phrasing and filler overuse |
| Georgian | 85.2 | Slightly stiff conversational tone |
| Basque | 85.0 | Stylistic and grammatical inconsistencies |
| Korean | 84.7 | Minor stylistic nuances |
| Finnish | 84.5 | Slightly stiff dialogue and literal idiom translations |
| Afrikaans | 84.1 | Reads stiffly and formally due to literal syntax |
| Icelandic | 84.0 | Significant fluency issues and awkward phrasing |
| Armenian | 83.7 | Lacks conversational tone |
| Bengali | 83.1 | Literal terminology and stilted phrasing |
| Estonian | 83.0 | Minor lexical and syntactic flaws reduce naturalness |
| Swahili | 82.7 | Relies heavily on literal calques from English syntax |
| Nepali | 82.6 | Reads like a literal translation |
| Italian | 82.0 | Literal translations cause stiff phrasing |
| Mongolian | 82.0 | Poor fluency and naturalness due to literal phrasing |
| Tagalog | 81.1 | Unnatural literalisms and awkward phrasing |
| Marathi | 80.9 | Awkward interjections and fillers |
| Chinese | 78.5 | Slightly fragmented sentence structure |
| Welsh | 78.3 | Pervasive orthographic and grammatical errors |
| Hungarian | 77.5 | Deletion of speaker tags |
| Kannada | 77.3 | Awkward phrasing and stiff tone |
| Tamil | 77.1 | Stiff, literal phrasing |
| Telugu | 77.0 | awkward structural choices |
| Khmer | 76.7 | Inappropriate slang and awkward phrasing |
| Lao | 76.2 | Unnatural syntax and excessive spacing |
| Burmese | 76.2 | Unnatural literal translation |
| Interlingua | 75.5 | Severe linguistic issues with fluency and naturalness |
| Malayalam | 74.4 | Poor fluency and awkward phrasing |
| Irish | 72.2 | Frequent lexical inaccuracies and non-standard terminology |
| Sinhala | 70.9 | Inaccurate vocabulary and awkward phrasing |
| Urdu | 70.8 | Unnatural verbal cues and inconsistent technical terms |
| Greek | 64.0 | Conflates amplitude and width |
