# examples/tr/onde/gpt-5.6-luna/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gpt-5.6-luna
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 92.8 | Minor fluency and naturalness issues |
| Portuguese | 92.2 | Persistent gender agreement errors |
| Danish | 92.0 | Leans slightly towards formal register |
| Dutch | 91.9 | Occasionally stiff dialogue flow |
| Polish | 91.8 | Literal phrasing from English syntax and non-idiomatic fillers |
| German | 91.6 | Slightly calqued sentence structures |
| Romanian | 91.5 | Minor fluency issues and literal phrasing |
| Russian | 91.0 | Slightly heavy sentence structure |
| Arabic | 90.6 | Slightly stiff phrasing and lack of polish |
| Ukrainian | 90.3 | Slight phrasing lacks colloquial ease |
| Spanish | 90.2 | Slightly less spontaneous conversational shifts |
| Bulgarian | 90.0 | Minor phrasing stiffness and non-idiomatic transitions |
| Malay | 89.9 | Non-native phrasing and literal translations |
| Latvian | 89.8 | Minor stiffness and literal loan translations |
| Chinese | 89.8 | Slightly stiff colloquial tone and repetitive phrasing |
| Albanian | 89.7 | Retains slight literalness from English structure |
| Czech | 89.6 | minor nuances in fluency |
| Vietnamese | 89.6 | Slightly literal conversational phrasing |
| Galician | 89.4 | Occasional anglicized sentence structures |
| Lithuanian | 89.4 | Slightly stiff dialogue and unnatural phrasing |
| Macedonian | 89.4 | occasional slight stiffness in sentence structures |
| Turkish | 89.2 | Slight structural rigidity from literal translation |
| Hungarian | 88.9 | Literal discourse markers slightly reduce naturalness |
| Serbian | 88.9 | Slightly stiff stylistic choices due to scientific content |
| Persian | 88.7 | Minor lack of naturalness due to literal phrasing |
| Indonesian | 88.3 | Slightly stiff phrasing |
| Georgian | 88.2 | Minor phrasing lacking idiomatic smoothness |
| Afrikaans | 88.1 | Minor phrasing choices lack idiomatic naturalness |
| Catalan | 88.1 | Slightly rigid syntax |
| French | 88.1 | Inconsistent use of tu and vous |
| Croatian | 88.0 | Slightly formal phrasing |
| Swedish | 88.0 | Slight rhythmic flow issues in speech phrases |
| Esperanto | 87.7 | Occasional stiffness and calques from English syntax |
| Armenian | 87.6 | Minor awkward phrasing and technical precision issues |
| Estonian | 87.2 | Phrasing feels slightly literal |
| Hindi | 87.2 | Slight translationese stiffness |
| Slovak | 86.9 | Minor stylistic quirks in fillers and phrasing |
| Belarusian | 86.7 | Awkward literalism and non-standard terms |
| Korean | 86.6 | Occasional stiffness due to sentence-by-sentence translation |
| Finnish | 86.5 | Minor literalisms hindering native fluency |
| Hebrew | 86.1 | Minor terminology inconsistencies |
| Slovene | 85.5 | Awkward syntax from literal translation |
| Tamil | 85.5 | Occasional stiff sentence structures |
| Basque | 85.3 | Unnatural loanwords and broken calques |
| Norwegian | 85.1 | Noticeable stiffness and lack of natural flow |
| Welsh | 83.9 | Slightly mechanical phrasing and unnatural conversational flow |
| Khmer | 83.9 | Slightly stiff conversational style |
| Nepali | 83.9 | Slight stiffness in syntax and transitions |
| Azerbaijani | 83.1 | Stiff dialogue tone and minor semantic errors |
| Swahili | 82.4 | Rigid and unnatural phrasing |
| Marathi | 82.0 | Slightly rigid or literal phrasing |
| Bengali | 81.8 | Lack of natural fluency and idiomatic ease |
| Mongolian | 81.8 | Rigid tone and literal phrasing |
| Irish | 80.5 | Lack of idiomatic polish |
| Malayalam | 80.5 | Inconsistent name localization |
| Icelandic | 80.2 | Grammatical errors and unnatural phrasing |
| Burmese | 80.0 | Awkward conversational flow and stiffness |
| Urdu | 79.9 | Excessive phonetic transliteration of English terms |
| Tagalog | 79.6 | unnatural formal phrasing and lexical errors |
| Lao | 78.5 | Unnatural phrasing and rigid syntax |
| Kannada | 78.3 | Awkward literal translation phrasing |
| Japanese | 78.2 | Untranslated English word |
| Interlingua | 77.5 | Hyper-literal phrasing and lack of fluency |
| Sinhala | 76.2 | Significant fluency and naturalness issues |
| Greek | 75.8 | Lacks natural spoken flow |
| Thai | 75.1 | Formatting artifacts and inconsistent tone |
| Telugu | 68.3 | Mixed English phrases in Telugu text |
