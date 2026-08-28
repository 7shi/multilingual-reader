# Experiment 06: Verifying Two-Stage Translation for Medium-Resource Languages

This directory verifies the effectiveness of "line-level refinement / two-stage translation (micro-level)" as an approach to improving translation quality for medium-resource languages (Dutch, Czech, etc.).

## Background and Purpose

Current medium-resource languages (e.g., Dutch, Czech — in the 70–85 point range) tend to plateau due to expression-level issues that don't involve grammatical breakdown, such as "literal-sounding phrasing" or "interference from neighboring languages."
In a previous experiment (`experimental/01`), complex processes such as reasoning-augmented translation and two-stage translation tended to backfire. However, this is likely because the language pair examined there — French → Spanish — was a "high-resource language pair," where direct translation already produced near-ceiling quality scores.
So we hypothesized that applying a "two-stage approach (refinement)" — reviewing and revising the translation output — to "medium-resource languages," which plateau at 70–85 points under direct translation, could resolve expression-level issues and raise the score.
As the simplest first test, we apply the previously implemented "line-level two-stage translation" and check whether it actually raises scores for medium-resource languages.

This experiment saves and evaluates both the draft translation (Draft) and the refined translation (Final), quantitatively comparing whether the refinement process actually contributes to score improvement.

## Comparison Baseline

Compared against the score of standard one-pass direct translation (equivalent to Level 0, with summary compression and term injection) under `examples/tr/onde/gemma4/`.
- Dutch: **78 points**
- Czech: **78 points**

## Script Structure

- **`translate.py`**:
  A dedicated script for this verification, extracting and restructuring just the two-stage translation functionality from `experimental/01/translate.py`. For each line, it runs a "draft translation → quality assessment/improvement suggestions → improved translation" process, outputting both the draft (Draft) and the final result (Final) simultaneously. Context is retained via a simple sliding context of the most recent 5 lines only.
- **`batch.sh`**:
  A batch script that fully automates translation, evaluation of both the draft and final translations, and aggregation.

## batch.sh Behavior

1. **Translation (two-stage translation)**
   - **Input**: `examples/onde-en.txt`
   - **Target languages**: Dutch (`nl`), Czech (`cs`)
   - **Translation model**: `ollama:gemma4:26b`
   - **Output** (4 files total):
     - Draft: `tr/onde-{lang}-draft.txt`
     - Final: `tr/onde-{lang}-final.txt`

2. **Evaluation**
   - **Evaluation model**: `ollama:qwen3.6`
   - `trtools eval` is run 3 times each for both the draft and final translations of each language, to account for score variance (2 languages × 2 types × 3 runs = 12 evaluations total).
   - **Output**:
     - Draft evaluations: `evals/onde-{lang}-draft-{1,2,3}.json`
     - Final evaluations: `evals/onde-{lang}-final-{1,2,3}.json`

3. **Aggregation**
   - `trtools agg` aggregates the median across all 12 evaluation result files, and writes the results to `SCORES.txt`.

## Results and Analysis

Running the batch script produced the following scores.

| Language | Baseline (one-pass direct translation) | Draft | Final (refined) |
| :--- | :---: | :---: | :---: |
| Dutch (nl) | 78 pts | 86 pts | **94 pts** |
| Czech (cs) | 78 pts | 56 pts | **72 pts** |

### Discussion
* **Dutch**: Already exceeded the baseline at the draft stage, and improved substantially to **94 points** after refinement, reaching the target 90s range. Line-level two-stage translation works very effectively here.
* **Czech**: The draft fell well below the baseline (78 points), scoring only 56 points. Refinement recovered it to 72 points, but this still fell short of one-pass direct translation.

**The Importance of Context Retention**
The likely cause of the Czech draft's sharp quality drop is that this `translate.py` operates with only a "simple sliding context of the most recent 5 lines." The baseline (78 points) was achieved by `trtools translate`, which retains context via "summary compression + term injection."
This shows that **while refinement (two-stage translation) does provide some benefit (56 → 72 points for Czech), context retention via KV-cache (summary compression) and term injection is essential before that.**
