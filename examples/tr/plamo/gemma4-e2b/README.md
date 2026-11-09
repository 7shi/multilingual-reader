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

In 14 of the 52 languages the model does not translate at all, and those score 0 by the language check. In 11 it returns the English source unchanged, byte for byte: Azerbaijani, Bulgarian, German, Estonian, Hungarian, Javanese, Lithuanian, Malay, Russian, Swahili and Chinese. In 3 it translates into Spanish instead: Catalan, Italian and Tagalog, each worded a little differently from its own Spanish. Ollama held the model with the 32,768-token context, so the request was not cut short. A later run of German alone, outside these results, did translate it, so whether a language is copied varies from run to run, and the record keeps the run as it came.

Where the model does translate, three languages lose their place:

- **Basque**: after line 69 it jumps to line 80 ("Super-resolution isn't magic"), skipping the evanescent waves and the near-field microscope; from there it skips the start of the summary (lines 81–84) as well, with the speakers swapped, and ends naturally 14 lines short.
- **Thai**: leaves out the closing line, ending on Luc's `Hmm.`, one line short.
- **Punjabi**: drops Camille's label from line 63 ("Diffraction…") and adds a line of its own after it, `ਕੈਮਿਲ: ਸਹੀ।` ("Camille: Right."), one line over.

The language check left Traditional Chinese for review, as it always does, since the detector does not tell the two scripts apart. It was settled as in the target language (`langcheck-resolved.jsonl`): it uses no simplified characters.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 93.1 | Very slight stiffness in transitions |
| Spanish | 92.2 | Critical vocabulary errors like riza and ingenuidad |
| Indonesian | 86.7 | Literal translation tone lacking natural flow |
| Chinese (Traditional) | 84.8 | Translationese and unnatural phrasing |
| Vietnamese | 83.5 | Awkward phrasing detracts from naturalness |
| Dutch | 82.2 | Unnatural phrasing and literal syntax |
| Polish | 80.0 | Unnatural phrasing and literal mistranslations |
| Korean | 79.9 | Mechanical terminology errors |
| Japanese | 79.2 | Retains stiffness |
| Arabic | 78.1 | Noticeable lack of fluency and naturalness |
| Khmer | 77.2 | Terminology inconsistency and unnatural phrasing |
| Marathi | 76.9 | Literal translation style |
| Persian | 76.8 | Noticeable awkwardness and lack of idiomatic naturalness |
| Hindi | 76.1 | Terminology mistranslations |
| Burmese | 75.7 | Awkward literalism undermining fluency |
| Thai | 75.0 | Lacks naturalness and fluency |
| Nepali | 74.8 | Inconsistent name rendering |
| Bengali | 74.2 | Mixed terminology and literal phrasing |
| Croatian | 73.8 | Grammatical errors and lexical inaccuracies |
| Tamil | 71.0 | Awkward syntax and stiff flow |
| Sinhala | 70.5 | Severe grammatical errors and unnatural phrasing |
| Telugu | 68.7 | Severe grammatical and terminology flaws |
| Hebrew | 67.5 | Severe code-switching and incorrect terminology |
| Malayalam | 67.3 | Critical mixed-language artifacts and incorrect scripts |
| Urdu | 66.8 | Inconsistent scientific terminology and transliteration |
| Cebuano | 66.2 | Severe mixed-language defect blending Tagalog into Cebuano |
| Gujarati | 66.1 | Mixed-language artifacts |
| Serbian | 65.1 | Pervasive mechanical errors |
| Georgian | 58.4 | Mixed language and incomprehensible grammar |
| Kazakh | 56.7 | Severe terminology errors and calques |
| Punjabi | 56.2 | Severe structural and logical failures |
| Uzbek | 55.4 | Severe grammatical errors and scientific mistranslations |
| Armenian | 54.9 | Severe grammatical errors and mixed languages |
| Slovak | 50.6 | Severe grammatical and lexical errors rendering it unintelligible |
| Belarusian | 45.2 | Severe grammatical errors and nonsensical vocabulary |
| Slovene | 43.8 | Contains random Chinese characters and broken syntax |
| Latvian | 33.0 | Incomprehensible gibberish with severe errors |
| Basque | 15.8 | Complete lack of coherence and fluency |
| Azerbaijani | 0.0 | Not in the target language (detected: English) |
| Bulgarian | 0.0 | Not in the target language (detected: English) |
| Catalan | 0.0 | Not in the target language (detected: Spanish) |
| German | 0.0 | Not in the target language (detected: English) |
| Estonian | 0.0 | Not in the target language (detected: English) |
| Hungarian | 0.0 | Not in the target language (detected: English) |
| Italian | 0.0 | Not in the target language (detected: Spanish) |
| Javanese | 0.0 | Not in the target language (detected: English) |
| Lithuanian | 0.0 | Not in the target language (detected: English) |
| Malay | 0.0 | Not in the target language (detected: English) |
| Russian | 0.0 | Not in the target language (detected: English) |
| Swahili | 0.0 | Not in the target language (detected: English) |
| Tagalog | 0.0 | Not in the target language (detected: Spanish) |
| Chinese | 0.0 | Not in the target language (detected: English) |
