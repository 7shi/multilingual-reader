# examples/tr/onde/gemma4-12b/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen.

- Translation model: gemma4:12b-it-qat
- Evaluation model: jev-1.14.0 (jev-1.13.0 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

> [!NOTE]
> During translation, the model often stopped responding partway through, and the run had to be stopped by hand and restarted. None of the other models behaved this way.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 92.8 | Minor literalness in transitions |
| French | 90.9 | Typographic convention errors |
| Vietnamese | 89.0 | Occasional unnatural conversational fillers |
| Dutch | 88.9 | Inconsistent terminology and calques |
| Arabic | 88.8 | Retains overly literal style |
| Portuguese | 88.0 | Significant semantic error with ingenuity |
| Russian | 87.8 | Inconsistent informal/formal pronouns and literal phrasing |
| Norwegian | 87.2 | Poor mathematical notation handling |
| Italian | 86.6 | Retained English interjections |
| Danish | 85.2 | Unnatural phrasing and grammar errors |
| Ukrainian | 83.5 | Somewhat rigid literal style |
| Indonesian | 82.2 | Stiff phrasing and lack of fluency |
| Polish | 81.2 | Significant mechanical and lexical errors |
| Chinese | 81.1 | Notable Chinglish glitch |
| Turkish | 80.6 | Unnatural phrasing and vocabulary errors |
| Serbian | 79.7 | Grammar and syntax errors |
| Thai | 79.4 | Presence of untranslated English text |
| Hindi | 79.0 | Lacks linguistic naturalness |
| Swedish | 78.6 | Severe literal mistranslation of greetings |
| Malay | 76.3 | Pervasive code-switching disrupts fluency |
| Japanese | 75.8 | Mixed-language character intrusions |
| Korean | 74.3 | Translationese hinders fluency |
| Finnish | 72.2 | Numerous severe mechanical and terminology errors |
| Hebrew | 71.6 | Numerous typographical and transliteration errors |
| Bulgarian | 70.8 | Mixed language in final paragraph |
| Persian | 70.2 | Repeated English mixing and untranslated words |
| Nepali | 69.8 | Major language mixing errors |
| German | 68.9 | Severe technical corruption and language mixing |
| Galician | 67.2 | Severe semantic errors and non-words |
| Swahili | 66.1 | Severe grammatical errors and nonsensical phrases |
| Tagalog | 65.2 | Severe multilingual intrusion and inconsistent phrasing |
| Urdu | 65.2 | Severe orthographic and terminology errors |
| Azerbaijani | 64.4 | Presence of Chinese characters |
| Catalan | 64.2 | Presence of Chinese characters |
| Khmer | 63.1 | Severe mixed-language errors and untranslated code |
| Sinhala | 63.0 | Inclusion of Chinese characters |
| Croatian | 62.9 | Severe mixed languages and gibberish |
| Malayalam | 62.9 | Severe script and language mixing |
| Czech | 62.7 | Intrusion of foreign languages and scripts |
| Afrikaans | 60.1 | Severe lexical errors and malapropisms |
| Albanian | 59.5 | Severe word corruption and grammatical breakdown |
| Bengali | 59.4 | Erratic mixing of multiple languages |
| Burmese | 59.4 | Foreign script artifacts |
| Telugu | 57.3 | Severe language contamination |
| Marathi | 55.1 | Severe code-switching and grammatical errors |
| Lao | 54.5 | Severe mixed language intrusions |
| Romanian | 54.1 | Severe multilingual contamination |
| Tamil | 53.8 | Extensive code-switching with foreign languages |
| Macedonian | 52.2 | Massive copy-paste corruption with inserted English text |
| Slovak | 49.5 | Severe mixed-language contamination |
| Mongolian | 48.6 | Unintelligible due to foreign language intrusions |
| Slovene | 48.1 | Severe lexical and grammatical errors |
| Kannada | 47.3 | Severe mixed-language contamination |
| Latvian | 45.7 | Severe corruption with mixed scripts |
| Greek | 44.5 | Severe code-switching with foreign languages |
| Belarusian | 43.9 | Severe structural defects and mixed scripts |
| Interlingua | 43.8 | Severe linguistic degradation and non-existent vocabulary |
| Hungarian | 43.1 | Severe foreign language intrusion |
| Esperanto | 42.2 | Massive code-switching to other languages |
| Georgian | 41.0 | Catastrophic mixed-language corruption |
| Icelandic | 40.0 | Severe lexical and grammatical errors |
| Lithuanian | 39.3 | Severe catastrophic failure with mixed scripts |
| Armenian | 38.3 | Severe language mixing and incoherence |
| Estonian | 37.0 | Presence of untranslated Chinese characters |
| Basque | 30.2 | Incomprehensible and structurally chaotic |
| Welsh | 27.8 | Severe grammatical breakdown and nonsensical output |
| Irish | 20.7 | Fundamentally broken and unintelligible |
