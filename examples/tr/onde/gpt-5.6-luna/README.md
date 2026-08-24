# examples/tr/onde/gpt-5.6-luna/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals/`, and scores to `SCORES.txt`.

- Translation model: gpt-5.6-luna
- Evaluation model: qwen3.6
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

After running `make`, append each language's quality trend here, based on the evaluation results (`SCORES.txt`) and manual content verification.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 100 | Flawless execution with minor notation style variations |
| Korean | 99 | Exceptional technical accuracy and natural conversational flow |
| Swedish | 98 | Slightly literal phrasing in two instances |
| Arabic | 97 | Near-perfect quality with minor stylistic repetitions and conventional scientific quirks |
| Catalan | 97 | Professional grade with minor stylistic adjustments needed |
| Czech | 97 | Exceptional quality with negligible minor stylistic polishing needed |
| Danish | 97 | Professional-grade scientific translation ready for publication |
| Spanish | 97 | Exceptional professional quality for broadcast |
| French | 97 | Pronoun inconsistency (tu/vous) |
| Georgian | 97 | Exceptional accuracy and naturalness |
| Dutch | 97 | Flawless technical accuracy and naturalness |
| Portuguese | 97 | High quality with minor gender agreement issues |
| Russian | 97 | Minor stylistic calques |
| Turkish | 97 | Negligible stylistic issues only |
| Vietnamese | 97 | Near perfect quality with minor cosmetic tweaks needed |
| German | 96 | High quality with minimal to no defects |
| Finnish | 96 | Minor stylistic adjustments needed for perfection |
| Indonesian | 96 | Highly accurate with minor terminology adjustments needed |
| Macedonian | 96 | Excellent quality with negligible room for improvement |
| Slovak | 96 | Minor grammatical awkwardness and mathematical phrasing |
| Ukrainian | 96 | Minor terminology deviations and literalness |
| Chinese | 96 | Excellent accuracy with minor literary tweaks needed |
| Afrikaans | 95 | Significant lexical error ('potgooi') noted multiple times |
| Bulgarian | 95 | Highly professional and scientifically accurate with minor stylistic refinements possible |
| Galician | 95 | High quality with minor terminology preferences |
| Croatian | 95 | Minor terminology adjustments needed for perfection |
| Hungarian | 95 | Minor fluency and typographical issues |
| Lithuanian | 95 | Minor terminology and declension issues |
| Romanian | 95 | Professional grade with negligible minor issues |
| Persian | 94 | Minor terminology inconsistencies and slight literalness |
| Hebrew | 94 | High quality with negligible minor defects |
| Armenian | 94 | Near-perfect execution with minor stylistic calques |
| Serbian | 94 | Minor terminology inaccuracies and localized quirks |
| Bengali | 93 | Highly polished and scientifically accurate |
| Hindi | 93 | Minor fluency refinements needed |
| Albanian | 93 | Minor stylistic calques and mathematical terminology issues |
| Azerbaijani | 92 | Minor typos reduce fluency |
| Polish | 92 | High quality with minor phrasing quirks |
| Burmese | 91 | Minor term standardization needed |
| Nepali | 91 | Minor stylistic refinements needed for standardization |
| Tamil | 91 | Minor terminology inconsistencies |
| Estonian | 90 | Minor grammatical and terminology issues |
| Latvian | 90 | Minor literal calques and slight stiffness |
| Norwegian | 90 | Minor terminology and typographic issues |
| Greek | 89 | Minor terminology inconsistencies and typos |
| Basque | 89 | Minor calques and terminology issues |
| Malayalam | 89 | Minor direct English intrusions and phrasing issues |
| Marathi | 89 | Minor literal phrasing and calques detract from native naturalness |
| Esperanto | 88 | Calques and non-standard scientific phrasing |
| Mongolian | 88 | Minor terminology and fluency issues |
| Malay | 88 | Terminology errors and Indonesian-leaning phrasing |
| Khmer | 87 | Minor phrasing stiffness and terminology inconsistencies |
| Japanese | 86 | Mixed-language placeholder artifact ("fascinates?") |
| Slovene | 86 | Minor technical inaccuracies and phrasing errors |
| Thai | 86 | Minor typos and awkward phrasing remain |
| Urdu | 85 | Consistent terminology with occasional stiffness |
| Irish | 83 | Minor terminology errors need refinement |
| Belarusian | 81 | Awkward lexical calques and non-standard terminology |
| Interlingua | 81 | Non-standard Interlingua terminology and lexical deviations |
| Kannada | 81 | Inconsistent terminology and unnatural phrasing |
| Telugu | 81 | Mixed-language artifacts and untranslated phrases |
| Swahili | 79 | Minor terminology and phrasing issues |
| Lao | 73 | Significant terminology inaccuracies and awkward phrasing |
| Sinhala | 70 | Inconsistent terminology and minor errors |
| Icelandic | 68 | Terminology errors and awkward phrasing |
| Welsh | 67 | Frequent typographical errors and non-standard terminology |
| Tagalog | 62 | Significant terminology and fluency issues |
