# examples/tr/onde/gpt-6.1-sol/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6.1-sol
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.3 | Slight lack of colloquialism |
| French | 94.3 | Nearly flawless with minor stylistic debates |
| Swedish | 93.2 | Slightly literal phrasing and terminology |
| Czech | 93.0 | Minor grammatical inconsistency with gender agreement |
| Croatian | 93.0 | Minor formal phrasing instead of colloquial speech |
| Slovak | 93.0 | Slight formality in dialogue markers |
| Russian | 92.7 | Minor swap of final speaker roles |
| Serbian | 92.5 | Minor non-idiomatic terminology |
| Galician | 91.9 | Subtle use of "largura" for width |
| Japanese | 91.9 | Minor filler word repetition and phrasing stiffness |
| Catalan | 91.8 | Minor fluency issues in rhythm |
| Ukrainian | 91.7 | Slight stiffness in conversational flow |
| Bulgarian | 91.5 | Occasionally stiff and overuses ellipses |
| Latvian | 91.3 | Occasional slight literalness in idioms |
| Polish | 91.3 | Occasional awkward particle placement and phrasing |
| Albanian | 91.2 | Occasional literal phrasing |
| Romanian | 91.1 | Minor stylistic hesitations in dialogue |
| German | 90.9 | Slight translationese and stiff phrasing |
| Thai | 90.8 | Inconsistent pronoun usage for speakers |
| Belarusian | 90.5 | Slightly stiff phrasing and transitions |
| Finnish | 90.3 | Slightly rigid sentence flow |
| Persian | 90.2 | Minor stylistic fluency issues |
| Chinese | 90.2 | Some rigid sentence structures and abrupt transitions |
| Turkish | 89.7 | Retains subtle stiffness from source language |
| Estonian | 89.5 | Occasional minor awkwardness in complex sentence clauses |
| Macedonian | 89.5 | Minor phrasing stiffness due to literal translation |
| Vietnamese | 89.5 | Slightly stiff sentence rhythm |
| Norwegian | 89.4 | Occasional stiff phrasing and unidiomatic interjections |
| Dutch | 89.2 | Slightly stiff phrasing |
| Arabic | 89.1 | Slightly literal phrasing and unidiomatic connectors |
| Danish | 89.1 | Slightly stiff phrasing |
| Armenian | 88.9 | Minor stylistic stiffness in isolated sentences |
| Hindi | 88.8 | Slightly stiff phrasing and formal tone |
| Slovene | 88.6 | Minor phrasing issues slightly reduce idiomatic flow |
| Georgian | 88.4 | Translationese quality in dialogue |
| Korean | 88.4 | Minor stiffness in phrasing and phonetic choices |
| Icelandic | 88.0 | Occasional stiffness and slight unidiomatic phrasing |
| Hungarian | 87.7 | Minor stylistic rigidity and awkward phrasing |
| Hebrew | 87.2 | Terminology consistency issues |
| Azerbaijani | 87.0 | Slightly literal and unidiomatic phrasing |
| Esperanto | 87.0 | Literalism and incorrect terminology |
| Basque | 87.0 | Minor syntactic calques from English |
| Indonesian | 87.0 | Minor pronoun inconsistency |
| Welsh | 86.8 | Minor grammatical inconsistencies |
| Tamil | 86.4 | Formal tone and stiff rhythm |
| Malay | 86.1 | Minor stylistic stiffiness and literal phrasing |
| Lithuanian | 85.8 | Slightly stiff phrasing and overly literal syntax |
| Portuguese | 85.3 | Slightly rigid conversational tone |
| Mongolian | 85.0 | awkward filler words and stiff tone |
| Marathi | 84.7 | Lacks natural fluency |
| Urdu | 84.5 | Minor translationese in complex clauses |
| Afrikaans | 84.2 | Literal sentence structures hinder naturalness |
| Swahili | 84.1 | Lacks natural phrasing |
| Khmer | 83.8 | Slightly rigid naturalness and fluency |
| Malayalam | 83.8 | Lack of idiomatic fluency |
| Burmese | 83.8 | Formal tone and unnatural phrasing |
| Greek | 83.7 | Inaccurate physics terminology |
| Lao | 83.0 | Awkward phrasing and literal translations |
| Italian | 82.9 | Minor stylistic inconsistencies and stiff phrasing |
| Sinhala | 82.2 | Translationese style reduces fluency and naturalness |
| Nepali | 81.3 | Literal translation causing awkward flow |
| Bengali | 80.6 | Inconsistent terminology and clunky phrasing |
| Tagalog | 80.5 | Unnatural scientific terminology |
| Kannada | 77.9 | Literal calques and stiff register disrupt fluency |
| Irish | 77.5 | Significant mistranslation of key scientific terms |
| Interlingua | 76.2 | Mechanical phrasing lacks natural flow |
| Telugu | 74.0 | Unnatural literalness and awkward phrasing |
