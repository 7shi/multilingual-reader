# Local LLM Translation Experiment: Performance Analysis by Reasoning Level and Practical Guidelines

Translated a podcast from French to Spanish and conducted objective evaluation using an LLM. Systematically analyzed the effect of structured output and reasoning level on translation quality.

※ As the reasoning level increases, structured output is used to guide the model toward more detailed reasoning. The specific schema is explained in each section.

## Background and Design Philosophy of the Experiment

### Theoretical Background of Reasoning Control via Structured Output

**Basic hypothesis**: The order of schema fields can control the model's processing order

Through schema design for structured output, we implemented a flexible system that dynamically switches the translation method via a `reasoning_level` parameter. The aim was to control the model's thought process and achieve stepwise quality improvement.

### Evolution of the Evaluation Method

#### Initial evaluation (evaluation by Claude Code)
| Method | Score | Improvement | Key Effect |
|:---|:---:|:---:|:---|
| Level 0 (direct translation) | 65 pts | - | Baseline |
| Level 1 (with reasoning) | 85 pts | +20 pts | Chain of thought |
| Level 2 (two-stage translation) | 93 pts | +28 pts | Self quality check |

Details 👉 [comparison/README.md](comparison/README.md)

**Problem**: Because the evaluation criteria were not defined and evaluation was done vaguely, the basis for the evaluation was unclear.

#### Evaluation with defined criteria
The same output was measured using 5 evaluation criteria:

- **Systematic 5-criteria evaluation**: readability, fluency, terminology, contextual adaptation, informational completeness
- **Reliability through repeated evaluation**: eliminated evaluation variance by using the median of 3 evaluation runs

**Findings different from the initial evaluation**:
- **Conventional hypothesis**: complex reasoning system → high-quality translation
- **New discovery via objective evaluation**: appropriate model selection → simple direct output = highest efficiency

#### Evolution of the Evaluator

After an initial evaluation by GPT-OSS 120B (the scores in this document), the evaluator was changed due to a ceiling-effect problem (maximum score of 92):

- **GPT-OSS 120B**: initial evaluator. Ceiling effect present; weak judgment due to MoE characteristics (discontinued as an evaluator)
- **gemma-4-31b**: candidate evaluated. Too lenient (18% of scores 97 or above); misses content accuracy issues (not adopted)
- **qwen3.6**: **officially adopted as evaluator**. Logical verification via CoT correctly identifies technical flaws, and it was concluded that operating it alone offers the highest reliability.

Details 👉 [evaluator_comparison/README.md](evaluator_comparison/README.md)

## Technical Details of the Evaluation System

### trtools eval: translation quality evaluation tool

**Overview**: An LLM-based 5-criteria translation quality evaluation system ([trtools/evaluate.py](../trtools/evaluate.py))

- **Evaluation criteria**: 5 criteria, 20 points each (100 points total) 👉 [EVAL.md](EVAL.md)
  1. **Readability and comprehensibility**: ease of understanding for readers of the target language
  2. **Fluency and naturalness**: naturalness for native speakers
  3. **Appropriateness of terminology**: accuracy and consistency of technical terms
  4. **Contextual adaptability**: appropriate reflection of the original text's intent and cultural background
  5. **Completeness of information**: concise and clear communication without missing or added information
- **Statistical reliability**: uses the median of 3 evaluation runs (`trtools agg`)
- **Evaluation results**: [SCORES.txt](SCORES.txt)

**Usage**:
```bash
uv run trtools eval --original original.txt --translation translation.txt \
  -m ollama:qwen3.6 -f French -t Spanish -o result.json
```

**Output format**: detailed reasoning and score for each criterion, plus an overall evaluation comment

### trtools agg: evaluation result aggregation tool

**Overview**: Achieves reliable quality measurement through statistical aggregation of repeated evaluations ([trtools/aggregate.py](../trtools/aggregate.py))

**Main features**:
- **Automatic detection of 3 evaluation runs**: recognizes the `filename-{1,2,3}.json` pattern
- **Statistical value calculation**: computes median, mean, and standard deviation per criterion and overall
- **Improved reliability**: statistically corrects for evaluation variance

**Usage**:
```bash
# Detailed display
uv run trtools agg evaluation-*-*.json --verbose

# Concise display (median only)
uv run trtools agg evaluation-*-*.json
```

**Statistical significance**: eliminates the subjective variance of a single evaluation via the median of 3 evaluation runs, achieving objective quality measurement

### Running the experiment and obtaining scores
Translation and evaluation are batch-processed via `batch.sh`, which automates the whole pipeline through to score aggregation:

```bash
sh batch.sh
```

Three evaluation runs are automatically performed for each translation result to ensure statistical reliability.

**Aggregation flow after evaluation**:
- `trtools agg`: aggregates the final scores and saves them to `SCORES.txt`
- `generate_scores_md.py`: generates `SCORES.md` from `SCORES.txt`
- `sync_scores.py`: automatically syncs the tables in `SCORES.md` into `README.md`

### Composition of the Translation System
- [translate.py](translate.py): 5-level reasoning via structured output
- [translate4.py](translate4.py): unstructured direct translation
- [translate5.py](translate5.py): unstructured simplified reasoning
- [translate6.py](translate6.py): unstructured detailed reasoning

### Legend
- Bold in the tables indicates the highest score in each row
- (t): `--translated-context` option (only the translated text is provided in the history)
- (nt): `--no-think` option (disables reasoning on reasoning models)
  - Due to an Ollama limitation, reasoning is disabled when structured output is used, giving the same effect as (nt)

## System Design by Reasoning Level and Experimental Scores
Reasoning level specified via the `-r` option of [translate.py](translate.py) (all structured output)

| Model | 0 | 1 | 2 | 3 | 4 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | **81** | 73 | 73 | 41 | 40 |
| **aya-expanse-32b** | **87** | 83 | 85 | 60 | 73 |
| **command-r7b** | **64** | 33 | 32 | 32 | 40 |
| **command-r-35b** | **82** | 74 | 47 | 66 | 79 |
| **gemma2-9b** | 76 | 37 | 77 | **81** | 27 |
| **gemma3-4b** | **41** | 21 | 20 | 34 | 19 |
| **gemma3-12b** | **95** | 11 | 86 | 88 | 90 |
| **gemma3-27b** | **98** | 67 | 70 | 70 | 80 |
| **gemma3n-e4b** | 73 | 21 | **86** | 54 | 62 |
| **gpt-oss-20b** | 86 | 94 | 91 | 92 | **95** |
| **gpt-oss-120b** | **96** | **96** | 95 | **96** | 92 |
| **llama3.3** | **93** | 86 | 45 | 58 | 21 |
| **llama4-scout** | **91** | 21 | 43 | 24 | 19 |
| **ministral-3-3b** | **52** | 0 | 25 | 19 | 18 |
| **ministral-3-8b** | **88** | 18 | 80 | 20 | 28 |
| **ministral-3-14b** | **86** | 12 | 32 | 23 | 0 |
| **mistral-small3.2** | 91 | 91 | 85 | **94** | **94** |
| **mixtral-8x7b** | **65** | 53 | 54 | 23 | 60 |
| **mixtral-8x22b** | **89** | 72 | 71 | 75 | 68 |
| **phi4** | 76 | 70 | 72 | 86 | **87** |
| **qwen3-4b** | **65** | 63 | 58 | 45 | 61 |
| **qwen3-4b (nt)** | 55 | 48 | 60 | 60 | **74** |
| **qwen3-14b** | 81 | 93 | 66 | 94 | **95** |
| **qwen3-14b (nt)** | 78 | 62 | **89** | 80 | 88 |
| **qwen3-30b** | 82 | 75 | 85 | **95** | 85 |
| **qwen3-30b (nt)** | 89 | 93 | **94** | 92 | 29 |
| **qwen3-32b** | 93 | 77 | 77 | 94 | **95** |
| **qwen3-32b (nt)** | 92 | 90 | 94 | **95** | 91 |

- **Level 0 (direct translation)**: the most stable. High-performing models (gemma3-27b, gpt-oss-120b) score very highly.
- **Level 1 (translation with reasoning)**: instructions become more complex under structured constraints, causing a marked degradation for many models (median 59 points). Planned for removal in the next-generation architecture.
- **Level 2 (two-stage translation)**: effective at boosting some models such as aya-expanse-8b and command-r-35b, but many models also degrade.
- **Levels 3 and 4**: some models, such as the Qwen3 series, record high scores (95 points), but the adverse effects of reasoning-induced complexity tend to appear, and there are cases (qwen3-30b) where unstructured output is essential, making these levels hard to handle.

**Conclusion**: Level 0 remains the primary axis for analysis and operation. Reasoning-augmented structured output (Level 1) is counterproductive and is therefore discontinued.

### Level 0: Direct Translation
**Characteristics**: the simplest translation method
```python
class Translation(BaseModel):
    translation: str = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")
```

The `--history` option of [translate.py](translate.py) specifies the number of history entries to include in the context (default is 5 if omitted)

- 0-20 was measured twice to check for variation (other entries are believed to have similar variation)

| Model | 0-05 | 0-10 | 0-15 | 0-20 | 0-20-a | 0-20-b | 0-25 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | 70 | 75 | - | - | 74 | **79** | - |
| **aya-expanse-32b** | 79 | 93 | - | - | 92 | **95** | - |
| **command-r7b** | 56 | 55 | - | - | **61** | 58 | - |
| **command-r-35b** | **93** | 71 | - | - | 63 | **93** | - |
| **gemma2-9b** | 48 | 55 | - | - | 60 | **87** | - |
| **gemma3-4b** | 54 | 42 | - | - | **71** | 61 | - |
| **gemma3-12b** | **87** | 82 | - | - | 82 | 81 | - |
| **gemma3-27b** | **97** | **97** | - | - | 96 | 95 | - |
| **gemma3n-e4b** | 55 | 78 | - | - | 68 | **79** | - |
| **gpt-oss-20b** | 88 | **94** | - | - | 91 | 88 | - |
| **gpt-oss-120b** | 95 | 95 | - | - | 94 | **98** | - |
| **llama3.3** | 78 | 94 | - | - | 94 | **95** | - |
| **llama4-scout** | **95** | 89 | - | - | 83 | 89 | - |
| **ministral-3-3b** | 64 | 59 | - | - | **74** | 64 | - |
| **ministral-3-8b** | 90 | 90 | - | - | 94 | **96** | - |
| **ministral-3-14b** | **95** | 87 | - | - | 92 | 87 | - |
| **mistral-small3.2** | 88 | **95** | - | - | 93 | 94 | - |
| **mixtral-8x7b** | 47 | 81 | - | - | **85** | 73 | - |
| **mixtral-8x22b** | 90 | 89 | - | - | 78 | **93** | - |
| **phi4** | 62 | **90** | - | - | 72 | 64 | - |
| **qwen3-4b** | **68** | 59 | 46 | 55 | 61 | 57 | 56 |
| **qwen3-4b (nt)** | **68** | 63 | 33 | 65 | 60 | 46 | 44 |
| **qwen3-4b (t)** | 47 | 37 | 39 | **48** | - | - | 41 |
| **qwen3-4b (nt,t)** | 55 | 52 | **69** | 66 | - | - | 45 |
| **qwen3-14b** | 79 | 67 | - | - | 62 | **81** | - |
| **qwen3-14b (nt)** | 62 | 76 | - | - | 81 | **86** | - |
| **qwen3-30b** | 84 | 88 | - | - | 94 | **95** | - |
| **qwen3-30b (nt)** | 93 | **95** | - | - | 86 | 76 | - |
| **qwen3-32b** | 78 | 91 | - | - | 93 | **94** | - |
| **qwen3-32b (nt)** | **94** | 84 | - | - | 82 | 91 | - |

- **(t)**: no consistent improvement was observed. Practical value is limited, so it is discontinued in the next-generation architecture.
- The optimal history value depends on the model. High-performing models (gemma3-27b, gpt-oss-120b) already reach high scores at history 5, but in some cases they record their highest score at history 20 (gpt-oss-120b: 98 points at 0-20-b).
- However, objective evaluation confirmed forgetting of history (terminology drift) caused by the sliding context, revealing an inherent limit to the approach of simply increasing the history count (--history).

**Conclusion**:
- The current approach of sliding the context history (--history) is discontinued; the next-generation architecture will move to "glossary-augmented summary compression."
- --translated-context (t) is discontinued.

## The Context History (--history) Option in Detail

### Overview
The `--history N` option provides the past N translation entries as context, improving dialogue consistency and translation quality.

### Settings and Effects
- **Default value**: `--history 5` (when omitted)
- **Recommended setting**: `--history 10` (significant improvement for mid/low-performing models)
- **History format**: included in the context as source–translation pairs

### Implementation Details
```python
# Add the last 5 (or N) translation results as context
context_lines = []
if context_history:
    context_lines.append("Previous conversation context:")
    context_lines.append("")
    for ctx in context_history[-N:]:  # N is specified via --history
        context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
        context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
        context_lines.append("")
```

### Effect by Model
- **High-performing models** (Gemma3 27B, GPT-OSS 120B): already reach high scores of 95+ at history 5, with little further boost from additional history, but can record their highest score when increased to 20 (gpt-oss-120b scored 98 at 0-20-b).
- **Models with strong context comprehension** (Phi4): **dramatic improvement (62 → 90 points, +28 points)**. History information greatly improves translation consistency, reaching a score comparable to larger, higher-performing models despite its mid size.
- **Models destabilized by more history** (Qwen3 4B, Gemma3 4B): tend to show lower or more volatile scores as history is increased.

### Limits of the Sliding Context
The current `--history` option uses a "sliding" approach that discards old history beyond a fixed count, but evaluation quantitatively confirmed the phenomenon that "terms in old history are forgotten and drift toward new wording." To address this, the history parameter itself is discontinued, and future work will move to a summary compression approach.

### Level 1: Translation with Reasoning
**Characteristics**: detailed reasoning across 5 criteria (syntactic analysis, contextual interpretation, vocabulary choice, cultural consideration, translation rationale)
```python
class Translation(BaseModel):
    reasoning: str = Field(description="""Detailed translation reasoning process:
1. Syntactic analysis of the original text...
2. Contextual interpretation of speaker's intent...
3. Evaluation of translation options...
4. Consideration of cultural nuances...
5. Justification for final translation choices...""")
    translation: str = Field(description="Translation result")
```

| Model | 1-05 | 1-10 | 1-15 | 1-20 | 1-25 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | 59 | **93** | - | 27 | - |
| **aya-expanse-32b** | **93** | 86 | - | 90 | - |
| **command-r7b** | **42** | 24 | - | 35 | - |
| **command-r-35b** | **49** | 34 | - | 31 | - |
| **gemma2-9b** | **67** | 26 | - | 33 | - |
| **gemma3-4b** | 29 | 16 | - | **43** | - |
| **gemma3-12b** | 0 | **6** | - | **6** | - |
| **gemma3-27b** | 93 | **96** | - | 83 | - |
| **gemma3n-e4b** | **59** | 24 | - | 57 | - |
| **gpt-oss-20b** | 91 | **95** | - | 94 | - |
| **gpt-oss-120b** | 94 | **95** | - | 94 | - |
| **llama3.3** | **94** | 89 | - | 89 | - |
| **llama4-scout** | **27** | 18 | - | 18 | - |
| **ministral-3-3b** | 5 | 6 | - | **11** | - |
| **ministral-3-8b** | 12 | 16 | - | **21** | - |
| **ministral-3-14b** | 28 | 50 | - | **57** | - |
| **mistral-small3.2** | 80 | **94** | - | 86 | - |
| **mixtral-8x7b** | 48 | 35 | - | **51** | - |
| **mixtral-8x22b** | 85 | **87** | - | 83 | - |
| **phi4** | 26 | 25 | - | **78** | - |
| **qwen3-4b** | **67** | 58 | 42 | 37 | 56 |
| **qwen3-4b (nt)** | 38 | 30 | **47** | 34 | 40 |
| **qwen3-4b (t)** | 68 | 47 | 63 | 37 | **69** |
| **qwen3-4b (nt,t)** | **63** | 46 | 53 | 44 | 49 |
| **qwen3-14b** | **85** | 72 | - | 69 | - |
| **qwen3-14b (nt)** | 85 | 73 | - | **87** | - |
| **qwen3-30b** | 94 | **96** | - | 94 | - |
| **qwen3-30b (nt)** | 94 | 78 | - | **96** | - |
| **qwen3-32b** | 70 | **90** | - | 79 | - |
| **qwen3-32b (nt)** | 28 | **48** | - | 22 | - |

- **(t)**: the output format becomes more stable, but the score improvement is unstable.
- Improvement from history is limited, and it rarely exceeds Level 0's direct translation.
- **Models that maintain high scores**: gpt-oss-120b (94–95), gpt-oss-20b (91–95), qwen3-30b (94–96), gemma3-27b (93–96), etc. — limited to a few powerful models that can withstand the reasoning constraint.
- **Marked degradation**: gemma3-12b (0–6, output collapse), ministral-3-3b/8b (5–21), llama4-scout (18–27), etc. — many models are incompatible with structured reasoning and their scores drop critically.
- **Mid-size and above tend to be stable**: aya-expanse-32b, mistral-small3.2, mixtral-8x22b maintain scores in the mid-80s to 90s depending on history.

**Conclusion**:
- Structured reasoning (Level 1) is counterproductive to translation quality overall (median 59 points), and is therefore discontinued as part of the move to the next-generation architecture.

### Level 2: Two-Stage Translation
**Characteristics**: two-stage translation that revises after a direct translation to produce the final translation
```python
class Translation(BaseModel):
    draft_translation: str = Field(description="First draft translation")
    quality_assessment: str = Field(description="Analyze translation for errors, mistranslations, language mixing...")
    improvement_suggestions: str = Field(description="Provide specific suggestions for improving quality")
    improved_translation: str = Field(description="Improved translation based on assessment")
```

| Model | 2-05 | 2-10 | 2-15 | 2-20 | 2-25 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | **85** | 71 | - | 84 | - |
| **aya-expanse-32b** | 61 | 63 | - | **79** | - |
| **command-r7b** | 33 | **57** | - | 32 | - |
| **command-r-35b** | 74 | **95** | - | 86 | - |
| **gemma2-9b** | 67 | 78 | - | **94** | - |
| **gemma3-4b** | **41** | 34 | - | 39 | - |
| **gemma3-12b** | **93** | 79 | - | 89 | - |
| **gemma3-27b** | 77 | 87 | - | **92** | - |
| **gemma3n-e4b** | **91** | 80 | - | 84 | - |
| **gpt-oss-20b** | 88 | 92 | - | **94** | - |
| **gpt-oss-120b** | 95 | **96** | - | **96** | - |
| **llama3.3** | 59 | **72** | - | 54 | - |
| **llama4-scout** | **29** | 21 | - | 16 | - |
| **ministral-3-3b** | 20 | **22** | - | 19 | - |
| **ministral-3-8b** | 76 | **95** | - | 94 | - |
| **ministral-3-14b** | 15 | 22 | - | **34** | - |
| **mistral-small3.2** | 87 | 77 | - | **91** | - |
| **mixtral-8x7b** | 41 | 35 | - | **62** | - |
| **mixtral-8x22b** | **89** | 71 | - | 88 | - |
| **phi4** | 78 | **88** | - | 83 | - |
| **qwen3-4b** | 65 | 60 | 54 | 68 | **72** |
| **qwen3-4b (nt)** | 60 | 57 | 56 | **63** | 55 |
| **qwen3-4b (t)** | **63** | 50 | 56 | 55 | 52 |
| **qwen3-4b (nt,t)** | 57 | 49 | 54 | **58** | 53 |
| **qwen3-14b** | 78 | **90** | - | 76 | - |
| **qwen3-14b (nt)** | 78 | **79** | - | **79** | - |
| **qwen3-30b** | **95** | 89 | - | **95** | - |
| **qwen3-30b (nt)** | 88 | 90 | - | **95** | - |
| **qwen3-32b** | 90 | 86 | - | **93** | - |
| **qwen3-32b (nt)** | **94** | 93 | - | 90 | - |

- Effective at boosting mid-to-small models in some cases. In particular, ministral-3-8b (95 points) and qwen3-14b (90 points) show notable high scores.
- High-performing models maintain a level comparable to Level 0: gpt-oss-120b (95–96), gpt-oss-20b (88–94).
- Effects vary by model: aya-expanse-8b shows improvement at history 5 (85 points), while phi4 drops slightly from Level 0 (90 points) to Level 2 (88 points).
- Some models degrade with more history: gemma3n-e4b scores 91 at history 5 but declines with more history.
- Among the ministral-3 series, only 8b scores well; 3b/14b lag behind.
- **(t)** has an unstable effect on qwen3-4b.

**Conclusion**: Level 2 is worth adopting for models where the quality-improvement effect is clear, but since many models already reach sufficient quality at Level 0 (direct translation), Level 0 is prioritized from a speed and cost perspective.

### Verifying the Translation Improvement Effect (Level 0 vs Level 2)

Verified the improvement effect of two-stage translation by comparing the performance of Level 0 (direct translation) and Level 2 (two-stage translation)

| Model | 0-05 | 0-10 | 0-20-a | 0-20-b | 2-05 | 2-10 | 2-20 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | 70 | 75 | 74 | 79 | **85** | 71 | 84 |
| **aya-expanse-32b** | 79 | 93 | 92 | **95** | 61 | 63 | 79 |
| **command-r7b** | 56 | 55 | **61** | 58 | 33 | 57 | 32 |
| **command-r-35b** | 93 | 71 | 63 | 93 | 74 | **95** | 86 |
| **gemma2-9b** | 48 | 55 | 60 | 87 | 67 | 78 | **94** |
| **gemma3-4b** | 54 | 42 | **71** | 61 | 41 | 34 | 39 |
| **gemma3-12b** | 87 | 82 | 82 | 81 | **93** | 79 | 89 |
| **gemma3-27b** | **97** | **97** | 96 | 95 | 77 | 87 | 92 |
| **gemma3n-e4b** | 55 | 78 | 68 | 79 | **91** | 80 | 84 |
| **gpt-oss-20b** | 88 | **94** | 91 | 88 | 88 | 92 | **94** |
| **gpt-oss-120b** | 95 | 95 | 94 | **98** | 95 | 96 | 96 |
| **llama3.3** | 78 | 94 | 94 | **95** | 59 | 72 | 54 |
| **llama4-scout** | **95** | 89 | 83 | 89 | 29 | 21 | 16 |
| **ministral-3-3b** | 64 | 59 | **74** | 64 | 20 | 22 | 19 |
| **ministral-3-8b** | 90 | 90 | 94 | **96** | 76 | 95 | 94 |
| **ministral-3-14b** | **95** | 87 | 92 | 87 | 15 | 22 | 34 |
| **mistral-small3.2** | 88 | **95** | 93 | 94 | 87 | 77 | 91 |
| **mixtral-8x7b** | 47 | 81 | **85** | 73 | 41 | 35 | 62 |
| **mixtral-8x22b** | 90 | 89 | 78 | **93** | 89 | 71 | 88 |
| **phi4** | 62 | **90** | 72 | 64 | 78 | 88 | 83 |
| **qwen3-4b** | **68** | 59 | 61 | 57 | 65 | 60 | **68** |
| **qwen3-4b (nt)** | **68** | 63 | - | - | 60 | 57 | 63 |
| **qwen3-14b** | 79 | 67 | 62 | 81 | 78 | **90** | 76 |
| **qwen3-14b (nt)** | 62 | 76 | - | - | 78 | **79** | **79** |
| **qwen3-30b** | 84 | 88 | 94 | **95** | **95** | 89 | **95** |
| **qwen3-30b (nt)** | 93 | **95** | - | - | 88 | 90 | **95** |
| **qwen3-32b** | 78 | 91 | 93 | **94** | 90 | 86 | 93 |
| **qwen3-32b (nt)** | **94** | 84 | - | - | **94** | 93 | 90 |

- **Clear improvement at Level 2**: command-r-35b (0-10: 71 → 2-10: 95, +24), qwen3-14b (0-10: 67 → 2-10: 90, +23), aya-expanse-8b (0-10: 75 → 2-05: 85, +10).
- **High-scoring models about the same**: gpt-oss-120b (0-10: 95, 2-10: 96), qwen3-30b (0-10: 88 → 2-05: 95, an improvement).
- **Level 0 is superior**: llama4-scout (0-05: 95 → 2-05: 29, -66), ministral-3-14b (0-05: 95 → 2-10: 22, -73), llama3.3 (0-10: 94 → 2-10: 72, -22), etc. — several models degrade sharply when reasoning is interposed.
- **History-dependent optimum**: gemma2-9b scores 94 at Level 2-20, its highest, while its Level 0 best is 87.
- gemma3-4b degrades with the two-stage process (0-10: 42, 2-10: 34, both low).
- gemma3n-e4b favors Level 2 at history 5 (0-10: 78 → 2-05: 91).

**Conclusion**: Some models (command-r-35b, qwen3-14b, etc.) show dramatic improvement, while many models such as the llama family degrade catastrophically when reasoning is interposed. Overall, direct translation (Level 0) has broad general applicability, and adopting Level 2 requires checking each model's individual suitability.

### Level 3: Two-Stage Translation with Reasoning

**Characteristics**: integrates Level 1's reasoning with Level 2's two-stage translation
```python
class Translation(BaseModel):
    reasoning: str = Field(description="Detailed translation reasoning process...")
    draft_translation: str = Field(description="First draft translation")
    quality_assessment: str = Field(description="Analyze the draft translation for errors...")
    improvement_suggestions: str = Field(description="Provide specific suggestions...")
    improved_translation: str = Field(description="Based on the quality assessment...")
```
- **Process**: reasoning → draft → quality assessment → improvement suggestions → final translation
- **Advantage**: the most detailed process, with full visibility into every step
- **Use case**: research purposes, quality analysis
- **Experimental result**: no clear improvement compared to Level 2

### Level 4: Split Two-Stage Translation with Reasoning

**Characteristics**: Level 3 split into two separately executed stages
```python
# First stage
class FirstStageTranslation(BaseModel):
    reasoning: str = Field(description="Detailed translation reasoning process...")
    draft_translation: str = Field(description="First draft translation")

# Second stage
class SecondStageTranslation(BaseModel):
    quality_assessment: str = Field(description="Analyze the draft translation for errors...")
    improvement_suggestions: str = Field(description="Provide specific suggestions...")
    improved_translation: str = Field(description="Based on the quality assessment...")
```
- **Process**: stage 1 (reasoning + draft) → stage 2 (quality assessment + improvement)
- **Advantage**: stepwise control, memory efficiency
- **Use case**: large-scale translation, experimental processing
- **Experimental result**: tends to degrade relative to Level 3 (adverse effect of context fragmentation)

## The Mechanism Behind the Counterproductive Effect of Complex Reasoning

Causes of quality degradation from complex reasoning, revealed by objective evaluation:

### 1. Confusion from an increased number of translation options
- Multiple translation candidates are considered during the reasoning process
- More options destabilize the decision
- The result is a less consistent translation

### 2. Prioritizing local optimization over consistency
- Optimization is attempted at each stage but the overall optimum is lost sight of
- Partial improvements harm overall quality
- Information is lost between phases

### 3. Destabilized judgment from a complex thought process
- Deeper reasoning tends to produce more hesitation
- Confusion from self-evaluation causes quality to drop
- A simple, direct translation produces more stable results

**Supplementary note**: the effectiveness of CoT is task-dependent. For tasks requiring implicit judgment, such as translation, it is counterproductive, but for evaluation (an analytical task), logical verification via CoT works extremely effectively (as demonstrated by the CoT of the evaluator qwen3.6).

## translate4.py: Verifying Structured-Output Constraints via Unstructured Direct Translation

Compared the direct-translation performance of structured output (translate.py -r 0) and unstructured output (translate4.py) to verify the impact of the structured constraint.

### Core Finding

**A comparative experiment between structured and unstructured output** revealed the importance of individual optimization according to model characteristics:

| Reasoning Method | Structured Output | Unstructured Output | Score Difference (e.g., Gemma3 12B, h05) |
|:---|:---|:---|:---|
| **Direct translation** | Level 0: 89 pts | translate4: 79 pts | **-10 pts** |

### Key Conclusions

1. **The effect of structured output is model-dependent**: there is no general adverse effect; it strongly depends on the combination of model and history count
2. **The importance of individual optimization**: uniform judgments should be avoided; settings need to match model characteristics
3. **The value of controlling reasoning**: controlling the reasoning process has a larger performance impact than the structured-output constraint itself
4. **Consideration of runtime stability**: evaluation scores do not always align with actual stability, so choices should prioritize practical usability

**Optimization strategy**:
- **Structured output favored**: Gemma3 12B, Gemma3 4B, Qwen3 14B (3/7 models, 43%)
- **Unstructured output favored**: Gemma2 9B, Gemma3n E4B, Phi4 (3/7 models, 43%)
- **Balanced at high scores**: at 90 points and above, structured and unstructured are roughly evenly matched (50% each)

### Investigating the Impact of Structured Output on Direct Translation (Level 0 vs tr4)

Structured output via the `-r 0` option of [translate.py](translate.py); unstructured output via [translate4.py](translate4.py)

| Model | 0-05 | 0-10 | 0-20-a | 0-20-b | tr4-05 | tr4-10 | tr4-20 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | 70 | 75 | 74 | **79** | 64 | 75 | 61 |
| **aya-expanse-32b** | 79 | 93 | 92 | 95 | **97** | 96 | 94 |
| **command-r7b** | 56 | 55 | 61 | 58 | 66 | **67** | 52 |
| **command-r-35b** | 93 | 71 | 63 | 93 | **96** | 91 | 94 |
| **gemma2-9b** | 48 | 55 | 60 | **87** | 73 | 68 | 68 |
| **gemma3-4b** | 54 | 42 | 71 | 61 | 37 | 36 | **74** |
| **gemma3-12b** | 87 | 82 | 82 | 81 | 69 | **91** | 89 |
| **gemma3-27b** | **97** | **97** | 96 | 95 | **97** | **97** | 95 |
| **gemma3n-e4b** | 55 | 78 | 68 | 79 | 73 | **81** | 78 |
| **gpt-oss-20b** | 88 | **94** | 91 | 88 | 93 | 90 | 85 |
| **gpt-oss-120b** | 95 | 95 | 94 | **98** | 94 | 84 | 94 |
| **llama3.3** | 78 | 94 | 94 | **95** | 92 | 85 | **95** |
| **llama4-scout** | **95** | 89 | 83 | 89 | 93 | 87 | 14 |
| **ministral-3-3b** | 64 | 59 | **74** | 64 | 31 | 19 | 34 |
| **ministral-3-8b** | 90 | 90 | 94 | **96** | 86 | 78 | 87 |
| **ministral-3-14b** | **95** | 87 | 92 | 87 | 79 | 91 | 78 |
| **mistral-small3.2** | 88 | 95 | 93 | 94 | 94 | **96** | 94 |
| **mixtral-8x7b** | 47 | 81 | **85** | 73 | 21 | 17 | 36 |
| **mixtral-8x22b** | 90 | 89 | 78 | **93** | 80 | 25 | 63 |
| **phi4** | 62 | 90 | 72 | 64 | 83 | 90 | **91** |
| **qwen3-4b** | **68** | 59 | 61 | 57 | 38 | 34 | 54 |
| **qwen3-4b (nt)** | **68** | 63 | - | - | 61 | 61 | 39 |
| **qwen3-14b** | 79 | 67 | 62 | **81** | **81** | 74 | 67 |
| **qwen3-14b (nt)** | 62 | 76 | - | - | 77 | **93** | 81 |
| **qwen3-30b** | 84 | 88 | 94 | **95** | 37 | 38 | 32 |
| **qwen3-30b (nt)** | 93 | **95** | - | - | 0 | 0 | 0 |
| **qwen3-32b** | 78 | 91 | 93 | 94 | 82 | **96** | 85 |
| **qwen3-32b (nt)** | **94** | 84 | - | - | 82 | 69 | 83 |

- **Structured output favored**: ministral-3-8b (0-10: 90 → tr4-10: 78, -12), qwen3-30b (0-10: 88 → tr4-05: 37, a large drop).
- **Unstructured output favored**: llama3.3 (0-05: 78 → tr4-05: 92, +14), qwen3-14b (nt) (0-10: 76 → tr4-10: 93, +17), command-r-35b (0-05: 93 → tr4-05: 96, +3), aya-expanse-32b (0-10: 93 → tr4-10: 96, +3).
- **Equivalent levels**: gemma3-27b (97 with both methods), gpt-oss-120b (0-05: 95, tr4-05: 94), mistral-small3.2 (0-10: 95, tr4-10: 96), phi4 (around 90 with both methods).
- **Important finding**: qwen3-30b (nt) fails completely with tr4 (0 points). The structured constraint such as JSON functions as a guardrail, without which unstructured output breaks down.
- **(nt)**: for models with reasoning disabled in Ollama, unstructured output (tr4) can improve significantly in some cases (qwen3-14b).
- mixtral-8x7b favors structured output (0-10: 81 → tr4-10: 17, -64).

**Conclusion**: the impact of the structured constraint depends strongly on model characteristics. The llama family, command-r-35b, and qwen3-14b (nt) favor unstructured output (tr4). qwen3-30b, on the other hand, requires structured output. When performance is equivalent, structured output (Level 0) is preferred for parsing stability.

## translate5.py: Verifying the Structured-Output Constraint via Free-Form Reasoning

To address the catastrophic failure at Level 1 (gemma3-12b: 11 points), we ran a free-form reasoning experiment with the structured-output constraint removed.

※ For results of models other than gemma3-12b, see the comparison with tr6

### Reasoning Prompt

```
First, briefly analyze the text for:
1. Key vocabulary and expressions
2. Speaker's intent and tone
3. Cultural context and appropriate register

Then provide your final translation on the last line.
```

### Experimental Results (gemma3-12b)

**A comparative experiment between structured and unstructured reasoning** demonstrated that even the same reasoning process can produce dramatically different performance depending on the implementation:

| Reasoning Method | Structured Output | Unstructured Output | Score Difference |
|:---|:---|:---|:---|
| **Direct translation** | Level 0: 95 pts | translate4: 79 pts | **-16 pts** |
| **Translation with reasoning** | Level 1: 11 pts | translate5: 93 pts | **+82 pts** |

1. **Demonstrated harm of the structured-output constraint**: a +82-point improvement from Level 1 (11) to translate5 (93)
2. **A limit inherent to the reasoning process itself**: translate5 (93) is a slight -2-point degradation from Level 0 (95)
3. **Overhead from verbalization**: explicit analysis consumes attention capacity and hampers translation quality
4. **The advantage of an after-the-fact explanation design**: presents a design principle that avoids the quality trade-off

**Conclusion**: for the translation task, direct translation (Level 0) is the optimal solution. The reasoning process is harmful under structured constraints, and while it nearly preserves quality in free form, it is inferior to direct translation in terms of cost-performance.

## translate6.py: A Comparative Experiment with Improved Free-Form Reasoning

An improved version of translate5.py's reasoning prompt, enabling a fair comparison with Level 1.

### Purpose of the Modification

In translate5.py's initial experiment, the reasoning content differed from that of Level 1, preventing a fair comparison. translate6.py makes the following improvements:

1. **Unified reasoning content**: implements the same detailed 5-criteria reasoning as translate.py -r 1
2. **Consideration of translation options**: adds evaluation of translation options for key vocabulary and idiomatic expressions
3. **Clarification of rationale**: strengthens the process of justifying the final translation choice

### Improved Reasoning Prompt

```
First, provide detailed translation reasoning covering:
1. Syntactic analysis of the original {args.from_lang} text (subject, predicate, object, modifiers, etc.)
2. Contextual interpretation of speaker's intent and emotional tone
3. Evaluation of {args.to_lang} translation options for key vocabulary and idiomatic expressions
4. Consideration of cultural nuances and appropriate register/politeness level
5. Justification for final {args.to_lang} translation choices and overall approach

Then provide your final translation on the last line.
```

### Value of the Experiment

translate6.py allows for more accurate measurement of the impact of the structured-output constraint, making it possible to verify the true performance difference from Level 1. In particular, it enables comparison of a complete reasoning process that includes the perspective of "how to translate."

### Investigating the Impact of Structured Output on Translation with Reasoning (Level 1 vs tr6)

Structured output via the `-r 1` option of [translate.py](translate.py); unstructured output via [translate6.py](translate6.py)

| Model | 1-05 | 1-10 | 1-20 | tr6-05 | tr6-10 | tr6-20 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | 59 | **93** | 27 | 70 | 68 | 81 |
| **aya-expanse-32b** | 93 | 86 | 90 | 90 | **96** | 92 |
| **command-r7b** | 42 | 24 | 35 | **55** | 44 | 31 |
| **command-r-35b** | 49 | 34 | 31 | 37 | **67** | 64 |
| **gemma2-9b** | 67 | 26 | 33 | 54 | **71** | 57 |
| **gemma3-4b** | 29 | 16 | 43 | **61** | 53 | 31 |
| **gemma3-12b** | 0 | 6 | 6 | **84** | 83 | 82 |
| **gemma3-27b** | 93 | **96** | 83 | 35 | **96** | 94 |
| **gemma3n-e4b** | 59 | 24 | 57 | 63 | **80** | 73 |
| **gpt-oss-20b** | 91 | **95** | 94 | 94 | 91 | 91 |
| **gpt-oss-120b** | 94 | **95** | 94 | 94 | **95** | 85 |
| **llama3.3** | **94** | 89 | 89 | 89 | 78 | **94** |
| **llama4-scout** | 27 | 18 | 18 | **89** | 80 | 77 |
| **ministral-3-3b** | 5 | 6 | 11 | 60 | 62 | **68** |
| **ministral-3-8b** | 12 | 16 | 21 | 65 | **76** | 71 |
| **ministral-3-14b** | 28 | 50 | 57 | 72 | 75 | **79** |
| **mistral-small3.2** | 80 | 94 | 86 | 88 | 19 | **95** |
| **mixtral-8x7b** | 48 | 35 | **51** | 8 | 8 | 11 |
| **mixtral-8x22b** | 85 | **87** | 83 | 84 | 46 | 85 |
| **phi4** | 26 | 25 | 78 | 80 | **90** | 60 |
| **qwen3-4b** | **67** | 58 | 37 | 59 | 57 | 56 |
| **qwen3-4b (nt)** | 38 | 30 | 34 | 39 | **56** | 51 |
| **qwen3-14b** | **85** | 72 | 69 | 65 | 78 | 67 |
| **qwen3-14b (nt)** | 85 | 73 | **87** | 81 | 69 | 66 |
| **qwen3-30b** | 94 | **96** | 94 | 0 | 9 | 0 |
| **qwen3-30b (nt)** | 94 | 78 | **96** | 0 | 0 | 0 |
| **qwen3-32b** | 70 | 90 | 79 | 92 | **94** | 69 |
| **qwen3-32b (nt)** | 28 | 48 | 22 | 68 | **88** | 78 |

- **Dramatic improvement with tr6**: gemma3-12b (1-10: 6 → tr6-10: 83, +77), phi4 (1-10: 25 → tr6-10: 90, +65), llama4-scout (1-10: 18 → tr6-05: 89, +71), ministral-3-3b (1-10: 6 → tr6-20: 68, +62), ministral-3-8b (1-10: 16 → tr6-10: 76, +60), qwen3-32b (nt) (1-10: 48 → tr6-10: 88, +40).
- **High-performing models are equivalent or favor structured output**: gpt-oss-120b (95 with both methods), gpt-oss-20b (1-10: 95 → tr6-05: 94, a slight decrease).
- **Structured output favored**: qwen3-30b (1-10: 96 → tr6-10: 9, -87, tr6 goes off the rails).
- **Important finding**: qwen3-30b (nt) fails completely with tr6 (0 points). Structured output (the 1-series) is essential as a guardrail.
- mixtral-8x7b performs poorly under both methods, but structured output is relatively better (1-20: 51, tr6-10: 8).

**Conclusion**: for models that degrade or collapse sharply under structured reasoning (Level 1) — such as gemma3-12b, llama4-scout, and phi4 — free-form reasoning (tr6) is an extremely effective workaround. Conversely, some models, such as qwen3-30b, break down in free form and require structured output, so making the reasoning process visible requires careful assessment of model suitability.

### Free-Form Reasoning Comparison (tr5 vs tr6)

[translate5.py](translate5.py) uses simplified reasoning, and [translate6.py](translate6.py) uses detailed reasoning

| Model | tr5-05 | tr5-10 | tr5-20 | tr6-05 | tr6-10 | tr6-20 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **aya-expanse-8b** | 52 | 53 | 54 | 70 | 68 | **81** |
| **aya-expanse-32b** | 88 | 86 | 82 | 90 | **96** | 92 |
| **command-r7b** | 34 | **71** | 20 | 55 | 44 | 31 |
| **command-r-35b** | 87 | **93** | 76 | 37 | 67 | 64 |
| **gemma2-9b** | 74 | 70 | **78** | 54 | 71 | 57 |
| **gemma3-4b** | **81** | 58 | 70 | 61 | 53 | 31 |
| **gemma3-12b** | **88** | 61 | 77 | 84 | 83 | 82 |
| **gemma3-27b** | **97** | 96 | 96 | 35 | 96 | 94 |
| **gemma3n-e4b** | 77 | 74 | 67 | 63 | **80** | 73 |
| **gpt-oss-20b** | 81 | 92 | 93 | **94** | 91 | 91 |
| **gpt-oss-120b** | **96** | 91 | **96** | 94 | 95 | 85 |
| **llama3.3** | 81 | 83 | 92 | 89 | 78 | **94** |
| **llama4-scout** | **94** | 59 | 56 | 89 | 80 | 77 |
| **ministral-3-3b** | 45 | **69** | 30 | 60 | 62 | 68 |
| **ministral-3-8b** | **82** | 28 | 47 | 65 | 76 | 71 |
| **ministral-3-14b** | 31 | 72 | **95** | 72 | 75 | 79 |
| **mistral-small3.2** | 94 | 94 | 83 | 88 | 19 | **95** |
| **mixtral-8x7b** | 0 | 0 | 8 | 8 | 8 | **11** |
| **mixtral-8x22b** | 63 | 60 | 66 | 84 | 46 | **85** |
| **phi4** | 68 | 85 | 83 | 80 | **90** | 60 |
| **qwen3-4b** | **59** | 32 | 50 | **59** | 57 | 56 |
| **qwen3-4b (nt)** | 15 | 22 | 40 | 39 | **56** | 51 |
| **qwen3-14b** | **83** | **83** | 80 | 65 | 78 | 67 |
| **qwen3-14b (nt)** | **82** | 67 | 68 | 81 | 69 | 66 |
| **qwen3-30b** | **10** | 0 | 6 | 0 | 9 | 0 |
| **qwen3-30b (nt)** | **0** | **0** | **0** | **0** | **0** | **0** |
| **qwen3-32b** | 74 | 84 | 89 | 92 | **94** | 69 |
| **qwen3-32b (nt)** | 80 | **90** | 87 | 68 | 88 | 78 |

- **tr6 improves things**: aya-expanse-32b (tr5-10: 86 → tr6-10: 96, +10), gpt-oss-20b (tr5-10: 92 → tr6-05: 94, +2), llama3.3 (tr5-20: 92 → tr6-20: 94, +2).
- **tr5 favored**: llama4-scout (tr5-05: 94 → tr6-05: 89, -5), ministral-3-14b (tr5-20: 95 → tr6-20: 79, -16), ministral-3-8b (tr5-05: 82 → tr6-10: 76, -6), gemma3-4b (tr5-05: 81 → tr6-05: 61, -20), gemma3-12b (tr5-05: 88 → tr6-05: 84, -4).
- **Equivalent levels**: gemma3-27b (96 with both methods), gpt-oss-120b (95–96), phi4 (85–90 with both methods).
- **Fails with both methods**: qwen3-30b (10 points or below for both tr5/tr6, 0 with nt), mixtral-8x7b (poor with both methods, around 10 points).

**Conclusion**: while detailed reasoning (tr6) works well for some models (e.g. aya-expanse-32b), simplifying the reasoning process (tr5) produces more stable quality for many models (ministral-3-14b, llama4-scout, gemma3-12b, etc.). The same counterproductive mechanism, where reasoning complexity hampers translation quality, can be observed here as well.

## List of Practical Settings by Model

Lists each model's top 3 entries (90 points or above) or single highest-scoring entry.

| Model | Score | Settings |
|:---|:---:|:---|
| **gemma3-27b** | 98 | 0 |
| **gemma3-27b** | 97 | 0-05, 0-10, tr4-05, tr4-10, tr5-05 |
| **gemma3-27b** | 96 | 0-20-a, 1-10, tr5-10, tr5-20, tr6-10 |
| **gpt-oss-120b** | 98 | 0-20-b |
| **gpt-oss-120b** | 96 | 0, 1, 2-10, 2-20, 3, tr5-05, tr5-20 |
| **gpt-oss-120b** | 95 | 0-05, 0-10, 1-10, 2, 2-05, tr6-10 |
| **aya-expanse-32b** | 97 | tr4-05 |
| **aya-expanse-32b** | 96 | tr4-10, tr6-10 |
| **aya-expanse-32b** | 95 | 0-20-b |
| **command-r-35b** | 96 | tr4-05 |
| **command-r-35b** | 95 | 2-10 |
| **command-r-35b** | 94 | tr4-20 |
| **ministral-3-8b** | 96 | 0-20-b |
| **ministral-3-8b** | 95 | 2-10 |
| **ministral-3-8b** | 94 | 0-20-a, 2-20 |
| **mistral-small3.2** | 96 | tr4-10 |
| **mistral-small3.2** | 95 | 0-10, tr6-20 |
| **mistral-small3.2** | 94 | 0-20-b, 1-10, 3, 4, tr4-05, tr4-20, tr5-05, tr5-10 |
| **qwen3-30b** | 96 | 1-10 |
| **qwen3-30b (nt)** | 96 | 1-nt-20 |
| **qwen3-30b** | 95 | 0-20-b, 2-05, 2-20, 3 |
| **qwen3-32b** | 96 | tr4-10 |
| **qwen3-32b (nt)** | 95 | 3-nt |
| **qwen3-32b** | 95 | 4 |
| **gemma3-12b** | 95 | 0 |
| **gemma3-12b** | 93 | 2-05 |
| **gemma3-12b** | 91 | tr4-10 |
| **gpt-oss-20b** | 95 | 1-10, 4 |
| **gpt-oss-20b** | 94 | 0-10, 1, 1-20, 2-20, tr6-05 |
| **gpt-oss-20b** | 93 | tr4-05, tr5-20 |
| **llama3.3** | 95 | 0-20-b, tr4-20 |
| **llama3.3** | 94 | 0-10, 0-20-a, 1-05, tr6-20 |
| **llama3.3** | 93 | 0 |
| **llama4-scout** | 95 | 0-05 |
| **llama4-scout** | 94 | tr5-05 |
| **llama4-scout** | 93 | tr4-05 |
| **ministral-3-14b** | 95 | 0-05, tr5-20 |
| **ministral-3-14b** | 92 | 0-20-a |
| **ministral-3-14b** | 91 | tr4-10 |
| **qwen3-14b** | 95 | 4 |
| **qwen3-14b** | 94 | 3 |
| **qwen3-14b** | 93 | 1 |
| **gemma2-9b** | 94 | 2-20 |
| **aya-expanse-8b** | 93 | 1-10 |
| **mixtral-8x22b** | 93 | 0-20-b |
| **gemma3n-e4b** | 91 | 2-05 |
| **phi4** | 91 | tr4-20 |
| **mixtral-8x7b** | 85 | 0-20-a |
| **gemma3-4b** | 81 | tr5-05 |
| **ministral-3-3b** | 74 | 0-20-a |
| **qwen3-4b (nt)** | 74 | 4-nt |
| **command-r7b** | 71 | tr5-10 |

※ Scores below 85 are not suitable for practical use.

## Recommended Models and Settings

Recommended models and settings for building a practical system, based on the latest standalone evaluation by qwen3.6 (716 cases) and comparative verification of structured vs. unstructured (free-form) output.

**Note**: Gemma 3 and earlier, as well as Llama, have license restrictions on generated content. Gemma 4 has been relaxed to the Apache 2.0 license. Models from Cohere (Command R, Aya Expanse) are not available for commercial use.

### Priority and Policy for Model Selection

1. **Balancing quality and stability (top priority)**: the `gpt-oss` series (120b/20b), `mistral-small3.2`, the `qwen3` series (30b/32b), and the `ministral` series (3-8b/3-14b). If license restrictions are acceptable, `gemma3-27b` offers the highest quality (98 points).
2. **Leveraging unstructured output (direct translation via tr4)**: for operating models whose true performance is unlocked by removing the structured constraint, such as the `llama` series, `command-r-35b`, `aya-expanse-32b`, and `qwen3-32b`.
3. **Educational/analytical use (visualizing the reasoning process)**: adopting models that maintain high quality with detailed free-form reasoning (`tr6`), such as `aya-expanse-32b` and the `gpt-oss` family. Structured reasoning (Level 1) is discontinued in principle.

---

### CPU Execution Environment (Lightweight Models)

1. **gemma3n-e4b** (max 91 points):
   - **Level 2 (h05)**: records its highest score (91 points) with two-stage translation (history 5). A strong performer despite its lightweight size.

If you have 32 GB or more of memory, the following MoE models are also candidates.

1. **qwen3-30b (nt)** (max 96 points):
   - **Level 1-nt (h20)**: **structured output is essential**. Unstructured output (tr4/tr5/tr6) causes complete runaway output (0 points), so the JSON schema must always be used as a guardrail. Level 0 is also stable at 93–95 points.
2. **gpt-oss-20b** (max 95 points):
   - **Level 0 / tr4**: combines high quality and high general applicability. Records stable high scores across multiple settings — 94 points at Level 0-10 and 94 points at tr6-05.

---

### GPU Execution Environment (High-Performance Models)

1. **gemma3-27b** (max 98 points):
   - **Level 0 / tr4**: extremely stable top quality across all settings, structured or unstructured.
   - **tr5 / tr6**: maintains high quality (96 points) even with free-form reasoning. The most robust model.
2. **gpt-oss-120b** (max 98 points):
   - **Level 0**: combines fast processing and top quality. Operation via API (Groq/Cerebras, etc.) is powerful.
3. **aya-expanse-32b** (max 97 points):
   - **tr4**: achieves its top score with direct translation once the structured constraint is removed.
   - **tr6**: performs very well with detailed reasoning (96 points), making it ideal for educational and analytical use.
4. **command-r-35b** (max 96 points):
   - **tr4**: performance improves dramatically once the structured constraint is removed (Level 0-10: 71 → tr4-05: 96).
5. **mistral-small3.2** (max 96 points):
   - **tr4-10**: achieves its top score with unstructured direct translation. Also highly stable at 94–95 points with Level 0.
6. **qwen3-30b / qwen3-30b (nt)** (max 96 points):
   - **Level 0 / Level 1**: **structured output is essential**. Unstructured output (tr4/tr5/tr6) causes complete runaway output (0 points), so the JSON schema must always be used as a guardrail.
7. **qwen3-32b / qwen3-32b (nt)** (max 96 points):
   - **tr4-10**: achieves its top score with unstructured direct translation. Also stable at 91–94 points with Level 0. Unlike qwen3-30b, it can also operate without structured output.
8. **ministral-3-8b** (max 96 points):
   - **0-20-b / 2-10**: an 8B-class model that records scores comparable to larger models. Also stable at 90–94 points with Level 0.

---

## Guidelines for Building a Practical System

### Summary of the Optimization Strategy

1. **The basis is "direct translation"**: the conventional hypothesis that complex reasoning systems = high-quality translation has been refuted. "Direct translation" (Level 0 or tr4), which avoids extra thinking steps, is both the most efficient and the highest quality.
2. **Checking suitability for structured constraints vs. free form**: it is essential to individually optimize by identifying whether the adopted model performs better with structured output (JSON, etc., e.g. qwen3-30b) or with unstructured text output (e.g. the llama family, command-r-35b).
3. **Moving to summary compression**: because the "forgetting/drift of terminology" caused by the sliding approach of the context history (`--history`) was quantitatively confirmed, the next-generation architecture will move to an approach that compresses and retains history as a "glossary + summary."

## Conclusion

Through comprehensive verification via objective evaluation, it was demonstrated that "appropriate model selection" combined with "adopting simple direct output suited to the model's characteristics" is the best approach for the translation task. While verbalizing the reasoning process (CoT) and structured constraints bring educational value and reliability of system integration, it was also revealed that, depending on the model, they can become a cognitive burden and a "counterproductive mechanism" that significantly hampers translation quality.

These findings are broadly applicable to language tasks beyond translation (text summarization, code generation, creative writing assistance, etc.), and it is important to always **first verify the effectiveness of simple direct output**.

## List of Other Experimental Tools

The following Python scripts are experimental tools created during research and development. For detailed implementation and evaluation results, see [OBSOLETE.md](OBSOLETE.md).

- **translate-exp.py**: a subcommand-based, multi-stage translation system (supporting Phase 1/2/2a/3)
- **translate2.py**: a self-contained, single-pass version of 3-stage multi-model translation
- **translate3.py**: a self-contained, single-pass version of the integrated Phase 2a system (recommended)
- **draft_to_text.py**: a utility for extracting text from JSON-format intermediate data
- **analyze_2stage_diff.py**: a tool for analyzing quality differences by translation method

These tools are highly experimental in nature, and since objective evaluation revealed the superiority of Level 0 (direct translation), they are retained as research records.
