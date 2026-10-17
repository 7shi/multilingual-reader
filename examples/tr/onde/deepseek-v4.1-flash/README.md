# examples/tr/onde/deepseek-v4.1-flash/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: DeepSeek V4.1 Flash
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Burmese | 78.2 | Awkward phrasing and tone inconsistencies |
| Danish | 76.6 | Untranslated word and misplaced dialogue line |
| Thai | 75.8 | Inconsistent tone and register |
| Swedish | 75.0 | Missing speaker tags |
| Khmer | 74.9 | Significant speaker attribution errors and awkward literalism |
| Czech | 74.5 | Noticeable issues in fluency and naturalness |
| Indonesian | 74.1 | Inconsistent pronoun usage |
| Spanish | 73.9 | Missing speaker tags and duplicated lines |
| Portuguese | 73.8 | Severe structural and editing errors |
| Chinese | 73.8 | Structural redundancy causes repetition error |
| French | 73.6 | Missing speaker label for Luc |
| Polish | 73.1 | Missing speaker labels throughout |
| Macedonian | 73.0 | Structural inconsistencies and awkward phrasing |
| Romanian | 72.6 | Frequent absence of speaker labels |
| Korean | 72.5 | Awkward phrasing and dialogue formatting issues |
| Italian | 72.4 | Mixed language fragments and missing speaker tags |
| Catalan | 72.2 | Stiff and unnatural dialogue flow |
| Ukrainian | 72.2 | Critical structural and formatting errors |
| Albanian | 72.1 | Severe structural and formatting issues |
| Japanese | 71.7 | Repeated line and speaker attribution issues |
| Russian | 71.5 | Missing speaker tags |
| Tamil | 71.0 | Omitted dialogue lines break flow and attribution |
| Bulgarian | 70.8 | Severe speaker attribution errors |
| Basque | 70.7 | Significant fluency and grammatical issues |
| Finnish | 70.7 | Severe structural errors and duplications |
| Hindi | 70.3 | Structural and continuity errors |
| Slovak | 70.3 | Missing speaker labels disrupt dialogue |
| German | 70.2 | Formatting breakdown obscuring speaker attribution |
| Croatian | 69.7 | Missing speaker labels throughout |
| Mongolian | 69.5 | Severe formatting errors |
| Norwegian | 69.5 | Poor dialogue formatting and attribution |
| Persian | 69.4 | Duplicate lines regarding diffraction |
| Arabic | 69.1 | Mechanical errors and inconsistent speaker tags |
| Azerbaijani | 68.1 | Severe speaker attribution errors |
| Armenian | 68.0 | Major structural and coherence defects |
| Malay | 68.0 | Missing speaker tags and awkward phrasing |
| Dutch | 67.7 | Severe dialogue formatting defects |
| Georgian | 67.6 | Stiff and mechanically translated |
| Turkish | 67.5 | Missing and swapped speaker labels |
| Slovene | 67.3 | Missing speaker attributions and repetition |
| Galician | 67.1 | Significant fluency and naturalness issues with awkward phrasing |
| Belarusian | 67.0 | Omitted conversational fillers and unnatural phrasing |
| Marathi | 66.8 | Missing speaker attributions |
| Irish | 66.5 | Severe grammatical errors and inaccurate terminology |
| Bengali | 66.2 | Inconsistent pronouns and missing speaker labels |
| Vietnamese | 66.2 | Severe editing artifacts like duplicated lines and broken speaker attribution |
| Hebrew | 66.1 | Missing speaker tags and poor formatting |
| Lithuanian | 66.0 | Severe structural and formatting errors |
| Malayalam | 65.8 | Severe grammatical and lexical flaws |
| Nepali | 65.8 | Missing dialogue tags |
| Tagalog | 65.5 | Multiple grammatical errors and structural omissions |
| Welsh | 65.2 | Pervasive non-standard forms and phonetic approximations |
| Estonian | 65.0 | Severe dialogue attribution errors |
| Esperanto | 64.9 | Complete breakdown of dialogue attribution |
| Icelandic | 64.8 | Severely broken dialogue flow and unnatural syntax |
| Serbian | 64.5 | Structural glitches and repetition |
| Latvian | 64.2 | Complete breakdown of dialogue structure and speaker attribution |
| Sinhala | 64.0 | Significant fluency and naturalness issues |
| Hungarian | 63.2 | Missing speaker attributions |
| Kannada | 63.1 | Formatting issues and unnatural phrasing |
| Greek | 62.5 | Structural defects and unnatural physics terminology |
| Lao | 62.5 | Terminology errors and unnatural phrasing |
| Urdu | 62.2 | Stiff tone and literal idioms |
| Afrikaans | 62.0 | Missing speaker labels |
| Telugu | 61.6 | Awkward phrasing and imprecise terminology |
| Swahili | 61.4 | Inconsistent scientific terminology and unnatural phrasing |
| Interlingua | 56.8 | Severe lack of consistency and standard adherence |
