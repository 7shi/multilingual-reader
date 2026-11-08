# examples/tr/onde/crouton-alpha/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: crouton-alpha
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Catalan | 92.6 | minor stylistic refinement needed |
| Italian | 92.0 | Slightly rigid and unnatural phrasing |
| French | 91.6 | Slightly literal phrasing |
| Spanish | 91.3 | Minor stylistic preference on "Hmm" |
| Swedish | 91.1 | Slightly stiff or literal phrasing |
| Dutch | 90.2 | Literal translation of mathematical notation |
| Portuguese | 89.8 | Minor stylistic friction and literal phrasing |
| Czech | 89.5 | minor phrasing issue |
| Romanian | 88.8 | Slightly literal phrasing and stiff idioms |
| Finnish | 88.6 | Inconsistent register and anglicisms |
| Lithuanian | 88.6 | Minor fluency issues |
| Hungarian | 88.2 | Stiff and overly literal phrasing |
| Slovene | 88.2 | Minor stylistic rigidities and awkward phrasing |
| Danish | 88.1 | Occasional stiffness and Anglicized structure |
| Bulgarian | 88.0 | Slightly stiff phrasing and mechanical fillers |
| Galician | 87.8 | Inconsistent use of largura for physical dimensions |
| Croatian | 87.8 | Occasionally stiff and literal phrasing |
| Malay | 87.8 | Awkward non-standard technical terms like belauan |
| Arabic | 87.7 | Retains rigid English sentence structure |
| Persian | 87.7 | Minor interjections feel like calques |
| Indonesian | 87.6 | Phrasing feels slightly rigid |
| Polish | 87.2 | Literal translations cause awkward phrasing |
| Albanian | 87.2 | awkward phrasing and literal translations |
| Chinese | 87.1 | Translationese affects naturalness |
| Icelandic | 86.9 | Slightly unnatural phrasing and lexical precision |
| Ukrainian | 86.9 | Slightly rigid phrasing and non-standard terminology |
| Vietnamese | 86.7 | Heavy translationese style |
| Norwegian | 86.3 | Awkward math notation phrasing |
| German | 86.2 | Significant fluency and naturalness issues |
| Slovak | 86.1 | Slightly stiff conversational phrasing |
| Latvian | 85.8 | Fluency issues and slight awkwardness |
| Japanese | 85.5 | Slightly unnatural phrasing and rigid sentence construction |
| Afrikaans | 85.1 | Linguistic rigidity |
| Thai | 84.8 | Unnatural filler words and awkward phrasing |
| Russian | 84.7 | Rigid literal structure sounds unnatural |
| Estonian | 84.4 | Minor fluency issues and literal phrasing |
| Macedonian | 83.9 | Notable calques and awkward phrasing |
| Hebrew | 83.5 | Slightly stiff phrasing |
| Hindi | 83.4 | Translationese and unnatural interjections |
| Turkish | 83.1 | Excessive literalism and awkward phrasing |
| Georgian | 82.9 | Latin character intrusions disrupt readability |
| Esperanto | 82.6 | Mechanical and unnatural phrasing |
| Azerbaijani | 82.5 | Mechanically generated feel |
| Armenian | 82.2 | Grammatical errors and unnatural phrasing |
| Urdu | 82.0 | Translationese affecting fluency |
| Marathi | 80.5 | Lacks fluency and naturalness |
| Basque | 80.3 | Stiff phrasing and unnatural fillers |
| Khmer | 80.2 | Rigid and overly literal syntax |
| Swahili | 80.2 | Literal and stiff phrasing |
| Serbian | 80.1 | Grammatical and syntactic errors impede fluency |
| Nepali | 79.5 | Literal phrasing and unnatural filler words |
| Irish | 79.2 | Rigid literal syntax and lexical inaccuracies |
| Tagalog | 79.2 | Artificial Taglish tone and unnatural phrasing |
| Bengali | 78.4 | unnatural phrasing and stiff dialogue |
| Tamil | 78.2 | Noticeable translationese impacts fluency |
| Interlingua | 78.1 | French calques such as il ha and plongear |
| Mongolian | 78.1 | Translationese and stiff syntax |
| Lao | 78.0 | Literal translation artifacts and stiff syntax |
| Welsh | 77.0 | Orthographic inconsistency and awkward phrasing |
| Belarusian | 76.9 | Significant lexical errors and orthographic inconsistencies |
| Kannada | 76.5 | Stiff and unnatural phrasing |
| Korean | 76.4 | Lacks fluency and natural flow |
| Malayalam | 76.4 | Lacks fluency and naturalness due to awkward phrasing |
| Burmese | 71.1 | Inconsistent terminology and unnatural phrasing |
| Sinhala | 70.8 | Severe grammatical failure and stiffness |
| Telugu | 70.8 | Unnatural phrasing and terminology inconsistency |
| Greek | 68.0 | Critical terminology errors and grammatical flaws |
