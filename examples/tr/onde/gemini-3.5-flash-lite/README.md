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
| Spanish | 97 | Minor unnatural conversational fillers |
| Swedish | 97 | Professional-grade accuracy and fluency |
| French | 96 | High quality with minor anglicisms |
| Korean | 95 | Minor stylistic stiffness and phrasing issues |
| Italian | 94 | Minor non-standard math phrasing 'psi quadro' and 'lambda mezzi' |
| Armenian | 93 | Minor typos and terminology inconsistencies |
| Polish | 92 | Minor speaker-label misattribution |
| Galician | 91 | Minor Lusitanisms and lexical errors |
| Georgian | 91 | Minor OCR typos and formatting glitches |
| Portuguese | 91 | Speaker tags swapped between interlocutors |
| Vietnamese | 91 | Minor stylistic adjustments needed for spoken fluency |
| Slovene | 90 | Minor terminology slips and literal phrasing |
| Hungarian | 89 | Minor typos and formatting errors |
| Burmese | 89 | Minor stylistic stiffness in technical sentences |
| Dutch | 89 | Minor fluency and attribution issues |
| Hebrew | 88 | Minor linguistic flaws and typos in an accurate scientific text |
| Czech | 86 | Minor grammatical and typographical imperfections |
| Catalan | 85 | Minor typographical errors and misattributed dialogue |
| Hindi | 85 | Minor fluency and terminology consistency issues |
| Afrikaans | 83 | Numerous critical lexical and typographical errors |
| Esperanto | 83 | Minor terminology inaccuracies in physics context |
| Malayalam | 82 | Requires linguistic polish and terminology standardization |
| Azerbaijani | 80 | Minor technical and stylistic issues |
| Serbian | 80 | Grammatical errors, speaker attribution mistakes, and terminology issues |
| Japanese | 79 | Single untranslated English line |
| Russian | 79 | Mixed-language fragments present |
| German | 78 | Grammatical errors and unnatural filler translations |
| Urdu | 78 | Inconsistent terminology and formatting glitches |
| Arabic | 74 | Critical untranslated English sentence defect |
| Basque | 74 | Typographical errors and terminology inconsistencies |
| Turkish | 73 | Untranslated sentence fragment disrupts completeness |
| Thai | 71 | Untranslated English sentence interrupts text |
| Bulgarian | 70 | Untranslated English segments |
| Persian | 69 | Mixed-language typos and untranslated sentences |
| Khmer | 69 | Naturalization and terminology standardization required |
| Indonesian | 68 | Semantic inversion and generation artifacts |
| Telugu | 68 | Grammatical errors and formatting glitches |
| Finnish | 67 | Critical terminology typo and meta-commentary |
| Norwegian | 65 | Missing speaker labels and formatting flaws |
| Romanian | 63 | Major grammatical errors and unedited artifacts |
| Croatian | 61 | Untranslated English paragraph remains mid-text |
| Kannada | 61 | Mixed scripts and terminology errors |
| Malay | 61 | Critical technical mistranslations and structural omissions |
| Danish | 59 | Speaker attribution glitches and terminology errors |
| Icelandic | 56 | Critical physics terminology errors and lexical mismatches |
| Nepali | 52 | Severe formatting artifacts and untranslated dialogue |
| Albanian | 52 | Systematic grammatical errors and case misuse |
| Slovak | 51 | Severe grammatical and syntactic errors |
| Latvian | 50 | Systematic grammatical and terminology errors |
| Lithuanian | 49 | Severe systemic grammatical errors |
| Tagalog | 49 | Major terminology and fluency defects |
| Chinese | 49 | Severe mixed-language artifacts disrupt quality |
| Belarusian | 42 | Presence of untranslated English text |
| Marathi | 42 | Severe mixed-language and structural defects |
| Ukrainian | 39 | Critical structural defects with untranslated segments |
| Macedonian | 36 | Critical omissions and mixed-language defects |
| Greek | 33 | Untranslated English segments and technical errors |
| Lao | 33 | Severe structural and spelling defects |
| Mongolian | 33 | Untranslated English sentences and mixed speaker attributions |
| Swahili | 33 | Critical mixed-language defects and structural corruption |
| Estonian | 32 | Critical untranslating and wrong speaker tags |
| Tamil | 30 | Critical foreign character insertion |
| Welsh | 28 | Untranslated English blocks and structural defects |
| Irish | 27 | Mixed-language intrusions and structural defects |
| Interlingua | 26 | Untranslated English paragraph inserted mid-text |
| Sinhala | 20 | Catastrophic structural corruption with mixed scripts |
| Bengali | 0 | Severely incomplete and garbled |
