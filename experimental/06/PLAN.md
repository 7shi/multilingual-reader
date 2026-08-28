# Future Action Plan

Based on the results of experiment 06 (verifying the effectiveness of two-stage translation using a simple sliding context approach), the plan going forward is as follows.

## Experiment 07: Integrating the Summary-Compression Approach + KV-Cache Optimization with Two-Stage Translation

In experiment 06, the simple sliding context approach succeeded in raising the score for Dutch (78 → 94 points), but for Czech, quality dropped significantly at the draft translation stage (78 → 56 points).
This is presumably because a simple sliding context cannot retain long-range context, which lowers the baseline translation quality itself.

Therefore, in the next experiment (07), the **"summary-compression approach and KV-cache optimization via term injection"** mechanism already adopted in the current `trtools translate` will be integrated into two-stage translation.
This aims to combine both a high baseline quality from better context retention and the refinement effect of two-stage translation, achieving both processing efficiency and translation quality.

## Future Consideration: Exploring Separate-Model Evaluation (Decoupling the Translation and Evaluation Models)

The current refinement process relies on "self-evaluation" by the translation model itself.
However, as prior verification (experiment 01, etc.) has shown, LLMs exhibit an asymmetry between reading and writing ability: "evaluation/analysis capability is high, but generation (writing) capability is limited."

Given this, the effectiveness of an approach where **separate models are responsible for translation and evaluation (refinement instructions)** — i.e., other-model evaluation — will also be considered in the future.
For example, this could take the form of a pipeline in which a model strong in a specific language performs the translation generation, while a model with superior logical verification ability (such as qwen3.6) handles the refinement and correction proposals.
