# examples/tr/onde/gemini-2.5-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemini-2.5-flash
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 97 | Professional grade with minor stylistic polishing needed |
| Spanish | 96 | Highly professional and accurate with minor flaws |
| French | 96 | Flawless professional quality with minor stylistic inconsistencies |
| Portuguese | 94 | Inconsistent PT-BR and PT-PT spelling |
| Turkish | 94 | Minor phrasing issues and missing speaker tags |
| Ukrainian | 94 | Minor terminology anglicisms and typos |
| Romanian | 93 | Minor typos and phrasing issues prevent perfection |
| Georgian | 92 | Minor dialogue formatting issues |
| Slovak | 92 | Minor typo and non-idiomatic phrasing |
| Arabic | 91 | Minor stylistic refinements needed for native fluency |
| Armenian | 91 | Minor terminology deviations and syntax issues |
| Macedonian | 91 | Minor stylistic stiffness and literal phrasing |
| Dutch | 91 | Minor grammatical and formatting flaws |
| Swedish | 91 | Minor typos and literal phrasing |
| Czech | 90 | Severe structural errors like speaker tag swaps |
| Persian | 90 | Minor terminology and phrasing issues |
| Chinese | 90 | Minor literalness and irregular structure |
| Hebrew | 89 | Minor grammar and terminology issues |
| Hindi | 89 | High quality with minor fluency issues |
| Croatian | 89 | Minor terminology and phrasing calques |
| Burmese | 89 | Minor typos and terminology deviations |
| Polish | 89 | Minor Cyrillic-Latin encoding glitch |
| Icelandic | 88 | High quality with minor terminology and phrasing issues |
| Telugu | 88 | Minor fluency and formatting issues |
| Italian | 86 | Missing speaker labels |
| Marathi | 86 | High quality with minor flow issues |
| Slovene | 86 | Speaker label consistency issues |
| German | 85 | Minor calques and stiff syntax |
| Korean | 85 | Minor typos and inconsistent tagging |
| Norwegian | 85 | Literal translation artifacts in mathematical terminology and exponents |
| Russian | 85 | Missing speaker tags |
| Tamil | 85 | Minor grammatical stiffness and formatting issues |
| Afrikaans | 84 | Minor terminology and formatting errors |
| Basque | 84 | Minor terminology errors and missing speaker labels |
| Lithuanian | 84 | Minor technical and grammatical errors |
| Finnish | 83 | Critical typo 'kaksoiraokeen', missing labels |
| Indonesian | 83 | Minor dialogue attribution glitches and non-idiomatic phrasing |
| Vietnamese | 81 | Grammar slips and unnatural phrasing |
| Belarusian | 80 | Missing speaker labels and typos |
| Bulgarian | 80 | Formatting inconsistencies and literal phrasing |
| Japanese | 80 | Missing speaker tags and formatting errors |
| Nepali | 80 | Minor fluency and formatting issues |
| Azerbaijani | 79 | Structural and typographical errors |
| Latvian | 79 | Inaccurate terminology and rigid phrasing |
| Urdu | 79 | Noticeable machine-translation artifacts and semantic errors |
| Esperanto | 78 | Lexical errors and awkward mathematical calques |
| Malayalam | 78 | Minor fluency and terminology issues |
| Serbian | 78 | Omission of speaker tags and terminology errors |
| Greek | 77 | Grammatical inconsistencies and missing speaker labels |
| Galician | 77 | Systematic loss of speaker tags and Portuguese interference |
| Bengali | 76 | Missing or inconsistent speaker tags |
| Danish | 76 | missing speaker tags |
| Khmer | 76 | Overly literal phrasing and inconsistent punctuation |
| Mongolian | 76 | Missing dialogue tags and awkward phrasing |
| Sinhala | 76 | Technical inaccuracies and rigid phrasing |
| Thai | 76 | Missing speaker tags and awkward phrasing |
| Albanian | 75 | Persistent grammatical agreement errors and unnatural phrasing |
| Swahili | 70 | Terminology inaccuracies and unnatural phrasing |
| Estonian | 66 | Missing speaker labels and terminology errors |
| Malay | 66 | Critical terminology errors and mixed-language artifacts |
| Kannada | 65 | Significant physics terminology errors |
| Hungarian | 64 | Missing speaker tags and structural errors |
| Tagalog | 64 | Significant terminology errors and unnatural phrasing |
| Interlingua | 63 | Mixed-language intrusions and structural defects |
| Irish | 60 | Pervasive technical terminology errors and non-idiomatic phrasing |
| Welsh | 53 | Significant grammatical errors and unnatural syntax |
| Lao | 49 | Major terminology inaccuracies and formatting issues |
