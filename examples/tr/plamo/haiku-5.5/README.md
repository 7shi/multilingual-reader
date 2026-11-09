# examples/tr/plamo/haiku-5.5/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/haiku-5.5/](../../onde/haiku-5.5/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: Claude Haiku 5.5
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), thinking not turned off (no `--no-think`) and the API's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/haiku-5.5/](../../onde/haiku-5.5/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which the model put between every line in some languages, are dropped, as the source has none (`trtools whole`).

The model kept the source's 99 lines in every language, with no line skipped, repeated, split or joined. In Arabic, Sinhala, Burmese and Traditional Chinese it marks the speaker names in Markdown bold (`**Name:**`) on every line, which the other languages and the source do not have.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 92.9 | Flawless execution with minor spoken style variations |
| Dutch | 91.9 | Minor subjective stylistic preferences |
| Spanish | 91.7 | Minor issues with idiomatic phrasing and stylistic polish |
| Chinese (Traditional) | 91.5 | Occasional slight stiffness in sentence structure |
| Catalan | 90.9 | Dialectal inconsistency and literal phrasing |
| German | 90.8 | Slight translated feel and literal phrasing |
| Slovak | 90.7 | Minor phrasing feels slightly translated |
| Serbian | 90.5 | Slightly unnatural phrasing and tone |
| Italian | 90.3 | Awkward phrasing like "un perfetto eco" |
| Japanese | 90.2 | Subtle nuances could use more localized idioms |
| Arabic | 89.8 | Slightly stiff phrasing detracts from naturalness |
| Vietnamese | 89.8 | Slightly rigid sentence structure |
| Chinese | 89.8 | Slight translationese and awkward phrasing |
| Indonesian | 89.7 | Slightly stiff sentence structures |
| Malay | 89.2 | Slightly literal phrasing affects natural flow |
| Hungarian | 89.1 | Slightly heavy sentence structure and academic tone |
| Croatian | 88.9 | Slightly literal phrasing affects fluency |
| Latvian | 88.1 | Minor literal translation artifacts and one untranslated English word |
| Lithuanian | 88.0 | Occasional stiffness and literal translations |
| Thai | 87.8 | Translationese causing stiffness and pronoun inconsistency |
| Korean | 87.6 | Sentence structures retain English traces |
| Armenian | 85.0 | Minor omissions and awkward phrasing |
| Polish | 85.0 | Grammatical errors and awkward phrasing |
| Hindi | 84.8 | Unnatural flow and grammatical rigidity |
| Uzbek | 84.5 | Awkward phrasing and mixed-language fragment |
| Urdu | 84.2 | Stiff syntax and phrasing |
| Azerbaijani | 83.4 | Awkward phrasing and literal translations |
| Tamil | 82.8 | Rigid adherence to English sentence structures |
| Marathi | 82.4 | Slightly rigid phrasing disrupts natural flow |
| Malayalam | 82.2 | Heavy reliance on transliteration |
| Slovene | 82.2 | Slightly stiff phrasing and terminology |
| Gujarati | 82.1 | Rigid syntax and unnatural phrasing |
| Estonian | 82.0 | Persistent grammatical errors and unnatural phrasing |
| Nepali | 81.8 | Literal word-for-word transcription reduces fluency |
| Persian | 81.6 | Stiff fluency and unnatural dialogue |
| Bengali | 81.1 | Stiff literal phrasing |
| Georgian | 80.6 | Fluent but stiff phrasing |
| Punjabi | 80.6 | Linguistic stiffness and awkward phrasing |
| Russian | 79.8 | Literal translations of idioms |
| Khmer | 79.7 | Stiff phrasing and some unnatural word choices |
| Swahili | 78.6 | Awkward literalism and incorrect lab terminology |
| Bulgarian | 78.5 | Mixed-language encoding error |
| Basque | 78.5 | Glaring mistranslation and stiff phrasing |
| Belarusian | 77.0 | Noticeable fluency issues |
| Tagalog | 75.7 | Poor fluency and unnatural phrasing |
| Hebrew | 75.5 | Systematic misuse of "הם" for conversational particles |
| Burmese | 75.5 | Stiff and overly literal tone |
| Kazakh | 73.6 | Russianisms |
| Sinhala | 71.4 | Lacks fluency and naturalness |
| Cebuano | 70.4 | Awkward and literal phrasing |
| Telugu | 70.2 | Grammatical inaccuracies and unnatural phrasing |
| Javanese | 68.5 | Inconsistent linguistic style and flow |
