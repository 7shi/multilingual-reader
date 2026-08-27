# examples/tr/onde/gemini-3-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gemini-3-flash-preview
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 98 | Minor formatting and missing speaker tags |
| Czech | 97 | Minor formatting inconsistencies |
| Vietnamese | 97 | Minor formatting and structural inconsistencies |
| Romanian | 96 | Minor dialogue formatting errors |
| Spanish | 95 | Minor typographical and formatting artifacts |
| Japanese | 95 | High quality with minor formatting issues |
| Portuguese | 95 | Minor formatting inconsistencies with speaker tags |
| Bulgarian | 94 | Minor formatting and terminology glitches |
| French | 94 | Minor formatting and grammatical inconsistencies |
| Tamil | 93 | Minor terminology inconsistencies |
| Finnish | 92 | Minor terminology and formatting errors |
| Ukrainian | 92 | Minor terminology non-standardization |
| Arabic | 91 | Repetition defect and missing speaker label |
| Macedonian | 91 | Minor structural inconsistencies with missing speaker labels |
| Russian | 91 | Minor formatting inconsistencies in dialogue tags |
| Slovene | 91 | Minor mathematical phrasing errors |
| Armenian | 90 | Minor duplication and typo issues |
| Polish | 90 | Minor formatting inconsistencies in dialogue tags |
| Chinese | 90 | Notable textual repetition error |
| Danish | 89 | Missing speaker labels and encoding artifact |
| German | 89 | Minor calques and structural issues |
| Hebrew | 89 | Minor linguistic and formatting inconsistencies |
| Hungarian | 89 | Speaker tags are missing throughout the text |
| Lithuanian | 89 | Minor formatting glitches and lexical slips |
| Thai | 89 | Minor fluency issues and editing artifacts |
| Korean | 88 | Missing speaker tags and duplicated paragraphs |
| Dutch | 88 | Missing speaker tags disrupt dialogue flow |
| Italian | 87 | Formatting artifacts and awkward phrasing |
| Swedish | 87 | Minor phrasing and formatting inconsistencies |
| Telugu | 87 | Minor stiffness and typos remain |
| Turkish | 87 | Minor formatting and filler translation issues |
| Afrikaans | 86 | Minor formatting and lexical issues |
| Belarusian | 86 | Minor typos and terminology errors |
| Malayalam | 85 | Drafting artifacts like duplication and merged lines |
| Marathi | 85 | Minor literal phrasing and missing speaker tags |
| Urdu | 85 | Minor fluency issues and formatting errors |
| Khmer | 83 | Minor physics terminology and fluency issues |
| Welsh | 82 | Anglicisms and literal translations |
| Estonian | 82 | Notable proofreading oversights and formatting glitches |
| Galician | 82 | Portuguese lexical interference and missing speaker labels |
| Croatian | 82 | Occurrences of literal English calques and minor grammatical issues |
| Georgian | 82 | Technical accuracy marred by typos and omissions |
| Sinhala | 82 | Technical accuracy hindered by stiff phrasing |
| Persian | 81 | Minor structural and formatting issues |
| Hindi | 81 | Missing and swapped speaker tags |
| Indonesian | 81 | Inconsistent dialogue tags and terminology errors |
| Nepali | 80 | Editorial defects: duplications and formatting errors |
| Serbian | 80 | Technical terminology and notation inconsistencies |
| Albanian | 78 | Minor typos and phrasing issues |
| Kannada | 76 | Inconsistent terminology and literal syntax |
| Greek | 74 | Critical physics terminology errors and inconsistencies |
| Azerbaijani | 73 | Structural defects and stray Chinese character |
| Burmese | 73 | Notable text duplication artifacts |
| Mongolian | 72 | Technical inaccuracies and unnatural phrasing |
| Latvian | 71 | Mixed-language artifact and formatting defects |
| Malay | 67 | Terminology errors and formatting artifacts |
| Basque | 63 | Severe truncation mid-dialogue |
| Norwegian | 60 | Severe dialogue formatting and speaker attribution errors |
| Icelandic | 41 | Missing speaker tags and mixed language artifacts |
| Interlingua | 40 | Severe structural contamination with French and English |
| Slovak | 40 | Raw JSON fragment embedded mid-text |
| Esperanto | 39 | Critical formatting errors and foreign artifacts |
| Swahili | 36 | Repetitive Chinese characters disrupt text |
| Irish | 27 | Mixed-language artifacts and structural errors |
| Lao | 26 | Critical generation loop with HTML tags |
| Tagalog | 24 | Severe structural and code artifacts corrupting coherence |
| Bengali | 16 | Severe numeric placeholder corruption |
