# examples/tr/onde/bonsai2-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: Ternary-Bonsai-2-27B-PTQ1_0 (ternary quantized Qwen 3.8 27B)
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 96 | Minor lexical inaccuracies and unnatural phrasing |
| Chinese | 93 | Minor terminology and phrasing adjustments needed |
| French | 91 | Minor inconsistencies and typos |
| Portuguese | 90 | Minor unlocalized English words like 'ripple' and 'stop' |
| Vietnamese | 81 | Presence of English word 'told' |
| Italian | 73 | Untranslated English phrase and typos |
| German | 59 | High frequency of grammatical errors and typos |
| Catalan | 58 | Persistent Spanish interference and false friends |
| Turkish | 58 | Severe grammatical errors and unnatural syntax |
| Malay | 53 | Major physics terminology errors and awkward phrasing |
| Polish | 50 | Severe grammatical errors and unnatural phrasing |
| Persian | 45 | Severe truncation and logical errors |
| Japanese | 44 | Mixed-language typos and abrupt truncation |
| Ukrainian | 40 | Severe errors and mixed-language artifacts |
| Galician | 36 | Heavy Portuguese/Spanish interference and lexical errors |
| Danish | 35 | Pervasive grammatical and lexical errors |
| Russian | 34 | Severe mixed-language intrusions and linguistic errors |
| Dutch | 32 | Severe truncation and mixed language errors |
| Swedish | 32 | Severe machine-translation artifacts and mixed language |
| Basque | 31 | Severe grammatical corruption and broken syntax |
| Hungarian | 31 | Severe errors and hallucinations |
| Bengali | 30 | Severe grammatical errors and mixed-language artifacts |
| Lithuanian | 30 | Severe grammatical and terminological errors |
| Nepali | 30 | Severe infinite text repetition loop |
| Malayalam | 29 | Severe grammatical corruption and incomprehensibility |
| Bulgarian | 28 | Severe mixed-language structural defects |
| Macedonian | 28 | Severe vocabulary errors and mixed language artifacts |
| Romanian | 28 | Severe structural fragmentation and untranslated text |
| Telugu | 28 | Severe grammatical errors and inaccurate technical translations |
| Urdu | 28 | Severe mistranslation of physics terms and fillers |
| Marathi | 27 | Severe linguistic and structural flaws |
| Norwegian | 27 | Severe lexical and grammatical errors |
| Belarusian | 24 | Severe grammatical and spelling errors |
| Hindi | 24 | Severe truncations and corrupted speaker names |
| Kannada | 23 | Severe structural and grammatical breakdown |
| Afrikaans | 21 | Heavy contamination with non-Afrikaans languages |
| Azerbaijani | 21 | Extensive structural corruption |
| Sinhala | 21 | Severe machine translation defects |
| Irish | 20 | Severe machine-translation artifacts and broken Irish grammar |
| Serbian | 20 | Pervasive errors and truncations |
| Tamil | 20 | Severe linguistic and technical failure |
| Tagalog | 19 | Critical structural and grammatical defects |
| Arabic | 18 | Structural collapse and mixed-language artifacts |
| Korean | 18 | severe mid-sentence truncations and code-mixing |
| Greek | 17 | Mixed language intrusions (Chinese, Korean, etc.) |
| Albanian | 17 | Pervasive grammatical errors and structural corruption |
| Latvian | 16 | Severe mixed-language corruption and structural defects |
| Khmer | 15 | Severe structural corruption and gibberish |
| Estonian | 13 | Catastrophic errors rendering it unintelligible |
| Icelandic | 13 | Severe lexical hallucination and grammatical collapse |
| Burmese | 12 | Massive character repetition loops |
| Esperanto | 11 | Catastrophic degradation and repetitive nonsense |
| Hebrew | 11 | Severe repetition loops and mixed-language fragments |
| Lao | 9 | Extensive repetition loops |
| Mongolian | 6 | Severe recursive repetition loops |
| Armenian | 5 | Severe lexical looping and grammatical collapse |
| Georgian | 5 | Catastrophic structural corruption and mixed-language artifacts |
| Czech | 0 | Severe truncation and broken formatting |
| Welsh | 0 | Severe corruption and repetition loops |
| Finnish | 0 | Missing Finnish translation |
| Croatian | 0 | Severe truncation and structural collapse |
| Interlingua | 0 | Critically incomplete and structurally broken |
| Indonesian | 0 | Severe structural corruption and missing content |
| Slovak | 0 | Truncated with repetitive speaker names |
| Slovene | 0 | Severe truncation and repetitive name dumping |
| Swahili | 0 | Critically incomplete with repetitive speaker names |
| Thai | 0 | Catastrophic corruption with repetitive garbage characters |
