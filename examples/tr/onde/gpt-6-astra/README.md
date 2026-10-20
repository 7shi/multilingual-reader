# examples/tr/onde/gpt-6-astra/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6-astra
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 93.9 | Exceptional quality with no identified shortcomings |
| Spanish | 93.8 | High quality with minor stylistic deductions |
| Italian | 93.6 | No shortcomings identified |
| Chinese | 93.0 | No identified defects |
| Dutch | 92.6 | Occasional slight stiffness in connecting sentences |
| Czech | 92.4 | Minor word choice inconsistencies |
| Galician | 92.3 | Minor fluency stiffness in technical discourse |
| Japanese | 91.8 | Slightly rigid sentence structures |
| Russian | 91.6 | Minor stylistic choices debated but non-detracting |
| German | 91.3 | Occasionally literal and stiff phrasing |
| Lithuanian | 91.2 | Minor stylistic awkwardnesses and stiff phrasing |
| Polish | 91.2 | Slight stylistic rigidities affect fluency |
| Slovak | 91.2 | Minor stiffness in transitions and idioms |
| Ukrainian | 90.6 | Minor stiffness and translated syntax |
| Catalan | 90.3 | Minor fluency and naturalness issues |
| Vietnamese | 90.2 | Slightly stiff conversational fillers |
| Croatian | 90.0 | Minor fluency issues due to literal calques |
| Macedonian | 89.8 | Slight stiffness and literalness in phrasing |
| Romanian | 89.4 | Slightly stiff phrasing |
| Norwegian | 89.2 | awkward math terminology like "i andre" for squared |
| Arabic | 89.1 | Slightly rigid phrasing |
| Thai | 89.1 | Occasional non-standard technical terms and stylistic shifts |
| Latvian | 89.0 | Minor stiffness from literal phrasing |
| Albanian | 89.0 | Occasional stiffness and literal phrasing |
| Indonesian | 88.9 | Minor awkwardness in transitions and punctuation |
| Bulgarian | 88.8 | Occasional literalness in phrasing |
| Korean | 88.8 | Minor fluency and phrasing issues |
| Serbian | 88.7 | Abov limit transliteration error |
| Danish | 88.6 | Minor stylistic stiffness in literal math notation and word choices |
| Turkish | 88.6 | Retains a slight foreign feel |
| Finnish | 88.5 | Minor phrasing choices less idiomatic than native speaker |
| Portuguese | 87.9 | Slight stiffness from direct translation |
| Afrikaans | 87.7 | Slightly stiff dialogue tags and interjections |
| Persian | 87.4 | Slightly literal stylistic nuances |
| Armenian | 87.4 | Translation-heavy phrasing |
| Hungarian | 87.3 | Occasional awkward phrasing disrupts natural flow |
| Hindi | 87.2 | Minor stylistic stiffness |
| Georgian | 87.0 | Slightly formal phrasing in dialogue and transitions |
| Malay | 87.0 | Scientific terminology errors |
| Azerbaijani | 86.8 | Slight awkwardness and literal phrasing |
| Belarusian | 86.5 | Reliance on non-standard transliterations |
| Estonian | 86.2 | Slightly stiff conversational tone |
| Slovene | 86.2 | Slightly stiff phrasing |
| Malayalam | 86.1 | Slight translationese and rigid syntax |
| Icelandic | 85.9 | Occasional grammatical errors and unnatural phrasing |
| Esperanto | 85.6 | Unidiomatic phrasing and terminology errors |
| Swedish | 85.6 | Slightly stiff phrasing and translationese |
| Hebrew | 85.3 | Minor phrasing issues |
| Tamil | 84.8 | Slightly rigid sentence structures |
| Marathi | 84.5 | Phrasing could be more idiomatic |
| Swahili | 84.4 | Lacks fluency and naturalness |
| Basque | 84.3 | Occasional calques and awkward phrasing |
| Mongolian | 83.5 | Rigid and unnatural conversational flow |
| Nepali | 83.2 | Slightly literal phrasing and tonal inconsistencies |
| Greek | 83.1 | Unnatural dialogue interjections |
| Urdu | 82.7 | Phrasing feels slightly literal or stiff |
| Sinhala | 82.4 | Awkward phrasing and unnatural sentence structures |
| Irish | 82.3 | Minor idiomatic stiffness and archaic phrasing |
| Tagalog | 81.6 | Foreignizing code-switching errors |
| Khmer | 81.5 | Excessive filler words undermine fluency |
| Bengali | 81.3 | Lacks idiomatic polish and natural cadence |
| Welsh | 81.2 | Fluency and naturalness flaws |
| Burmese | 80.4 | Stiff dialogue due to literal phrasing |
| Lao | 80.2 | Awkward phrasing and wrong scientific terms |
| Kannada | 79.6 | Rigid, overly literal style |
| Interlingua | 79.2 | Stiff and overly formal style |
| Telugu | 70.2 | Mechanically adheres to English structures |
