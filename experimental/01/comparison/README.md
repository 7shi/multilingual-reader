# Translation Quality Comparison Analysis: Effect of the Reasoning Feature

## Experiment Overview

We analyzed the quality difference caused by enabling or disabling the reasoning feature when translating a French podcast transcript into Spanish.

**Translation target:** `examples/finetuning-fr.txt` (a technical dialogue about AI training methods)
**Translation direction:** French → Spanish
**Model used:** `ollama:gemma3n:e4b`

**Generated files:**
- `comparison/0.txt`: generated with reasoning level 0 (basic translation)
- `comparison/1.txt`: generated with reasoning level 1 (translation with a reasoning process)
- `comparison/2.txt`: generated with reasoning level 2 (two-stage quality-checked translation)

## Evaluation Results (translation by Gemma 3n E4B)

| Condition | Output file | Score | Key characteristics |
|------|-------------|--------|----------|
| Without reasoning | `0.txt` | 75 | Reduced accuracy in word choice, incomplete grasp of context |
| With reasoning | `1.txt` | 88 | Appropriate word choice, natural expression, consistency |
| **Two-stage translation** | **`2.txt`** | **93** | **Highest quality, unified language, only minor redundancy** |

## Detailed Analysis

### Issues without reasoning (0.txt)
- **Critical mistranslation**: "C'est-à-dire ?" → "Quiero decir?" (a serious mistranslation that breaks the conversational context)
- **Major translation omissions**: shallow handling due to insufficient understanding of French-specific expressions
- **Word choice**: "bachotage" → "memorizar para un examen" (a literal expression that doesn't fit the context)
- **Terminology**: "antisèche" → "libreta de consulta" (lack of cultural adaptation)
- **Consistency**: language confusion and breaks in context

### Advantages with reasoning (1.txt)
- **Accurate free translation**: "C'est-à-dire ?" → "¿A qué te refieres?" (an appropriate translation suited to the context)
- **Word-choice accuracy**: "bachotage" → "bachotear" (a natural Spanish expression that fits the context)
- **Cultural adaptation**: "antisèche" → "libreta de apuntes" (an accurate cultural equivalent)
- **Terminology**: consistent, accurate translation of technical concepts
- **Thinking process**: deeper contextual understanding through the Chain of Thought effect
- **Minor issue**: some original-language words such as "donc" remain (can be improved through proofreading)

## Key Findings

### Mechanism of the reasoning feature's effect

**Quality improvement through Chain of Thought:**
1. **Verbalizing the thinking process**: analyzing the source text's meaning, context, cultural nuance, and speaker intent before translating
2. **Forcing multi-angle consideration**: promoting careful, deep contextual understanding rather than a surface-level interpretation
3. **Deeper contextual understanding**: achieving translation at the concept level rather than the word level
4. **Cultural nuance**: appropriate handling of language-specific expressions
5. **Improved consistency**: unified treatment of terminology and concepts
6. **Quality stability**: more predictable, reliable output

### Technical implications and prompt design strategy
- **Specialized domains**: reasoning is especially effective for technical and academic documents
- **Cultural elements**: improves translation accuracy for idiomatic expressions and culture-specific concepts
- **Long-text handling**: clearly improves the ability to maintain context
- **Versatility**: the reasoning requirement is also effective for advanced language tasks beyond translation

## Overall Conclusion

The reasoning feature brought a **significant 13-point improvement** in translation quality, demonstrating that verbalizing the thinking process draws out the model's latent capability. In particular:

1. Deeper conceptual understanding for **specialized content**
2. Appropriate handling of **cultural nuance**
3. Improved accuracy of **word choice** (from literal translation to context adaptation)
4. **Avoidance of critical mistranslations** (maintaining conversational context)
5. Ensuring **overall consistency**

**Value as a prompt design strategy:** requiring reasoning forces the model to consider things from multiple angles and carefully, and is a highly effective strategy for greatly reducing the risk of mistranslation from surface-level interpretation.

## Additional Verification of Two-Stage Translation

We evaluated the results of a newly implemented two-stage translation (reasoning level 2).

### Advantages of two-stage translation (2.txt): 93 points

**Breakthrough improvements:**
- **Complete language unification**: language mixing was fully eliminated
- **Naturalness of expression**: more appropriate Spanish expressions were chosen
- **Quality stability**: consistently high-quality translation was achieved

**Minor issues (-7 points):**
- Some duplicate expressions and redundancy remain (e.g., "¿es ahí donde se aplica... ¿O es ahí donde entra...?")
- Some unnatural expressions ("experto a tiempo completo/definitivo")

### Evolutionary Improvement of Translation Methods

| Method | Score | Improvement | Key effect |
|------|--------|--------|----------|
| Without reasoning | 75 | - | Baseline |
| With reasoning | 88 | +13 | Deeper contextual understanding |
| **Two-stage translation** | **93** | **+18** | **Quality-check effect** |

### Mechanism of the Two-Stage Translation Effect

1. **Draft stage**: generates an initial translation
2. **Quality-check stage**: identifies mistranslations, language mixing, and unnatural expressions
3. **Final translation stage**: produces a high-quality translation with the identified issues fixed

Through this three-stage process, issues that conventional methods overlooked were systematically corrected, **achieving the highest quality translation**.

## Comparison with Other Models

Under the same condition (two-stage translation at reasoning level 2), we verified the translation performance of Gemma 3 4B and Qwen3 4B.

### Translation Quality Evaluation by Model

| Model | Claude score | Gemini score | Average score | Characteristics |
|--------|------------|------------|------------|------|
| **Gemma 3n E4B (2.txt)** | 88 | 95 | **91.5** | **Highest quality, best suited for technical documents** |
| **Gemma 3 4B** | 85 | 80 | **82.5** | **Natural expression, suited for general audiences** |
| **Qwen3 4B** | 78 | 65 | **71.5** | **Basic translation is possible, but needs revision** |

### Detailed Analysis Results

#### Gemma 3n E4B (original): 91.5 points
**Advantages in the combined evaluation:**
- **Terminology consistency**: accurate and consistent translation of AI/machine learning terms
- **Technical accuracy**: precise explanation of concepts and faithfulness to the source text
- **Structured expression**: logically and systematically organized sentences

**Points both evaluators agreed on:**
- Excellent translation of technical terms such as "aprendizaje por transferencia"
- Accurate conveyance of technical concepts
- Quality stability from the reasoning feature

#### Gemma 3 4B: 82.5 points
**Notable qualities:**
- **Natural conversational tone**: fluency well suited to a podcast format
- **Readability**: the most accessible expression for a general audience
- **Appropriateness of free translation**: flexible translation suited to context

**Issues:**
- Some free translations shift the nuance of the source text
- Instability in terminology consistency
- Omission at the end of the text (due to processing limits)

#### Qwen3 4B: 71.5 points
**Basic performance:**
- Achieved a basic understanding of the main concepts
- Maintained sentence structure

**Major issues:**
- **Critical mistranslation**: "antisèche" → "antiestática" (cheat sheet → anti-static)
- **Vocabulary processing error**: "bachotage" left untranslated
- **Grammatical inconsistencies**: basic grammar errors such as verb conjugation

### Model Selection Guidance

#### Recommended Model by Use Case

**Technical documents, academic papers, official documents:**
- **First choice**: Gemma 3n E4B (reasoning level 2)
- The best solution when accuracy and specialization are the priority

**General-audience articles, blogs, marketing materials:**
- **Recommended**: Gemma 3 4B
- When readability and approachability are the priority

**Drafts, reference translations, bulk processing:**
- **Limited use**: Qwen3 4B
- Human proofreading and correction are always required

#### Cost-Efficiency Analysis

| Model | Quality | Processing speed | Correction cost | Overall efficiency |
|--------|------|----------|------------|----------|
| Gemma 3n E4B | Highest | Medium | Minimal | **Best** |
| Gemma 3 4B | High | High | Low | Good |
| Qwen3 4B | Medium | Highest | High | Low |

### Overall Recommendations

**Guidelines by use case:**
- **When the highest quality is required**: Gemma 3n E4B (reasoning level 2) — important/official documents
- **Standard high quality**: Gemma 3n E4B (reasoning level 1) — specialized documents, culturally sensitive content
- **When readability is the priority**: Gemma 3 4B — general-audience content
- **When bulk processing/speed is the priority**: without reasoning (reasoning level 0) — general documents, draft stage
- **Cost efficiency**: choose the model and reasoning level according to document importance and processing volume

**General principle for prompt design:**
Requiring verbalization of the thinking process makes it possible to draw out a model's latent capability to the fullest in advanced language tasks. Although two-stage translation increases processing time, the **18-point quality improvement** demonstrates that it is an extremely effective method for translating important documents. In model selection, choosing appropriately according to the use case and the required quality level is important.

### Implementation Flexibility Through Structured Output

An important technical value of this experiment lies in **a schema-based implementation that leverages structured output**.

**Technical advantages:**
- **Switching functionality via schema alone**: translation methods can be changed without code changes
- **Dynamic quality control**: a single reasoning-level parameter selects among three translation strategies
- **Extensibility**: new translation methods can be implemented simply by adding a schema
- **Maintainability**: each translation mode is managed as an independent schema class

**Implementation example:**
```python
# Level 0: simple translation only
class Translation(BaseModel):
    translation: str

# Level 1: with a reasoning process
class Translation(BaseModel):
    reasoning: str
    translation: str

# Level 2: two-stage quality check
class Translation(BaseModel):
    draft_translation: str
    quality_check: str
    translation: str
```

This **schema-driven approach** cleanly separates complex translation logic and allows the optimal translation method to be easily chosen for each use case. It is a design that takes full advantage of the power of structured output, with excellent extensibility and maintainability.
