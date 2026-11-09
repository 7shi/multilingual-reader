# examples/tr/plamo/gpt-6-luna/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gpt-6-luna/](../../onde/gpt-6-luna/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6-luna
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), thinking not turned off (no `--no-think`) and the API's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/gpt-6-luna/](../../onde/gpt-6-luna/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna itself and proofread, where the other columns were translated by gemma4-31b. On those seven, the model is given a glossary it wrote.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which the model put between every line in some languages, are dropped, as the source has none (`trtools whole`). Without being asked to, it kept the source's 99 lines in every language, with no line skipped, repeated, split or joined.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.7 | Negligible minor stylistic deductions |
| French | 94.2 | No single flaw identified; minor deductions for style/punctuation |
| Catalan | 93.8 | Minor phrasing could be more idiomatic |
| Dutch | 92.8 | Slightly less idiomatic expressions |
| Russian | 92.2 | Minor English-calque fluency issues |
| Chinese (Traditional) | 91.7 | Minor direct calques affect natural flow |
| Arabic | 91.5 | Scattered minor flaws confined to one to three lines |
| Japanese | 91.3 | Minor nuance loss in "implacable" |
| Latvian | 91.3 | Minor register inconsistencies and phrasing |
| Indonesian | 91.1 | Slightly stiff phrasing lacking podcast flow |
| Slovak | 90.9 | No significant shortcomings identified |
| Chinese | 90.8 | Slightly constructed rhythm in reflective lines |
| German | 90.5 | Slight stiffness in connective phrases and idioms |
| Croatian | 90.5 | minor structural nuances adapted well |
| Thai | 90.5 | Minor terminology and phrasing adjustments needed |
| Hungarian | 90.2 | Minor literal phrasing issues |
| Vietnamese | 90.2 | Repetitive fillers and slight literalness |
| Belarusian | 90.0 | Phrases feel slightly literal or formal |
| Polish | 90.0 | Extremely subtle stylistic variations |
| Malay | 89.7 | Minor stylistic rigidities |
| Serbian | 89.7 | Phrasing feels slightly less idiomatic than native speech |
| Georgian | 89.5 | Slight stiffness in sentence structures and filler words |
| Bulgarian | 89.0 | Slight anglicisms affecting fluency |
| Estonian | 88.6 | Minor stylistic stiffness and literal phrasing |
| Korean | 88.4 | Slightly stiff phrasing and tone inconsistencies |
| Slovene | 88.4 | Register too formal for podcast |
| Azerbaijani | 88.2 | Non-standard scientific terminology |
| Lithuanian | 88.2 | Minor literalness and punctuation issues |
| Italian | 88.1 | Slight nuances in idiomatic flow vary by personal taste |
| Basque | 87.9 | Slightly stiff idiomatic expression |
| Marathi | 87.8 | Stiff phrasing and unnatural syntax |
| Uzbek | 87.3 | Phrasing could be more idiomatic |
| Hindi | 87.0 | Stiff and unnatural phrasing |
| Armenian | 86.4 | slight stiffness and translationese |
| Tamil | 85.5 | Slightly stiff English syntax |
| Nepali | 85.2 | Technical inaccuracies and unnatural phrasing |
| Hebrew | 84.7 | Terminology inconsistency |
| Malayalam | 84.4 | Literal English syntax |
| Javanese | 84.2 | Rigid adherence to English sentence structures |
| Bengali | 84.1 | Translationese and stiff phrasing |
| Kazakh | 83.9 | Stiff dialogue and literal phrasing |
| Punjabi | 83.8 | Literal translation tone |
| Burmese | 83.7 | Slightly literal phrasing disrupts naturalness |
| Swahili | 83.4 | Awkward literal phrasing disrupts fluency |
| Urdu | 83.1 | Syntactic rigidity and awkward phrasing |
| Khmer | 82.8 | Poor fluency and unnatural phrasing |
| Sinhala | 82.3 | Stylistic awkwardness and literalism |
| Persian | 81.7 | Glaring spelling errors in scientific terms |
| Gujarati | 79.5 | Translationese style |
| Tagalog | 79.0 | Slightly unnatural phrasing |
| Cebuano | 78.8 | Stiff and mechanical sentence structure |
| Telugu | 76.7 | Awkward and stiff phrasing |
