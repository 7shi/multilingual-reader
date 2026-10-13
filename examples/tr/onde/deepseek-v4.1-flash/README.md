# examples/tr/onde/deepseek-v4.1-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: DeepSeek V4.1 Flash
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Czech | 79.2 | Noticeable issues in fluency and naturalness |
| Burmese | 78.1 | Awkward phrasing and tone inconsistencies |
| Danish | 76.6 | Untranslated word and misplaced dialogue line |
| French | 76.3 | Missing speaker label for Luc |
| Macedonian | 76.1 | Structural inconsistencies and awkward phrasing |
| Ukrainian | 76.1 | Critical structural and formatting errors |
| Indonesian | 75.8 | Inconsistent pronoun usage |
| Swedish | 75.8 | Missing speaker tags |
| Chinese | 75.0 | Structural redundancy causes repetition error |
| Catalan | 74.2 | Stiff and unnatural dialogue flow |
| Arabic | 73.2 | Mechanical errors and inconsistent speaker tags |
| Norwegian | 73.0 | Poor dialogue formatting and attribution |
| Thai | 72.8 | Inconsistent tone and register |
| Spanish | 72.6 | Missing speaker tags and duplicated lines |
| Khmer | 72.5 | Significant speaker attribution errors and awkward literalism |
| Russian | 72.0 | Missing speaker tags |
| Tamil | 72.0 | Omitted dialogue lines break flow and attribution |
| Albanian | 71.8 | Severe structural and formatting issues |
| Italian | 71.7 | Mixed language fragments and missing speaker tags |
| Romanian | 71.5 | Frequent absence of speaker labels |
| Persian | 71.3 | Duplicate lines regarding diffraction |
| Korean | 71.1 | Awkward phrasing and dialogue formatting issues |
| Basque | 70.8 | Significant fluency and grammatical issues |
| Slovak | 70.6 | Missing speaker labels disrupt dialogue |
| German | 70.4 | Formatting breakdown obscuring speaker attribution |
| Telugu | 70.3 | Awkward phrasing and imprecise terminology |
| Mongolian | 70.0 | Severe formatting errors |
| Dutch | 70.0 | Severe dialogue formatting defects |
| Portuguese | 69.8 | Severe structural and editing errors |
| Armenian | 69.6 | Major structural and coherence defects |
| Hindi | 69.5 | Structural and continuity errors |
| Croatian | 69.5 | Missing speaker labels throughout |
| Nepali | 69.5 | Missing dialogue tags |
| Slovene | 69.5 | Missing speaker attributions and repetition |
| Tagalog | 69.4 | Multiple grammatical errors and structural omissions |
| Azerbaijani | 69.3 | Severe speaker attribution errors |
| Marathi | 69.2 | Missing speaker attributions |
| Bulgarian | 69.0 | Severe speaker attribution errors |
| Finnish | 69.0 | Severe structural errors and duplications |
| Galician | 69.0 | Significant fluency and naturalness issues with awkward phrasing |
| Turkish | 68.7 | Missing and swapped speaker labels |
| Urdu | 68.7 | Stiff tone and literal idioms |
| Georgian | 68.4 | Stiff and mechanically translated |
| Japanese | 68.1 | Repeated line and speaker attribution issues |
| Malay | 68.1 | Missing speaker tags and awkward phrasing |
| Vietnamese | 67.8 | Severe editing artifacts like duplicated lines and broken speaker attribution |
| Bengali | 67.5 | Inconsistent pronouns and missing speaker labels |
| Irish | 67.5 | Severe grammatical errors and inaccurate terminology |
| Polish | 67.3 | Missing speaker labels throughout |
| Malayalam | 67.2 | Severe grammatical and lexical flaws |
| Lithuanian | 66.5 | Severe structural and formatting errors |
| Estonian | 66.3 | Severe dialogue attribution errors |
| Swahili | 66.3 | Inconsistent scientific terminology and unnatural phrasing |
| Icelandic | 66.0 | Severely broken dialogue flow and unnatural syntax |
| Belarusian | 65.9 | Omitted conversational fillers and unnatural phrasing |
| Sinhala | 65.8 | Significant fluency and naturalness issues |
| Hebrew | 65.6 | Missing speaker tags and poor formatting |
| Serbian | 65.6 | Structural glitches and repetition |
| Welsh | 65.2 | Pervasive non-standard forms and phonetic approximations |
| Latvian | 63.6 | Complete breakdown of dialogue structure and speaker attribution |
| Lao | 62.5 | Terminology errors and unnatural phrasing |
| Hungarian | 62.3 | Missing speaker attributions |
| Kannada | 62.2 | Formatting issues and unnatural phrasing |
| Esperanto | 61.5 | Complete breakdown of dialogue attribution |
| Afrikaans | 61.2 | Missing speaker labels |
| Greek | 61.2 | Structural defects and unnatural physics terminology |
| Interlingua | 60.2 | Severe lack of consistency and standard adherence |
