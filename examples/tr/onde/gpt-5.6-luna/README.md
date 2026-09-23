# examples/tr/onde/gpt-5.6-luna/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gpt-5.6-luna
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.0 | Slightly less spontaneous conversational shifts |
| Romanian | 93.0 | Minor fluency issues and literal phrasing |
| Polish | 92.5 | Literal phrasing from English syntax and non-idiomatic fillers |
| Russian | 92.5 | Slightly heavy sentence structure |
| Italian | 92.3 | Minor fluency and naturalness issues |
| Danish | 92.2 | Leans slightly towards formal register |
| Albanian | 92.1 | Retains slight literalness from English structure |
| Czech | 92.0 | minor nuances in fluency |
| Ukrainian | 92.0 | Slight phrasing lacks colloquial ease |
| Arabic | 91.8 | Slightly stiff phrasing and lack of polish |
| Finnish | 91.6 | Minor literalisms hindering native fluency |
| Croatian | 91.6 | Slightly formal phrasing |
| Galician | 91.5 | Occasional anglicized sentence structures |
| Slovak | 91.5 | Minor stylistic quirks in fillers and phrasing |
| Swedish | 91.4 | Slight rhythmic flow issues in speech phrases |
| Macedonian | 91.1 | occasional slight stiffness in sentence structures |
| Dutch | 90.9 | Occasionally stiff dialogue flow |
| Serbian | 90.9 | Slightly stiff stylistic choices due to scientific content |
| Georgian | 90.6 | Minor phrasing lacking idiomatic smoothness |
| Bulgarian | 90.5 | Minor phrasing stiffness and non-idiomatic transitions |
| Latvian | 90.4 | Minor stiffness and literal loan translations |
| Esperanto | 90.3 | Occasional stiffness and calques from English syntax |
| Hungarian | 89.9 | Literal discourse markers slightly reduce naturalness |
| German | 89.8 | Slightly calqued sentence structures |
| Estonian | 89.8 | Phrasing feels slightly literal |
| Catalan | 89.5 | Slightly rigid syntax |
| Persian | 89.5 | Minor lack of naturalness due to literal phrasing |
| Malay | 89.4 | Non-native phrasing and literal translations |
| Chinese | 89.3 | Slightly stiff colloquial tone and repetitive phrasing |
| Hindi | 89.2 | Slight translationese stiffness |
| Belarusian | 88.6 | Awkward literalism and non-standard terms |
| Vietnamese | 88.5 | Slightly literal conversational phrasing |
| Turkish | 88.4 | Slight structural rigidity from literal translation |
| Armenian | 88.1 | Minor awkward phrasing and technical precision issues |
| Korean | 87.7 | Occasional stiffness due to sentence-by-sentence translation |
| Indonesian | 87.6 | Slightly stiff phrasing |
| Hebrew | 87.3 | Minor terminology inconsistencies |
| Lithuanian | 87.3 | Slightly stiff dialogue and unnatural phrasing |
| Azerbaijani | 86.8 | Stiff dialogue tone and minor semantic errors |
| Basque | 86.1 | Unnatural loanwords and broken calques |
| Afrikaans | 85.7 | Minor phrasing choices lack idiomatic naturalness |
| Tamil | 85.4 | Occasional stiff sentence structures |
| Welsh | 85.1 | Slightly mechanical phrasing and unnatural conversational flow |
| French | 84.5 | Inconsistent use of tu and vous |
| Swahili | 84.4 | Rigid and unnatural phrasing |
| Marathi | 83.0 | Slightly rigid or literal phrasing |
| Slovene | 83.0 | Awkward syntax from literal translation |
| Portuguese | 82.7 | Persistent gender agreement errors |
| Tagalog | 82.7 | unnatural formal phrasing and lexical errors |
| Nepali | 82.5 | Slight stiffness in syntax and transitions |
| Mongolian | 82.2 | Rigid tone and literal phrasing |
| Khmer | 81.9 | Slightly stiff conversational style |
| Norwegian | 81.8 | Noticeable stiffness and lack of natural flow |
| Malayalam | 81.6 | Inconsistent name localization |
| Bengali | 81.4 | Lack of natural fluency and idiomatic ease |
| Burmese | 81.3 | Awkward conversational flow and stiffness |
| Irish | 81.0 | Lack of idiomatic polish |
| Lao | 80.2 | Unnatural phrasing and rigid syntax |
| Kannada | 80.1 | Awkward literal translation phrasing |
| Urdu | 76.5 | Excessive phonetic transliteration of English terms |
| Sinhala | 76.2 | Significant fluency and naturalness issues |
| Japanese | 76.0 | Untranslated English word |
| Interlingua | 73.9 | Hyper-literal phrasing and lack of fluency |
| Thai | 73.6 | Formatting artifacts and inconsistent tone |
| Telugu | 73.3 | Mixed English phrases in Telugu text |
| Icelandic | 72.8 | Grammatical errors and unnatural phrasing |
| Greek | 71.2 | Lacks natural spoken flow |
