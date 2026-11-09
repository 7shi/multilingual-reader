# examples/tr/plamo/gemma4-31b/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gemma4-31b/](../../onde/gemma4-31b/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:31b-it-qat on Ollama, its context set to 32,768 tokens (`OLLAMA_CONTEXT_LENGTH=32768`), as for PLaMo, since the whole text and its translation go in one request
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), no CoT (`--no-think`) and Ollama's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/gemma4-31b/](../../onde/gemma4-31b/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language and kept the source's 99 lines in every one, with no line skipped, repeated, split or joined.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 93.9 | No significant shortcoming |
| Spanish | 93.8 | Lexical error: "ingenuidad" instead of "ingenio" |
| German | 92.3 | Minor literal translation issues |
| Russian | 92.3 | Slightly literal phrasing |
| Italian | 91.0 | Occasionally literal phrasing rather than fully idiomatic prose |
| Chinese (Traditional) | 90.5 | Minor phrasing stiffness |
| Japanese | 90.0 | Stylistic inconsistencies |
| Vietnamese | 89.7 | Retains literalness hindering naturalness |
| Chinese | 89.4 | Slightly rigid sentence structure |
| Persian | 89.1 | Awkward filler words and unnatural phrasing |
| Indonesian | 89.0 | Rigid sentence structure reduces naturalness |
| Polish | 89.0 | Slightly literal phrasing and tonal mismatch |
| Korean | 88.0 | Slight stiffness in idiomatic expressions |
| Arabic | 87.5 | Slightly rigid or literal syntax mirrors English |
| Thai | 87.0 | Occasional slight stiffness in sentence structures |
| Gujarati | 85.5 | Persistent use of informal 'you' forms |
| Dutch | 84.2 | Noticeable "translationese" quality |
| Croatian | 84.1 | Noticeable translationese |
| Malay | 84.0 | Translation-heavy and mechanically derived |
| Uzbek | 82.2 | Grammatical errors and awkward phrasing |
| Javanese | 81.6 | Struggles with fluency and naturalness |
| Bengali | 81.2 | Persistent typographical errors |
| Hebrew | 80.0 | Major lexical error and awkward phrasing |
| Catalan | 79.5 | Anglicisms and spelling errors |
| Swahili | 79.1 | Inconsistent register and code-switching |
| Burmese | 78.8 | inconsistent name transliteration |
| Serbian | 78.7 | Broken text and typos |
| Azerbaijani | 78.6 | Lacks fluency and naturalness |
| Marathi | 78.3 | Excessive English and German insertions |
| Hindi | 77.4 | Language mixing and awkward phrasing |
| Urdu | 77.3 | Fluent and natural style lacking due to translationese tone |
| Telugu | 76.2 | Language mixing disrupts fluency |
| Nepali | 75.2 | Consistent wrong speaker labels |
| Sinhala | 75.0 | Severe mixed script interference |
| Bulgarian | 73.8 | Inclusion of Russian words and unnatural phrasing |
| Tamil | 73.1 | Foreign script errors and stiff fluency |
| Slovak | 72.7 | Foreign character intrusion and grammatical errors |
| Cebuano | 71.3 | Awkward phrasing and inconsistent terminology |
| Armenian | 70.7 | Raw English fragments and terminology inaccuracies |
| Slovene | 68.0 | Severe foreign language intrusion and gross errors |
| Tagalog | 67.8 | Translationese and inconsistent terminology |
| Kazakh | 67.3 | Mixed languages and untranslated terms |
| Punjabi | 65.3 | Untranslated English words and Hindi script |
| Belarusian | 64.6 | Catastrophic terminology and lexical errors |
| Malayalam | 60.6 | Severe linguistic contamination with Hindi and English |
| Lithuanian | 58.8 | Severe structural and grammatical errors |
| Hungarian | 58.7 | Severe code-switching and terminology errors |
| Estonian | 55.5 | Severe mixed-language contamination |
| Latvian | 53.4 | Severe grammatical errors and non-existent vocabulary |
| Georgian | 50.2 | Extensive mixed-language code-switching |
| Khmer | 50.0 | Severe mixed-language contamination |
| Basque | 47.5 | Severe foreign language intrusion |
