# examples/tr/onde/bonsai2-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: Ternary-Bonsai-2-27B-PTQ1_0 (ternary quantized Qwen 3.8 27B)
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Chinese | 90.2 | Occasional slight stiffness in phrasing |
| Spanish | 79.7 | Awkward phrasings and calques from English source structure |
| French | 78.7 | Inconsistent use of tu and vous |
| Portuguese | 77.5 | Lexical error: untranslated English word "ripple" |
| Vietnamese | 75.0 | Mixed-language error in Luc's first sentence |
| Italian | 74.8 | Untranslated English fragments |
| Polish | 73.4 | Significant mechanical errors |
| Malay | 70.6 | Inconsistent register and mistranslated technical terms |
| German | 67.8 | Severe grammatical and lexical errors |
| Catalan | 67.0 | Severe grammatical errors and lack of fluency |
| Ukrainian | 65.3 | Severe grammar errors and mixed-language corruption |
| Swedish | 65.1 | Mixed languages and severe grammatical errors |
| Galician | 63.1 | Intrusion of non-Galician elements and severe grammatical errors |
| Russian | 58.9 | Severe mixed-language defects and incomplete translation |
| Turkish | 58.9 | Severe terminological errors and malformed vocabulary |
| Japanese | 55.1 | Fatal truncation and mixed-language errors |
| Danish | 53.3 | Severe grammatical errors and unnatural phrasing |
| Norwegian | 53.0 | Severe grammatical breakdowns and nonsense |
| Urdu | 51.7 | Severe terminology and grammatical errors |
| Persian | 51.5 | Severe content omissions and grammatical errors |
| Bulgarian | 49.8 | Severe mixed-language artifacts and Chinese characters |
| Lithuanian | 49.5 | Catastrophic linguistic and semantic failure |
| Nepali | 49.3 | Corrupted text with nonsensical repetition |
| Dutch | 47.2 | Catastrophic truncation and mixed-language artifacts |
| Macedonian | 43.0 | Severe lexical hallucinations and grammatical collapse |
| Bengali | 42.3 | Severe linguistic degradation and mixed languages |
| Romanian | 41.9 | Severe incoherence and terminology failures |
| Hungarian | 40.7 | Grammatical and syntactic collapse |
| Telugu | 40.4 | Pervasive nonsense words |
| Marathi | 40.2 | severe language mixing and grammatical errors |
| Basque | 40.0 | Catastrophic lexical errors and hallucinations |
| Hindi | 39.6 | Severe structural and linguistic failures |
| Tamil | 38.8 | Severe lexical hallucinations and nonsense |
| Arabic | 38.5 | Mixed Chinese characters and severe fragmentation |
| Tagalog | 37.6 | Catastrophic grammatical errors and mixed languages |
| Belarusian | 37.5 | Severe grammatical and lexical errors |
| Afrikaans | 37.2 | Severe mixed-language contamination and untranslated segments |
| Serbian | 36.8 | Severely flawed and unintelligible translation |
| Kannada | 34.6 | Severe grammatical and terminology errors |
| Latvian | 33.8 | Mixed language artifacts and severe grammatical errors |
| Sinhala | 32.5 | Complete failure of meaning and grammar |
| Greek | 31.2 | Severe code-switching with Chinese and Russian |
| Indonesian | 30.7 | Mechanical repetition of dialogue tags with missing content |
| Estonian | 30.1 | Severe grammatical and hallucinatory defects |
| Korean | 29.4 | Collapsed into gibberish |
| Azerbaijani | 28.6 | Massive nonsensical repetition |
| Albanian | 28.0 | Severe grammatical errors and lexical hallucinations |
| Croatian | 26.6 | Catastrophic incompleteness and gibberish |
| Irish | 26.5 | Severe machine translation errors and nonsensical gibberish |
| Hebrew | 26.2 | Pervasive severe lexical and grammatical errors |
| Malayalam | 26.0 | Completely unintelligible gibberish |
| Khmer | 25.6 | Extensive corruption and severe grammatical errors |
| Icelandic | 24.4 | Incomprehensible and nonsensical gibberish |
| Czech | 23.7 | Severe truncation and repetitive loops cause massive information loss |
| Interlingua | 18.1 | Severe incompleteness and structural breakdown |
| Burmese | 17.9 | Utterly unintelligible due to severe errors |
| Slovak | 17.1 | Catastrophic failure and non-existent translation |
| Slovene | 14.9 | Complete content loss due to truncation |
| Esperanto | 14.8 | Severe gibberish and nonsense repetition throughout |
| Lao | 13.4 | Severely defective and incomprehensible |
| Thai | 13.3 | Catastrophic failure with severe structural defects and garbage data |
| Mongolian | 11.7 | Severe degradation and infinite repetition loops |
| Swahili | 9.6 | Severe structural defects and incomplete translation |
| Georgian | 8.1 | Completely unintelligible and corrupted nonsense |
| Armenian | 6.7 | Complete loss of meaning and grammatical nonsense |
| Finnish | 3.8 | Structurally broken and meaningless |
| Welsh | 2.6 | Extensive meaningless repetition and word salad |
