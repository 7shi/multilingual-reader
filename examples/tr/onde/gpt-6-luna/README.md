# examples/tr/onde/gpt-6-luna/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: gpt-6-luna
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.7 | Slight stylistic variations in connective phrases |
| Catalan | 93.6 | No significant shortcomings identified |
| French | 93.6 | Negligible slight formalities in spoken tone |
| Galician | 92.9 | Minor stylistic hesitations in fluency |
| Swedish | 92.8 | Minor syntactic flow issues |
| Dutch | 92.0 | Slightly literal phrasing |
| Russian | 91.8 | Minor sentence structure adjustments |
| Czech | 91.6 | No significant shortcoming identified |
| German | 91.5 | Retains a scripted rhythm and uses non-standard terminology |
| Romanian | 91.4 | Slight echo of English syntax in filler words |
| Bulgarian | 90.5 | minor phrasing stiffness and literalness |
| Indonesian | 90.5 | Minor non-idiomatic phrasing |
| Arabic | 90.2 | Minor English-influenced syntax affecting naturalness |
| Portuguese | 90.2 | Phrasing slightly literal |
| Macedonian | 90.1 | Sentence structures feel slightly rigid |
| Japanese | 90.0 | Minor stiffness in connective phrases |
| Vietnamese | 90.0 | Slight syntactic stiffness |
| Finnish | 89.8 | slightly rigid syntax |
| Norwegian | 89.8 | minor friction in sentence structures |
| Serbian | 89.8 | Slightly polished phrasing needed |
| Afrikaans | 89.7 | Lacks idiomatic naturalness |
| Persian | 88.7 | Stiff dialogue |
| Polish | 88.7 | slight residual awkwardness in transitional phrases |
| Turkish | 88.7 | Slightly rigid conversational tone |
| Albanian | 88.5 | Negligible fluency issues with complex metaphors |
| Hindi | 88.4 | Grammatical consistency issues with verb tense and aspect |
| Azerbaijani | 88.2 | Slightly mechanical phrasing |
| Icelandic | 88.0 | Slightly literal phrasing and awkward rhythm |
| Georgian | 87.9 | Minor fluency and naturalness issues |
| Korean | 87.8 | Occasional stiffness and overly literal sentence structures |
| Slovene | 87.8 | Fluency affected by literal phrasing and repetition |
| Estonian | 87.7 | Minor non-idiomatic phrasing issues |
| Slovak | 87.7 | Minor literal idioms |
| Danish | 87.6 | Stiff phrasing reduces naturalness |
| Croatian | 87.3 | Occasional slight stiffness in transitions |
| Malay | 87.3 | Noticeable spelling errors and informal slang |
| Esperanto | 87.2 | Minor stylistic nuance with word choice |
| Armenian | 87.0 | Inconsistent name transliteration for "Luc" |
| Italian | 87.0 | Inconsistent use of interjections |
| Tamil | 86.4 | Slight syntactic rigidity |
| Chinese | 86.3 | Slightly literal tone and unnatural phrasing |
| Belarusian | 86.0 | Stiff phrasing and lack of natural flow |
| Malayalam | 85.1 | Occasional awkward phrasing |
| Marathi | 85.1 | Slightly formal academic tone |
| Nepali | 84.7 | Occasionally stiff phrasing from literal translations |
| Khmer | 84.2 | Stiff and overly literal tone |
| Swahili | 84.2 | unnatural interjections and stiff phrasing |
| Hebrew | 84.0 | Minor literalness and missing rhetorical nuances |
| Urdu | 82.7 | Inconsistent technical terminology |
| Tagalog | 82.3 | Awkward phrasing and literal translations |
| Kannada | 82.0 | Significant lack of native fluency and naturalness |
| Sinhala | 82.0 | Rigid and unnatural fluency |
| Lithuanian | 81.2 | Structural consistency issues in dialogue formatting |
| Thai | 79.5 | Translationese quality |
| Ukrainian | 79.5 | Lack of consistent speaker attribution |
| Burmese | 79.2 | Minor lexical and fluency issues |
| Interlingua | 78.8 | Slightly formal style |
| Hungarian | 78.4 | Significant mechanical errors including missing speaker label and typos |
| Latvian | 77.3 | Inconsistent diacritical marks and clunky phrasing |
| Greek | 76.8 | Slightly rigid phrasing with Anglicized rhythm |
| Basque | 76.3 | Grammatical fragments and logical negation errors |
| Bengali | 75.3 | Inconsistent language usage and awkward phrasing |
| Welsh | 75.2 | Minor typos and slightly literal phrasing |
| Mongolian | 74.8 | Abrupt cutoff with English artifact "providername" |
| Irish | 74.2 | Grammatical inconsistencies and awkward phrasing |
| Lao | 72.8 | Significant lexical errors |
| Telugu | 71.1 | Overly literal and stiff phrasing |
