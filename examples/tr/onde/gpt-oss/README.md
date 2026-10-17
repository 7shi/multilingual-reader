# examples/tr/onde/gpt-oss/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, aggregation, and the trend column in one batch. Translations go to `tr/`, Jev's evaluations to `jev.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `jev-1.13.0/` holds the same three files from jev-1.13.0, kept frozen. `evals/`, `SCORES.txt`, and `TRENDS.jsonl` are the record of the previous evaluator, qwen3.6.

- Translation model: `gpt-oss:120b` (Ollama)
- Evaluation model: jev-1.14.0 (jev-1.13.0 and qwen3.6 before it)
- Trend column: written by qwen3.6 from Jev's scores
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

**Note**: `gpt-oss:120b` cannot disable CoT (thinking process) output, so translation takes a very long time. Running translation in this directory is intended purely for quality verification.

## Translation quality overview

The score is Jev's total, and the trend analysis is a phrase written by qwen3.6 to describe it (`trtools trend --jev`), as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| French | 75.3 | Severe structural and formatting errors |
| Spanish | 74.7 | Frequent misattribution of dialogue lines |
| Russian | 74.2 | Severe speaker misalignment |
| Arabic | 72.7 | Mechanical dialogue attribution errors |
| Ukrainian | 71.3 | Significant structural integrity issues with speaker labels |
| Romanian | 71.2 | Severe structural and editing errors |
| Hungarian | 70.3 | Structural chaos and grammatical errors |
| Portuguese | 70.3 | severe structural and coherence errors |
| Swedish | 70.1 | Inconsistent speaker tags and missing attributions |
| Dutch | 69.9 | Severe structural errors and inconsistencies |
| Japanese | 69.7 | Inconsistent dialogue attribution |
| Italian | 69.4 | Missing speaker tags |
| Slovak | 68.9 | Major formatting breakdown and awkward syntax |
| Polish | 68.5 | Missing speaker labels |
| Indonesian | 68.2 | Severe formatting errors and structural flaws |
| Chinese | 67.9 | Inconsistent dialogue tagging |
| Persian | 67.8 | Broken dialogue structure and missing content |
| Catalan | 67.5 | Missing speaker labels |
| Latvian | 67.2 | Critical grammatical errors and unnatural phrasing |
| Slovene | 67.2 | Severe structural and formatting defects |
| Bulgarian | 67.0 | Severe dialogue attribution loss |
| Thai | 66.9 | Inconsistent speaker attribution |
| Tagalog | 66.9 | Severe terminology errors and unnatural phrasing |
| German | 66.5 | Broken speaker attribution |
| Macedonian | 66.2 | Severe structural and grammatical defects |
| Belarusian | 66.0 | Terminological inaccuracies and unnatural phrasing |
| Serbian | 65.8 | Broken dialogue structure and repetition |
| Turkish | 65.7 | Critical dialogue attribution errors |
| Malay | 65.5 | Lack of dialogue speaker labels |
| Armenian | 65.4 | Lexical errors reversing meaning |
| Galician | 65.3 | Incomplete and structurally defective translation |
| Hebrew | 65.2 | Flawed dialogue attribution and translation accuracy |
| Vietnamese | 64.6 | Broken speaker attribution and formatting errors |
| Korean | 64.5 | Inconsistent speech levels and formatting errors |
| Welsh | 64.2 | Critical mechanical failures and pervasive linguistic errors |
| Hindi | 64.2 | Missing speaker labels and untranslated English words |
| Icelandic | 64.2 | Systematic failure to translate psi squared |
| Albanian | 64.0 | Severe structural and grammatical flaws |
| Tamil | 64.0 | Unnatural syntax and awkward interjections |
| Lithuanian | 63.8 | Severe structural and editorial failures |
| Basque | 63.2 | Severe speaker labeling inconsistencies |
| Finnish | 62.8 | Catastrophic structural and terminological errors |
| Czech | 62.5 | Structural instability and grammatical errors |
| Urdu | 62.4 | Missing speaker attribution |
| Danish | 62.3 | Missing speaker labels and untranslated fillers |
| Bengali | 62.0 | Severe fluency and structural defects |
| Marathi | 62.0 | Severe speaker attribution and script errors |
| Norwegian | 61.5 | Missing speaker attributions |
| Afrikaans | 61.3 | Severe structural defects and missing content |
| Burmese | 61.3 | Severe accuracy and coherence issues |
| Interlingua | 61.2 | Inconsistent dialogue tags |
| Khmer | 61.1 | Severe language mixing and script corruption |
| Estonian | 60.9 | Missing speaker tags and omissions |
| Croatian | 60.8 | Missing content and intrusive meta-text |
| Malayalam | 60.6 | Systematic text loss and missing dialogue |
| Esperanto | 60.5 | Missing speaker labels and grammar errors |
| Greek | 60.0 | Severe dialogue formatting breakdown |
| Swahili | 60.0 | Severe systematic errors rendering text unintelligible |
| Mongolian | 59.2 | Structural breakdowns and grammar errors |
| Nepali | 59.0 | Inconsistent speaker attribution |
| Kannada | 58.7 | Severe fluency and terminology issues |
| Azerbaijani | 58.1 | Unattributed dialogue lines |
| Georgian | 54.2 | Unintelligible and broken |
| Irish | 52.0 | Systematic misuse of vocabulary and severe grammatical errors |
| Telugu | 51.2 | Severe mixed-language and formatting errors |
| Sinhala | 50.9 | Severe degradation and unreadability |
| Lao | 48.0 | Severe lexical and grammatical errors |

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
