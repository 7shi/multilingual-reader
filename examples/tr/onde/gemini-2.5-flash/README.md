# examples/tr/onde/gemini-2.5-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-2.5-flash
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Romanian | 90.9 | Occasional stiff or literal phrasing |
| French | 85.1 | Mixed formal and informal address |
| Spanish | 81.5 | Dialogue attribution error between speakers |
| Catalan | 81.3 | Slightly rigid tone |
| Slovak | 79.5 | Fluency and contextual adaptation issues |
| Norwegian | 79.0 | Unnatural phrasing and rigid syntax |
| Chinese | 78.8 | Unnatural translationese and rigid phrasing |
| Czech | 78.7 | Broken sentence structures and gender agreement errors |
| Icelandic | 78.7 | Grammar and syntax errors disrupt natural flow |
| Croatian | 78.4 | Significant fluency and notation errors |
| Vietnamese | 78.3 | Grammatical errors and mechanical artifacts reduce fluency |
| Persian | 77.5 | Fluency and stylistic issues |
| Arabic | 77.0 | awkward phrasing and stiff syntax |
| German | 76.9 | Gender pronoun mismatch for Camille |
| Latvian | 76.7 | Awkward phrasing and stiff expressions |
| Dutch | 76.3 | Broken speaker tags and awkward phrasing |
| Slovene | 75.7 | Speaker attribution errors and redundant lines |
| Tagalog | 74.4 | Severe inconsistencies and poor linguistic accuracy |
| Welsh | 74.2 | Significant mechanical errors and inconsistent terminology |
| Indonesian | 73.9 | Inconsistent speaker attribution |
| Swedish | 73.7 | Missing speaker attribution and typo |
| Khmer | 73.6 | Unnatural phrasing and awkward syntax |
| Turkish | 73.3 | Significant dialogue attribution errors |
| Armenian | 73.2 | Stiff sentence construction |
| Japanese | 73.0 | inconsistent speaker tags |
| Finnish | 72.8 | Severe dialogue attribution errors |
| Macedonian | 72.8 | Inconsistent speaker label formatting and awkward phrasing |
| Malay | 72.6 | Includes stray English text |
| Serbian | 72.2 | Missing speaker labels cause confusion |
| Ukrainian | 71.7 | Missing speaker labels and dropped lines |
| Danish | 71.5 | Severe loss of dialogue formatting |
| Galician | 71.4 | Missing dialogue lines |
| Mongolian | 71.4 | Poor dialogue formatting and critical scientific errors |
| Albanian | 71.2 | Significant grammatical errors and structural omissions |
| Hebrew | 70.6 | Speaker attribution errors |
| Burmese | 70.5 | Inconsistent male pronouns for Luc |
| Estonian | 70.2 | Missing speaker labels |
| Polish | 70.0 | Russian text contamination and omissions |
| Lithuanian | 69.9 | Collapsed dialogue structure and severe grammatical errors |
| Afrikaans | 69.8 | Stiff dialogue and formatting errors |
| Portuguese | 69.4 | Inconsistent mix of Brazilian and European Portuguese |
| Georgian | 69.2 | Structural fragmentation and misplaced dialogue tags |
| Malayalam | 69.0 | Inconsistent speaker attribution |
| Telugu | 69.0 | Awkward phrasing and literal syntax |
| Marathi | 68.9 | Severe inconsistent address forms and grammar |
| Tamil | 68.9 | Inconsistent speaker names |
| Russian | 68.6 | Severe speaker misattribution |
| Urdu | 68.5 | Lack of fluency and naturalness |
| Azerbaijani | 68.3 | Severe name typo and lack of polish |
| Kannada | 67.8 | Inconsistent speaker labels |
| Sinhala | 67.2 | Unnatural phrasing and literal syntax |
| Swahili | 66.7 | Inconsistent diacritical marks and translation errors |
| Esperanto | 66.5 | Severe vocabulary errors |
| Basque | 66.5 | Stiff and overly literal syntax |
| Thai | 66.4 | Speaker label misalignment |
| Hindi | 66.3 | Severe lack of fluency and naturalness |
| Belarusian | 66.2 | Critical mechanical errors and omitted speaker labels |
| Bulgarian | 65.5 | Poor speaker attribution breaks flow |
| Bengali | 65.2 | Speaker attribution errors disrupt fluency |
| Greek | 65.2 | Critical confusion of width and amplitude |
| Lao | 65.2 | Severe structural breakdown and mixed speaker attribution |
| Korean | 65.0 | Severe speaker attribution errors collapsing dialogue |
| Italian | 63.8 | Grammatical errors and formatting issues |
| Hungarian | 63.0 | Mixed language errors and broken formatting |
| Interlingua | 62.2 | Heavily relies on English syntax and vocabulary |
| Nepali | 62.0 | Major translation errors and awkward phrasing |
| Irish | 61.7 | Missing speaker labels and numerous errors |
