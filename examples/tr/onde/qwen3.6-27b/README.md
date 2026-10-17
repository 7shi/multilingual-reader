# examples/tr/onde/qwen3.6-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: qwen3.6-27b
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 92.4 | Rigid conversational connectors and grammatical errors |
| Chinese | 90.0 | Slightly stiff conversational tone |
| Catalan | 89.8 | Overly literal syntax and awkward filler words |
| Dutch | 89.3 | Awkward phrasing and specific errors |
| French | 87.5 | Register inconsistency between tu and vous |
| Russian | 87.5 | Awkward conversational tone and filler integration |
| Spanish | 87.3 | Minor formality inconsistencies and Anglo-Saxon syntax |
| Ukrainian | 86.5 | Persistent mistranslation of "undulate" as "кохтить" |
| Japanese | 86.3 | Minor awkwardness and dialogue flow issues |
| Galician | 84.3 | Significant linguistic inconsistencies and Spanish intrusions |
| Polish | 83.7 | Noticeable linguistic imperfections and grammatical errors |
| Bulgarian | 83.6 | Awkwardness and lexical errors |
| Persian | 83.4 | Awkward filler words and unnatural rhythm |
| Portuguese | 82.7 | Inconsistent pronoun usage breaks immersion |
| Vietnamese | 82.5 | Literal calques and awkward filler words |
| Czech | 80.7 | Unnatural phrasing and syntax |
| Slovak | 80.0 | Disjointed mix of formal and informal registers |
| German | 79.3 | Grammatical errors and stiff phrasing |
| Afrikaans | 79.2 | Severe lexical errors and nonsense phrases |
| Hindi | 78.7 | Unnatural formal vocabulary and literal syntax |
| Lithuanian | 78.7 | Unnatural phrasing and literal calques |
| Hungarian | 78.5 | Significant fluency issues and inconsistent register |
| Swedish | 78.2 | Missing negation reverses meaning and odd emotional tone |
| Latvian | 76.5 | Grammatical errors and unnatural phrasing |
| Danish | 76.3 | Literal style and unnatural phrasing |
| Norwegian | 76.3 | Significant lexical errors |
| Indonesian | 76.2 | Significant mixed-language defect |
| Korean | 76.2 | Foreign language intrusions |
| Slovene | 75.7 | Mechanical errors and unnatural phrasing |
| Croatian | 75.5 | Obvious errors and inconsistent tone |
| Malay | 75.5 | Severe terminology inconsistencies and lexical errors |
| Thai | 75.5 | Presence of untranslated Chinese text |
| Macedonian | 75.1 | Poor handling of mixed language and technical terms |
| Estonian | 74.3 | Nonsense words and literal translations |
| Arabic | 73.8 | Mechanical errors and typos |
| Romanian | 72.8 | Critical lexical errors and non-words |
| Interlingua | 72.3 | Awkward and mechanical phrasing |
| Belarusian | 72.2 | Inconsistent orthography and unnatural phrasing |
| Azerbaijani | 71.2 | Severe translationese and unnatural syntax |
| Urdu | 70.5 | Inconsistent terminology and literal calques |
| Turkish | 70.4 | Awkward phrasing and logical errors |
| Hebrew | 70.3 | Severe systematic errors and nonsense |
| Esperanto | 69.7 | Frequent critical lexical errors distort meaning |
| Serbian | 69.1 | Mixed language characters and encoding errors |
| Icelandic | 68.9 | Severe grammatical instability and unnatural phrasing |
| Bengali | 68.2 | Intrusive non-Bengali characters |
| Albanian | 67.5 | Pervasive grammatical errors and critical mistranslations |
| Finnish | 67.0 | Severe lexical errors and unidiomatic phrasing |
| Marathi | 67.0 | Severe lexical inaccuracies |
| Swahili | 66.7 | Severe terminology errors and unnatural phrasing |
| Nepali | 65.8 | Critical "Yes" translated as "No" |
| Mongolian | 64.7 | Severe terminology and grammatical failures |
| Khmer | 62.3 | Severe terminology errors and hallucinations |
| Tamil | 61.7 | Severe language intrusion and terminology errors |
| Georgian | 59.4 | Severe lexical errors and nonsense words |
| Kannada | 59.3 | Critical scientific terminology errors |
| Welsh | 59.2 | Severe hallucinations and gibberish |
| Lao | 58.8 | Severe terminology errors and unnatural fluency |
| Armenian | 58.4 | Severe typos and grammar errors |
| Tagalog | 58.2 | Severe grammatical and vocabulary errors |
| Greek | 57.5 | Major semantic inaccuracies and technical errors |
| Basque | 55.1 | Severe linguistic errors and nonsense vocabulary |
| Malayalam | 54.1 | Severe linguistic contamination |
| Irish | 53.5 | Severe grammatical errors and gibberish |
| Telugu | 52.9 | Severe lexical errors and hallucinations |
| Sinhala | 49.8 | Severe semantic degradation and technical nonsense |
| Burmese | 47.8 | Poor quality with critical errors |
