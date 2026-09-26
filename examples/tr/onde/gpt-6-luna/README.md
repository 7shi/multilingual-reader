# examples/tr/onde/gpt-6-luna/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6-luna
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 95.0 | No significant shortcomings identified |
| French | 94.2 | Negligible slight formalities in spoken tone |
| Swedish | 93.8 | Minor syntactic flow issues |
| Czech | 93.4 | No significant shortcoming identified |
| Spanish | 93.3 | Slight stylistic variations in connective phrases |
| Dutch | 92.8 | Slightly literal phrasing |
| Russian | 92.7 | Minor sentence structure adjustments |
| Romanian | 92.3 | Slight echo of English syntax in filler words |
| Serbian | 92.1 | Slightly polished phrasing needed |
| Galician | 91.7 | Minor stylistic hesitations in fluency |
| Polish | 91.6 | slight residual awkwardness in transitional phrases |
| Slovak | 91.3 | Minor literal idioms |
| Albanian | 91.2 | Negligible fluency issues with complex metaphors |
| German | 90.9 | Retains a scripted rhythm and uses non-standard terminology |
| Croatian | 90.9 | Occasional slight stiffness in transitions |
| Arabic | 90.8 | Minor English-influenced syntax affecting naturalness |
| Indonesian | 90.5 | Minor non-idiomatic phrasing |
| Japanese | 90.2 | Minor stiffness in connective phrases |
| Macedonian | 90.2 | Sentence structures feel slightly rigid |
| Danish | 90.0 | Stiff phrasing reduces naturalness |
| Azerbaijani | 89.9 | Slightly mechanical phrasing |
| Estonian | 89.9 | Minor non-idiomatic phrasing issues |
| Finnish | 89.8 | slightly rigid syntax |
| Georgian | 89.8 | Minor fluency and naturalness issues |
| Bulgarian | 89.5 | minor phrasing stiffness and literalness |
| Hindi | 89.5 | Grammatical consistency issues with verb tense and aspect |
| Slovene | 89.3 | Fluency affected by literal phrasing and repetition |
| Norwegian | 89.2 | minor friction in sentence structures |
| Persian | 89.1 | Stiff dialogue |
| Marathi | 88.0 | Slightly formal academic tone |
| Turkish | 87.8 | Slightly rigid conversational tone |
| Armenian | 87.6 | Inconsistent name transliteration for "Luc" |
| Icelandic | 87.6 | Slightly literal phrasing and awkward rhythm |
| Chinese | 87.5 | Slightly literal tone and unnatural phrasing |
| Tamil | 87.4 | Slight syntactic rigidity |
| Esperanto | 87.0 | Minor stylistic nuance with word choice |
| Vietnamese | 87.0 | Slight syntactic stiffness |
| Malayalam | 86.9 | Occasional awkward phrasing |
| Korean | 86.4 | Occasional stiffness and overly literal sentence structures |
| Malay | 86.1 | Noticeable spelling errors and informal slang |
| Afrikaans | 85.9 | Lacks idiomatic naturalness |
| Hebrew | 85.8 | Minor literalness and missing rhetorical nuances |
| Portuguese | 85.8 | Phrasing slightly literal |
| Swahili | 85.2 | unnatural interjections and stiff phrasing |
| Nepali | 84.8 | Occasionally stiff phrasing from literal translations |
| Belarusian | 84.6 | Stiff phrasing and lack of natural flow |
| Tagalog | 84.5 | Awkward phrasing and literal translations |
| Khmer | 83.6 | Stiff and overly literal tone |
| Italian | 83.1 | Inconsistent use of interjections |
| Kannada | 81.8 | Significant lack of native fluency and naturalness |
| Urdu | 81.7 | Inconsistent technical terminology |
| Burmese | 81.0 | Minor lexical and fluency issues |
| Sinhala | 80.3 | Rigid and unnatural fluency |
| Telugu | 80.1 | Overly literal and stiff phrasing |
| Greek | 79.1 | Slightly rigid phrasing with Anglicized rhythm |
| Ukrainian | 77.8 | Lack of consistent speaker attribution |
| Lithuanian | 77.4 | Structural consistency issues in dialogue formatting |
| Basque | 77.0 | Grammatical fragments and logical negation errors |
| Hungarian | 77.0 | Significant mechanical errors including missing speaker label and typos |
| Thai | 77.0 | Translationese quality |
| Welsh | 75.9 | Minor typos and slightly literal phrasing |
| Bengali | 75.4 | Inconsistent language usage and awkward phrasing |
| Lao | 75.1 | Significant lexical errors |
| Interlingua | 74.9 | Slightly formal style |
| Latvian | 74.2 | Inconsistent diacritical marks and clunky phrasing |
| Mongolian | 73.7 | Abrupt cutoff with English artifact "providername" |
| Irish | 69.8 | Grammatical inconsistencies and awkward phrasing |
