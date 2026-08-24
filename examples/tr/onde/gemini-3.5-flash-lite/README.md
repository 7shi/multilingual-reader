# examples/tr/onde/gemini-3.5-flash-lite/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemini-3.5-flash-lite
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 97 | Minor non-natural filler words |
| Swedish | 97 | Flawless and publication-ready quality |
| French | 96 | High quality with minor linguistic oversights |
| Korean | 95 | Minor stylistic stiffness and particle notation issues |
| Italian | 94 | Minor non-standard mathematical phrasing |
| Armenian | 93 | High quality with minor typos and terminology inconsistencies |
| Polish | 92 | High quality with minor speaker-label and syntactic issues |
| Galician | 91 | Minor Lusitanisms (e.g., quadrado) and typos |
| Georgian | 91 | Minor OCR artifacts in otherwise excellent translation |
| Portuguese | 91 | Minor speaker tag inconsistencies |
| Vietnamese | 91 | Minor stylistic adjustments needed for spoken fluency |
| Slovene | 90 | Minor terminology slips and literal phrasing artifacts |
| Dutch | 89 | Minor errors and non-natural phrasing |
| Czech | 86 | Minor typographical and grammatical errors require light editing |
| Catalan | 85 | Minor errors and typos |
| Hindi | 85 | Minor fluency and formatting issues |
| Afrikaans | 83 | Typographical errors and incorrect terminology |
| Esperanto | 83 | Minor terminology inaccuracies |
| Malayalam | 82 | Ready for publication with high quality |
| Burmese | 81 | Minor typos and terminology errors |
| Azerbaijani | 80 | Literal phrasing and terminology inconsistencies |
| Serbian | 80 | Terminology and grammatical errors |
| Japanese | 79 | One untranslated English dialogue line |
| Russian | 79 | Mixed-language fragments disrupt coherence |
| German | 78 | Grammatical errors and unnatural phrasing |
| Urdu | 78 | Inconsistent speaker tags and technical terminology |
| Arabic | 74 | Untranslated English sentence present |
| Turkish | 73 | Missing sentence fragment disrupts flow |
| Thai | 71 | One full sentence left untranslated in English |
| Bulgarian | 70 | Significant untranslated English segments |
| Persian | 69 | Mixed-language placeholders and untranslated sentences |
| Indonesian | 68 | Critical semantic inversion and generation artifacts |
| Telugu | 68 | Structural defects and typographical errors |
| Finnish | 67 | Critical typos, structural placeholders, and meta-commentary |
| Norwegian | 65 | Persistent artifacts and non-standard math notation |
| Kannada | 63 | Significant technical inaccuracies and unnatural phrasing |
| Romanian | 63 | Multiple grammatical errors and artifacts |
| Croatian | 61 | Mixed-language insertion and lexical errors |
| Malay | 61 | Critical terminology errors and structural omissions |
| Hebrew | 60 | Untranslated English line breaks language consistency |
| Danish | 59 | Frequent speaker attribution errors and typos |
| Icelandic | 56 | Critical terminology and semantic errors |
| Hungarian | 53 | Unremoved placeholder and literal mistranslation |
| Nepali | 52 | Mixed-language artifacts and untranslated lines |
| Albanian | 52 | Pervasive grammatical errors |
| Slovak | 51 | Severe grammatical defects |
| Khmer | 50 | Critical structural defects and unnatural phrasing |
| Latvian | 50 | Systematic grammatical errors and terminology mismatches |
| Lithuanian | 49 | Severe systematic grammatical errors |
| Tagalog | 49 | Major terminology and fluency defects |
| Chinese | 49 | Mixed-language artifacts and untranslated text |
| Basque | 45 | Critical structural glitches and repetitive errors |
| Belarusian | 42 | Untranslated English sentences and inconsistent speaker labeling |
| Marathi | 42 | Severe structural and mixed-language defects |
| Ukrainian | 39 | Missing English text segments |
| Bengali | 38 | Pervasive encoding corruption and mixed language |
| Macedonian | 36 | Critical mixed-language defects and lexical errors |
| Greek | 33 | Critical structural defects and mixed-language content |
| Lao | 33 | Structural defects and mixed orthography |
| Mongolian | 33 | Critical structural flaws and untranslated English sentences |
| Swahili | 33 | Mixed-language defects and garbled output |
| Estonian | 32 | Critical structural defects and untranslated content |
| Tamil | 30 | Severe foreign character corruption throughout text |
| Irish | 27 | Severe mixed-language intrusions and critical terminology errors |
| Interlingua | 26 | Critical structural defects and mixed language |
| Welsh | 23 | Mixed-language character intrusions and structural defects |
| Sinhala | 20 | Severe mixed-script contamination |
