# examples/tr/onde/glm-5.3/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: z-ai/glm-5.3
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Galician | 90.5 | Minor stylistic fluency issues |
| Bulgarian | 89.8 | Some sentences feel slightly literal or stiff |
| Croatian | 89.1 | Slight translationese and awkward transitions |
| French | 88.1 | Repetitive dialogue artifacts disrupt fluency |
| Malay | 88.0 | Retains English sentence structure |
| Korean | 87.8 | Slightly rigid and literal syntax |
| Estonian | 86.2 | Minor lack of naturalness and flow |
| Georgian | 85.5 | Lacks naturalness and fluency |
| Hindi | 85.1 | Notable fluency and naturalness deficits |
| Italian | 84.8 | Severe copy-paste defects causing dialogue duplication |
| Norwegian | 84.2 | Duplications and typos reduce fluency |
| Armenian | 83.9 | Stiff fluency and minor grammatical issues |
| Malayalam | 83.8 | Stiff and unnatural tone |
| Portuguese | 83.8 | Copy-paste line duplication errors |
| Swedish | 83.5 | Duplicate line and formatting glitches |
| Turkish | 83.3 | Stiff phrasing and mixed language errors |
| German | 82.4 | Repetition artifacts disrupt flow |
| Dutch | 82.2 | Significant sentence duplication error |
| Macedonian | 80.9 | Significant text duplications throughout |
| Slovene | 80.9 | Repetitive dialogue tags |
| Spanish | 80.8 | Duplicated line and stiff phrasing |
| Indonesian | 80.8 | inconsistent character register shift |
| Nepali | 80.8 | Stiff literal tone lacks natural fluency |
| Chinese | 80.6 | Repetition error and stiffness |
| Catalan | 80.5 | severe copy-paste glitches |
| Vietnamese | 80.3 | Severe mechanical text duplications and punctuation errors |
| Thai | 79.9 | Notable copy-paste glitch in summary |
| Danish | 79.8 | Noticeable awkwardness and stiffness in phrasing |
| Sinhala | 79.4 | Fluency and naturalness issues |
| Lao | 78.7 | Inconsistent scientific terminology and poor fluency |
| Russian | 78.7 | Severe text duplication and meta-commentary |
| Bengali | 78.6 | Inconsistent tone and awkward phrasing |
| Persian | 78.6 | Prominent duplicated lines disrupting the text |
| Czech | 78.5 | Severe duplication errors compromise readability |
| Japanese | 77.7 | Prominent text glitches disrupt fluency |
| Esperanto | 77.6 | Severe mechanical editing errors and duplicated text |
| Kannada | 77.3 | Heavy reliance on transliterated English terms |
| Lithuanian | 77.2 | Editing artifacts and grammatical errors |
| Greek | 77.0 | Duplicate sentence due to editing error |
| Hebrew | 77.0 | Significant duplication error disrupts flow |
| Afrikaans | 76.9 | Dialogue attribution error and spelling inaccuracies |
| Ukrainian | 76.4 | Severe duplication and mixed-language fragments |
| Hungarian | 76.2 | Duplicated dialogue and stiff phrasing |
| Tamil | 76.2 | Rigid prose and unnatural phrasing |
| Arabic | 76.1 | Noticeable typos and glitches |
| Polish | 76.1 | Significant structural integrity issues |
| Serbian | 75.9 | Formatting glitches with duplicated lines |
| Albanian | 75.3 | Significant duplication glitch in the middle of the text |
| Belarusian | 74.9 | Untranslated English and text duplication |
| Slovak | 74.0 | Severe duplication and missing dialogue lines |
| Finnish | 73.8 | Severe mechanical editing errors and artifacts |
| Latvian | 73.6 | Duplicated labels and omitted dialogue |
| Telugu | 73.4 | Awkward phrasing due to translationese |
| Azerbaijani | 72.5 | Poor fluency and missing dialogue tags |
| Khmer | 71.5 | Significant linguistic awkwardness and lexical errors |
| Burmese | 71.3 | Awkward literal phrasing and stiff tone |
| Romanian | 71.2 | Broken flow from English meta-commentary |
| Irish | 70.9 | Critical structural defects and duplicate lines |
| Marathi | 69.5 | Mechanical errors and inconsistent address |
| Icelandic | 69.0 | Major technical errors and scientific terminology inconsistencies |
| Swahili | 67.8 | Structural corruption and flawed terminology |
| Basque | 66.4 | Fatal errors including non-existent words and duplicate lines |
| Urdu | 64.2 | Extensive meta-commentary embedded in text |
| Mongolian | 63.8 | Corrupted speaker labels |
| Tagalog | 62.5 | Mechanical text repetitions and unnatural phrasing |
| Interlingua | 58.0 | Significant grammatical errors and mixed language |
| Welsh | 56.7 | Severe mixed language and corrupted Welsh |
