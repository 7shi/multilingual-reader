# examples/tr/onde/gpt-6-sol/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6-sol
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 93.8 | Minor stiffness in long compound sentences |
| Swedish | 93.5 | Flawless professional-grade quality |
| French | 92.8 | Near-perfect fidelity and naturalness |
| Czech | 92.7 | Minor nuance and repetition issues remain |
| Dutch | 92.4 | Minor stylistic phrasing variations |
| Chinese | 92.0 | Subtle syntactic calques |
| Romanian | 91.9 | Minor stylistic preferences reduce colloquialism slightly |
| Slovak | 91.6 | Slight stylistic stiffness in idioms and punctuation |
| Galician | 91.5 | Slightly literal syntax in some sentences |
| Arabic | 91.4 | Minor awkwardness in casual speech interjections |
| Spanish | 91.2 | Negligible fluency imperfections |
| Indonesian | 91.2 | Minor stylistic stiffness in transitions |
| Russian | 91.0 | Slight stylistic rigidity |
| Catalan | 90.9 | Minor stylistic choices slightly less idiomatic |
| German | 90.9 | Slight formalities reduce colloquial sparkle |
| Japanese | 90.9 | Minor nuances and filler word cadence deviations |
| Turkish | 90.9 | Slightly stiff spoken tone |
| Ukrainian | 90.9 | Mostly met criteria |
| Danish | 90.5 | Minor literalness in connectors |
| Finnish | 90.5 | Slightly formal phrasing |
| Vietnamese | 90.1 | Minor stylistic choices reduce fluency |
| Croatian | 90.0 | Minor phrasing could be more idiomatic |
| Norwegian | 89.9 | Minor tone variations add Nordic character |
| Persian | 89.6 | Needs more natural conversational tone |
| Portuguese | 89.5 | Occasional slight stiffness in transitions |
| Albanian | 89.5 | Phrasing feels slightly stiff |
| Serbian | 89.5 | Some literal phrasing feels stiff |
| Polish | 89.3 | Some phrases feel slightly literal or formal for spoken Polish |
| Latvian | 89.2 | Minor spelling inconsistencies |
| Afrikaans | 89.1 | Slightly stiff phrasing and literal translations |
| Belarusian | 89.1 | Untranslated English prefix "Super-" |
| Slovene | 88.9 | Slight stiffness and literalness |
| Lithuanian | 88.7 | Slightly formal phrasing |
| Bulgarian | 88.5 | Inconsistent gender agreement |
| Georgian | 88.4 | Slight calque reduces fluency |
| Malay | 88.2 | Occasional stiff phrasing and minor punctuation issues |
| Hindi | 87.9 | Slightly stiff fluency |
| Macedonian | 87.9 | Minor non-idiomatic phrasing |
| Armenian | 87.8 | Minor stiffness and slight literalism |
| Korean | 87.2 | Minor lack of absolute naturalness |
| Basque | 86.6 | Occasional rigid phrasing |
| Azerbaijani | 86.4 | Slightly stiff or literal phrasing |
| Esperanto | 86.4 | Incorrect use of radiumo for ray |
| Estonian | 86.2 | Occasionally awkward phrasing and unnatural fillers disrupt fluency |
| Bengali | 85.6 | Slightly literal phrasing and terminology inconsistencies |
| Urdu | 85.5 | Minor stylistic formality issues |
| Mongolian | 85.4 | Stiff and unnatural phrasing |
| Greek | 85.1 | Lacks fluency and naturalness |
| Nepali | 84.9 | Awkward conversational fillers |
| Tamil | 84.8 | Awkward literal phrasing |
| Marathi | 84.6 | Hindi interjections disrupt fluency |
| Tagalog | 84.4 | Literal and unnatural phrasing |
| Malayalam | 84.1 | awkward phrasing |
| Hebrew | 83.5 | Slightly stiff phrasing |
| Khmer | 83.0 | Inconsistent use of English and Khmer for scientific terms |
| Sinhala | 82.9 | Slightly less idiomatic phrasing |
| Swahili | 82.8 | Rigid and literal phrasing lacks idiomatic flow |
| Hungarian | 82.6 | Stiff and literal phrasing lacks naturalness |
| Welsh | 81.7 | Stiff, unnatural Welsh sentence structure |
| Burmese | 81.7 | Overly literal and rigid phrasing |
| Irish | 81.6 | Translation feels unnatural and non-idiomatic |
| Icelandic | 81.2 | Lack of native idiomatic polish |
| Kannada | 80.5 | Mechanical phrasing and rigid syntax |
| Interlingua | 78.5 | Significant stylistic issues and unnatural phrasing |
| Lao | 77.8 | Critical terminology errors and fluency issues |
| Thai | 74.9 | Significant lexical errors and inconsistent tone |
| Telugu | 73.9 | Rigid sentence structure |
