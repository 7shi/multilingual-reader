# examples/tr/onde/gpt-5.6-terra/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gpt-5.6-terra
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| German | 98 | Slightly literal spoken-phrasing choices |
| Danish | 97 | Minor editorial artifact and phrasing glitches |
| Spanish | 97 | Minor speaker name typos |
| Persian | 97 | Outstanding academic accuracy and natural flow |
| Georgian | 97 | Flawless publication-ready physics translation |
| Portuguese | 97 | Minor typo 'Camian' instead of 'Camille' |
| Hebrew | 96 | Minor typographical issues and inconsistencies |
| Hungarian | 96 | Excellent translation with minor formatting issues |
| Japanese | 96 | Minor typo in speaker name consistency |
| Russian | 96 | Exemplary scientific and conversational quality |
| Ukrainian | 96 | Excellent quality with minor stylistic flaws |
| Afrikaans | 95 | Flawless scientific precision and natural tone |
| Macedonian | 95 | Minor stylistic issues and literal phrasing |
| Nepali | 95 | High accuracy with minor stylistic flaws |
| Slovene | 95 | Minor literal phrasing and one typo |
| Bengali | 93 | High quality with minor terminology slips |
| Urdu | 92 | High accuracy with minor terminology inconsistencies |
| Bulgarian | 91 | Single corrupted encoding artifact |
| Greek | 91 | Minor non-standard physics terminology |
| Galician | 91 | Minor typos and terminology issues |
| Armenian | 91 | Minor literal phrasing affects fluency |
| Malayalam | 91 | Minor stylistic refinements needed for fluency |
| Marathi | 91 | Minor grammatical and typographical errors |
| Romanian | 91 | Minor typos and awkward phrasing |
| Serbian | 91 | Minor typos in names and terms |
| Turkish | 91 | Minor structural artifact disrupts flow |
| Burmese | 90 | Balanced technical accuracy with accessible tone |
| Latvian | 89 | Minor terminology inconsistencies and typos |
| Azerbaijani | 88 | Minor terminological and grammatical errors |
| Belarusian | 88 | Minor terminology and stylistic issues |
| Mongolian | 88 | Minor lexical calques impact fluency |
| Telugu | 88 | Minor terminology inconsistencies and anglicized phrasing |
| Thai | 86 | Mixed encoding and embedded English notes |
| Lithuanian | 85 | Uncleaned translator notes and typos |
| Italian | 83 | Critical mixed-language structural artifacts |
| Hindi | 82 | Minor structural glitches and slightly literal phrasing |
| Khmer | 82 | Inconsistent physics terminology and formatting |
| Tamil | 81 | Minor terminology inconsistencies and copy-paste artifacts |
| Kannada | 80 | Inconsistent technical accuracy and terminology |
| Slovak | 80 | Critical structural artifact disrupts coherence |
| Swedish | 79 | Encoding artifacts and typos |
| Interlingua | 78 | Structural artifact and literal phrasing |
| Albanian | 77 | Corrupted structural artifact disrupts flow |
| Esperanto | 76 | Terminology errors and non-standard phrasing |
| Czech | 74 | Embedded meta-commentary artifact |
| Estonian | 74 | Notable multilingual intrusion and terminology errors |
| French | 74 | Critical structural artifact and line omissions |
| Sinhala | 74 | Mixed-language typographical corruption |
| Chinese | 73 | Corrupted mixed-language artifacts |
| Basque | 71 | Critical structural defect: unedited English text artifact |
| Tagalog | 71 | Non-standard terminology and unnatural phrasing |
| Polish | 69 | Critical structural defects and editing artifacts |
| Catalan | 66 | Untranslatable English meta-comments disrupt structure |
| Indonesian | 64 | Mixed-language artifact and structural defects |
| Malay | 61 | Critical structural glitch and inaccurate physics terminology |
| Finnish | 58 | Corrupted mixed-script artifacts disrupt readability |
| Icelandic | 56 | Persistent mixed-language artifact and grammatical errors |
| Irish | 54 | Critical structural defect and lexical errors |
| Vietnamese | 50 | Unremoved English meta-commentary |
| Swahili | 49 | Critical terminology errors and structural defects |
| Lao | 45 | English meta-commentary disrupts text |
| Arabic | 41 | Mixed-language meta-text intrusion disrupts flow |
| Korean | 39 | Random non-Korean characters disrupt fluency |
| Norwegian | 37 | Severe structural corruption from injected meta-prompts and mixed languages |
| Welsh | 32 | Critical structural defect: mixed-language spam insertion |
| Dutch | 24 | Critical structural artifacts disrupt narrative flow |
| Croatian | 9 | Mixed-language artifacts and editorial notes |
