# Hybrid Mode Translation Experiment

An experiment directory that extends the [experimental/02](../02/) summary compression method by implementing **hybrid mode** for CoT-capable models.

## Background and motivation

experimental/02 adopted `--no-think` to avoid history bloat and cache misses from CoT. Meanwhile, summary generation is a scenario where CoT shines, since it requires "synthesizing multiple pieces of information into a judgment." In this experiment:

- **Translation itself**: no CoT (ensures speed and stability)
- **Summary generation**: with CoT (improves accuracy; since it's infrequent, the extra cost is limited)
- **The summary is excluded from history**: the translation history is never polluted by the summary and consists purely of translation pairs. The summary is only injected at the reorganization point

This lets CoT-driven refinement concentrate on the summary while maintaining KV cache efficiency in the translation loop.

## Translation system

Scripts must always be run with `uv run`.

### translate.py

```bash
uv run translate.py <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**Options:**

| Option | Default | Description |
|---|---|---|
| `--threshold` | 20 | Interval (in translation pairs) between summary generations |
| `--keep` | 5 | Number of translation pairs between a summary and reorganization |
| `--no-think` | none | Disable CoT for summary generation (translation always runs without CoT) |

experimental/02's `--summary` / `--schema` / `--no-summary-history` were dropped and replaced with fixed behavior. Glossary and removing the summary from history are now always active.

### Operating spec (threshold=20, keep=5)

| Translation i | Behavior |
|---|---|
| 1-20 | Translate (no CoT). Accumulates in chat_history |
| Right after 20 completes | **Generate summary (with CoT) → remove from history** (chat_history stays as translations 1-20) |
| 21-25 | Translation continues. Unpolluted by the summary, so KV cache stays active |
| Right after 25 completes | **Reorganize**: `chat_history = [system, summary1, the 5 pairs 21-25]` |
| 26-40 | Translation continues (appends to the reorganized history) |
| Right after 40 completes | Generate summary (merging the previous summary1) → remove from history |
| 41-45 | Translation continues |
| Right after 45 completes | Reorganize: `[system, summary2, 41-45]` |
| ... | ... |

- Summary timing: `i % threshold == 0` → 20, 40, 60, ...
- Reorganization timing: `keep` lines after the summary → 25, 45, 65, ...
- If a reorganization near the end would exceed the entry count (`i + keep > len(entries)`), the summary is skipped

### batch.sh

```bash
bash batch.sh
```

Runs **3 translation runs × 3 evaluation runs** for the 3 models in [MODELS.txt](MODELS.txt) (qwen3.6-27b, gemma4-26b, gemma4-e4b). experimental/02 measured only "evaluation variance" with 1 translation run × 3 evaluations, but this experiment also measures translation variance since narrowing down the model list left more time budget.

**File naming:**

```
tr/<model>-<trrun>.txt                     e.g. tr/qwen3.6-27b-1.txt
evals/<model>-<trrun>-eval-<evrun>.json    e.g. evals/qwen3.6-27b-1-eval-1.json
```

3 models × 3 translation runs × 3 evaluation runs = 27 evaluation files are generated, then aggregated per translation run into [SCORES.txt](SCORES.txt).

## Target models

Narrowed down to the top 3 models based on experimental/02's Phase B results. All support CoT and fit within a practical resource range.

| Model | experimental/02 score | Characteristics |
|---|:---:|---|
| qwen3.6-27b | 97 | High accuracy in think mode |
| gemma4-26b | 97 | Highest score stability (range of 1), zero structural flaws |
| gemma4-e4b | 95 | Lightweight, yet perfect information completeness across all 3 evaluations |

The experimental/02 score is from Phase B (`--summary glossary`, `--no-think`, 1 translation run, median of 3 evaluations). See [experimental/02/README.md](../02/README.md) for details.

### KV cache behavior

- **gemma4 series (26b, e4b)**: KV cache active. Fast prefill during the translation loop.
  - **Right after the summary (with CoT)**: the KV cache becomes inactive. See [20/README.md](20/README.md) for measured values.
  - **Right after the summary (without CoT)**: the cache stays active even after the summary. Confirmed with measured values (gemma4-26b: translation 10 at 0.33s → translation 11 at 0.12s; gemma4-e4b: translation 10 at 0.08s → translation 11 at 0.05s) in the 10-nt trial.
- **qwen3.6-27b**: behavior unclear. Translations 1-7 are cold (no cache), with duration scaling with token count, then the cache suddenly kicks in from 8 onward. However, duration still keeps increasing linearly afterward. (Possibly related to using internal tags to switch CoT modes?)

## Evaluation system

Uses the [experimental/01](../01/) evaluation pipeline as-is. See [experimental/02/README.md](../02/README.md) for details.

- Evaluator: `ollama:qwen3.6`
- 5 items × 20 points = 100 points max
- Aggregation: median of 3 evaluation runs

## Trials

| Trial | Script | threshold | Summary CoT | Result |
|---|---|:---:|:---:|---|
| [20/](20/) | translate.py | 20 | yes | gemma4-26b most stable (96, 96, 100). Confirmed the risk of glossary early-mistranslation lock-in |
| [10/](10/) | translate.py | 10 | yes | qwen3.6-27b's plunge resolved (95, 94, 95). gemma4-e4b underperformed (88, 87, 92) |
| [10-nt/](10-nt/) | translate.py | 10 | no | gemma4-26b performed best (95, 99, 96). Plunge runs occurred for qwen3.6/e4b |
| [exp2/](exp2/) | experimental/02/translate.py | 10 | no | comparison trial using experimental/02 settings. Plunge runs occurred for qwen3.6/e4b |

## Comparison of results

Summary of scores across all trials (plunge runs in bold):

| Model | exp2/ (th=10) | 20/ (th=20) | 10/ (th=10) | 10-nt/ (th=10) |
|---|:---:|:---:|:---:|:---:|
| qwen3.6-27b | **84** / 96 / 95 | 95 / 94 / **87** | 95 / 94 / 95 | 96 / **86** / 94 |
| gemma4-26b | 96 / **98** / 96 | 96 / 96 / **100** | **97** / 94 / **97** | 95 / **99** / 96 |
| gemma4-e4b | 95 / **83** / 94 | 96 / **68** / 94 | 88 / 87 / 92 | 95 / 96 / **84** |

For gemma4-26b, bold marks a high-score run; for the other models, bold marks a plunge run.

### Comparison across configurations

Plunges occurred in every configuration, so they don't depend on a specific setting. exp2/ (experimental/02's settings) also had plunges for qwen3.6-27b and gemma4-e4b, confirming this is a random phenomenon caused by variance in initial glossary accumulation.

- **qwen3.6-27b**: 1 run plunged to 84-87 points in every trial. The runs without a plunge stayed at 94-96 points, so the underlying quality is high.
- **gemma4-26b**: no plunges in any trial or run. Scores ranged 94-100, with differences between configurations within the margin of error.
- **gemma4-e4b**: plunge risk exists in every configuration. threshold=20 (20/) produced the most extreme plunge (68 points), suggesting the damage from a plunge is larger there than in other configurations. However, exp2/ (threshold=15) also had a run with an eval-1 of 68 points, suggesting the probabilistic variance of initial glossary accumulation dominates over differences in threshold. threshold=10 (10/) eliminated the plunges but underperformed overall (87-92 points), showing a trade-off between plunge risk and average quality.

Since CoT only applies to summary generation and never to translation itself, the presence or absence of summary CoT (10/ vs 10-nt/) produces no meaningful difference in translation quality.

### Comparison with experimental/02 (effect of removing the summary from history)

exp2/ used the same settings as experimental/02 (keeping the summary in translation history), translated 3 times. Comparing it with 10-nt/ (summary excluded from history) provides a fair test of hybrid mode's effect:

| Model | exp2/ (kept in history) | 10-nt/ (excluded from history) |
|---|:---:|:---:|
| qwen3.6-27b | **84** / 96 / 95 | 96 / **86** / 94 |
| gemma4-26b | 96 / **98** / 96 | 95 / **99** / 96 |
| gemma4-e4b | 95 / **83** / 94 | 95 / 96 / **84** |

- **qwen3.6-27b, gemma4-26b**: the depth and level of plunges are comparable, no visible difference.
- **gemma4-e4b**: exp2/'s plunge run (83 points) includes an eval-1 of 68 points, while 10-nt/'s plunge run (84 points) has a minimum eval of 82 points. This is consistent with the theoretical prediction that inserting a stylistically different summary text into the translation history makes the style more prone to disruption. However, with only 3 runs, this is too small a sample to be conclusive and should be treated as a trend.

The KV cache efficiency benefit that is hybrid mode's design goal was achieved without a quality trade-off (and even with a hint of improvement for the smaller model).

## Conclusion

No significant difference in translation quality was found based on threshold or the presence of CoT. Plunges occur probabilistically in every configuration due to variance in initial glossary accumulation. Hybrid mode, which excludes the summary from translation history (10-nt), shows a hint of smaller damage during plunges for gemma4-e4b, and is also theoretically sound in avoiding interference with translation style. The one exception is gemma4-e4b, where plunge damage was largest at threshold=20, suggesting a possible impact of long-context load on smaller models.

From a processing-time standpoint, **threshold=10 with no CoT (10-nt) is recommended**. Translation always runs without CoT, and disabling CoT for the summary as well speeds up summary generation. There's no quality downside, and KV cache efficiency is maintained.

Recommendations by model:

- **gemma4-26b**: top recommendation. Stable and high-quality across every configuration with no plunges. Since the evaluator is from the qwen3.6 family (a different architecture), this high rating is a reliable, independent judgment.
- **gemma4-e4b**: an alternative under resource constraints. Plunge risk remains, but threshold=10 secures reasonable quality.
- **qwen3.6-27b**: little compelling reason to adopt. Carries plunge risk, doesn't benefit from the KV cache, and takes longer to process.

The sample size of each trial (3 translation runs) is too small for statistical certainty, and it's hard to definitively attribute score differences to configuration effects. That said, this experiment surfaced theoretical points not visible at the experimental/02 stage — the risk of style interference from keeping the summary in translation history, and long-context load on smaller models — which is itself meaningful.
