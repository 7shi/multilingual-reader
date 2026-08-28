# Project Memo

This file records the design intentions, model characteristic analysis, evaluation task history, and future development tasks (TODO) for the translation experiment project. For the objective evaluation score tables and conclusions on practical settings, see `README.md`.

---

## 1. Evaluation Task: Choosing an Evaluator

### Evaluator History and Conclusion

- **GPT-OSS 120B**: The initial evaluator. It hit a "ceiling effect" where the highest score plateaued at 92 points, making it impossible to differentiate between top-tier models. This is presumed to be due to its MoE characteristics giving it plenty of knowledge but weak judgment, so it was discontinued as an evaluator.
- **gemma-4-31b**: Investigated as a candidate. It tends to skew toward high scores, evaluating in an "absolute" manner. With 18% of scores at 97 or above, it proved too lenient, often getting swept up by superficial fluency and missing terminology inconsistencies and contextual omissions (accuracy of proper nouns, terminology, and formatting), so it was not adopted.
- **qwen3.6**: **Adopted as the official evaluator.** Scores are widely distributed in the 70s-90s range, evaluating in a "relative, aesthetic" manner. Using CoT, it rigorously identifies logical inconsistencies and terminology inconsistencies, appropriately deducting points for serious technical flaws. We concluded that running it alone is the most reliable approach.

### Effectiveness of CoT in Evaluation Tasks
While translation—an "intuitive, implicit task"—showed CoT (verbalized reasoning) to be counterproductive, evaluation, which is an "analytical task," was demonstrated through testing with qwen3.6 to benefit greatly from logical verification via CoT.

### Attempts to Control CoT, and Why They Were Abandoned

- **qwen3.6 --no-think**: Abandoned due to an Ollama bug where disabling CoT breaks the schema structure (the nested structure of `ReasoningAndScore` collapses into a flat integer). We operate with CoT enabled only.
- **gemma4:31b (with thinking)**: Abandoned because processing was too slow, estimated to take about a week for a full evaluation run. gemma4 was not adopted as an evaluator.
- **gemma4:26b (MoE)**: Abandoned due to unstable behavior, with structured output frequently failing.

### Cloud API Utilization Strategy

Strategy for running parallel processing via cloud APIs when local hardware is occupied by another task:

| Model | API | Speed | Cost | Use case |
|--------|-----|------|--------|------|
| GPT-OSS 120B | Groq / Cerebras | Fast | Paid | Speed-focused tasks |
| gemma-4-31b | Gemini API | Moderate | Free tier available | Substitute when local hardware is busy |
| gemini-2.5-flash | Gemini API | Fast | Free tier reduced / paid | High-quality evaluation (used previously) |

---

## 2. Translation Task: Structured vs. Unstructured Output

Structured output reliably extracts the desired result, but forcing conformance to a format raises concerns about degraded quality; we compared the characteristics of both approaches.

| Aspect | Structured output (Level 0/1/2) | Unstructured output (tr4/tr5/tr6) |
|------|-----------|-------------|
| Quality stability | Suppresses unwanted output, stable | Unstable, depends on model/settings |
| Handling runaway or truncated output | Parse failures can be retried mechanically | Runaway generation before the answer risks hallucination |
| Impact of format constraints | Quality collapses for some models (→ unstructured output is effective) | Some models run away (→ structured output is essential) |

* For the analysis of the concrete score impact (the harm of structured constraints and the counterproductive effect of increased reasoning complexity), see `README.md`.

### Using Unstructured Output: A Two-Stage Approach
For models that don't produce good quality with structured output, an effective method is to generate freely in the first stage, then extract only the translation result in the second stage. Approaches such as fixing a lightweight model dedicated to extraction, or using majority voting to extract the correct answer, are also conceivable.
However, there are operational challenges, such as the first stage failing to produce a translation, or wording being unintentionally altered during extraction.

### Assumptions About the Processing Environment and Model Selection
We assume a desktop or cloud environment. Given sufficient VRAM, MoE models run at speeds comparable to small dense models, so there's little need to deliberately choose a small model.
However, dense models have the advantage for tasks requiring judgment, such as evaluation and translation, while MoE is better suited to use cases that leverage breadth of knowledge (e.g., terminology verification, background knowledge supplementation) or scenarios where speed is the priority.

---

## 3. Next-Generation Architecture: KV Cache and Summary Compression

The current translation experiment (`translate.py`) uses a sliding-context approach, where the starting point of the context shifts every time, so the KV cache doesn't function effectively.

On the other hand, an approach that accumulates the entire history becomes impractically slow once the history reaches around 40 entries, and inference quality also degrades (because the computational cost of a Transformer's self-attention grows quadratically with context length).

Therefore, to resolve the "forgetting" (terminology drift) inherent in the sliding approach while keeping computational cost down, a **summary-based approach that compresses old history into dense tokens is structurally inevitable**.

### Design Policy for the New Architecture
- **Fixed separation of the system prompt**: By keeping it always at the head, independent of the conversation history, caching stays enabled at all times.
- **Summary compression with a fixed head**: Once a certain number of entries is reached, old history is compressed into a "glossary + summary," rebuilding the structure into a fixed `system + summary + most recent N entries` layout. This stabilizes the context starting point, allowing the KV cache to be reused.
- **Optimizing the timing of compression**: By generating the summary right before compression, the cache for the most recent N entries remains valid even after compression.
