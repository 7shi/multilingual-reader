# examples/tr/onde/plamo-3-translate-0.8b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: every language the [model card](https://huggingface.co/pfnet/plamo-3-translate-0.8b) lists as supported except the source English, set in the [Makefile](Makefile). Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. The comparison with other models cuts them and counts the corpus languages missing here as 0. A first run over every corpus language is kept in [experimental/16](../../../../experimental/16/): outside the list, the translations came out in another language, mixed or collapsed.

The translations under `tr/` are outputs of PLaMo 3 Translate 0.8B (`plamo-3-translate-0.8b-Q4_K_M.gguf`), provided under the [PLaMo Community License](https://plamo.preferredai.jp/info/plamo-community-license-en).

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: PLaMo 3 Translate 0.8B Q4_K_M on `llama-server -c 32768 --jinja --no-prefill-assistant` (32,768 tokens, input and output combined, is the training length in the model card), reached through `OPENAI_BASE_URL`
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools plamo`), temperature 0, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

The other models translate line by line with summary and glossary messages (`trtools translate`). Those messages do not fit this model's chat template, which skips system messages and reads every user/assistant pair as a source/translation example, so the options go in its template variables instead. `zh` is sent as the model's `zh-hans`.

The seven languages outside the corpus have no column in the term TSV yet, so they were translated without a glossary; columns for them are planned ([PLAMO.md](../../PLAMO.md)).

The model is not meant to translate line by line, so its output is kept as it came, even where the lines no longer match the source's 99: Burmese and Punjabi skip a long stretch of the dialogue and end naturally, Gujarati translates the closing passage early and repeats two of its lines, Kazakh, Telugu, and Sinhala end in a loop repeating one phrase, and Armenian splits a line. The scores include these.

The language check left Serbian and Traditional Chinese for review, and both were settled as in the target language (`langcheck-resolved.jsonl`): the Serbian is in Latin script with some Croatian forms (`točno`, `što`), and the Traditional Chinese uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 78.5 | Notable grammatical and lexical errors |
| Vietnamese | 77.2 | Inconsistent tone and awkward phrasing |
| Spanish | 77.0 | Awkward phrasing and grammatical errors |
| Hungarian | 76.5 | Significant grammatical and stylistic issues |
| Indonesian | 74.3 | Awkward and unnatural phrasing |
| French | 73.2 | Lexical errors and unnatural phrasing |
| Malay | 73.1 | Severe terminology and syntax errors |
| Javanese | 72.7 | Severe lexical errors and non-existent words |
| Dutch | 71.8 | No shortcoming mentioned |
| Georgian | 71.7 | Significant fluency and syntax issues |
| Chinese (Traditional) | 70.7 | Notable technical slip-up and linguistic stiffness |
| Japanese | 70.1 | Scientifically incorrect Abbe limit definition |
| Swahili | 69.7 | Significant scientific terminology errors and mistranslation of key concepts like "coherent" as "interaction" |
| Arabic | 69.0 | High frequency of errors |
| Thai | 68.6 | Catastrophic gender consistency and speaker role swapping |
| Cebuano | 68.2 | Fluent mixing of English and Cebuano |
| Croatian | 67.7 | Severe grammatical and terminology errors |
| Chinese | 67.5 | Lacks fluency and natural flow |
| Korean | 67.4 | Critical physics terminology errors |
| Catalan | 66.6 | Mixes multiple languages with severe physics terminology errors |
| Serbian | 66.5 | Severe linguistic failures and grammatical errors |
| German | 65.5 | Pervasive grammatical flaws and unnatural phrasing |
| Polish | 65.4 | Severe physics terminology and grammar errors |
| Hindi | 64.5 | Severe technical and grammatical errors |
| Khmer | 63.8 | Inconsistent terminology and awkward phrasing |
| Nepali | 62.8 | Critical speaker attribution errors and technical inaccuracies |
| Slovene | 60.8 | Pervasive grammatical and terminology errors |
| Marathi | 60.1 | Critical mistranslation of "matter" as "India" |
| Urdu | 59.2 | Inaccurate technical terminology and poor grammar |
| Azerbaijani | 57.5 | Severe errors and non-Azerbaijani characters |
| Bengali | 57.1 | Catastrophic lexical and grammatical failures |
| Hebrew | 57.0 | Systematic lexical errors and gibberish |
| Russian | 56.8 | Severe linguistic degradation and multiple errors |
| Bulgarian | 56.6 | Pervasive grammatical and terminological errors |
| Slovak | 55.1 | Non-existent words and severe grammatical errors |
| Latvian | 54.1 | Severe grammatical and vocabulary errors |
| Tamil | 53.8 | Pervasive grammatical errors and syntactic awkwardness |
| Armenian | 53.4 | Severe linguistic unnaturalness and mechanical errors |
| Tagalog | 52.0 | Severe grammatical errors and Taglish mixing |
| Lithuanian | 51.9 | Catastrophic terminology errors |
| Belarusian | 51.8 | Severe lexical and grammatical errors throughout |
| Basque | 51.5 | Severe grammatical and semantic errors |
| Uzbek | 51.5 | Severe spelling and terminology errors |
| Estonian | 51.0 | Severe structural and lexical failures |
| Persian | 50.6 | Severe physics terminology errors and hallucinations |
| Gujarati | 49.5 | Severe terminology errors and hallucinations |
| Burmese | 40.7 | Severe incompleteness and logical gaps |
| Malayalam | 40.1 | Severe hallucination and repetition |
| Punjabi | 39.0 | Severe terminology and structural errors |
| Telugu | 38.4 | Abruptly cuts off with repetitive nonsense |
| Kazakh | 35.6 | Severe repetition errors leading to gibberish |
| Sinhala | 33.4 | Incomplete and inaccurate with many errors |
