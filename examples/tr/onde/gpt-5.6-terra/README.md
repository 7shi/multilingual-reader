# examples/tr/onde/gpt-5.6-terra/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: gpt-5.6-terra
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Russian | 91.5 | Register consistency |
| Latvian | 90.8 | Minor stylistic rigidity in colloquial exchanges |
| Persian | 90.6 | Subtle stylistic nuances |
| Macedonian | 90.6 | Swapped speaker names in one exchange |
| Ukrainian | 90.2 | Minor stylistic awkwardness in gendered terms and flow |
| Belarusian | 88.8 | Occasional literal phrasing reduces fluency |
| Japanese | 88.4 | Minor speaker name inconsistency |
| Nepali | 84.0 | Lacks naturalness and idiomatic fluency |
| Bengali | 83.0 | Awkward phrasing and stiff dialogue |
| Hebrew | 81.9 | Inconsistent transliteration of "Luc" |
| Basque | 81.6 | Intrusive meta-commentary artifacts |
| Malayalam | 81.4 | Translationese style disrupts naturalness |
| Thai | 80.7 | Mixed-language script errors |
| Czech | 80.2 | Mixed-language meta-commentary |
| Georgian | 80.0 | Reads rigidly and literally |
| Urdu | 79.8 | Rigid literal sentence structure |
| German | 79.7 | Awkward fragmented sentences and literal phrasing |
| Burmese | 79.7 | Slightly stiff phrasing |
| Greek | 79.4 | Mechanical errors and typos |
| Slovene | 78.8 | Imprecise physics terminology like delček |
| Marathi | 77.5 | Incomplete proofreading of transliterated names |
| Bulgarian | 77.2 | Critical corrupted text encoding error |
| Danish | 77.0 | Literal phrasing and visible meta-commentary disrupt flow |
| Armenian | 77.0 | Stiff phrasing and punctuation issues |
| Kannada | 76.9 | Inconsistent technical terminology |
| Portuguese | 76.0 | Speaker name typo and stiff phrasing |
| Serbian | 75.7 | Hallucinated character name |
| Italian | 75.2 | Mixed language artifacts and typos |
| Estonian | 74.9 | Unexplained Georgian script insertion |
| Romanian | 74.8 | Accidental insertion of English labels into the Romanian text |
| Slovak | 74.5 | Severe text generation glitches and awkward phrasing |
| Galician | 74.3 | Unreadable mixed-language text and typos |
| French | 74.2 | severe formatting breaks and omissions |
| Spanish | 74.0 | Missing dialogue and name typos |
| Hindi | 74.0 | Mixed-language fragments and formatting errors |
| Khmer | 73.7 | Inconsistent speaker attribution |
| Polish | 73.6 | Unexplained meta-tags and untranslated English |
| Albanian | 73.6 | Contains non-Albanian text fragment |
| Catalan | 73.3 | Structural defects and corrupted text |
| Esperanto | 73.3 | Significant mechanical and editing errors |
| Tamil | 72.8 | Intrusive Bengali script fragment |
| Vietnamese | 72.8 | Missing dialogue lines and translator notes |
| Lao | 72.7 | Untranslated meta-commentary interrupts dialogue |
| Indonesian | 72.5 | Corrupted text fragments disrupt readability |
| Dutch | 72.5 | Severe artifact insertion breaking fluency |
| Arabic | 71.8 | Missing segment and meta-text |
| Icelandic | 71.8 | Mixed language artifacts and broken dialogue tags |
| Telugu | 71.8 | Stiff phrasing and fluency issues |
| Norwegian | 71.7 | Severe structural integrity issues with mixed artifacts |
| Afrikaans | 71.5 | Untranslated English sentence inserted |
| Chinese | 71.5 | Inexplicable machine-generated glitches in speaker labels |
| Welsh | 71.4 | Critical data corruption (spam insertion) and grammatical inaccuracies |
| Turkish | 71.4 | System glitch artifact present |
| Azerbaijani | 71.2 | Insertion of non-translational instructions |
| Lithuanian | 71.2 | Occasional awkward phrasing and typo |
| Swedish | 71.1 | Severe mechanical errors and mixed-language intrusion |
| Hungarian | 70.8 | Major typographical error with character name |
| Finnish | 70.6 | Code snippets and formatting errors |
| Korean | 70.1 | Mixed-language fragments disrupt fluency |
| Irish | 69.8 | Untranslated English fragments and awkward grammar |
| Swahili | 69.7 | Consistency errors and terminology issues |
| Mongolian | 69.3 | Significant issues in fluency, naturalness, and consistency |
| Malay | 69.2 | Disruptive code artifacts and speaker tag errors |
| Sinhala | 69.1 | Corrupted encoding artifacts and poor linguistic quality |
| Tagalog | 68.2 | Persistent spelling errors |
| Croatian | 66.7 | Untranslated meta-commentary and English fragments remain |
| Interlingua | 63.4 | Mixed language contamination and truncations |
