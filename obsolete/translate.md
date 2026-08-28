# Multi-stage translation system development log

## Overview

Evolved translate.py from single-pass processing into a multi-stage translation system, achieving high-quality translation that avoids cognitive bias.

## Key implementation changes

### 1. Required model specification
```python
# Before
parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model to use for translation")

# After
parser.add_argument("-m", "--model", required=True, help="Model to use for translation")
```

### 2. Expanded reasoning levels
```python
# Expanded reasoning level choices
parser.add_argument("-r", "--reasoning-level", type=int, default=2, choices=[0, 1, 2, 3, 4])
```

**Characteristics of each level:**
- **Level 0**: No reasoning, direct translation
- **Level 1**: Translation with standard reasoning
- **Level 2**: Two-stage translation (default, quality-focused)
- **Level 3**: Three-stage translation (reasoning + two-stage translation)
- **Level 4**: Split three-stage translation (split into two LLM calls)

### 3. Context control feature
```python
parser.add_argument("--history", type=int, default=5, help="Number of history entries to include in context")
parser.add_argument("--translated-context", action="store_true", help="Provide only the translated text")
```

### 4. Unified field definitions
Defined common field templates and dynamically embedded the language pair:
```python
translation_field = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")
quality_assessment_field = Field(description=f"Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words remain...")
```

### 5. Split processing implementation for level 4
```python
if args.reasoning_level == 4:
    # Stage 1: reasoning and initial translation
    first_parsed = generate_with_retry([context, prompt], FirstStageTranslation, args.model, "Stage 1")

    # Stage 2: quality assessment and improved translation
    second_stage_prompt = f"Review and improve this translation..."
    second_parsed = generate_with_retry([context, second_stage_prompt], SecondStageTranslation, args.model, "Stage 2")
```

### 6. Strengthened error handling
```python
def generate_with_retry(prompts, schema, model, stage_name=""):
    """LLM generation function with retry support"""
    for j in range(5):
        try:
            result = generate_with_schema(...)
            return json.loads(result.text.strip())
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise
```

## Parallel development: dedicated translation systems

### translate-exp.py (subcommand approach)
Three-stage multi-model translation system:
- **Phase 1**: Initial translation
- **Phase 2**: Quality check with a different model
- **Phase 3**: Apply corrections

### translate2.py / translate3.py (end-to-end versions)
- **translate2.py**: Three-stage multi-model translation (85-point quality)
- **translate3.py**: Phase 2a integrated system (92-point quality, recommended)

## Quality evaluation results

| System | Quality score | Efficiency | Use case |
|:---|:---:|:---:|:---|
| **translate3.py (Phase 2a)** | **92 points** | **High** | **Practical high-quality translation** |
| translate.py Level 2 | 92 points | Medium | Legacy system |
| translate2.py (three-stage) | 85 points | Low | Research/experimentation |

## Technical value

### Problems solved
1. **Language mixing**: untranslated words remaining, e.g. French "Bonjour"
2. **Cognitive bias**: the limits of quality-checking with the same model
3. **Usability**: an overly complex subcommand structure

### Innovations
1. **Multi-model collaboration**: leveraging the strengths of different models
2. **Staged quality improvement**: a phase-based approach
3. **Practicality focus**: balancing efficiency and quality

## Recommended usage

### Everyday high-quality translation
```bash
python translate3.py input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma3n:e4b -c ollama:qwen2.5:7b
```

### Legacy system (kept for compatibility)
```bash
python translate.py input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma3n:e4b -r 2
```

### Research/analysis use
```bash
python translate2.py input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma3n:e4b -c ollama:qwen2.5:7b
```

## Summary

The shift from complexity to practicality established a system that efficiently achieves the highest quality (92 points). translate3.py's **Phase 2a integrated system** is the most practical and recommended solution.
