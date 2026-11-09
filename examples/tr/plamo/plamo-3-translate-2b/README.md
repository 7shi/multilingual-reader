# examples/tr/plamo/plamo-3-translate-2b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: every language the [model card](https://huggingface.co/pfnet/plamo-3-translate-2b) lists as supported except the source English, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/). Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared only with the other models under [plamo/](../), on these languages ([PLAMO.md](../../PLAMO.md)).

The translations under `tr/` are outputs of PLaMo 3 Translate 2B (`plamo-3-translate-2b-Q4_K_M.gguf`), provided under the [PLaMo Community License](https://plamo.preferredai.jp/info/plamo-community-license-en).

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: PLaMo 3 Translate 2B Q4_K_M on `llama-server -c 32768 --jinja --no-prefill-assistant` (32,768 tokens, input and output combined, is the training length in the model card), reached through `OPENAI_BASE_URL`
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools plamo`), temperature 0, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

The other models translate line by line with summary and glossary messages (`trtools translate`). Those messages do not fit this model's chat template, which skips system messages and reads every user/assistant pair as a source/translation example, so the options go in its template variables instead. `zh` is sent as the model's `zh-hans`.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

The model is not meant to translate line by line, so its output is kept as it came, even where the lines no longer match the source's 99. Telugu skips about 40 lines of the middle, from the conservation of probability to the summary. Gujarati and Punjabi each skip 18 lines in the double-slit and Born-rule passage, Burmese 26 lines from the optics parallel to the Abbe limit, and Marathi and Malayalam 17 and 28 lines from the Abbe limit on; all of these end naturally. Khmer stops at the summary's line 83 in a loop repeating one word (`អំពី`, "about"), so the closing lines are missing. Vietnamese adds a line of its own (`Vì sao?`, "Why?"). The scores include these.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 90.5 | occasionally stiff phrasing |
| Dutch | 90.1 | Slightly mechanical phrasing of math notation |
| Chinese (Traditional) | 87.3 | Unnatural literal phrasing and filler retention |
| Chinese | 87.0 | Structural rigidity due to direct translation |
| Arabic | 85.9 | Noticeable stylistic awkwardness and translationese |
| Korean | 85.5 | Some parts feel slightly more "written" than "spoken" |
| French | 83.7 | Stylistic inconsistencies |
| Slovene | 82.3 | Noticeable fluency and grammatical inaccuracies |
| Serbian | 82.0 | Severe lexical error altering tone and register inconsistency |
| Uzbek | 81.6 | Inconsistent tone and unnatural phrasing |
| Georgian | 81.2 | Rigid syntactic structures mirror English patterns |
| German | 81.1 | Awkward phrasing and grammatical inaccuracies |
| Russian | 80.3 | Significant fluency issues and awkward phrasing |
| Catalan | 80.2 | Awkward phrasings and literalisms reduce fluency |
| Thai | 79.5 | Inconsistent polite particles |
| Swahili | 78.8 | Rigid literal syntax and grammatical errors |
| Croatian | 78.4 | Grammatical errors and unnatural phrasing |
| Spanish | 78.1 | Tonal and lexical inconsistencies |
| Estonian | 77.8 | Poor scientific terminology and unnatural phrasing |
| Malay | 76.8 | Unnatural phrasing and awkward literal translations |
| Japanese | 76.5 | Awkward phrasing and literal translations |
| Urdu | 76.4 | Critical lexical error "flesh" and fluency issues |
| Lithuanian | 76.3 | Severe grammatical and syntactic defects |
| Persian | 76.2 | Inconsistent notation and wrong term |
| Polish | 74.2 | Confusing speaker attribution |
| Indonesian | 73.9 | Terminological inaccuracies and unnatural phrasing |
| Vietnamese | 73.6 | Orphaned phrase and grammatical errors |
| Kazakh | 73.0 | Awkward literalism and tone inconsistencies |
| Nepali | 73.0 | Inconsistent tone and register |
| Bulgarian | 72.7 | Significant grammatical and fluency issues |
| Belarusian | 72.5 | Severe grammatical and terminology errors |
| Hindi | 72.3 | Critical physics error: Lambda/2 mistranslated as lambda times 2 |
| Armenian | 72.0 | Technical terminology errors and awkward phrasing |
| Tamil | 71.9 | Overly literal and stilted phrasing |
| Cebuano | 69.4 | Awkward phrasing and terminology accuracy |
| Bengali | 69.0 | Severe typographical and orthographic errors |
| Gujarati | 68.8 | Critical mistranslation of scientific terminology like lambda and Abbe |
| Hebrew | 68.4 | Significant scientific terminology errors and grammatical issues |
| Javanese | 68.2 | Inconsistent register and orthography |
| Latvian | 68.2 | Severe grammatical and terminology errors |
| Hungarian | 67.4 | Persistent mechanical errors and awkward phrasing |
| Sinhala | 66.7 | Severe linguistic errors and awkward phrasing |
| Azerbaijani | 66.3 | Persistent grammatical and transliteration errors |
| Basque | 65.2 | Severe grammatical and syntax errors |
| Tagalog | 63.5 | Severe linguistic and stylistic flaws |
| Punjabi | 63.3 | Significant linguistic and terminology errors |
| Marathi | 59.3 | Severe speaker dialogue swapping |
| Slovak | 58.4 | Severe structural and linguistic errors |
| Khmer | 54.4 | Severe truncation and catastrophic repetition errors |
| Malayalam | 53.4 | Incomplete final dialogue segment |
| Burmese | 51.4 | Speaker misattribution |
| Telugu | 50.6 | Severe content loss and structural breakdown |
