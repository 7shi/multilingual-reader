# examples/tr/onde/gemma4/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemma4:26b
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.7 | Minor nuance: "ingenuidad" for "ingenio" |
| French | 93.1 | Minor inconsistencies in pronoun usage and tone |
| Portuguese | 90.5 | Critical mistranslation of "Constantly" to "Constantes" |
| Polish | 90.3 | Slightly stiff phrasing reduces fluency |
| Dutch | 89.8 | Awkward calques and stiff phrasing |
| Vietnamese | 89.7 | Slight translated feel in fluency |
| Russian | 89.1 | Pronoun inconsistency |
| Norwegian | 88.9 | Awkward mathematical phrasing |
| Chinese | 88.8 | Fluency and addressing errors |
| German | 88.0 | Lacks spontaneous charm |
| Persian | 88.0 | Occasional stiff literal translations and non-idiomatic fillers |
| Thai | 88.0 | Noticeable stiffness in dialogue fluency |
| Ukrainian | 88.0 | Stiff fillers and discourse markers |
| Finnish | 87.9 | Occasional literal phrasing |
| Arabic | 87.3 | Translationese and stiff filler words |
| Serbian | 87.3 | Anchored phrasing and terminology inconsistencies |
| Swedish | 87.1 | Overly literal phrasing and lack of idiomatization |
| Italian | 87.0 | Unnatural conversational tone and grammatical errors |
| Japanese | 86.8 | Slight stiffness in phrasing and filler sounds |
| Korean | 86.2 | Slightly stiff dialogue phrasing |
| Croatian | 85.5 | Lacks fluency and naturalness |
| Afrikaans | 85.4 | Significant fluency issues |
| Danish | 85.0 | Notable translationese |
| Hindi | 84.1 | Excessive code-switching and rigid syntax |
| Bulgarian | 83.9 | Slightly formal and stiff dialogue flow |
| Indonesian | 83.8 | Literal and unnatural phrasing |
| Galician | 82.3 | Grammatical errors and unnatural phrasing |
| Malay | 81.1 | Unnatural fluency and literal calques |
| Azerbaijani | 80.6 | Severe translationese and grammar errors |
| Swahili | 78.9 | Overly literal and unnatural phrasing |
| Romanian | 78.6 | Calques and awkward phrasing disrupt fluency |
| Albanian | 78.0 | Grammatical and idiomatic errors |
| Burmese | 77.9 | Mechanical errors in encoding and punctuation |
| Nepali | 77.9 | Inconsistent loanword usage and awkward phrasing |
| Slovak | 77.8 | Lexical errors and calques |
| Macedonian | 77.6 | Mixed script and gibberish |
| Czech | 77.5 | Awkward literal phrasing and typos |
| Armenian | 77.5 | Awkward phrasing and unnatural flow |
| Urdu | 77.4 | Inconsistent scientific terminology |
| Malayalam | 77.3 | Linguistic inconsistency and mechanical errors |
| Turkish | 77.0 | Structural dialogue errors and unnatural phrasing |
| Catalan | 75.7 | Significant grammatical and spelling errors |
| Bengali | 75.1 | Systematic orthographic errors degrade readability |
| Tagalog | 73.3 | Stiff translationese and awkward phrasing |
| Marathi | 73.2 | Missing speaker labels |
| Lao | 73.0 | Severe linguistic interference and poor fluency |
| Georgian | 72.6 | Chinese characters mistakenly inserted |
| Esperanto | 72.4 | Significant language mixing and grammatical errors disrupt fluency |
| Telugu | 72.3 | Stiff and unnatural syntax |
| Hebrew | 72.2 | Inconsistent tone and register |
| Mongolian | 72.1 | Lacks fluency and naturalness |
| Khmer | 72.0 | Severe mixed-language artifact |
| Kannada | 71.9 | Significant fluency issues |
| Slovene | 71.3 | Major grammatical defects and unnatural phrasing |
| Tamil | 70.5 | Untranslated English word "magnificent" |
| Sinhala | 68.8 | Rigid, unnatural sentence construction |
| Belarusian | 67.3 | Pervasive grammatical errors and incorrect terminology |
| Hungarian | 66.4 | Mixed-language intrusions |
| Interlingua | 65.3 | Severe contamination and untranslated text |
| Icelandic | 62.4 | Severe semantic and grammatical errors |
| Greek | 60.0 | Severe typos and garbled text |
| Estonian | 54.8 | Mixed languages with Chinese characters |
| Lithuanian | 50.9 | Critical structural and content corruption |
| Latvian | 43.9 | Severe lexical errors and script mixing |
| Basque | 39.8 | Catastrophic errors and mixed languages |
| Welsh | 34.2 | Invented vocabulary and nonsense words |
| Irish | 28.1 | Severe text corruption and gibberish |
