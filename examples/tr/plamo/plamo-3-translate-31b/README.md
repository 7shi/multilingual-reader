# examples/tr/plamo/plamo-3-translate-31b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: every language the [model card](https://huggingface.co/pfnet/plamo-3-translate-31b) lists as supported except the source English, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/). Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared only with the other models under [plamo/](../), on these languages ([PLAMO.md](../../PLAMO.md)).

The translations under `tr/` are outputs of PLaMo 3 Translate 31B (`plamo-3-translate-31b-Q4_K_M.gguf`), provided under the [PLaMo Community License](https://plamo.preferredai.jp/info/plamo-community-license-en).

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: PLaMo 3 Translate 31B Q4_K_M on `llama-server -c 32768 --jinja --no-prefill-assistant` (32,768 tokens, input and output combined, is the training length in the model card), reached through `OPENAI_BASE_URL`
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools plamo`), temperature 0, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

The other models translate line by line with summary and glossary messages (`trtools translate`). Those messages do not fit this model's chat template, which skips system messages and reads every user/assistant pair as a source/translation example, so the options go in its template variables instead. `zh` is sent as the model's `zh-hans`.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

The model is not meant to translate line by line, so its output is kept as it came, even where the lines no longer match the source's 99. Kazakh joins two of Camille's lines near the start, dropping Luc's `Okay.` between them, and Burmese does the same with two of Luc's lines on the Abbe limit, dropping Camille's `Ah!`; both are two lines short and end naturally. The scores include these.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 93.6 | No shortcomings identified |
| Spanish | 92.0 | Slightly stiff syntax |
| Chinese (Traditional) | 90.8 | Occasional literal phrasing lacks native fluency |
| Chinese | 90.7 | Slight stiffness in phrasing |
| Japanese | 90.3 | Minor phrasing feels slightly literal or formal |
| Korean | 88.8 | Slightly stiff phrasing and formal tone |
| Vietnamese | 88.1 | Retains stiffness and lacks natural flow |
| Arabic | 88.0 | Awkward phrasing and literal tone |
| Catalan | 88.0 | Slightly literal phrasing and unlocalized interjections |
| Dutch | 87.8 | Unnatural literal translations of math terms |
| German | 87.7 | Translationese style |
| Indonesian | 87.6 | Stiff stylistic adaptation |
| Malay | 86.2 | Overly literal syntax |
| Italian | 86.0 | Literal calques and minor grammatical slips |
| Polish | 85.9 | Grammatical and gender errors |
| Russian | 84.5 | Literal calques and stiff syntax |
| Croatian | 83.2 | Noticeable issues in fluency and naturalness |
| Thai | 82.2 | Inconsistent honorific particles and unnatural phrasing |
| Hindi | 81.8 | Slightly stiff and literal phrasing |
| Serbian | 81.6 | Significant fluency and naturalness issues |
| Uzbek | 81.6 | Stiff, literal phrasing |
| Javanese | 81.5 | Slightly rigid fluency and naturalness |
| Marathi | 81.5 | Awkward phrasing and unnatural syntax |
| Estonian | 81.1 | Grammatical errors and awkward phrasing |
| Nepali | 79.0 | awkward phrasing and stiff syntax |
| Khmer | 78.8 | Inconsistent terminology and unnatural phrasing |
| Persian | 78.2 | Literal and awkward phrasing |
| Hungarian | 77.9 | Frequent grammatical errors and unnatural phrasing |
| Azerbaijani | 77.5 | Awkward phrasing and literal translations |
| Punjabi | 77.5 | Awkward phrasing and literal translations |
| Bengali | 77.0 | Translationese stiffness |
| Belarusian | 76.7 | Lexical errors and non-native phrasing |
| Georgian | 76.6 | Translationese with stiff syntax and literal idioms |
| Cebuano | 75.6 | Unnatural phrasing and lack of fluency |
| Slovak | 74.8 | Grammatical errors and awkward phrasing |
| Hebrew | 74.5 | Significant lexical errors and unnatural phrasing |
| Kazakh | 74.2 | Unnatural phrasing and register issues |
| Bulgarian | 73.9 | Prominent Russian interference and grammatical errors |
| Gujarati | 73.0 | Literalness and awkward phrasing |
| Urdu | 72.7 | Awkward literal phrasing and poor terminology |
| Malayalam | 72.0 | Terminology inconsistency and unnatural syntax |
| Armenian | 71.9 | Glaring speaker label error |
| Tagalog | 71.2 | Awkward fluency and incorrect terminology |
| Slovene | 70.3 | Severe lexical hallucinations and grammatical errors |
| Lithuanian | 69.2 | Severe lexical errors and grammar |
| Sinhala | 68.6 | Lack of tonal consistency and fluency |
| Latvian | 68.2 | Critical scientific inaccuracies and grammatical failures |
| Tamil | 68.0 | Terminology errors and grammatical awkwardness |
| Swahili | 67.3 | Severe linguistic inaccuracies |
| Basque | 64.6 | Lexical hallucinations and non-existent words |
| Burmese | 62.6 | Inaccurate physics terminology |
| Telugu | 61.4 | Severe terminology and tone errors |
