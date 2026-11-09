# examples/tr/plamo/qwen3.8-flash-next/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/qwen3.8-flash-next/](../../onde/qwen3.8-flash-next/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S (125B-A6B MoE with 51B of n-gram embeddings, GSQ-RCO quantized, run with Strata), its context set to 32,768 tokens, as for PLaMo, since the whole text and its translation go in one request
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), no CoT (`--no-think`) and the server's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/qwen3.8-flash-next/](../../onde/qwen3.8-flash-next/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model kept the source's 99 lines in every language, with no line skipped, repeated, split or joined, and translated every language into the target language, but English is left in some of them:

- **Russian**: leaves Luc's closing remark on line 88 in English ("Fascinating to see how all these concepts…").
- **Bulgarian**: leaves some English words in, such as "perfectly" and "psi squared", and the same remark on line 88 ("Fascinating", written with a Cyrillic first letter); it also keeps the speaker names Camille and Luc in Latin script.
- **Chinese**: leaves English words in, such as "necessarily" on line 45 and the spelled-out "delta x", "lambda over two".

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 93.5 | Minor idiom issues but technically precise |
| Spanish | 90.8 | Literal phrasing lacks fluency |
| Italian | 90.7 | Retains a "translated" feel |
| Vietnamese | 89.1 | Minor stylistic issues and awkward phrasing |
| German | 89.0 | Minor stiffness and literal phrasing |
| Lithuanian | 88.3 | Occasional stiff phrasing and inconsistent dialogue markers |
| Croatian | 88.2 | Fluent and natural dialogue phrasing |
| Polish | 88.1 | Slightly rigid phrasing and unnatural filler words |
| Japanese | 88.0 | Glaring Chinese character intrusion |
| Korean | 87.9 | Occasional stiff and literal phrasing |
| Slovak | 87.8 | Slightly stiff dialogue and non-idiomatic phrasing |
| Serbian | 86.9 | Slight translationese and awkward phrasing |
| Indonesian | 86.6 | Stiff and literal phrasing |
| Hungarian | 86.4 | Slight stiffness in phrasing prevents natural fluency |
| Slovene | 86.3 | Pervasive preposition misuse |
| Estonian | 85.5 | Awkward physics terminology and unnatural phrasing |
| Persian | 85.5 | Stiff literal calques |
| Catalan | 83.9 | Issues in fluency and naturalness |
| Uzbek | 83.9 | Literal calques from English |
| Dutch | 83.8 | Noticeable Spanish word insertion |
| Hindi | 83.0 | Awkward phrasing and unnatural sentence structures |
| Armenian | 83.0 | Translationese and unnatural phrasing |
| Latvian | 82.5 | Awkward literal translation |
| Hebrew | 81.6 | Mistranslation of "probability of presence" as "probability of reality" |
| Chinese (Traditional) | 81.6 | Lacks fluency and naturalness |
| Belarusian | 81.4 | Inconsistent orthography mixing Karastenka and Taraskievica |
| Chinese | 81.2 | Mixed-language proofreading error |
| Thai | 81.1 | Unnatural phrasing and awkward flow |
| Swahili | 80.9 | Unnatural phrasing and poor idiomatic adaptation |
| Arabic | 80.7 | Literalism and awkward phrasing |
| Bengali | 79.7 | Awkward phrasing and stiff connectives |
| Nepali | 79.7 | Stiff literal translationese |
| Azerbaijani | 79.4 | Lexical and grammatical errors |
| Tamil | 76.8 | Stiff literal syntax lacking natural flow |
| Javanese | 76.3 | Indonesian-influenced syntax and vocabulary |
| Russian | 76.3 | Direct insertion of an English sentence into Russian text |
| Gujarati | 76.1 | Translationese disrupting natural fluency |
| Khmer | 75.8 | Calque effects reduce fluency and naturalness |
| Tagalog | 75.5 | Unnatural phrasing and syntax |
| Punjabi | 75.0 | Literalness and awkward phrasing |
| Basque | 74.5 | Significant fluency and grammatical errors disrupt readability |
| Urdu | 74.0 | Inconsistent style and awkward phrasing |
| Kazakh | 73.8 | Stiff phrasing and mistranslations |
| Georgian | 72.9 | Significant linguistic flaws and unnatural phrasing |
| Malayalam | 72.7 | Significant grammatical errors |
| Sinhala | 72.2 | Notable fluency and naturalness issues |
| Bulgarian | 72.0 | Untranslated English words and phrases |
| Marathi | 68.9 | Significant terminology misuse and grammatical inaccuracies |
| Malay | 64.0 | Overuse of English terms |
| Telugu | 63.8 | Pervasive grammatical errors and unnatural phrasing |
| Burmese | 62.7 | Severe mistranslation of key terms and poor flow |
| Cebuano | 61.8 | Severe fluency and semantic errors |
