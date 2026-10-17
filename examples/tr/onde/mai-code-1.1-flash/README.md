# examples/tr/onde/mai-code-1.1-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: MAI-Code-1.1-Flash-Q2-XS
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 90.8 | Adheres too closely to English syntax |
| Slovene | 87.7 | Slight stiffness and literalness |
| Malay | 85.8 | Awkward phrasing and literalism |
| Dutch | 85.2 | Awkward "psi squared" phrasing |
| Catalan | 84.7 | Inconsistent address forms (tu vs vostè/vós) |
| Swedish | 84.0 | Awkward phrasing and unnatural literalism |
| Croatian | 83.8 | Minor gender agreement errors and awkward phrasing |
| Danish | 82.0 | Lacks idiomatic fluency |
| Polish | 81.9 | Misaligned speaker labels and unnatural phrasing |
| Afrikaans | 81.8 | Lack of naturalness and stiffness |
| French | 81.6 | Awkward syntax and formatting error |
| Portuguese | 79.9 | Missing speaker labels |
| Norwegian | 78.8 | Significant grammatical errors and unnatural phrasing |
| Serbian | 78.3 | Spelling errors and mixed-language defects |
| Ukrainian | 78.2 | Phonetic transliteration of math symbols |
| Esperanto | 77.9 | Awkward phrasing and literal calquing |
| Spanish | 77.8 | Missing speaker tag and minor mechanical errors |
| Galician | 76.6 | Significant issues in fluency and naturalness |
| Turkish | 76.1 | Frequent vowel harmony errors |
| Persian | 74.3 | Language leakage with non-Persian characters |
| Latvian | 74.0 | Pervasive grammatical and syntactic errors |
| Vietnamese | 74.0 | Untranslated English words and syntax |
| Mongolian | 73.9 | Lacks natural flow and fluency |
| German | 73.8 | Inconsistent use of informal and formal address forms |
| Romanian | 73.4 | Missing dialogue cues and repetitive lines |
| Korean | 72.8 | Mixed-language errors |
| Slovak | 72.4 | Missing speaker labels |
| Finnish | 72.3 | Grammatical errors and awkward phrasing |
| Indonesian | 72.3 | Duplicated paragraph and disjointed dialogue |
| Icelandic | 72.2 | Significant terminology and fluency issues |
| Bulgarian | 72.0 | Untranslated English words disrupt fluency |
| Albanian | 70.7 | Stiff literalism lacking naturalness |
| Hungarian | 70.2 | Significant fluency issues and literal calques |
| Lithuanian | 70.2 | Incomplete with missing speaker tags and code-switching |
| Estonian | 70.1 | Significant quality issues and mechanical errors |
| Welsh | 69.5 | Frequent lexical errors and broken grammar |
| Japanese | 69.5 | Structural errors and inconsistent speaker attribution |
| Russian | 69.2 | Mixed languages and literal calques |
| Chinese | 68.9 | Incomplete and missing translation |
| Czech | 68.3 | Significant mechanical errors and formatting inconsistencies |
| Hindi | 68.2 | Inconsistent Sanskritized terminology |
| Thai | 68.1 | Systematic mechanical errors and mistranslations |
| Basque | 66.5 | Severe language mixing and structural defects |
| Macedonian | 66.2 | Untranslated English words and duplicated paragraphs |
| Swahili | 65.5 | Inconsistent code-switching and awkward phrasing |
| Irish | 65.2 | Severe linguistic flaws and unnatural phrasing |
| Belarusian | 64.3 | Pervasive terminology errors and Russianisms |
| Tagalog | 64.2 | Untranslated English phrases |
| Azerbaijani | 63.7 | Terminological inconsistencies and unnatural phrasing |
| Arabic | 62.2 | Frequent grammatical and terminology errors |
| Marathi | 62.1 | Severe grammatical gender agreement errors |
| Greek | 61.9 | Severe text duplication and terminology errors |
| Bengali | 60.4 | Severely fragmented structure and grammar |
| Armenian | 60.2 | Severe structural failures and untranslated segments |
| Telugu | 57.9 | Pervasive spelling errors and poor terminology |
| Urdu | 57.5 | Severe terminology and name errors |
| Nepali | 55.9 | Severe mixed-language infiltration and technical errors |
| Tamil | 55.3 | Pervasive misuse of suffixes and grammar |
| Interlingua | 54.5 | Pseudo-translation mixing multiple languages |
| Sinhala | 54.3 | Poor scientific terminology and unnatural grammar |
| Khmer | 53.8 | Frequent mixed language |
| Hebrew | 46.6 | Untranslated English fragments throughout |
| Georgian | 41.9 | Extensive untranslated code-switching |
| Lao | 37.5 | Severe hallucinations and gibberish |
| Kannada | 34.8 | Severe errors and unintelligibility |
| Malayalam | 28.5 | Severe language mixing and fragmentation |
| Burmese | 25.9 | Severe hallucination and nonsensical phrases |
