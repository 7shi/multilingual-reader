# Experiment 16: PLaMo 3 Translate 0.8B over Every Language

The first run of `examples/tr/plamo/plamo-3-translate-0.8b/` over all 67 target languages, before the target languages were narrowed to the ones the [model card](https://huggingface.co/pfnet/plamo-3-translate-0.8b) lists as supported. The languages were left unnarrowed on purpose, to set the model card's list against what the language check finds.

**Answer: the list holds.** Outside it, every language but Chinese came out in another language, mixed or collapsed, so the benchmark now translates only the listed languages.

**Status**: frozen, 2026-11-08.

The translations under `tr/` are outputs of PLaMo 3 Translate 0.8B (`plamo-3-translate-0.8b-Q4_K_M.gguf`), provided under the [PLaMo Community License](https://plamo.preferredai.jp/info/plamo-community-license-en).

## Setup

- `trtools plamo` at the time: the whole of `onde-en.txt` in one request per language, the target language's whole column of `examples/tr/terms/onde-en.tsv` as the glossary, temperature 0. `zh` was sent as it is, before it was mapped to the model's `zh-hans`
- `llama-server -c 16384 --jinja --no-prefill-assistant`
- Jev (`jev-1.14.0`), the language check (`langcheck.jsonl`), `SCORES-jev.txt` and `TREND-jev.jsonl` as `make` writes them

## Supported Languages (44 of the Corpus)

- **36 came through whole**: 99 lines, all `ok` in the language check. Italian 79.2, Indonesian 79.0 and Spanish 77.4 lead, down to Estonian at 49.1
- **5 were cut off by the context window**: Khmer (69 lines), Burmese (46), Telugu (64), Malayalam (72) and Sinhala (69). These scripts take many tokens; for Khmer the source's 1,540 tokens, the glossary and the template plus 12,011 output tokens reached the server's 16,384. `trtools plamo` warned only of the line count, since its runaway guard is a character limit of its own and the server's stop was not reported
- **2 split lines**: Bengali (102 lines) and Armenian (100, the last line without its speaker tag), both `ok`
- **Serbian is `wrong`**: Latin script, mostly Serbian (ekavian *sveta*, *vreme*, *razumem*, *ko*), with Croatian *točno* six times and *što* five. fastText gave Serbian 0.39, and Jev Croatian 0.71

## Unsupported Languages (23 of the Corpus)

- **Chinese** (66.8, `ok`): Simplified Chinese, although `zh` is not one of the model's codes
- **Albanian** (38.0, `ok`): a mixture of Albanian (*Urat në Fizikë*, *fizikan teorik*), Cebuano (*ug*, *sa*, *kita*) and Serbo-Croatian (*Točno tako*, *svakodnevnog života*). Jev read it as Albanian at 0.96; a mixture line by line is outside what the language check sees
- **Kannada** (1.7, `ok`): one line of collapsed text, in Kannada script
- **20 are `wrong`**, in a supported language:
  - a related one: Portuguese, Swedish, Romanian, Icelandic and Greek as Spanish, Ukrainian as Polish, Afrikaans and Norwegian as Dutch, Interlingua as Italian, Finnish and Czech as Hungarian, Danish as Low German
  - an unrelated script: Turkish as Korean, Esperanto as Armenian, Mongolian as Bengali, Lao as Hebrew, Irish as Gujarati, Macedonian as Khmer, Galician as Sinhala, Welsh as Telugu
  - several also collapsed: Danish (1 line), Icelandic (4), Welsh (6), Macedonian (17), Galician (41)

The language check zeroed every translation that is not in its target language except the mixed Albanian; the collapsed Kannada is in the right script and Jev scores it near 0.

## Translation Quality Overview

As `trtools trend --jev --sync` wrote it into the model's README.

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Italian | 79.2 | Careless lexical errors and stylistic rigidities |
| Indonesian | 79.0 | Awkward phrasing and non-idiomatic expressions |
| Spanish | 77.4 | awkward literal calques and gender errors |
| Vietnamese | 76.2 | Severe mistranslation of physics terms |
| Hungarian | 76.1 | Significant grammatical errors and non-standard terminology |
| French | 73.6 | Frequent grammatical errors and awkward phrasing |
| Japanese | 73.6 | Critical physics error regarding lambda over two |
| Malay | 73.0 | Severe mistranslations and awkward phrasing |
| Georgian | 71.7 | Pervasive grammatical errors and awkward phrasing |
| Dutch | 71.2 | Multiple severe language mixing and terminology errors |
| Swahili | 70.2 | Severe literalism and lexical inaccuracies |
| Arabic | 68.8 | Mechanical syntax hindering fluency |
| Croatian | 68.8 | Severe grammatical and terminology errors |
| Korean | 68.8 | Critical scientific mistranslation of wavelength limit |
| Thai | 68.3 | Severe gender and pronoun inconsistency |
| Chinese | 66.8 | Systematic mistranslation of mathematical notation and prepositions |
| Catalan | 66.1 | Grammar, typos, and technical inaccuracies |
| German | 65.0 | Grammatical errors and awkward phrasing |
| Hindi | 64.6 | Severe terminology errors and unnatural phrasing |
| Nepali | 63.0 | Inconsistent speaker attribution |
| Bulgarian | 61.4 | Severe grammatical errors and mixed scripts |
| Slovene | 61.3 | Severe grammatical errors and incorrect terminology |
| Polish | 60.6 | Severe systemic errors and grammatical breakdowns |
| Urdu | 59.5 | Heavy literalism and terminology errors |
| Khmer | 58.8 | Incomplete and critically flawed |
| Azerbaijani | 58.4 | Significant Chinese script intrusion and lexical errors |
| Burmese | 58.4 | Critically incomplete and truncated |
| Hebrew | 57.1 | Severe gibberish and nonsensical neologisms |
| Russian | 57.1 | Severe grammatical and lexical errors |
| Tamil | 57.1 | Significant scientific inaccuracies and poor fluency |
| Telugu | 57.0 | Severe incompleteness and technical errors |
| Marathi | 56.6 | Severe lexical and syntactic errors |
| Persian | 56.3 | Severe terminology errors and nonsensical phrases |
| Bengali | 56.2 | Severe hallucination and meaning distortion |
| Slovak | 54.5 | Severe grammatical and terminology errors |
| Latvian | 54.2 | Severe linguistic degeneration and nonsensical output |
| Armenian | 53.8 | Severe translation errors and nonsense phrases |
| Tagalog | 53.3 | Severe linguistic inconsistencies and mixed languages |
| Belarusian | 52.6 | Severe errors in orthography and terminology |
| Basque | 51.9 | Severe linguistic errors |
| Lithuanian | 51.3 | Catastrophic semantic and terminology errors |
| Malayalam | 50.9 | Severe truncation cuts off the end |
| Estonian | 49.1 | Severe grammatical failures and corrupted data insertion |
| Albanian | 38.0 | Fundamentally flawed mixed-language gibberish |
| Sinhala | 33.4 | severe structural breakdowns and repetition |
| Kannada | 1.7 | Incomplete repetitive nonsense |
| Afrikaans | 0.0 | Not in the target language (detected: Dutch) |
| Czech | 0.0 | Not in the target language (detected: Hungarian) |
| Welsh | 0.0 | Not in the target language (detected: Telugu) |
| Danish | 0.0 | Not in the target language (detected: Low German) |
| Greek | 0.0 | Not in the target language (detected: Spanish) |
| Esperanto | 0.0 | Not in the target language (detected: Armenian) |
| Finnish | 0.0 | Not in the target language (detected: Hungarian) |
| Irish | 0.0 | Not in the target language (detected: gu) |
| Galician | 0.0 | Not in the target language (detected: Sinhala) |
| Interlingua | 0.0 | Not in the target language (detected: Italian) |
| Icelandic | 0.0 | Not in the target language (detected: Spanish) |
| Lao | 0.0 | Not in the target language (detected: Hebrew) |
| Macedonian | 0.0 | Not in the target language (detected: Khmer) |
| Mongolian | 0.0 | Not in the target language (detected: Bengali) |
| Norwegian | 0.0 | Not in the target language (detected: Dutch) |
| Portuguese | 0.0 | Not in the target language (detected: Spanish) |
| Romanian | 0.0 | Not in the target language (detected: Spanish) |
| Serbian | 0.0 | Not in the target language (detected: Croatian) |
| Swedish | 0.0 | Not in the target language (detected: Spanish) |
| Turkish | 0.0 | Not in the target language (detected: Korean) |
| Ukrainian | 0.0 | Not in the target language (detected: Polish) |
