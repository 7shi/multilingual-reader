# examples/tr/onde/gemini-2.5-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gemini-2.5-flash
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Romanian | 89.7 | Occasional stiff or literal phrasing |
| French | 87.5 | Mixed formal and informal address |
| Spanish | 83.8 | Dialogue attribution error between speakers |
| Vietnamese | 80.0 | Grammatical errors and mechanical artifacts reduce fluency |
| Slovak | 78.8 | Fluency and contextual adaptation issues |
| Catalan | 78.5 | Slightly rigid tone |
| German | 78.5 | Gender pronoun mismatch for Camille |
| Norwegian | 78.5 | Unnatural phrasing and rigid syntax |
| Portuguese | 77.2 | Inconsistent mix of Brazilian and European Portuguese |
| Croatian | 77.1 | Significant fluency and notation errors |
| Persian | 76.7 | Fluency and stylistic issues |
| Icelandic | 76.7 | Grammar and syntax errors disrupt natural flow |
| Latvian | 76.7 | Awkward phrasing and stiff expressions |
| Czech | 76.5 | Broken sentence structures and gender agreement errors |
| Turkish | 76.3 | Significant dialogue attribution errors |
| Slovene | 76.2 | Speaker attribution errors and redundant lines |
| Chinese | 76.2 | Unnatural translationese and rigid phrasing |
| Japanese | 75.8 | inconsistent speaker tags |
| Swedish | 75.8 | Missing speaker attribution and typo |
| Dutch | 75.1 | Broken speaker tags and awkward phrasing |
| Arabic | 73.3 | awkward phrasing and stiff syntax |
| Malay | 73.0 | Includes stray English text |
| Macedonian | 72.9 | Inconsistent speaker label formatting and awkward phrasing |
| Welsh | 72.8 | Significant mechanical errors and inconsistent terminology |
| Afrikaans | 72.7 | Stiff dialogue and formatting errors |
| Polish | 72.5 | Russian text contamination and omissions |
| Albanian | 72.2 | Significant grammatical errors and structural omissions |
| Tagalog | 72.1 | Severe inconsistencies and poor linguistic accuracy |
| Indonesian | 72.0 | Inconsistent speaker attribution |
| Khmer | 71.8 | Unnatural phrasing and awkward syntax |
| Lithuanian | 71.7 | Collapsed dialogue structure and severe grammatical errors |
| Galician | 71.3 | Missing dialogue lines |
| Serbian | 71.1 | Missing speaker labels cause confusion |
| Danish | 70.6 | Severe loss of dialogue formatting |
| Marathi | 70.5 | Severe inconsistent address forms and grammar |
| Ukrainian | 70.2 | Missing speaker labels and dropped lines |
| Hebrew | 70.1 | Speaker attribution errors |
| Urdu | 69.8 | Lack of fluency and naturalness |
| Azerbaijani | 69.7 | Severe name typo and lack of polish |
| Finnish | 68.8 | Severe dialogue attribution errors |
| Basque | 68.6 | Stiff and overly literal syntax |
| Malayalam | 68.6 | Inconsistent speaker attribution |
| Mongolian | 68.5 | Poor dialogue formatting and critical scientific errors |
| Burmese | 68.2 | Inconsistent male pronouns for Luc |
| Armenian | 68.0 | Stiff sentence construction |
| Russian | 67.5 | Severe speaker misattribution |
| Telugu | 67.1 | Awkward phrasing and literal syntax |
| Estonian | 66.7 | Missing speaker labels |
| Thai | 66.5 | Speaker label misalignment |
| Tamil | 66.2 | Inconsistent speaker names |
| Hungarian | 66.0 | Mixed language errors and broken formatting |
| Sinhala | 66.0 | Unnatural phrasing and literal syntax |
| Bulgarian | 65.8 | Poor speaker attribution breaks flow |
| Bengali | 65.6 | Speaker attribution errors disrupt fluency |
| Swahili | 65.3 | Inconsistent diacritical marks and translation errors |
| Hindi | 65.1 | Severe lack of fluency and naturalness |
| Esperanto | 65.0 | Severe vocabulary errors |
| Georgian | 64.6 | Structural fragmentation and misplaced dialogue tags |
| Kannada | 64.1 | Inconsistent speaker labels |
| Greek | 64.0 | Critical confusion of width and amplitude |
| Belarusian | 63.4 | Critical mechanical errors and omitted speaker labels |
| Interlingua | 63.2 | Heavily relies on English syntax and vocabulary |
| Korean | 62.8 | Severe speaker attribution errors collapsing dialogue |
| Italian | 62.6 | Grammatical errors and formatting issues |
| Lao | 62.6 | Severe structural breakdown and mixed speaker attribution |
| Nepali | 61.6 | Major translation errors and awkward phrasing |
| Irish | 61.4 | Missing speaker labels and numerous errors |
