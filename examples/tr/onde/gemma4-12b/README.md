# examples/tr/onde/gemma4-12b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`.

- Translation model: gemma4:12b-it-qat
- Evaluation model: jev-1.13.0
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

> [!NOTE]
> During translation, the model often stopped responding partway through, and the run had to be stopped by hand and restarted. None of the other models behaved this way.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 92.1 | Typographic convention errors |
| Spanish | 91.8 | Minor literalness in transitions |
| Arabic | 89.8 | Retains overly literal style |
| Dutch | 89.1 | Inconsistent terminology and calques |
| Russian | 88.4 | Inconsistent informal/formal pronouns and literal phrasing |
| Vietnamese | 88.2 | Occasional unnatural conversational fillers |
| Ukrainian | 86.3 | Somewhat rigid literal style |
| Norwegian | 85.9 | Poor mathematical notation handling |
| Portuguese | 84.7 | Significant semantic error with ingenuity |
| Italian | 84.5 | Retained English interjections |
| Danish | 84.2 | Unnatural phrasing and grammar errors |
| Indonesian | 83.8 | Stiff phrasing and lack of fluency |
| Serbian | 81.2 | Grammar and syntax errors |
| Swedish | 79.8 | Severe literal mistranslation of greetings |
| Chinese | 79.8 | Notable Chinglish glitch |
| Polish | 78.8 | Significant mechanical and lexical errors |
| Turkish | 78.6 | Unnatural phrasing and vocabulary errors |
| Hindi | 78.4 | Lacks linguistic naturalness |
| Thai | 77.5 | Presence of untranslated English text |
| Malay | 75.5 | Pervasive code-switching disrupts fluency |
| Japanese | 74.3 | Mixed-language character intrusions |
| Korean | 73.8 | Translationese hinders fluency |
| Hebrew | 71.2 | Numerous typographical and transliteration errors |
| Bulgarian | 70.9 | Mixed language in final paragraph |
| Finnish | 69.7 | Numerous severe mechanical and terminology errors |
| Persian | 68.0 | Repeated English mixing and untranslated words |
| Nepali | 67.6 | Major language mixing errors |
| Tagalog | 66.5 | Severe multilingual intrusion and inconsistent phrasing |
| German | 64.8 | Severe technical corruption and language mixing |
| Swahili | 64.8 | Severe grammatical errors and nonsensical phrases |
| Malayalam | 62.7 | Severe script and language mixing |
| Galician | 62.5 | Severe semantic errors and non-words |
| Urdu | 62.4 | Severe orthographic and terminology errors |
| Khmer | 61.7 | Severe mixed-language errors and untranslated code |
| Czech | 59.8 | Intrusion of foreign languages and scripts |
| Bengali | 59.7 | Erratic mixing of multiple languages |
| Azerbaijani | 59.3 | Presence of Chinese characters |
| Catalan | 59.1 | Presence of Chinese characters |
| Sinhala | 58.8 | Inclusion of Chinese characters |
| Croatian | 56.8 | Severe mixed languages and gibberish |
| Telugu | 55.3 | Severe language contamination |
| Burmese | 54.4 | Foreign script artifacts |
| Albanian | 54.0 | Severe word corruption and grammatical breakdown |
| Romanian | 51.4 | Severe multilingual contamination |
| Afrikaans | 50.5 | Severe lexical errors and malapropisms |
| Lao | 50.0 | Severe mixed language intrusions |
| Tamil | 49.1 | Extensive code-switching with foreign languages |
| Marathi | 48.9 | Severe code-switching and grammatical errors |
| Slovak | 48.4 | Severe mixed-language contamination |
| Macedonian | 46.8 | Massive copy-paste corruption with inserted English text |
| Mongolian | 45.7 | Unintelligible due to foreign language intrusions |
| Slovene | 43.6 | Severe lexical and grammatical errors |
| Kannada | 41.4 | Severe mixed-language contamination |
| Greek | 41.3 | Severe code-switching with foreign languages |
| Interlingua | 41.3 | Severe linguistic degradation and non-existent vocabulary |
| Icelandic | 38.2 | Severe lexical and grammatical errors |
| Esperanto | 37.9 | Massive code-switching to other languages |
| Georgian | 36.9 | Catastrophic mixed-language corruption |
| Hungarian | 36.2 | Severe foreign language intrusion |
| Belarusian | 35.9 | Severe structural defects and mixed scripts |
| Latvian | 35.4 | Severe corruption with mixed scripts |
| Lithuanian | 35.2 | Severe catastrophic failure with mixed scripts |
| Armenian | 35.0 | Severe language mixing and incoherence |
| Estonian | 31.9 | Presence of untranslated Chinese characters |
| Basque | 26.0 | Incomprehensible and structurally chaotic |
| Welsh | 25.0 | Severe grammatical breakdown and nonsensical output |
| Irish | 17.5 | Fundamentally broken and unintelligible |
