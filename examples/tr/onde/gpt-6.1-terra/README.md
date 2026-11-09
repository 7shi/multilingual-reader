# examples/tr/onde/gpt-6.1-terra/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gpt-6.1-terra
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, thinking not turned off (no `--no-think`), term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 94.2 | minor stylistic nuances slightly formal for podcast |
| Catalan | 93.7 | No notable shortcomings mentioned |
| Swedish | 93.1 | Minor deductions in fluency standards for spoken dialogue scripts |
| French | 92.1 | minor stylistic preferences |
| Galician | 92.0 | Minor stylistic phrasing issues |
| Indonesian | 91.4 | Slightly less idiomatic phrasing |
| Dutch | 91.4 | Occasional stiffness in fluency and register consistency |
| Russian | 91.4 | Slightly less idiomatic phrasing |
| Slovak | 91.2 | Minor stylistic variations from spoken English to written Slovak |
| Ukrainian | 91.1 | Minor structural rigidity and prepositional adjustments |
| Latvian | 90.9 | Minor stylistic stiffness and literal phrasing |
| Japanese | 90.8 | Minor subtle stylistic choices |
| Bulgarian | 90.2 | Minor stylistic stiffness and literal phrasing |
| Polish | 90.0 | Slightly literal and stiff phrasing |
| Hungarian | 89.8 | Occasional minor stylistic stiffness or overly literal phrasing |
| German | 89.7 | Occasionally slightly literal phrasing |
| Lithuanian | 89.7 | Slightly rigid adherence to English syntax |
| Finnish | 89.6 | Minor stylistic nuance issues |
| Chinese | 89.4 | Slightly rigid phrasing and literal pauses |
| Croatian | 89.1 | Minor awkwardness in colloquialisms and prepositions |
| Estonian | 89.0 | Slight awkwardness and literal translations cause translationese |
| Belarusian | 88.9 | Gloring typo and minor stylistic issues |
| Albanian | 88.9 | Slightly literal phrasing reduces fluency |
| Afrikaans | 88.8 | occasionally literal phrasing |
| Portuguese | 88.8 | Minor stylistic adjustments needed for fluency |
| Vietnamese | 88.8 | Fluency and naturalness |
| Macedonian | 88.4 | Slightly literal phrasing |
| Italian | 88.3 | Overuse of explicit back-channeling cues |
| Serbian | 88.3 | minor stiffness and unnatural phrasing |
| Georgian | 88.2 | Slightly literal syntax and filler words |
| Korean | 88.0 | Tone nuances lost |
| Thai | 88.0 | Inconsistent tone and register |
| Norwegian | 87.5 | Occasionally lacks idiomatic flow |
| Romanian | 87.5 | Noticeable stiffness and awkward phrasing |
| Hindi | 87.4 | Slightly stiff phrasing and minor register inconsistencies |
| Czech | 87.3 | Minor stylistic hesitations and literal phrasing |
| Slovene | 87.2 | Minor stylistic issues |
| Malay | 86.7 | Unnatural phrasing and incorrect terminology |
| Arabic | 86.6 | Rigid translated feel |
| Esperanto | 86.6 | Lexical inaccuracies and unnatural phrasing |
| Icelandic | 86.6 | Minor stiffening and slight translationese quality |
| Marathi | 86.5 | Minor phrasing awkwardness and dialogue inconsistencies |
| Danish | 86.3 | Stiff and literal phrasing |
| Armenian | 86.3 | Minor stylistic choices slightly formal |
| Persian | 86.2 | Awkward literal syntax and forced fillers |
| Turkish | 86.2 | Literal conversational fillers and awkward phrasing |
| Azerbaijani | 85.5 | Retains stiffness and "translationese" |
| Greek | 85.5 | Stiff phrasing and literal conversational markers |
| Khmer | 85.1 | Slightly literal or stiff phrasing |
| Basque | 84.8 | Minor stiffness and awkward phrasing |
| Urdu | 84.5 | Slightly rigid phrasing |
| Swahili | 84.4 | Translationese and stiff phrasing |
| Hebrew | 83.9 | Stiff phrasing and poor symbol transliteration |
| Nepali | 83.7 | Noticeable translationese affects fluency |
| Malayalam | 83.3 | Minor stiffness and awkward phrasing |
| Tagalog | 82.9 | Poor naturalness and stiffness |
| Bengali | 82.2 | Slightly literal and stiff phrasing |
| Lao | 82.0 | Rigid fluency and naturalness |
| Mongolian | 81.8 | Stiff and literal dialogue |
| Irish | 81.5 | Awkward lexical choices and semantic inaccuracies |
| Tamil | 81.5 | Retains English syntactic patterns |
| Welsh | 81.3 | Tonally inconsistent between formal and casual registers |
| Burmese | 80.8 | Stiff phrasing and non-idiomatic structures |
| Sinhala | 80.2 | Translationese disrupts fluency |
| Interlingua | 77.8 | Significant fluency issues and stiffness |
| Kannada | 76.3 | Stiff and awkward phrasing |
| Telugu | 71.7 | Pronoun misuse and stiff phrasing |
