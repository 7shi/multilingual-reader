# examples/tr/onde/gemma4/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemma4:26b
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.3 | Minor nuance: "ingenuidad" for "ingenio" |
| Polish | 91.5 | Slightly stiff phrasing reduces fluency |
| French | 91.1 | Minor inconsistencies in pronoun usage and tone |
| Finnish | 90.6 | Occasional literal phrasing |
| Dutch | 89.6 | Awkward calques and stiff phrasing |
| Serbian | 89.5 | Anchored phrasing and terminology inconsistencies |
| Vietnamese | 89.5 | Slight translated feel in fluency |
| German | 89.2 | Lacks spontaneous charm |
| Ukrainian | 89.1 | Stiff fillers and discourse markers |
| Persian | 88.1 | Occasional stiff literal translations and non-idiomatic fillers |
| Russian | 87.8 | Pronoun inconsistency |
| Chinese | 87.3 | Fluency and addressing errors |
| Swedish | 87.2 | Overly literal phrasing and lack of idiomatization |
| Thai | 87.1 | Noticeable stiffness in dialogue fluency |
| Bulgarian | 86.7 | Slightly formal and stiff dialogue flow |
| Japanese | 86.5 | Slight stiffness in phrasing and filler sounds |
| Danish | 86.2 | Notable translationese |
| Arabic | 86.0 | Translationese and stiff filler words |
| Croatian | 85.6 | Lacks fluency and naturalness |
| Afrikaans | 85.2 | Significant fluency issues |
| Portuguese | 84.8 | Critical mistranslation of "Constantly" to "Constantes" |
| Norwegian | 84.7 | Awkward mathematical phrasing |
| Korean | 84.5 | Slightly stiff dialogue phrasing |
| Swahili | 84.0 | Overly literal and unnatural phrasing |
| Galician | 82.7 | Grammatical errors and unnatural phrasing |
| Hindi | 82.5 | Excessive code-switching and rigid syntax |
| Azerbaijani | 82.3 | Severe translationese and grammar errors |
| Indonesian | 81.8 | Literal and unnatural phrasing |
| Romanian | 81.7 | Calques and awkward phrasing disrupt fluency |
| Malay | 80.8 | Unnatural fluency and literal calques |
| Slovak | 80.2 | Lexical errors and calques |
| Italian | 79.6 | Unnatural conversational tone and grammatical errors |
| Burmese | 79.2 | Mechanical errors in encoding and punctuation |
| Tagalog | 78.5 | Stiff translationese and awkward phrasing |
| Albanian | 77.8 | Grammatical and idiomatic errors |
| Turkish | 77.8 | Structural dialogue errors and unnatural phrasing |
| Malayalam | 77.6 | Linguistic inconsistency and mechanical errors |
| Lao | 76.9 | Severe linguistic interference and poor fluency |
| Bengali | 76.2 | Systematic orthographic errors degrade readability |
| Czech | 76.2 | Awkward literal phrasing and typos |
| Nepali | 76.2 | Inconsistent loanword usage and awkward phrasing |
| Armenian | 75.8 | Awkward phrasing and unnatural flow |
| Telugu | 75.0 | Stiff and unnatural syntax |
| Slovene | 74.5 | Major grammatical defects and unnatural phrasing |
| Sinhala | 73.8 | Rigid, unnatural sentence construction |
| Marathi | 73.5 | Missing speaker labels |
| Macedonian | 73.4 | Mixed script and gibberish |
| Hebrew | 73.0 | Inconsistent tone and register |
| Catalan | 72.9 | Significant grammatical and spelling errors |
| Esperanto | 72.4 | Significant language mixing and grammatical errors disrupt fluency |
| Urdu | 72.2 | Inconsistent scientific terminology |
| Khmer | 71.5 | Severe mixed-language artifact |
| Mongolian | 71.3 | Lacks fluency and naturalness |
| Kannada | 70.2 | Significant fluency issues |
| Tamil | 69.3 | Untranslated English word "magnificent" |
| Georgian | 69.2 | Chinese characters mistakenly inserted |
| Belarusian | 63.8 | Pervasive grammatical errors and incorrect terminology |
| Hungarian | 60.9 | Mixed-language intrusions |
| Greek | 60.6 | Severe typos and garbled text |
| Icelandic | 60.2 | Severe semantic and grammatical errors |
| Interlingua | 54.5 | Severe contamination and untranslated text |
| Estonian | 49.0 | Mixed languages with Chinese characters |
| Lithuanian | 43.0 | Critical structural and content corruption |
| Latvian | 40.9 | Severe lexical errors and script mixing |
| Basque | 37.8 | Catastrophic errors and mixed languages |
| Welsh | 32.2 | Invented vocabulary and nonsense words |
| Irish | 23.6 | Severe text corruption and gibberish |
