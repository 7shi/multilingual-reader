# examples/tr/onde/gpt-oss/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch.

- Translation model: `gpt-oss:120b` (Ollama)
- Evaluation model: `qwen3.6` (Ollama)
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

**Output**: translations `tr/`, evaluations `evals/`, scores `SCORES.txt`

**Note**: `gpt-oss:120b` cannot disable CoT (thinking process) output, so translation takes a very long time. Running translation in this directory is intended purely for quality verification.

## Translation quality overview

The quality trend for each language, based on the evaluation results (`SCORES.txt`) and manual content verification, is as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 98 | Minor missing speaker tags |
| French | 97 | Professional quality with occasional missing speaker tags |
| Catalan | 96 | High quality with missing speaker tags |
| Italian | 95 | Inconsistent speaker attribution formatting |
| Japanese | 94 | Inconsistent omission of speaker tags |
| Vietnamese | 93 | Missing speaker labels disrupts flow |
| Portuguese | 90 | Speaker labels dropped; technical accuracy high |
| Swedish | 89 | Missing speaker tags and minor grammatical errors |
| Ukrainian | 88 | Missing speaker tags and literal phrasing |
| Dutch | 86 | Accurate content marred by formatting and fluency issues |
| Arabic | 83 | Minor fluency and formatting issues |
| German | 83 | Frequent omission of speaker attribution tags |
| Turkish | 83 | Minor formatting and phrasing issues |
| Afrikaans | 81 | Missing speaker labels disrupt dialogue format |
| Bulgarian | 80 | Missing speaker attribution and formatting inconsistencies |
| Czech | 80 | Missing speaker tags and minor errors |
| Galician | 80 | Missing speaker labels and gender errors |
| Russian | 79 | Systematic omission of speaker tags |
| Chinese | 79 | Missed speaker attribution tags |
| Indonesian | 78 | Structural formatting errors |
| Danish | 77 | Missing speaker tags and grammatical errors |
| Hungarian | 77 | Structural flaws and grammatical errors |
| Nepali | 77 | Systemic grammatical errors and typos |
| Macedonian | 75 | Lack of proofreading and structural errors |
| Persian | 74 | Missing speaker tags disrupt flow |
| Interlingua | 73 | Inconsistencies between evaluations on quality and errors |
| Slovene | 73 | Significant formatting errors and grammatical fractures |
| Slovak | 71 | Critical omission of speaker labels and minor typos |
| Urdu | 70 | Inconsistent scientific transliteration and terminology |
| Belarusian | 69 | Notable terminology errors and formatting issues |
| Malay | 69 | Significant terminology errors and missing speaker labels |
| Norwegian | 69 | Missing speaker tags and awkward calques |
| Polish | 67 | Missing speaker labels |
| Tagalog | 67 | Significant linguistic and grammatical flaws |
| Greek | 66 | Significant terminology and structural errors |
| Azerbaijani | 65 | Missing speaker tags disrupt dialogue format |
| Hebrew | 65 | Missing speaker labels and grammatical errors |
| Korean | 65 | Missing speaker tags disrupt readability |
| Finnish | 63 | Missing speaker labels and typos |
| Latvian | 61 | Missing speaker labels and grammatical errors |
| Serbian | 61 | Missing speaker tags and formatting issues |
| Marathi | 60 | Pervasive orthographic errors |
| Swahili | 58 | Significant scientific terminology errors |
| Esperanto | 57 | Missing dialogue speaker tags |
| Croatian | 57 | Severe formatting and structural defects |
| Romanian | 56 | Significant structural and formatting defects |
| Malayalam | 54 | Pervasive orthographic and grammatical errors |
| Albanian | 54 | Missing speaker tags and grammatical errors |
| Estonian | 53 | Severe grammatical errors and terminology inaccuracies |
| Welsh | 52 | severe grammatical and terminology flaws |
| Mongolian | 52 | Heavy machine-translation artifacts and terminology errors |
| Bengali | 50 | Severe orthographic and grammatical errors |
| Kannada | 49 | pervasive linguistic and technical defects |
| Lithuanian | 48 | Major structural and terminological defects |
| Basque | 45 | Systematic grammatical errors and missing speaker labels |
| Icelandic | 45 | Grammatical errors and awkward calques |
| Thai | 42 | Pervasive orthographic errors throughout |
| Armenian | 41 | Frequent lexical and critical mistranslations |
| Hindi | 39 | Major typographical and formatting defects |
| Telugu | 39 | Severe mixed-script corruption and pervasive grammatical errors |
| Burmese | 38 | Severe spelling errors |
| Sinhala | 33 | Pervasive orthographic errors and unnatural phrasing |
| Khmer | 32 | Systematic orthographic errors and rigid syntax |
| Georgian | 31 | Severe grammatical and structural errors |
| Tamil | 30 | Severe orthographic and grammatical errors |
| Irish | 29 | Major grammatical and terminology defects |
| Lao | 23 | Critical terminology errors and mixed language |

Overall, contrary to the model's scale, translation of low-resource languages was extremely unstable, with frequent multilingual contamination, leakage of situational awareness, and speaker-tag dropout.

## Past Experiment: Comparison with OpenRouter

Initially, the same process was run in parallel on both the local (Ollama) and cloud API (OpenRouter) environments to verify behavioral differences between providers. For stricter verification, the translations generated on OpenRouter were evaluated by both OpenRouter and Ollama (`evals/` and `evals-ollama/` under `openrouter/`).

The table below shows scores for the three combinations (ol: Ollama, or: OpenRouter).
- **ol-ol**: local translation, local evaluation (an excerpt of 8 languages from the past, from `SCORES.txt`)
- **or-ol**: cloud translation, local evaluation (`openrouter/SCORES-ollama.txt`)
- **or-or**: cloud translation, cloud evaluation (`openrouter/SCORES.txt`)

| Language | ol-ol | or-ol | or-or |
| :--- | :--- | :--- | :--- |
| Turkish | 83 | 89 | 87 |
| Korean | 65 | 81 | 80 |
| Serbian | 61 | 81 | 53 |
| Hindi | 39 | 68 | 67 |
| Esperanto | 57 | 30 | 33 |
| Telugu | 39 | 31 | 30 |
| Estonian | 53 | 24 | 20 |
| Kannada | 49 | 10 | 7 |
※ Only the 8 languages used at the time are covered.

This enables comparison from the following two perspectives.
- **Comparing execution environments for the translation model (ol-ol vs or-ol)**: fixing the evaluator to Ollama, the difference is which environment did the translation. Since each environment was only run once, it's not possible to distinguish whether score swings are provider differences or simple sampling noise. However, in either environment many low-resource languages still scored below 60, remaining impractical, so the outcome is effectively no different.
- **Comparing execution environments for the evaluation model (or-ol vs or-or)**: fixing translation to OpenRouter, the difference is which environment did the evaluation.

### Perfect Agreement in Error-Detection Ability

Using the same evaluation model (`qwen3.6`), it was proven that **whether local (Ollama) or cloud (OpenRouter), it has an identical ability (reading ability) to accurately detect and point out errors in the text — garbled text, other-language contamination, prompt leakage — down to the last detail**. The few-to-ten-point swings seen in scores aren't a difference in provider capability, but merely random noise from run to run (sampling).

Note that for Serbian, there was a large evaluation gap between `or-ol` (81) and `or-or` (53). Checking the evaluation logs, the OpenRouter-generated translation text contained a structural flaw partway through (a meaningless fragment, `Cam… ... ... ...`), and **both the Ollama and OpenRouter evaluation models accurately detected this same error**. However, while some of the Ollama-side evaluation runs dismissed this error as minor and gave a high score (91), the OpenRouter-side evaluation runs followed the guidelines and strictly deducted points for it as a "critical structural flaw" (24, 53, etc.), producing a large gap in the average score. This too isn't a difference in detection ability, but random variation in how strict the evaluation is (the weight given to the penalty).

### Difference in Structured-Output (JSON Format) Stability

As an important operational insight, a clear difference was observed between providers in how structured-output bugs manifest.

- **OpenRouter (cloud)**: structured output sometimes became unstable, with several cases where the `reasoning` field got "meaningless content" and the output broke. In this case, the JSON syntax itself remained valid, making programmatic error detection difficult and requiring visual inspection and manual re-runs.
- **Ollama (local)**: breakage from meaningless output content didn't occur, but instead the `overall_comment` field's output fell into an "infinite loop" at a certain rate. However, this is automatically retried by the tool's loop-detection feature, keeping the operational overhead low.

This suggests that building a fully automated pipeline requires error handling that accounts for each provider's own quirks in how hallucinations manifest.
