# examples/tr/onde/qwen3.8/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: qwen3.8
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Portuguese | 98 | Exemplary technical localization and audio-script adaptation |
| Spanish | 97 | Minor stylistic variations in filler words and punctuation |
| French | 97 | Professional-grade scientific accuracy and naturalness |
| Italian | 95 | Minor terminology tweaks needed for mathematical notation |
| Chinese | 95 | Professional quality with minor terminology nuances |
| German | 91 | Minor lexical errors and typos |
| Vietnamese | 91 | Minor unnatural fillers and literal phrasing |
| Catalan | 90 | Minor grammatical issues and calques slightly impact fluency |
| Romanian | 89 | Minor grammatical errors and literal phrasing |
| Turkish | 88 | Minor fluency and typographical issues |
| Ukrainian | 86 | Natural-sounding yet linguistically unpolished |
| Russian | 85 | Mixed-language glitch and minor non-idiomatic phrasing |
| Swedish | 85 | Minor grammar and unnatural phrasing |
| Danish | 83 | Grammatical errors and typos |
| Arabic | 77 | Scientifically accurate but lacks fluency |
| Macedonian | 77 | Notable typos and lack of fluency |
| Dutch | 77 | Missing English word and unnatural phrasing |
| Polish | 77 | Grammatical errors and literal calques |
| Galician | 75 | Portuguese interference and lexical inaccuracies |
| Malay | 71 | Inconsistent terminology and literal calques |
| Norwegian | 71 | Grammatical errors and typos |
| Afrikaans | 68 | Notable lexical errors and unnatural phrasing |
| Lithuanian | 67 | Persistent grammatical errors and non-standard terminology |
| Serbian | 65 | Frequent grammatical errors and terminology mistakes |
| Czech | 60 | Grammatical errors and Cyrillic intrusion |
| Indonesian | 60 | Mixed-language glitch with Chinese characters |
| Croatian | 59 | Severe typos and technical inaccuracies |
| Urdu | 59 | Literal phrasing and lexical inaccuracies |
| Bulgarian | 58 | Grammatical errors and terminology issues |
| Hindi | 57 | Significant technical terminology errors |
| Japanese | 56 | Mixed-language artifacts severely degrade fluency |
| Hungarian | 55 | Pervasive technical inaccuracies and grammatical errors |
| Marathi | 54 | Severe grammar and structural errors |
| Interlingua | 53 | Pervasive lexical mixing and uncorrected calques |
| Nepali | 52 | Severe quality issues and critical structural defects |
| Albanian | 52 | Severe lexical errors and MT artifacts |
| Persian | 50 | Mixed-language insertion and structural defects |
| Slovak | 50 | Frequent grammatical errors and unnatural literal translations |
| Slovene | 50 | Pervasive linguistic and typographical defects |
| Finnish | 48 | Severe linguistic quality issues and numerous grammatical errors |
| Bengali | 42 | Significant mistranslations and mechanical errors |
| Belarusian | 37 | Severe terminology and grammatical errors |
| Estonian | 33 | Pervasive grammatical and terminology errors |
| Tagalog | 33 | Severe physics mistranslations and hallucinated vocabulary |
| Azerbaijani | 32 | Severe grammatical errors and loss of tone |
| Hebrew | 32 | Severe semantic and grammatical errors |
| Georgian | 32 | Catastrophic errors requiring complete rewrite |
| Greek | 31 | Severe mixed-language fragments and terminology errors |
| Esperanto | 31 | Severe grammatical, lexical, and terminological errors |
| Latvian | 31 | Severe grammatical and terminological errors |
| Tamil | 30 | Mixed scripts and broken syntax |
| Korean | 29 | Severe incompleteness and mixed-language fragments |
| Thai | 28 | Severe truncation and technical typos |
| Armenian | 27 | Catastrophic machine translation errors |
| Welsh | 26 | Catastrophic vocabulary and structural breakdowns |
| Basque | 26 | Critical repetition loop ('agoa') and terminology failures |
| Khmer | 26 | Severe machine translation artifacts and gibberish |
| Kannada | 26 | Severe mixed scripts and lexical defects |
| Swahili | 26 | Severe lexical hallucinations and flawed terminology |
| Telugu | 26 | Severe scientific inaccuracies and poor fluency |
| Malayalam | 22 | Severe structural and lexical defects |
| Burmese | 22 | Severe lexical, grammatical, and technical errors |
| Icelandic | 21 | Severe semantic errors and poor technical handling |
| Lao | 21 | Severe machine-translation artifacts and broken grammar |
| Sinhala | 20 | Severe syntax errors and inaccurate terminology |
| Mongolian | 18 | Severe machine-translation artifacts |
| Irish | 14 | Severe grammatical and lexical errors |
