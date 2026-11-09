# examples/tr/plamo/gemma4-e2b/

Translation and evaluation of the onde text under PLaMo 3 Translate's conditions ([PLAN.md](../PLAN.md)), by a general model.

Target languages: PLaMo 3 Translate's, set in [common.mk](../common.mk), the same as for [plamo-3-translate-0.8b](../plamo-3-translate-0.8b/) and the other sizes. Seven of them are outside the corpus's `CORE_LANGS` + `EXTRA_LANGS` ([common.mk](../../common.mk)): Traditional Chinese (`zh-hant`), Cebuano, Gujarati, Javanese, Kazakh, Punjabi and Uzbek. It is compared with the other models under [plamo/](../) on these languages, and with its own line-by-line translation in [onde/gemma4-e2b/](../../onde/gemma4-e2b/) on the 45 corpus languages among them.

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:e2b on Ollama, its context set to 32,768 tokens (`OLLAMA_CONTEXT_LENGTH=32768`), as for PLaMo, since the whole text and its translation go in one request
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: the whole text in one request per language (`trtools whole`), no CoT (`--no-think`) and Ollama's default temperature, as in onde/, the target language's whole column of `../../terms/onde-en.tsv` as the glossary

Only the method differs from [onde/gemma4-e2b/](../../onde/gemma4-e2b/), which translates line by line with summary and glossary messages (`trtools translate`). Here the model gets what PLaMo 3 Translate's template variables carry and nothing more: a system message naming the source and target languages, with the glossary, and the source text alone as the user message. It is not asked to keep the lines.

The term TSV's columns for the seven languages outside the corpus were translated by gpt-6-luna and proofread, where the other columns were translated by gemma4-31b.

As for PLaMo, the output is kept as it came, even where the lines no longer match the source's 99, and the scores include it. The one change is layout: blank lines, which a model may put between every line, are dropped where the source has none (`trtools whole`).

The model translated every language into the target language. Two lose their place:

- **Uzbek**: folds line 15 ("It's the square of its amplitude…", without the "height") into line 13 and drops Luc's `Ah yes.` on line 16, so from there it runs two lines behind the source with the speakers in step, and ends naturally two lines short.
- **Thai**: leaves out the closing line, ending on Luc's `Hmm.`, one line short.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 93.4 | Subtle idiomatic deviations |
| Spanish | 91.6 | Slightly stiff idioms and colloquialisms |
| Italian | 88.9 | Occasional Anglicized rhythm and stiffness |
| Korean | 86.0 | Slight stiffness in dialogue mechanics |
| Malay | 84.7 | Mistranslation of diffraction as belauan |
| Vietnamese | 84.5 | Literal translation causing stiffness |
| Dutch | 83.8 | Literal phrasing lacks natural fluency |
| Polish | 83.6 | Notable fluency and naturalness issues |
| Chinese (Traditional) | 83.0 | Stylistic rigidity |
| Indonesian | 80.8 | Unnatural phrasing from literal translation |
| German | 80.7 | Stiff, literal phrasing lacking fluency |
| Gujarati | 79.8 | Fluency and naturalness issues |
| Russian | 79.5 | Noticeable literal translation artifacts |
| Arabic | 78.5 | Mechanical inconsistencies disrupt fluency |
| Burmese | 78.0 | Unnatural conversational tone |
| Chinese | 77.7 | Rigid adherence to English syntax causes awkward phrasing |
| Japanese | 77.2 | Fluency and natural phrasing issues |
| Persian | 75.0 | Intrusive Chinese characters |
| Bengali | 74.9 | Unnatural phrasing and literal calques |
| Hindi | 74.5 | Unnatural literal syntax |
| Thai | 74.3 | Inconsistent first-person pronouns and mixed languages |
| Javanese | 74.2 | Unnatural mixing of Indonesian and Javanese |
| Nepali | 74.2 | Inconsistent character naming and vocalizations |
| Tagalog | 74.2 | Unnatural phrasing and incorrect lexical choices |
| Serbian | 73.1 | Significant grammatical inconsistencies and unnatural phrasing |
| Urdu | 70.8 | Inconsistent technical term transliteration |
| Croatian | 70.0 | Severe mixed language and grammatical errors |
| Marathi | 69.4 | Mechanical translation artifacts |
| Swahili | 69.2 | Pervasive mechanical errors and mistranslation of "yes" |
| Hebrew | 68.6 | Unidiomatic "hot" interjections and French code-switching |
| Sinhala | 68.3 | Significant script mixing and grammatical errors |
| Khmer | 68.0 | Poor linguistic and technical accuracy |
| Malayalam | 66.6 | Presence of foreign script and mixed-language fragments |
| Tamil | 65.2 | Mixed language artifacts and incorrect terminology |
| Telugu | 64.7 | Severe linguistic inaccuracies and incorrect scientific terminology |
| Cebuano | 64.6 | Catastrophic mistranslations and grammatical errors |
| Kazakh | 62.9 | Pervasive literal mistranslation of "Yes" as possessive |
| Uzbek | 62.4 | Severe lexical errors and unnatural syntax |
| Punjabi | 60.7 | Severe terminology and grammar errors |
| Catalan | 59.8 | Severe lexical and grammatical errors with mixed-language artifacts |
| Slovak | 58.7 | Severe grammatical breakdowns |
| Azerbaijani | 56.8 | Severe grammatical and semantic errors |
| Georgian | 56.2 | Mixed-language contamination and severe incoherence |
| Bulgarian | 54.2 | Presence of Chinese characters and severe errors |
| Armenian | 53.7 | Severe machine translation artifacts and language mixing |
| Slovene | 47.9 | Catastrophic grammatical breakdowns and nonsense |
| Hungarian | 46.7 | Severe structural and lexical errors |
| Lithuanian | 38.0 | Severely degenerated into nonsensical fragments |
| Belarusian | 37.8 | Severe lexical and grammatical incoherence |
| Latvian | 36.2 | Fundamentally broken and unintelligible |
| Estonian | 35.6 | Fundamentally flawed and nonsensical |
| Basque | 22.9 | Completely incomprehensible gibberish |
