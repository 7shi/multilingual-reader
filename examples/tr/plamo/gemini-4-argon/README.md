# examples/tr/plamo/gemini-4-argon/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemini-4-argon
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), thinking not turned off (no `--no-think`) and the API's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary, token usage recorded (`--save-usage`)

Unlike the line-by-line translation in [onde/](../../onde/) (`trtools translate`, with summary and glossary messages), the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language and kept the source's 99 lines in all but two:

- **Khmer**: breaks off in the middle of line 16, on the first letter of Luc's `Ah yes.`, with no ending (16 lines). gemini-3.8-flash breaks off a line later, on line 17; the cause was not recorded.
- **Traditional Chinese**: keeps the 99 lines but gives Camille's `Hmm.` on line 89 to Luc, so Luc speaks three lines in a row.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.2 | Minor stylistic preferences |
| French | 93.8 | No shortcomings found |
| Catalan | 93.4 | Minor stylistic preferences slightly reduce fluency |
| Polish | 91.5 | Idiomatic phrasing and tone |
| Japanese | 90.7 | Slightly staged interjections |
| Hungarian | 90.2 | Minor filler word usage |
| Croatian | 89.8 | Minor phrasing stiffness |
| Dutch | 89.8 | Slightly formal phrasing |
| Thai | 89.8 | Slightly stiff phrasing and inconsistent honorifics |
| Slovak | 89.5 | Slightly less idiomatic phrasing in transitions |
| Russian | 89.4 | Slight residual formality |
| Serbian | 89.3 | Minor stylistic phrasing issues |
| Indonesian | 89.2 | Slight stiffness in phrasing |
| Lithuanian | 89.2 | Stiff or literal phrasing |
| German | 88.6 | Minor fluency and terminology issues |
| Korean | 88.6 | Tone inconsistency and stiffness |
| Vietnamese | 88.6 | Slightly stiff phrasing and literal fillers |
| Latvian | 88.0 | Slightly rigid and unnatural phrasing |
| Bulgarian | 87.8 | Slightly translated tone |
| Chinese | 87.4 | Slightly stiff fluency and naturalness |
| Belarusian | 86.6 | Residual awkwardness and literal phrasing |
| Slovene | 86.6 | Stiff phrasing and unnatural flow |
| Armenian | 86.2 | Minor stylistic stiffness and lack of idiomatic elegance |
| Chinese (Traditional) | 86.2 | Minor gendered pronoun choice lacks textual basis |
| Georgian | 85.9 | Slight syntactic awkwardness and literal idioms |
| Uzbek | 85.7 | Translationese lacks naturalness |
| Estonian | 85.1 | Unnatural filler words and minor terminology issues |
| Hebrew | 84.9 | Awkward phrasing retains a translated feel |
| Azerbaijani | 84.6 | Slightly stiff phrasing and literal idioms |
| Malayalam | 84.4 | Stiff and unnatural phrasing |
| Kazakh | 83.6 | awkward phrasing and literalism |
| Swahili | 83.1 | Overly formal register in informal context |
| Persian | 83.0 | Awkward phrasing and unnatural transitions |
| Marathi | 83.0 | Inconsistent pronouns and stiffness |
| Tamil | 82.7 | Reads slightly rigid and literal |
| Gujarati | 82.5 | Translationese and grammatical inconsistencies |
| Arabic | 82.3 | Awkward phrasing from literal rendering |
| Hindi | 82.3 | Awkward literal phrasing and poor flow |
| Basque | 81.8 | Signs of translationese and awkward phrasing |
| Italian | 81.7 | Lacks native polish due to stiff phrasing and literal translations |
| Punjabi | 81.7 | Culturally mismatched tone and greeting |
| Bengali | 81.5 | Noticeable character usage glitches |
| Sinhala | 81.5 | Noticeable stiffness and unnatural phrasing |
| Urdu | 81.3 | Slightly rigid and unnatural phrasing |
| Burmese | 81.0 | Translationese style and stiff phrasing |
| Malay | 80.6 | Notable translationese artifacts and awkward phrasing |
| Nepali | 79.6 | unnatural english syntax |
| Javanese | 79.5 | Erratic register mixing |
| Tagalog | 79.5 | Code-switching disrupts fluency |
| Cebuano | 77.4 | Unnatural phrasing and stiffness |
| Khmer | 76.3 | Critical truncation mid-dialogue |
| Telugu | 72.0 | Inconsistent terminology and awkward grammar |
