# examples/tr/onde/ox-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: ox-alpha (glm-5.3-flash stealth)
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 94.5 | Professional grade, no significant corrections |
| Spanish | 93.6 | No shortcomings identified |
| Catalan | 92.9 | Minor stylistic rough spots in long sentences |
| Swedish | 92.0 | Minor stylistic choices do not detract from clarity |
| Portuguese | 91.5 | Minor phrasing and filler overuse |
| Galician | 91.4 | Inxenuidade mistranslated for ingenuity |
| Romanian | 91.1 | Minor fluency and tone issues |
| Russian | 90.5 | Slight informal/pronoun inconsistency |
| Croatian | 90.3 | Minor stylistic fluency issues |
| German | 90.1 | Minor grammatical error and slight stiffness |
| Arabic | 89.2 | Literal phrasing feels slightly unnatural |
| Polish | 89.2 | Slightly rigid phrasing compared to native speech |
| Norwegian | 89.0 | Minor stylistic choices on mathematical notation |
| Macedonian | 88.9 | minor stylistic tweaks needed for native elegance |
| Dutch | 88.9 | Slightly stiff Dutch phrasing |
| Slovene | 88.9 | Overly literal phrasing causes slight stiffness |
| Bulgarian | 88.7 | minor phrasing stiffness and grammatical errors |
| Slovak | 88.7 | Slight awkwardness in phrasing |
| Serbian | 88.6 | Overuse of filler words like "Uh" and "Aha" |
| Albanian | 88.3 | Occasional stiff phrasing |
| Danish | 88.0 | Adjective inflection and phrasing issues |
| Japanese | 87.9 | Slight stiffness in conversational connectors |
| Lithuanian | 87.9 | Literal calques disrupting natural rhythm |
| Persian | 87.5 | Minor stylistic and punctuation issues |
| Afrikaans | 87.2 | Reads stiffly and formally due to literal syntax |
| Indonesian | 87.2 | Inconsistent use of pronouns |
| Italian | 87.1 | Literal translations cause stiff phrasing |
| Thai | 87.1 | Slightly rigid phrasing disrupts natural flow |
| Malay | 86.4 | Pervasive typographical errors and non-standard spellings |
| Vietnamese | 86.3 | Retains structural artifacts from English source |
| Turkish | 86.1 | Slightly rigid syntax lacks fluency |
| Hindi | 85.5 | Structural rigidity |
| Finnish | 85.4 | Slightly stiff dialogue and literal idiom translations |
| Esperanto | 85.3 | Literal phrasing reduces naturalness |
| Czech | 84.2 | Awkward conversational phrasing |
| Korean | 84.2 | Minor stylistic nuances |
| Azerbaijani | 84.1 | Rigid syntax and unnatural phrasing |
| Hebrew | 83.9 | Phrasing feels slightly literal or translation-heavy |
| Basque | 83.8 | Stylistic and grammatical inconsistencies |
| Georgian | 83.5 | Slightly stiff conversational tone |
| Icelandic | 83.4 | Significant fluency issues and awkward phrasing |
| Latvian | 83.4 | Slight stiffness in phrasing |
| Armenian | 83.0 | Lacks conversational tone |
| Mongolian | 82.0 | Poor fluency and naturalness due to literal phrasing |
| Ukrainian | 81.9 | Slight awkwardness in idiomatic transitions |
| Estonian | 81.8 | Minor lexical and syntactic flaws reduce naturalness |
| Marathi | 81.5 | Awkward interjections and fillers |
| Bengali | 81.3 | Literal terminology and stilted phrasing |
| Swahili | 80.2 | Relies heavily on literal calques from English syntax |
| Nepali | 80.1 | Reads like a literal translation |
| Chinese | 79.5 | Slightly fragmented sentence structure |
| Tagalog | 78.8 | Unnatural literalisms and awkward phrasing |
| Belarusian | 78.7 | Slightly stiff phrasing from source structure |
| Interlingua | 78.4 | Severe linguistic issues with fluency and naturalness |
| Hungarian | 76.2 | Deletion of speaker tags |
| Tamil | 75.5 | Stiff, literal phrasing |
| Kannada | 75.0 | Awkward phrasing and stiff tone |
| Urdu | 74.9 | Unnatural verbal cues and inconsistent technical terms |
| Burmese | 74.8 | Unnatural literal translation |
| Irish | 74.7 | Frequent lexical inaccuracies and non-standard terminology |
| Lao | 74.1 | Unnatural syntax and excessive spacing |
| Welsh | 74.0 | Pervasive orthographic and grammatical errors |
| Telugu | 74.0 | awkward structural choices |
| Khmer | 73.5 | Inappropriate slang and awkward phrasing |
| Malayalam | 73.0 | Poor fluency and awkward phrasing |
| Sinhala | 70.8 | Inaccurate vocabulary and awkward phrasing |
| Greek | 65.1 | Conflates amplitude and width |
