# examples/tr/onde/gpt-oss/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: `gpt-oss:120b` (Ollama)
- Evaluation model: jev-1.13.0 (qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

**Note**: `gpt-oss:120b` cannot disable CoT (thinking process) output, so translation takes a very long time. Running translation in this directory is intended purely for quality verification.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 78.3 | Severe structural and formatting errors |
| Spanish | 77.8 | Frequent misattribution of dialogue lines |
| Arabic | 74.0 | Mechanical dialogue attribution errors |
| Russian | 71.6 | Severe speaker misalignment |
| Romanian | 71.3 | Severe structural and editing errors |
| Japanese | 71.2 | Inconsistent dialogue attribution |
| Swedish | 71.2 | Inconsistent speaker tags and missing attributions |
| Hungarian | 70.5 | Structural chaos and grammatical errors |
| Ukrainian | 70.4 | Significant structural integrity issues with speaker labels |
| Thai | 70.0 | Inconsistent speaker attribution |
| Tagalog | 69.9 | Severe terminology errors and unnatural phrasing |
| Catalan | 69.4 | Missing speaker labels |
| Bulgarian | 68.7 | Severe dialogue attribution loss |
| Slovak | 68.7 | Major formatting breakdown and awkward syntax |
| Chinese | 68.3 | Inconsistent dialogue tagging |
| Czech | 68.0 | Structural instability and grammatical errors |
| Polish | 68.0 | Missing speaker labels |
| Belarusian | 67.5 | Terminological inaccuracies and unnatural phrasing |
| Galician | 67.5 | Incomplete and structurally defective translation |
| Vietnamese | 67.0 | Broken speaker attribution and formatting errors |
| Hebrew | 66.8 | Flawed dialogue attribution and translation accuracy |
| Dutch | 66.8 | Severe structural errors and inconsistencies |
| Slovene | 66.8 | Severe structural and formatting defects |
| Indonesian | 66.2 | Severe formatting errors and structural flaws |
| Korean | 66.2 | Inconsistent speech levels and formatting errors |
| Macedonian | 66.2 | Severe structural and grammatical defects |
| Malay | 66.2 | Lack of dialogue speaker labels |
| Icelandic | 65.8 | Systematic failure to translate psi squared |
| Italian | 65.6 | Missing speaker tags |
| Lithuanian | 65.5 | Severe structural and editorial failures |
| Turkish | 65.5 | Critical dialogue attribution errors |
| Portuguese | 65.3 | severe structural and coherence errors |
| German | 65.2 | Broken speaker attribution |
| Norwegian | 65.2 | Missing speaker attributions |
| Finnish | 64.8 | Catastrophic structural and terminological errors |
| Welsh | 64.7 | Critical mechanical failures and pervasive linguistic errors |
| Serbian | 64.3 | Broken dialogue structure and repetition |
| Tamil | 64.1 | Unnatural syntax and awkward interjections |
| Hindi | 63.9 | Missing speaker labels and untranslated English words |
| Persian | 63.8 | Broken dialogue structure and missing content |
| Latvian | 63.8 | Critical grammatical errors and unnatural phrasing |
| Albanian | 63.8 | Severe structural and grammatical flaws |
| Estonian | 63.6 | Missing speaker tags and omissions |
| Urdu | 63.5 | Missing speaker attribution |
| Esperanto | 63.2 | Missing speaker labels and grammar errors |
| Armenian | 62.9 | Lexical errors reversing meaning |
| Bengali | 62.7 | Severe fluency and structural defects |
| Swahili | 61.9 | Severe systematic errors rendering text unintelligible |
| Danish | 61.5 | Missing speaker labels and untranslated fillers |
| Azerbaijani | 60.9 | Unattributed dialogue lines |
| Khmer | 60.9 | Severe language mixing and script corruption |
| Basque | 60.8 | Severe speaker labeling inconsistencies |
| Kannada | 60.5 | Severe fluency and terminology issues |
| Afrikaans | 60.1 | Severe structural defects and missing content |
| Interlingua | 60.0 | Inconsistent dialogue tags |
| Marathi | 60.0 | Severe speaker attribution and script errors |
| Greek | 59.5 | Severe dialogue formatting breakdown |
| Nepali | 59.1 | Inconsistent speaker attribution |
| Malayalam | 59.0 | Systematic text loss and missing dialogue |
| Burmese | 59.0 | Severe accuracy and coherence issues |
| Mongolian | 58.8 | Structural breakdowns and grammar errors |
| Croatian | 57.8 | Missing content and intrusive meta-text |
| Irish | 54.6 | Systematic misuse of vocabulary and severe grammatical errors |
| Sinhala | 52.9 | Severe degradation and unreadability |
| Georgian | 52.7 | Unintelligible and broken |
| Telugu | 50.7 | Severe mixed-language and formatting errors |
| Lao | 50.4 | Severe lexical and grammatical errors |

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
