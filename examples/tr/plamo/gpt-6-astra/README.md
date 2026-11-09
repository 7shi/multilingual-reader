# examples/tr/plamo/gpt-6-astra/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gpt-6-astra/](../../onde/gpt-6-astra/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6-astra
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), thinking not turned off (no `--no-think`) and the API's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/gpt-6-astra/](../../onde/gpt-6-astra/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language and, without being asked to, kept the source's 99 lines in every one, with no line skipped, repeated, split or joined.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 94.1 | Professional grade ready for publication |
| Catalan | 93.6 | Very minor stylistic formality issues |
| Chinese | 93.0 | Minor areas for improvement in absolute naturalness |
| Spanish | 92.4 | Minor fluency variations are negligible |
| German | 92.3 | Phrasing could be more idiomatic |
| Dutch | 92.2 | Minor stylistic nuances and preserved loanwords |
| Japanese | 92.0 | No shortcomings mentioned |
| Polish | 92.0 | Very minor stylistic nuances could be refined |
| Chinese (Traditional) | 91.7 | Occasional stiff phrasing |
| Russian | 91.0 | Minor naturalness issues |
| Lithuanian | 90.8 | Minor stylistic quirks |
| Slovak | 90.5 | Slight translated feel in 1-3 lines |
| Indonesian | 90.2 | Slight variations in formality |
| Latvian | 90.2 | Slight translationese and stiff phrasing |
| Croatian | 90.0 | Slight stiffness and translationese feel |
| Vietnamese | 89.8 | Minor structural rigidity |
| Serbian | 89.7 | Minor phrasing nuances slightly impede native flow |
| Arabic | 89.5 | Slightly heavy or overly literal syntax |
| Belarusian | 89.2 | Occasional stiffness from calques |
| Thai | 89.2 | Slightly literal phrasing |
| Hungarian | 88.8 | Literalisms disrupt natural flow |
| Italian | 88.7 | Slightly stiff phrasing and literal rhythm |
| Korean | 88.7 | Slightly rigid tone and formal phrasing |
| Bulgarian | 88.1 | Occasionally lacks stylistic polish and feels stiff |
| Azerbaijani | 88.0 | Minor phrasing and tone inconsistencies |
| Malay | 88.0 | Minor spelling and fluency issues |
| Slovene | 87.7 | Stylistically rigid and overly formal |
| Georgian | 87.6 | Slightly stiff phrasing |
| Hindi | 86.8 | Inconsistent tone register |
| Persian | 86.4 | occasional translationese feel |
| Armenian | 86.2 | Slightly stiff phrasing |
| Hebrew | 85.9 | Minor fluency and terminology inconsistencies |
| Javanese | 85.9 | Slightly stilted sentence structure |
| Malayalam | 85.5 | Leans towards literal rendering |
| Basque | 85.4 | Slightly stiff and literal phrasing |
| Marathi | 85.4 | Lacks natural fluency |
| Khmer | 85.2 | Mechanically translated with awkward fluency |
| Nepali | 84.7 | Translationese affecting fluency |
| Uzbek | 84.4 | Minor stylistic inconsistencies |
| Urdu | 83.9 | Translationese and awkward terminology |
| Gujarati | 83.6 | Minor stylistic inconsistencies and slight translationese |
| Swahili | 83.6 | Awkward phrasing and literal calques |
| Tamil | 83.6 | Some stiff phrasing from direct translation |
| Bengali | 83.5 | Unnatural phrasing and literal terms |
| Punjabi | 83.0 | Slightly stiff and unnatural phrasing |
| Kazakh | 82.8 | Awkward phrasing from rigid syntax |
| Burmese | 82.4 | Translationese feel from rigid syntax |
| Sinhala | 82.2 | Translated feel due to awkward phrasing |
| Tagalog | 81.8 | Fluency and naturalness issues |
| Estonian | 80.8 | Awkward terminology and filler word rendering |
| Cebuano | 78.5 | Stiff literal phrasing |
| Telugu | 71.9 | Literal syntax causing stiff fluency |
