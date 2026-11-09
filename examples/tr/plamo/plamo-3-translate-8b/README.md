# examples/tr/plamo/plamo-3-translate-8b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: every language the [model card](https://huggingface.co/pfnet/plamo-3-translate-8b) lists as supported except the source English, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/). Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared only with the other models under [plamo/](../), on these languages ([PLAN.md](../PLAN.md)).

The translations under `tr/` are outputs of PLaMo 3 Translate 8B (`plamo-3-translate-8b-Q4_K_M.gguf`), provided under the [PLaMo Community License](https://plamo.preferredai.jp/info/plamo-community-license-en).

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: PLaMo 3 Translate 8B Q4_K_M on `llama-server -c 32768 --jinja --no-prefill-assistant` (32,768 tokens, input and output combined, is the training length in the model card), reached through `OPENAI_BASE_URL`
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools plamo`), temperature 0, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

The other models translate line by line with summary and glossary messages (`trtools translate`). Those messages do not fit this model's chat template, which skips system messages and reads every user/assistant pair as a source/translation example, so the options go in its template variables instead. `zh` is sent as the model's `zh-hans`.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

The model is not meant to translate line by line, so its output is kept as it came, even where the lines no longer match the source's 99. Japanese, after Camille's "But what if we take the logic to the extreme", goes back to Luc's "Wait. So the 'probability of presence'..." and runs through the same fifteen lines again, then once more starts them before jumping to the Abbe limit, skipping the lines in between; it ends naturally at 105 lines. Burmese, Sinhala and Malayalam skip 29, 33 and 20 lines in the second half (Burmese from the amplitude and width of a wave on, Sinhala from the uncertainty principle on, Malayalam from the Abbe limit on) and end naturally. Punjabi splits Luc's "Exactly! Why this extra step?" into two lines, the second labelled as Camille's. The scores include these.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 91.9 | Subtle literalness in pacing and phrasing |
| Spanish | 90.9 | Minor literal phrasing reducing fluency |
| Chinese | 89.4 | Minor stylistic rigidity in handling conversational nuances |
| Chinese (Traditional) | 89.0 | Literal translation disrupts natural dialogue flow |
| Polish | 88.8 | Slightly rigid syntax and literal phrasing |
| Dutch | 88.0 | Translation-heavy and stiff tone |
| Vietnamese | 87.8 | Slightly stiff phrasing and literal idioms |
| Catalan | 87.1 | Awkward phrasing and non-native interjections |
| Italian | 85.5 | Misuse of informal filler words |
| German | 85.2 | Grammatical errors and awkward phrasing |
| Hungarian | 84.7 | Slightly rigid syntax and minor errors |
| Malay | 84.7 | Code-switching and unlocalized fillers |
| Arabic | 84.2 | Stilted "translationese" style |
| Estonian | 83.7 | Grammatical errors and unnatural phrasing |
| Thai | 82.5 | Awkward phrasing and stiff syntax |
| Georgian | 81.2 | Awkward phrasing and unnatural sentence structures |
| Slovene | 81.1 | Grammatical errors and awkward phrasing |
| Urdu | 80.4 | Unnatural Urdu syntax |
| Bulgarian | 79.4 | Literal syntax and non-idiomatic phrasing |
| Swahili | 79.2 | Repetitive 'Kwa hivoro' and grammar errors |
| Korean | 79.1 | Stiff and unnatural phrasing |
| Javanese | 78.4 | Lacks natural Javanese phrasing |
| Azerbaijani | 78.0 | Critical semantic errors and awkward phrasing |
| Indonesian | 77.5 | Stiff phrasing and awkward literalism |
| Croatian | 77.2 | Numerous grammatical and gender errors |
| Armenian | 77.2 | Pervasive scientific terminology errors |
| Serbian | 76.8 | Terminology errors like "Abov limit" |
| Nepali | 76.7 | Reads like literal translation |
| Hebrew | 76.5 | unnatural syntax and terminology errors |
| Uzbek | 76.5 | Noticeable translationese and vocabulary errors |
| Lithuanian | 76.2 | Grammatical errors and unnatural phrasing |
| Marathi | 75.6 | Significant lexical and register errors |
| Cebuano | 75.0 | Unnatural phrasing and calqued syntax |
| Belarusian | 74.9 | Awkward phrasing and weak fluency |
| Slovak | 74.8 | Major speaker tag inconsistencies and unnatural phrasing |
| Latvian | 73.1 | Grammatical errors and non-standard word choices |
| Tagalog | 72.3 | Pervasive lack of linguistic naturalness and inconsistent terminology |
| Russian | 71.7 | Significant factual error: "Electron squared" instead of E-squared |
| Hindi | 70.9 | Gender agreement errors and mistranslated technical terms |
| Tamil | 70.8 | Stiff conversational tone |
| Gujarati | 67.4 | Terminological inconsistency and awkward phrasing |
| Kazakh | 67.3 | Severe terminological inaccuracies in physics terms |
| Persian | 66.4 | Significant terminology inconsistencies and errors |
| Basque | 65.7 | Severe grammatical and lexical errors |
| Malayalam | 64.7 | Disrupted dialogue structure |
| Telugu | 62.5 | Severe mechanical errors and inaccurate terminology |
| Khmer | 62.1 | Frequent misuse of physics terminology |
| Bengali | 61.2 | Severe orthographic errors |
| Japanese | 60.0 | Severe duplication and logical breakdown |
| Punjabi | 57.0 | Excessive code-switching and inaccurate terminology |
| Sinhala | 50.8 | Severely incomplete with missing dialogue and structural breaks |
| Burmese | 49.8 | Catastrophic paragraph alignment breakdown |
