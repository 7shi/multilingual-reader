# examples/tr/plamo/gemini-3.8-flash/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemini-3.8-flash
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), thinking not turned off (no `--no-think`) and the API's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary, token usage recorded (`--save-usage`)

Unlike the line-by-line translation in [onde/](../../onde/) (`trtools translate`, with summary and glossary messages), the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language and kept the source's 99 lines in all but one:

- **Khmer**: breaks off in the middle of line 17, Camille's line on the Born rule, with no ending (17 lines). gemini-4-argon breaks off a line earlier, on line 16; the cause was not recorded.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 93.3 | Minor stylistic variations |
| Catalan | 93.0 | Minor stylistic variations exist between versions |
| French | 92.8 | Flawless technical precision and tone |
| Polish | 91.7 | Slightly literal phrasing reduces naturalness |
| Lithuanian | 90.4 | Occasionally stiff phrasing reduces naturalness |
| Russian | 90.1 | Minor syntactic rigidities |
| Korean | 89.6 | slight stiffness in sentence endings |
| Japanese | 89.5 | Slight translated feel and formal tone |
| Chinese | 89.5 | Speaker attribution errors |
| Latvian | 89.3 | Slightly rigid and translated phrasing |
| Dutch | 89.2 | Idiomatic consistency issues with numerical notation |
| Vietnamese | 89.2 | Rigid literal structure |
| Thai | 89.1 | Slightly stiff phrasing lacking natural flow |
| Bulgarian | 89.0 | Minor phrasing stiffness |
| Arabic | 88.9 | Occasionally stiff sentence structures and overly literal phrasing |
| Chinese (Traditional) | 88.4 | Occasionally stiff style |
| Serbian | 88.0 | Slight stiffness in idiomatic expressions |
| Hungarian | 87.8 | Occasional stiffness and foreign phrasing |
| Georgian | 87.2 | Slightly stiff and literal phrasing |
| Malay | 87.2 | Literal phrasing reduces naturalness |
| German | 86.7 | Awkward calques and literal phrasing |
| Armenian | 86.6 | Slightly formal tone reduces naturalness |
| Slovak | 86.5 | Slightly stiff dialogue tone and interjections |
| Persian | 86.4 | Minor literalness and terminology issues |
| Gujarati | 86.1 | Slightly stiff phrasing |
| Croatian | 85.6 | Some phrasing feels literal rather than idiomatic |
| Estonian | 85.4 | Severe syntactic errors disrupt fluency |
| Hebrew | 85.4 | Inconsistent speaker attribution |
| Belarusian | 85.2 | Unnatural phrasing and incorrect terminology |
| Basque | 85.2 | Mistranslation of "clever" as "light" |
| Italian | 85.0 | Specific phrasing errors like lambda mezzi |
| Marathi | 84.6 | Awkward dialogue flow |
| Indonesian | 84.1 | Translationese tone and stiff syntax |
| Punjabi | 84.0 | Literal translation of idiomatic expressions |
| Kazakh | 83.9 | Awkward idiomatic expressions and conversational markers |
| Urdu | 83.9 | Syntactic rigidity |
| Uzbek | 82.6 | Literal and awkward phrasing |
| Tamil | 82.4 | Stilted conversational flow |
| Azerbaijani | 82.2 | Incorrect technical terminology used |
| Javanese | 82.0 | Strong Indonesianized features |
| Malayalam | 82.0 | Fluency and naturalness of syntax |
| Sinhala | 82.0 | Awkward conversational tone |
| Slovene | 81.5 | Repeated literal math errors and awkward phrasing |
| Hindi | 81.2 | Overly literal syntax |
| Burmese | 80.3 | Heavy translationese and rigid phrasing |
| Bengali | 80.1 | Frequent awkward phrasing and syntactic structures feel like direct calques from English rather than natural Bengali idioms |
| Swahili | 79.5 | Inaccurate terminology and stiff fluency |
| Cebuano | 78.1 | Stiff fluency and unnatural syntax |
| Tagalog | 78.1 | Rigid literal structure and unnatural phrasing |
| Nepali | 78.0 | Inconsistent scientific terminology |
| Telugu | 73.7 | Severe terminology errors |
| Khmer | 66.3 | Severely truncated and incomplete translation |
