# examples/tr/onde/qwen3.6-27b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: qwen3.6-27b
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 92.9 | Rigid conversational connectors and grammatical errors |
| Catalan | 89.1 | Overly literal syntax and awkward filler words |
| Spanish | 88.7 | Minor formality inconsistencies and Anglo-Saxon syntax |
| Japanese | 88.4 | Minor awkwardness and dialogue flow issues |
| Russian | 88.4 | Awkward conversational tone and filler integration |
| Dutch | 88.2 | Awkward phrasing and specific errors |
| Chinese | 87.7 | Slightly stiff conversational tone |
| Ukrainian | 87.2 | Persistent mistranslation of "undulate" as "кохтить" |
| French | 86.9 | Register inconsistency between tu and vous |
| Polish | 82.4 | Noticeable linguistic imperfections and grammatical errors |
| Bulgarian | 82.1 | Awkwardness and lexical errors |
| Vietnamese | 81.5 | Literal calques and awkward filler words |
| Persian | 81.2 | Awkward filler words and unnatural rhythm |
| Galician | 81.1 | Significant linguistic inconsistencies and Spanish intrusions |
| Slovak | 80.5 | Disjointed mix of formal and informal registers |
| Czech | 80.4 | Unnatural phrasing and syntax |
| German | 80.1 | Grammatical errors and stiff phrasing |
| Portuguese | 79.8 | Inconsistent pronoun usage breaks immersion |
| Hindi | 79.6 | Unnatural formal vocabulary and literal syntax |
| Lithuanian | 78.9 | Unnatural phrasing and literal calques |
| Croatian | 78.5 | Obvious errors and inconsistent tone |
| Swedish | 77.5 | Missing negation reverses meaning and odd emotional tone |
| Hungarian | 77.4 | Significant fluency issues and inconsistent register |
| Slovene | 76.7 | Mechanical errors and unnatural phrasing |
| Romanian | 75.2 | Critical lexical errors and non-words |
| Latvian | 75.0 | Grammatical errors and unnatural phrasing |
| Norwegian | 75.0 | Significant lexical errors |
| Danish | 74.5 | Literal style and unnatural phrasing |
| Malay | 73.7 | Severe terminology inconsistencies and lexical errors |
| Indonesian | 73.5 | Significant mixed-language defect |
| Afrikaans | 73.2 | Severe lexical errors and nonsense phrases |
| Thai | 73.1 | Presence of untranslated Chinese text |
| Macedonian | 73.0 | Poor handling of mixed language and technical terms |
| Korean | 72.9 | Foreign language intrusions |
| Arabic | 71.6 | Mechanical errors and typos |
| Estonian | 70.5 | Nonsense words and literal translations |
| Turkish | 69.9 | Awkward phrasing and logical errors |
| Esperanto | 69.8 | Frequent critical lexical errors distort meaning |
| Urdu | 69.7 | Inconsistent terminology and literal calques |
| Serbian | 69.6 | Mixed language characters and encoding errors |
| Azerbaijani | 69.5 | Severe translationese and unnatural syntax |
| Interlingua | 69.5 | Awkward and mechanical phrasing |
| Belarusian | 69.1 | Inconsistent orthography and unnatural phrasing |
| Finnish | 68.0 | Severe lexical errors and unidiomatic phrasing |
| Marathi | 67.3 | Severe lexical inaccuracies |
| Hebrew | 66.0 | Severe systematic errors and nonsense |
| Icelandic | 66.0 | Severe grammatical instability and unnatural phrasing |
| Nepali | 65.8 | Critical "Yes" translated as "No" |
| Swahili | 64.8 | Severe terminology errors and unnatural phrasing |
| Bengali | 64.6 | Intrusive non-Bengali characters |
| Albanian | 64.0 | Pervasive grammatical errors and critical mistranslations |
| Mongolian | 63.8 | Severe terminology and grammatical failures |
| Tamil | 61.2 | Severe language intrusion and terminology errors |
| Khmer | 60.5 | Severe terminology errors and hallucinations |
| Georgian | 60.0 | Severe lexical errors and nonsense words |
| Welsh | 59.5 | Severe hallucinations and gibberish |
| Basque | 59.1 | Severe linguistic errors and nonsense vocabulary |
| Lao | 58.8 | Severe terminology errors and unnatural fluency |
| Tagalog | 57.6 | Severe grammatical and vocabulary errors |
| Kannada | 57.5 | Critical scientific terminology errors |
| Armenian | 55.9 | Severe typos and grammar errors |
| Malayalam | 53.0 | Severe linguistic contamination |
| Telugu | 52.5 | Severe lexical errors and hallucinations |
| Irish | 51.8 | Severe grammatical errors and gibberish |
| Greek | 50.8 | Major semantic inaccuracies and technical errors |
| Sinhala | 50.4 | Severe semantic degradation and technical nonsense |
| Burmese | 46.2 | Poor quality with critical errors |
