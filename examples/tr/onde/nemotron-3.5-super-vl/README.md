# examples/tr/onde/nemotron-3.5-super-vl/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: nvidia/nemotron-3.5-super-vl (120B-A12B MoE)
- Evaluation model: jev-1.14.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 91.5 | Phrasing feels slightly literal or stiff |
| Swedish | 90.2 | Slight awkwardness in phrasing |
| French | 90.1 | Minor address form inconsistency |
| Portuguese | 89.5 | Unnatural dialogue tags and interjections |
| Italian | 89.2 | Retains English interjections and has minor grammatical errors |
| Japanese | 88.7 | Minor issues with naturalness |
| German | 88.3 | Register inconsistency between du and Sie |
| Chinese | 87.4 | Mechanical tone and rigid phrasing |
| Dutch | 86.8 | Slightly stiff phrasing and literal translations |
| Polish | 84.4 | Overly literal phrasing lacking fluency |
| Thai | 84.1 | Unnatural conversational markers and stiff phrasing |
| Galician | 81.3 | Portuguese influence and unnatural phrasing |
| Indonesian | 80.2 | Terminology accuracy and fluency issues |
| Korean | 78.0 | Inappropriate untranslated English word "perplexing" |
| Russian | 74.7 | Untranslated English words disrupt fluency |
| Danish | 73.7 | Grammatical errors and awkward phrasing |
| Czech | 73.2 | Code-switching and linguistic inconsistencies |
| Nepali | 72.2 | Unnatural fluency and grammar |
| Afrikaans | 71.6 | Multiple severe lexical and grammatical errors |
| Hebrew | 71.3 | Significant mechanical errors in non-English vocalizations |
| Hindi | 69.0 | Mistranslation of interjections as pronouns |
| Norwegian | 67.7 | Significant linguistic and grammatical errors |
| Finnish | 66.7 | Severe grammatical and structural errors |
| Arabic | 65.7 | Mixed language intrusion |
| Malay | 65.5 | Severe structural and linguistic integrity issues |
| Ukrainian | 65.3 | Mixed Chinese characters in Ukrainian text |
| Vietnamese | 64.2 | Severe mixed-language intrusions |
| Serbian | 61.3 | Heavy code-switching and poor lexical selection |
| Romanian | 60.9 | Systematic grammatical errors and awkward phrasing |
| Catalan | 60.5 | Frequent grammatical errors and incorrect vocabulary |
| Marathi | 59.8 | Severe language mixing and code-switching |
| Slovak | 59.1 | Major mixing with Czech and severe grammatical errors |
| Turkish | 59.1 | Incoherent German phrases mixed in with Turkish text |
| Urdu | 55.9 | Mixed language fragments and random characters |
| Croatian | 52.9 | Poor quality with significant errors |
| Slovene | 52.1 | Severe grammatical errors and nonsensical phrases |
| Interlingua | 50.5 | Severe language mixing |
| Tagalog | 49.5 | Severe grammatical errors and gibberish output |
| Esperanto | 49.3 | Severe linguistic instability and machine-translation artifacts |
| Bulgarian | 46.1 | Severe contamination by untranslated English and Chinese |
| Lithuanian | 42.4 | Catastrophic semantic failures and gibberish |
| Latvian | 41.9 | Severe grammatical and lexical errors |
| Swahili | 41.8 | Catastrophic semantic errors and offensive vocabulary |
| Hungarian | 39.9 | Severe linguistic breakdowns and mixed languages |
| Bengali | 39.8 | Catastrophic structural errors and script mixing |
| Macedonian | 38.9 | Heavy language pollution and corruption |
| Albanian | 38.0 | Severe grammatical and lexical errors |
| Persian | 36.0 | Severe multilingual contamination |
| Telugu | 35.6 | Mixed languages and severe errors |
| Icelandic | 35.0 | Severe hallucinations and fabricated words |
| Estonian | 34.6 | Severe corruption with nonsense words and grammar errors |
| Malayalam | 34.6 | Severe code-mixing and fragmentation |
| Greek | 30.5 | Severe language mixing and garbled grammar |
| Tamil | 30.2 | Severe linguistic contamination |
| Welsh | 30.0 | Majority English fragments and gibberish Welsh |
| Belarusian | 29.4 | Severely corrupted and unintelligible mixed-language text |
| Kannada | 29.4 | Severe language mixing and hallucination |
| Burmese | 28.4 | Extremely low quality, nonsensical hybrid text |
| Lao | 27.9 | Incomprehensible gibberish due to severe lexical and grammatical errors |
| Azerbaijani | 26.6 | Severe grammatical errors and lexical hallucinations |
| Irish | 25.4 | Severe grammatical errors and mixed languages |
| Mongolian | 20.4 | Complete failure with gibberish and mixed languages |
| Sinhala | 16.8 | Severe machine-translation artifacts |
| Basque | 16.7 | Nonsensical gibberish with Chinese intrusion |
| Armenian | 16.6 | Corrupted noise from multiple languages |
| Georgian | 13.1 | Severe mixed-language pollution and structural defects |
| Khmer | 8.9 | Severe hallucination and repetition loop |
