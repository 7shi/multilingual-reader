# examples/tr/onde/glm-5.3/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: z-ai/glm-5.3
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Croatian | 92.0 | Slight translationese and awkward transitions |
| Galician | 90.2 | Minor stylistic fluency issues |
| Bulgarian | 90.0 | Some sentences feel slightly literal or stiff |
| Estonian | 88.4 | Minor lack of naturalness and flow |
| Malay | 87.9 | Retains English sentence structure |
| Georgian | 87.4 | Lacks naturalness and fluency |
| Korean | 86.1 | Slightly rigid and literal syntax |
| French | 86.0 | Repetitive dialogue artifacts disrupt fluency |
| Hindi | 85.4 | Notable fluency and naturalness deficits |
| Malayalam | 83.9 | Stiff and unnatural tone |
| Italian | 83.8 | Severe copy-paste defects causing dialogue duplication |
| Armenian | 82.5 | Stiff fluency and minor grammatical issues |
| Swedish | 81.5 | Duplicate line and formatting glitches |
| Nepali | 81.3 | Stiff literal tone lacks natural fluency |
| Turkish | 81.1 | Stiff phrasing and mixed language errors |
| Norwegian | 80.8 | Duplications and typos reduce fluency |
| Czech | 80.2 | Severe duplication errors compromise readability |
| Catalan | 79.5 | severe copy-paste glitches |
| German | 79.5 | Repetition artifacts disrupt flow |
| Indonesian | 79.5 | inconsistent character register shift |
| Russian | 79.5 | Severe text duplication and meta-commentary |
| Chinese | 79.5 | Repetition error and stiffness |
| Portuguese | 79.3 | Copy-paste line duplication errors |
| Dutch | 79.2 | Significant sentence duplication error |
| Danish | 79.0 | Noticeable awkwardness and stiffness in phrasing |
| Spanish | 78.8 | Duplicated line and stiff phrasing |
| Esperanto | 78.7 | Severe mechanical editing errors and duplicated text |
| Bengali | 78.5 | Inconsistent tone and awkward phrasing |
| Macedonian | 78.2 | Significant text duplications throughout |
| Belarusian | 77.8 | Untranslated English and text duplication |
| Tamil | 77.8 | Rigid prose and unnatural phrasing |
| Hebrew | 77.7 | Significant duplication error disrupts flow |
| Lao | 77.7 | Inconsistent scientific terminology and poor fluency |
| Telugu | 77.6 | Awkward phrasing due to translationese |
| Thai | 77.4 | Notable copy-paste glitch in summary |
| Slovene | 77.1 | Repetitive dialogue tags |
| Lithuanian | 76.7 | Editing artifacts and grammatical errors |
| Vietnamese | 76.7 | Severe mechanical text duplications and punctuation errors |
| Kannada | 76.6 | Heavy reliance on transliterated English terms |
| Sinhala | 76.6 | Fluency and naturalness issues |
| Serbian | 76.4 | Formatting glitches with duplicated lines |
| Arabic | 75.8 | Noticeable typos and glitches |
| Persian | 75.8 | Prominent duplicated lines disrupting the text |
| Japanese | 75.8 | Prominent text glitches disrupt fluency |
| Greek | 75.4 | Duplicate sentence due to editing error |
| Afrikaans | 74.2 | Dialogue attribution error and spelling inaccuracies |
| Slovak | 74.2 | Severe duplication and missing dialogue lines |
| Hungarian | 73.8 | Duplicated dialogue and stiff phrasing |
| Latvian | 73.7 | Duplicated labels and omitted dialogue |
| Finnish | 73.6 | Severe mechanical editing errors and artifacts |
| Albanian | 73.2 | Significant duplication glitch in the middle of the text |
| Ukrainian | 72.6 | Severe duplication and mixed-language fragments |
| Polish | 72.5 | Significant structural integrity issues |
| Khmer | 72.4 | Significant linguistic awkwardness and lexical errors |
| Burmese | 72.1 | Awkward literal phrasing and stiff tone |
| Marathi | 70.5 | Mechanical errors and inconsistent address |
| Azerbaijani | 70.2 | Poor fluency and missing dialogue tags |
| Irish | 69.4 | Critical structural defects and duplicate lines |
| Icelandic | 69.4 | Major technical errors and scientific terminology inconsistencies |
| Romanian | 68.6 | Broken flow from English meta-commentary |
| Tagalog | 65.9 | Mechanical text repetitions and unnatural phrasing |
| Swahili | 65.7 | Structural corruption and flawed terminology |
| Basque | 65.5 | Fatal errors including non-existent words and duplicate lines |
| Urdu | 62.9 | Extensive meta-commentary embedded in text |
| Mongolian | 61.2 | Corrupted speaker labels |
| Welsh | 56.0 | Severe mixed language and corrupted Welsh |
| Interlingua | 55.1 | Significant grammatical errors and mixed language |
