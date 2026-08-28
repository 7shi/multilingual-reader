# Experiment 07: Revising and correcting existing translations via third-party evaluation

This directory verifies the effectiveness of a "third-party evaluation approach," in which high-quality baseline translations already output by `trtools` (with KV-cache optimization and terminology injection) are used as input, and `qwen3.6` — a model with strong logical verification and evaluation capabilities — revises them line by line.

## Background and purpose

In Experiment 06, we tried "two-stage translation," in which the translation model itself self-evaluates and revises its own output. However, LLMs exhibit an asymmetry in reading/writing ability: "evaluation and analysis ability is high, but generation (writing) ability has limits." Self-evaluation risks being dragged down by this limitation, and the degradation of baseline quality caused by a simple sliding context was also an issue.

Therefore, this experiment verifies **an approach that separates the roles of "translation" and "evaluation (revision instructions)."**
By having a revision-dedicated model re-examine a baseline (trtools output) whose context has already been preserved, we check whether expression-level issues in medium-resource languages (literal-translation tone, interference) are effectively resolved, and whether scores rise into the target 90s.

## Scope and assumptions

- **Target**: Translated text already output by `trtools` (Dutch, Czech, etc.).
- **Revision model**: `ollama:qwen3.6`
- **Approach**: Feed pairs of the original and translated lines one line at a time, and evaluate/correct using a staged prompt.
- **Context management**: Since `qwen3.6` is structurally inefficient at using the KV cache, we avoid complex mechanisms like summary compression and instead adopt a **simple sliding-context method with a scope of 10 lines**.

## Script structure and staged prompts

- **`review.py`**:
  A revision-dedicated script that reads the original text and the translation already output by `trtools`, and issues the following two prompts line by line using an evaluation model such as `qwen3.6`. It adopts a free-form (unstructured) approach, avoiding the constraints of structured output, in order to draw out the model's analytical ability to the fullest.
  1. **Identifying issues (Prompt 1)**: Freely point out any issues such as literal-translation tone or interference from neighboring languages, and add them to the chat history.
  2. **Generating the corrected translation (Prompt 2)**: Output only the final translation with the pointed-out issues resolved.
- **`batch.sh`**:
  A batch script that fully automates everything from revision using `review.py`, through evaluation of the generated corrected translations, to aggregation.

## How batch.sh works

1. **Running the revision**
   - **Input**:
     - Original text: `examples/onde-en.txt`
     - Baseline translation: `examples/tr/onde/gemma4/tr/onde-{lang}.txt`
   - **Target languages**: Dutch (`nl`), Czech (`cs`)
   - **Revision model**: `ollama:qwen3.6`
   - **Output** (2 files total):
     - Revised: `tr/onde-{lang}-reviewed.txt`

2. **Evaluation**
   - **Evaluation model**: `ollama:qwen3.6`
   - Runs `trtools eval` 3 times for each language's revised translation (2 languages × 3 = 6 evaluations total).
   - **Output**: `evals/onde-{lang}-reviewed-{1,2,3}.json`

3. **Aggregation**
   - Uses `trtools agg` to aggregate the median of the evaluation results across all 6 files, outputting the result to `SCORES.txt`.

### Validity of `--no-think` in the revision process

When running the revision script, we specify the `--no-think` option to disable explicit internal reasoning (CoT: the `<think>` tag).
This is because, for a model like `qwen3.6` that excels at logical verification, when given a free-form instruction such as "identify issues (analyze... point out...)", **it spontaneously develops staged reasoning (pseudo-CoT / in-context reasoning) using the output text itself.**
If explicit `<think>` and text-output analysis both occur, processing time becomes enormous, so specifying `--no-think` speeds up the revision process without lowering the quality of the analysis.

## Results and analysis

We ran the batch script (elapsed time: 56m7.696s) and obtained the following scores.
*The baseline is the result from `examples/tr/onde/gemma4/SCORES.txt` (batch direct translation via trtools, with summary compression).

| Language | Baseline (batch direct translation) | Revised |
| :--- | :---: | :---: |
| Dutch (nl) | 78 pts | **97 pts** |
| Czech (cs) | 78 pts | **94 pts** |

### Discussion
* **Dutch**: Improved dramatically from a baseline of 78 points to **97 points**. This score is even higher than Experiment 06's self-evaluation (final translation: 94 points), confirming the effectiveness of the approach of having a model with strong evaluation ability revise a high-quality baseline.
* **Czech**: Improved dramatically from a baseline of 78 points to **94 points**, reaching the target 90s range. This is the result of starting from a context-preserved baseline and having a model with strong logical verification correct expression-level issues (literal-translation tone, interference).

**Conclusion**
The approach of separating the roles of "translation (thorough context preservation)" and "revision (logical verification / third-party evaluation)" has proven to be a highly effective means of improving quality in medium-resource languages. Even languages that had been stuck in the 70s under the baseline can, through this revision process, reach the same level as high-quality languages (mid-90s).
