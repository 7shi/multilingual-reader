# examples/tr/onde/gpt-6.1-sol/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: gpt-6.1-sol
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 94.0 | Nearly flawless with minor stylistic debates |
| Spanish | 93.1 | Slight lack of colloquialism |
| Swedish | 93.0 | Slightly literal phrasing and terminology |
| Galician | 92.5 | Subtle use of "largura" for width |
| Czech | 92.2 | Minor grammatical inconsistency with gender agreement |
| Dutch | 92.2 | Slightly stiff phrasing |
| Russian | 92.2 | Minor swap of final speaker roles |
| Portuguese | 92.0 | Slightly rigid conversational tone |
| Slovak | 91.2 | Slight formality in dialogue markers |
| Ukrainian | 91.2 | Slight stiffness in conversational flow |
| Japanese | 91.0 | Minor filler word repetition and phrasing stiffness |
| Bulgarian | 90.8 | Occasionally stiff and overuses ellipses |
| German | 90.5 | Slight translationese and stiff phrasing |
| Polish | 90.5 | Occasional awkward particle placement and phrasing |
| Arabic | 90.3 | Slightly literal phrasing and unidiomatic connectors |
| Turkish | 90.3 | Retains subtle stiffness from source language |
| Lithuanian | 90.2 | Slightly stiff phrasing and overly literal syntax |
| Finnish | 89.7 | Slightly rigid sentence flow |
| Persian | 89.5 | Minor stylistic fluency issues |
| Latvian | 89.5 | Occasional slight literalness in idioms |
| Macedonian | 89.5 | Minor phrasing stiffness due to literal translation |
| Serbian | 89.5 | Minor non-idiomatic terminology |
| Croatian | 89.4 | Minor formal phrasing instead of colloquial speech |
| Vietnamese | 89.2 | Slightly stiff sentence rhythm |
| Chinese | 89.2 | Some rigid sentence structures and abrupt transitions |
| Catalan | 88.8 | Minor fluency issues in rhythm |
| Thai | 88.8 | Inconsistent pronoun usage for speakers |
| Norwegian | 88.7 | Occasional stiff phrasing and unidiomatic interjections |
| Armenian | 88.5 | Minor stylistic stiffness in isolated sentences |
| Korean | 88.5 | Minor stiffness in phrasing and phonetic choices |
| Italian | 88.2 | Minor stylistic inconsistencies and stiff phrasing |
| Afrikaans | 88.1 | Literal sentence structures hinder naturalness |
| Icelandic | 87.8 | Occasional stiffness and slight unidiomatic phrasing |
| Hindi | 87.7 | Slightly stiff phrasing and formal tone |
| Albanian | 87.5 | Occasional literal phrasing |
| Malay | 87.4 | Minor stylistic stiffiness and literal phrasing |
| Romanian | 87.4 | Minor stylistic hesitations in dialogue |
| Hungarian | 86.9 | Minor stylistic rigidity and awkward phrasing |
| Slovene | 86.9 | Minor phrasing issues slightly reduce idiomatic flow |
| Estonian | 86.8 | Occasional minor awkwardness in complex sentence clauses |
| Indonesian | 86.6 | Minor pronoun inconsistency |
| Azerbaijani | 86.3 | Slightly literal and unidiomatic phrasing |
| Esperanto | 86.1 | Literalism and incorrect terminology |
| Belarusian | 85.9 | Slightly stiff phrasing and transitions |
| Georgian | 85.9 | Translationese quality in dialogue |
| Urdu | 85.8 | Minor translationese in complex clauses |
| Hebrew | 85.6 | Terminology consistency issues |
| Marathi | 85.5 | Lacks natural fluency |
| Welsh | 85.3 | Minor grammatical inconsistencies |
| Tamil | 85.2 | Formal tone and stiff rhythm |
| Danish | 85.0 | Slightly stiff phrasing |
| Basque | 84.7 | Minor syntactic calques from English |
| Khmer | 84.6 | Slightly rigid naturalness and fluency |
| Malayalam | 84.5 | Lack of idiomatic fluency |
| Greek | 84.2 | Inaccurate physics terminology |
| Mongolian | 83.9 | awkward filler words and stiff tone |
| Nepali | 83.9 | Literal translation causing awkward flow |
| Swahili | 83.9 | Lacks natural phrasing |
| Bengali | 82.3 | Inconsistent terminology and clunky phrasing |
| Burmese | 82.0 | Formal tone and unnatural phrasing |
| Sinhala | 82.0 | Translationese style reduces fluency and naturalness |
| Lao | 81.6 | Awkward phrasing and literal translations |
| Tagalog | 80.6 | Unnatural scientific terminology |
| Interlingua | 80.0 | Mechanical phrasing lacks natural flow |
| Irish | 78.9 | Significant mistranslation of key scientific terms |
| Kannada | 78.6 | Literal calques and stiff register disrupt fluency |
| Telugu | 71.1 | Unnatural literalness and awkward phrasing |
