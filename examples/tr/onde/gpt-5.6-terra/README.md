# examples/tr/onde/gpt-5.6-terra/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gpt-5.6-terra
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Russian | 90.2 | Register consistency |
| Ukrainian | 90.1 | Minor stylistic awkwardness in gendered terms and flow |
| Persian | 90.0 | Subtle stylistic nuances |
| Macedonian | 89.5 | Swapped speaker names in one exchange |
| Latvian | 88.4 | Minor stylistic rigidity in colloquial exchanges |
| Belarusian | 87.7 | Occasional literal phrasing reduces fluency |
| German | 86.7 | Awkward fragmented sentences and literal phrasing |
| Portuguese | 84.5 | Speaker name typo and stiff phrasing |
| Nepali | 84.3 | Lacks naturalness and idiomatic fluency |
| Japanese | 84.1 | Minor speaker name inconsistency |
| Hebrew | 84.0 | Inconsistent transliteration of "Luc" |
| Malayalam | 83.9 | Translationese style disrupts naturalness |
| Thai | 83.9 | Mixed-language script errors |
| Czech | 82.6 | Mixed-language meta-commentary |
| Georgian | 81.9 | Reads rigidly and literally |
| Bengali | 81.7 | Awkward phrasing and stiff dialogue |
| Marathi | 81.7 | Incomplete proofreading of transliterated names |
| Greek | 81.6 | Mechanical errors and typos |
| Slovene | 81.6 | Imprecise physics terminology like delček |
| Urdu | 81.1 | Rigid literal sentence structure |
| Basque | 80.0 | Intrusive meta-commentary artifacts |
| Bulgarian | 79.2 | Critical corrupted text encoding error |
| Estonian | 79.2 | Unexplained Georgian script insertion |
| Burmese | 79.2 | Slightly stiff phrasing |
| Italian | 78.9 | Mixed language artifacts and typos |
| Afrikaans | 78.8 | Untranslated English sentence inserted |
| Arabic | 78.3 | Missing segment and meta-text |
| Spanish | 78.3 | Missing dialogue and name typos |
| French | 78.3 | severe formatting breaks and omissions |
| Armenian | 78.3 | Stiff phrasing and punctuation issues |
| Indonesian | 78.2 | Corrupted text fragments disrupt readability |
| Galician | 78.1 | Unreadable mixed-language text and typos |
| Danish | 77.8 | Literal phrasing and visible meta-commentary disrupt flow |
| Romanian | 77.3 | Accidental insertion of English labels into the Romanian text |
| Norwegian | 77.2 | Severe structural integrity issues with mixed artifacts |
| Albanian | 76.6 | Contains non-Albanian text fragment |
| Polish | 76.3 | Unexplained meta-tags and untranslated English |
| Lithuanian | 76.0 | Occasional awkward phrasing and typo |
| Dutch | 76.0 | Severe artifact insertion breaking fluency |
| Slovak | 75.8 | Severe text generation glitches and awkward phrasing |
| Vietnamese | 75.8 | Missing dialogue lines and translator notes |
| Serbian | 75.5 | Hallucinated character name |
| Khmer | 75.2 | Inconsistent speaker attribution |
| Esperanto | 75.0 | Significant mechanical and editing errors |
| Catalan | 74.7 | Structural defects and corrupted text |
| Tamil | 74.7 | Intrusive Bengali script fragment |
| Turkish | 74.0 | System glitch artifact present |
| Chinese | 74.0 | Inexplicable machine-generated glitches in speaker labels |
| Hungarian | 73.8 | Major typographical error with character name |
| Finnish | 73.7 | Code snippets and formatting errors |
| Azerbaijani | 73.4 | Insertion of non-translational instructions |
| Hindi | 73.2 | Mixed-language fragments and formatting errors |
| Swedish | 73.2 | Severe mechanical errors and mixed-language intrusion |
| Icelandic | 73.1 | Mixed language artifacts and broken dialogue tags |
| Welsh | 72.8 | Critical data corruption (spam insertion) and grammatical inaccuracies |
| Malay | 72.8 | Disruptive code artifacts and speaker tag errors |
| Kannada | 72.7 | Inconsistent technical terminology |
| Lao | 72.3 | Untranslated meta-commentary interrupts dialogue |
| Irish | 72.0 | Untranslated English fragments and awkward grammar |
| Mongolian | 71.7 | Significant issues in fluency, naturalness, and consistency |
| Sinhala | 71.3 | Corrupted encoding artifacts and poor linguistic quality |
| Korean | 71.1 | Mixed-language fragments disrupt fluency |
| Swahili | 71.1 | Consistency errors and terminology issues |
| Tagalog | 70.0 | Persistent spelling errors |
| Croatian | 68.3 | Untranslated meta-commentary and English fragments remain |
| Interlingua | 67.0 | Mixed language contamination and truncations |
| Telugu | 65.8 | Stiff phrasing and fluency issues |
