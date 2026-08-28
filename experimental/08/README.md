# Experiment 08: Verifying single-step revision using CoT

This directory further optimizes the "third-party evaluation approach" that succeeded in Experiment 07, verifying a "single-step approach" in which the evaluation model's (`qwen3.6`) internal reasoning (CoT: the `<think>` tag) is enabled, and analysis and output of the corrected translation are completed in a single prompt.

## Script structure

- **`review.py`**:
  Based on Experiment 07's script, with `LLMClient(think=True)` enabling CoT. Unlike Experiment 07 (two-step approach / pseudo-CoT), which split "identifying issues" and "generating the corrected translation" into two calls, this version instructs the model to "analyze, then output the corrected translation" in a single prompt.
  In this approach, the thought process (analysis) is not accumulated as normal text in the context history but stays only within the hidden `<think>` block, so we check how this difference affects quality and consistency.
- **`batch.sh`**:
  A batch script that fully automates everything from single-step revision using `review.py`, through evaluation of the generated corrected translations, to aggregation.

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

## Results and analysis

We ran the batch script (elapsed time: 221m44.407s) and obtained the following scores.
*The baseline is the Experiment 07 result (two-step approach, CoT disabled).

| Language | Experiment 07 (two-step, CoT disabled) | Experiment 08 (single-step, CoT enabled) | Experiment 08 (single-step, CoT disabled) |
| :--- | :---: | :---: | :---: |
| Dutch (nl) | **97 pts** | 96 pts | 75 pts |
| Czech (cs) | **94 pts** | 86 pts | 59 pts |

### Discussion

* **Dutch**: 96 points, roughly equivalent to Experiment 07's 97 points.
* **Czech**: Dropped significantly from Experiment 07's 94 points to 86 points. The individual evaluation scores also varied widely — 79, 84, and 95 points, a spread of 16 points — showing that evaluation stability has also decreased.

  A detailed log analysis revealed that the revised text for the original's 4th line (`Luc: And I'm Luc, an experimental physicist...`) became `Luc: ` (empty). This shows that when CoT is enabled, the model can become absorbed in its thinking within the `<think>` block and omit the translated text output — a **structural problem** that is difficult to solve through prompt improvements alone.

  Also, unlike Experiment 07's two-step approach, in which analysis results accumulate as normal text in the chat history, here the thought process stays only within the `<think>` block, which likely makes contextual consistency with preceding/following lines easier to lose.

### Fallback verification (`tr-fb/`)

We created `apply_fallback.py`, which fills empty output lines with the base translation, and applied it to the Czech revision results (Dutch had no empty output). The score dropped further as a result (86 → 74 points; 3 evaluations: 72, 89, 69 points).

Investigation revealed that line 4 of the baseline translation `onde-cs.txt` contained **foreign-language interference** in the form of `meteen` (Dutch for "immediately"; the correct Czech would be `hned` / `okamžitě`). Note this is unrelated to the fact that Dutch was also a target language in this experiment — it is an incidental interference introduced by gemma4:26b during baseline translation. The same file also contains French interference (line 55: `Of koncentrovat...`) and grammar/notation issues (`dvouštěbinový`, `za svým ohniska`).

Experiment 07's revision (94 points) had managed to fix these issues, but in Experiment 08 the problem line had simply gone missing due to the empty output. The fallback fills that gap, but when the baseline itself has quality problems, it merely restores the problem line rather than solving it. We concluded that **fallback processing should not be built into `review.py`**.

### CoT-disabled (single-step, `--no-think`) additional verification (`tr-nt/`)

Completed in 23m1.158s. Scores were even worse than with CoT enabled: Dutch 75 points (72, 75, 84) and Czech 59 points (49, 59, 73). Without CoT, the model outputs immediately without analyzing, so it fails to function as a revision: for Dutch, we saw contamination from `wahrscheinlichkeit` (German) and `psi-squared` left untranslated in English, while for Czech there were frequent mistranslations, such as `psi` incorrectly rendered as `pí`, and `coherent` mistranslated as `souhlasný` (meaning "in agreement") — a physics-term error.

**Final conclusion**

Regardless of whether CoT is enabled, the single-step approach fell short of Experiment 07's two-step, CoT-disabled approach. The two-step approach, in which analysis results accumulate in the chat history as "normal text," is essential for effective revision, and CoT introduces unnecessary overhead into the revision process. **We will adopt Experiment 07's approach (two-step, CoT disabled) as the revision process going forward, and expand it to other medium-resource languages.**

**Supplementary note: "guiding thought" vs. "delegating thought"**

The finding that guiding thought via a two-step approach outperforms delegating thought to CoT may seem counterintuitive. However, while CoT leaves the content and direction of thinking entirely up to the model, the two-step approach explicitly splits the task — "first analyze the problem (step 1), then generate the corrected translation based on that analysis (step 2)" — thereby guiding the model's thinking from the outside. Furthermore, because the analysis accumulates as normal text in the chat history, revision of subsequent lines can reference that context. CoT (the `<think>` block) is used implicitly within each step; what matters is not whether CoT is present, but **whether the direction of thought can be controlled through task decomposition**.

## Purpose

We compare which approach — this one or Experiment 07 (two-step approach / `--no-think`) — is superior in the following respects (i.e., which offers a better balance of quality and speed).

1. **Quality and contextual consistency**: Does not leaving the analysis results as "conversational text" in the chat history context adversely affect the revision quality of preceding/following lines?
2. **Processing speed and practicality**: Weighing the halved number of API calls against the processing overhead of CoT itself, how does the total processing time change?

Once this verification determines the optimal revision process, we plan to expand its scope of application to other medium-resource languages.
