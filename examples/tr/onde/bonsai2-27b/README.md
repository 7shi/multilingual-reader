# examples/tr/onde/bonsai2-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: Ternary-Bonsai-2-27B-PTQ1_0 (ternary quantized Qwen 3.8 27B)
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Chinese | 89.6 | Occasional slight stiffness in phrasing |
| French | 82.1 | Inconsistent use of tu and vous |
| Spanish | 81.9 | Awkward phrasings and calques from English source structure |
| Portuguese | 78.3 | Lexical error: untranslated English word "ripple" |
| Italian | 77.2 | Untranslated English fragments |
| Vietnamese | 76.2 | Mixed-language error in Luc's first sentence |
| Malay | 71.7 | Inconsistent register and mistranslated technical terms |
| Polish | 71.7 | Significant mechanical errors |
| German | 68.2 | Severe grammatical and lexical errors |
| Catalan | 68.1 | Severe grammatical errors and lack of fluency |
| Ukrainian | 67.8 | Severe grammar errors and mixed-language corruption |
| Swedish | 64.4 | Mixed languages and severe grammatical errors |
| Galician | 62.0 | Intrusion of non-Galician elements and severe grammatical errors |
| Turkish | 61.4 | Severe terminological errors and malformed vocabulary |
| Russian | 61.3 | Severe mixed-language defects and incomplete translation |
| Japanese | 57.9 | Fatal truncation and mixed-language errors |
| Urdu | 57.5 | Severe terminology and grammatical errors |
| Bulgarian | 56.8 | Severe mixed-language artifacts and Chinese characters |
| Norwegian | 55.9 | Severe grammatical breakdowns and nonsense |
| Danish | 54.8 | Severe grammatical errors and unnatural phrasing |
| Lithuanian | 54.8 | Catastrophic linguistic and semantic failure |
| Nepali | 53.7 | Corrupted text with nonsensical repetition |
| Persian | 52.2 | Severe content omissions and grammatical errors |
| Dutch | 46.7 | Catastrophic truncation and mixed-language artifacts |
| Romanian | 46.7 | Severe incoherence and terminology failures |
| Macedonian | 45.7 | Severe lexical hallucinations and grammatical collapse |
| Basque | 43.8 | Catastrophic lexical errors and hallucinations |
| Marathi | 43.8 | severe language mixing and grammatical errors |
| Serbian | 43.6 | Severely flawed and unintelligible translation |
| Afrikaans | 43.2 | Severe mixed-language contamination and untranslated segments |
| Bengali | 42.9 | Severe linguistic degradation and mixed languages |
| Hungarian | 42.5 | Grammatical and syntactic collapse |
| Hindi | 42.0 | Severe structural and linguistic failures |
| Tagalog | 41.6 | Catastrophic grammatical errors and mixed languages |
| Tamil | 41.0 | Severe lexical hallucinations and nonsense |
| Telugu | 40.9 | Pervasive nonsense words |
| Belarusian | 40.1 | Severe grammatical and lexical errors |
| Arabic | 38.4 | Mixed Chinese characters and severe fragmentation |
| Kannada | 35.9 | Severe grammatical and terminology errors |
| Sinhala | 35.9 | Complete failure of meaning and grammar |
| Latvian | 35.7 | Mixed language artifacts and severe grammatical errors |
| Greek | 35.2 | Severe code-switching with Chinese and Russian |
| Albanian | 33.7 | Severe grammatical errors and lexical hallucinations |
| Estonian | 32.0 | Severe grammatical and hallucinatory defects |
| Azerbaijani | 31.1 | Massive nonsensical repetition |
| Khmer | 30.7 | Extensive corruption and severe grammatical errors |
| Indonesian | 30.6 | Mechanical repetition of dialogue tags with missing content |
| Korean | 30.1 | Collapsed into gibberish |
| Hebrew | 29.7 | Pervasive severe lexical and grammatical errors |
| Irish | 28.0 | Severe machine translation errors and nonsensical gibberish |
| Malayalam | 26.9 | Completely unintelligible gibberish |
| Icelandic | 26.7 | Incomprehensible and nonsensical gibberish |
| Czech | 26.1 | Severe truncation and repetitive loops cause massive information loss |
| Croatian | 25.6 | Catastrophic incompleteness and gibberish |
| Interlingua | 23.4 | Severe incompleteness and structural breakdown |
| Slovak | 23.0 | Catastrophic failure and non-existent translation |
| Burmese | 21.2 | Utterly unintelligible due to severe errors |
| Slovene | 18.4 | Complete content loss due to truncation |
| Esperanto | 15.3 | Severe gibberish and nonsense repetition throughout |
| Lao | 15.0 | Severely defective and incomprehensible |
| Swahili | 14.4 | Severe structural defects and incomplete translation |
| Mongolian | 13.6 | Severe degradation and infinite repetition loops |
| Thai | 12.6 | Catastrophic failure with severe structural defects and garbage data |
| Georgian | 9.3 | Completely unintelligible and corrupted nonsense |
| Armenian | 7.0 | Complete loss of meaning and grammatical nonsense |
| Finnish | 5.6 | Structurally broken and meaningless |
| Welsh | 3.4 | Extensive meaningless repetition and word salad |
