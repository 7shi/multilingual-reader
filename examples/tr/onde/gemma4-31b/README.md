# examples/tr/onde/gemma4-31b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemma4:31b-it-qat
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The quality trend for each language, based on the evaluation results (`SCORES.txt`) and manual content verification, is as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 98 | Exceptional quality ready for professional use |
| Japanese | 97 | Minor stylistic phrasing issues |
| Portuguese | 97 | Minor literal translations and false friends |
| Swedish | 97 | Minor stylistic tweaks for spoken flow noted |
| Turkish | 97 | Excellent technical accuracy and natural flow |
| Chinese | 97 | Minor awkwardness in conversational phrases |
| Danish | 96 | Minor issues with mathematical expression rendering |
| Russian | 96 | Exceptional scientific accuracy and natural podcast tone |
| Ukrainian | 96 | Minor stylistic calques present but negligible |
| German | 95 | Minor stylistic calques present |
| Italian | 95 | Minor stylistic calques and notation issues |
| Thai | 95 | Exceptionally high-quality and publication-ready |
| Indonesian | 94 | Minor terminology adjustments needed |
| Korean | 94 | Minor psi transliteration quirks |
| Dutch | 94 | Minor stylistic issues with mathematical notation phrasing |
| Norwegian | 94 | Minor terminology and notation quirks |
| Vietnamese | 94 | Minor stylistic and technical phrasing refinements needed |
| Romanian | 93 | Minor stylistic calques and rigid phrasing |
| Bulgarian | 92 | Minor fluency and idiomatic issues remain |
| Galician | 92 | Minor orthographic and lexical inconsistencies |
| Arabic | 91 | Minor phrasing and terminology issues |
| Spanish | 91 | Mistranslation of 'ingenuity' as 'ingenuidad' |
| Hindi | 91 | Minor stylistic inconsistencies and register mixing |
| Tamil | 91 | Minor literalism and typos |
| Persian | 90 | Minor literal phrasing and filler word issues |
| Hebrew | 90 | Minor vocabulary and syntax errors prevent perfection |
| Serbian | 89 | Minor errors and non-standard terminology |
| Telugu | 88 | Minor grammatical errors and literal phrasing |
| Finnish | 87 | Minor typographical slips and literal phrasing |
| Croatian | 87 | Minor terminology and syntax errors |
| Polish | 84 | Physics terminology errors (e.g., zachowanie vs zasada zachowania) and typos |
| Nepali | 83 | Minor language slips and typos |
| Albanian | 79 | Minor fluency and terminology issues with one mixed-language defect |
| Malay | 77 | Terminology errors and literal calques |
| Marathi | 75 | Mixed-language artifact 'dividido' and wrong term for amplitude |
| Urdu | 75 | Inconsistent physics terminology and literal phrasing |
| Czech | 74 | Persistent anglicisms and unnatural phrasing |
| Greek | 73 | Recurring terminology conflation and typos |
| Azerbaijani | 71 | Terminology errors and awkward phrasing |
| Swahili | 70 | Non-standard terminology and awkward phrasing |
| Bengali | 64 | Pervasive Unicode corruption and typos |
| Tagalog | 61 | Non-standard physics terminology |
| Catalan | 60 | Mixed-language artifact and lexical errors |
| Macedonian | 59 | Significant machine-translation artifacts and mixed-language errors |
| Afrikaans | 54 | Pervasive lexical errors and machine-translation artifacts |
| Slovak | 53 | Pervasive MT artifacts and grammatical errors |
| Hungarian | 43 | Severe machine translation artifacts and typos |
| Esperanto | 40 | Severe terminological and grammatical errors |
| Kannada | 38 | Mixed scripts and languages |
| Belarusian | 34 | Severe text corruption and Russian interference |
| Armenian | 34 | Severe mixed-language artifacts and encoding errors |
| Icelandic | 33 | Severe technical and linguistic defects |
| Latvian | 33 | Severe mixed-language errors and gibberish |
| Burmese | 32 | Mixed-language script artifacts |
| Sinhala | 32 | Mixed-language script corruption |
| Slovene | 32 | Severe lexical and grammatical errors with machine-translation artifacts |
| Mongolian | 31 | Severe MT artifacts and mixed-language intrusion |
| Lao | 24 | Severe mixed-language corruption and structural defects |
| Lithuanian | 24 | Pervasive structural defects and mixed-language intrusions |
| Basque | 21 | Severe multilingual contamination and broken grammar |
| Interlingua | 19 | Severe mixed-language structural corruption |
| Khmer | 17 | Severe mixed-language corruption |
| Malayalam | 17 | Severe multilingual script contamination |
| Irish | 16 | Catastrophic language mixing and structural defects |
| Welsh | 15 | Catastrophic linguistic breakdown and nonsense |
| Georgian | 12 | Pervasive mixed-language script injections |
| Estonian | 11 | Severe mixed-language corruption and structural defects |
