# Summary Compression Translation Experiment

An experiment directory that migrates the [experimental/01](../01/) translation architecture to a "summary compression" approach.

## Background and motivation

The old architecture ([experimental/01/translate.py](../01/translate.py)) used a sliding-window approach, embedding past translations as a string into every request, which caused:

- **KV cache disabled**: since the beginning of the prompt changed every time, the model's cache couldn't be reused
- **Terminology drift**: once older history was pushed out of the window, the translation of proper nouns and technical terms would change

The new architecture is based on the [reference implementation](ref/) and maintains a fixed `system + summary + most recent N entries` structure, solving both problems.

## Translation system

Scripts must always be run with `uv run` (calling `python` directly won't resolve dependencies).

### translate.py

```bash
uv run translate.py <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**Options:**

| Option | Default | Description |
|---|---|---|
| `--threshold` | 10 | Interval (in translation pairs) between summary generations |
| `--keep` | 5 | Number of translation pairs kept between a summary and reorganization |
| `--summary glossary` | none | Summary method (defaults to simple deletion if unspecified) |
| `--schema` | none | Enable structured output (JSON schema) (not used for direct translation output tasks) |
| `--no-think` | none | Disable reasoning (for Qwen3/Gemma4, generally specified during translation) |

**About CoT (think):**

Reasons `--no-think` is generally specified during translation:

- **Quality**: CoT-based refinement is overkill for a simple line-by-line translation task. An earlier experiment ([experimental/01/README.md](../01/README.md)) also concluded that CoT is harmful for translation.
- **Speed**: CoT inflates processing time by tens of times.
- **KV cache**: since CoT tokens are included in the model's generation history, removing CoT from the history when passing it changes the sequence and causes cache misses. On the other hand, keeping CoT in the history would accumulate dozens of times more volume than the translation text itself. With `--no-think`, this problem doesn't arise at all.

CoT is useful in scenarios that require "synthesizing multiple pieces of information into a judgment," and there's little room for that in single-line translation. Passing whole sections at once would allow refining consistency of context and style, but with 30B-class models there's a risk of dropped lines or hallucination partway through a long output. "Line-by-line, no-think" is a practical optimum balancing reliability and quality for 30B-class models.

**Concrete example of CoT harm (debug1):** with gemma4:31b (think) × `--schema` (glossary-schema), the output at line 23 of 43 collapsed. When translating `bachoter pour un examen` (a French idiom), CoT's reasoning process mixed multiple languages, and under the schema constraint it failed to fully return to Spanish, producing:

```
Camille: ¿La diferencia entre estudiar hurriedlyдля an exam and truly mastering a subject?
```

English (`hurriedly`) and Cyrillic (`для`, Russian) were mixed into a Spanish sentence. This single instance caused the score to plunge to 62 points. With `--no-think` on the same model, the score recovered to 96, suggesting this is an issue specific to the `think × schema` combination.

**Glossary method design:**

We also considered extracting all terminology from the whole text up front, but since that could miss terms, we adopted a local approach that picks up terms incrementally while translating (`--summary glossary`). As the glossary accumulates during translation, consistency improves as the text progresses.

**Summary method behavior (threshold=10, keep=5):**

- A summary is generated every 10 lines, and 5 lines after the summary is generated, the context is compressed into `system + latest summary + most recent 5 entries` (compression occurs at lines 15, 25, 35, ...)
- A summary is generated at line 10, followed by 5 more translations, then compression happens at line 15. Between summary generation and compression, the 5 entries benefit from the KV cache. The request right after compression is a cold start since the prefix changes, after which caching resumes with the new prefix (details → [debug2/README.md](debug2/README.md))
- The most recent N entries act as few-shot examples of the translation style. If the session were reconstructed from the summary alone, the model could be pulled toward the summary's phrasing and the translation quality could degrade, so keeping several actual translation examples stabilizes the style

**Implementation notes:**

- Translating line by line prevents dropped lines and hallucination (a phenomenon where the model drifts into free composition mid-translation)
- Structured output (`pydantic.BaseModel`) is only used when `--schema` is specified; otherwise raw text is received
- Calls go through `llm7shi.compat.generate_with_schema`, allowing provider switching via `ollama:`, `openai:`, `google:` prefixes
- Passing `chat_history` (with roles) as-is enables the KV cache (details → [debug2/README.md](debug2/README.md))

**KV cache concern (hybrid mode):** the design where the summary is removed from history after generation and translation continues assumes Ollama supports prefix-based caching. It's unconfirmed whether Ollama can reuse the cache up to `[system, u1..u10]` when sending a rewound history (`[system, u1..u10, u11]`) after a summary-generation request. If it doesn't, translation after a summary would incur a cache miss every time.

### batch.sh

A script that runs translation, evaluation, and aggregation for the specified models × variants in one batch.

```bash
bash batch.sh
```

The three phases (translation, evaluation, aggregation) are separate, and existing files are skipped, so the run is resumable from any point. Translation results go to [tr/](tr/), evaluation results to [evals/](evals/), and it finally produces [SCORES.txt](SCORES.txt).

---

## Evaluation system

Uses the [experimental/01](../01/) evaluation pipeline as-is.

### Evaluation criteria (5 items × 20 points = 100 points max)

| Item | Description |
|---|---|
| **Readability and comprehensibility** | Whether a target-language reader can easily understand the content; whether the text structure is logical. |
| **Fluency and naturalness** | Whether it reads naturally to a native speaker; absence of awkward literal translations or word choices. |
| **Terminology appropriateness** | Whether technical terms (`fine-tuning`, `in-context learning`, etc.) are handled appropriately and consistently. |
| **Contextual adaptation** | Whether the original's intent is conveyed; consideration for the target culture. |
| **Information completeness** | Absence of missing or superfluously added important information. |

Detailed scoring criteria → [experimental/01/EVAL.md](../01/EVAL.md)

### Scoring guide

| Score band | Assessment |
|---|---|
| 18-20 points | High quality, no notable flaws |
| 13-17 points | Minor issues present |
| 6-12 points | Major flaws (grammar errors, untranslated portions, etc.) |
| 0-5 points | Structural flaws (mixed languages, JSON fragments, etc.) |

### Evaluation pipeline

```bash
# 1. Individual evaluation (once)
uv run trtools eval \
  --original ../../examples/finetuning-fr.txt \
  --translation <translation.txt> \
  -f French -t Spanish -m ollama:qwen3.6 -w 3 -o <output.json>

# 2. Evaluate 3 times → aggregate median
uv run trtools agg evals/*.json

# 3. Generate SCORES.md
uv run ../01/generate_scores_md.py -1 91 -2 92 SCORES.txt
```

**Evaluator:** `qwen3.6` (accurately identifies technical flaws through logical CoT verification)
**Aggregation:** median of 3 evaluation runs (removes evaluation noise)
**Statistics:** median, mean, and standard deviation computed per item and overall

Background on evaluator selection → [experimental/01/MEMO.md](../01/MEMO.md)

### Evaluating the reference translation (Gemini 2.5 Pro)

Scored [examples/finetuning-es.txt](../../examples/finetuning-es.txt) (a reference translation by Gemini 2.5 Pro) through the same pipeline (3 evaluation runs, median).

| Item | eval-1 | eval-2 | eval-3 | Median |
|---|:---:|:---:|:---:|:---:|
| readability | 19 | 19 | 19 | **19** |
| fluency | 19 | 19 | 19 | **19** |
| terminology | 19 | 20 | 20 | **20** |
| contextual_adaptation | 20 | 19 | 19 | **19** |
| information_completeness | 20 | 20 | 20 | **20** |
| **Total** | **97** | **97** | **97** | **97** |

All three runs scored 97 with zero evaluation variance.

**Points deducted:**

- **readability -1 (all 3 runs)**: no specific issue cited; appears to be a ceiling effect
- **fluency -1 (all 3 runs)**: `Lo has entendido todo` (overly literal, noted in eval-3), `guía rápida` (a weak metaphor for `antisèche`, noted in eval-2)
- **terminology -1 (eval-1 only)**: no clear reason given for the deduction; the reasoning was actually positive, calling it "standard and consistent." Possibly a ceiling effect
- **contextual_adaptation -1 (eval-2, eval-3)**: noted that `Tech Relámpago` (a literal rendering of `Tech Éclair`) doesn't fully reproduce the original's wordplay

**Notes:**

- `Tech Relámpago` was translated on the assumption that the podcast's original was Spanish; the evaluator was not told about this premise for this experiment. Since the evaluator scored it as a translation from French, this point reflects that mismatched premise.
- `antisèche` was translated as `guía rápida` (quick guide), and while `chuleta` (crib sheet) would be closer to the original meaning, this evaluation did not flag it.

---

## Experimental results

### Phase A: functional check (gemma3:27b)

Translation input: [examples/finetuning-fr.txt](../../examples/finetuning-fr.txt) (43 lines, French podcast)
Target language: Spanish (median of 3 evaluation runs)

| Variant | Processing time | Score (median of 3) |
|---|---|---|
| `none` | 4.0 min | 95 points |
| `glossary` | 6.8 min | 98 points |

Run without `--schema` (raw text output). Re-evaluated after the `llm7shi` v0.10.1 update (fixing the role-conversion issue), confirming `glossary` now outperforms `none`.

**Example terminology translations (glossary mode):**
- `pré-entraînement` → `pre-entrenamiento`
- `ajuste fino (fine-tuning)` (English noted in parentheses)
- `aprendizaje por transferencia`
- `aprendizaje en contexto (ICL)`
- `anclaje (grounding)`
- `bachoter` → `memorizar para un examen` (culturally localized)

### debug1: method selection

| Model | none | glossary | none-schema | glossary-schema |
|---|---|---|---|---|
| gemma3:27b | 95 | **98** | 99 | 96 |
| gemma4:31b (think) | 98 | **98** | 97 | 62 |
| gemma4:31b (no-think) | 98 | **97** | 96 | 96 |
| gpt-oss:120b | **97** | 87 | 88 | 90 |
| qwen3.6 (think) | 96 | **97** | 96 | 96 |
| qwen3.6 (no-think) | 93 | **94** | — | — |

- `--schema` dropped: gemma4:31b's glossary-schema=62 is emblematic — quality dropped across multiple models
- `--summary glossary` adopted: it was counterproductive for gpt-oss:120b (`bachotaje`, a direct French transliteration, issue) and only 1 point (97 vs 98) worse for gemma4:31b (no-think), but equal or better for every other model
- `--no-think` adopted: qwen3.6 shows a gap between think (97) and no-think (94), but since processing time balloons by tens of times, no-think is sufficient

### Phase B: production run

All models in [MODELS.txt](MODELS.txt) (34 models) × `glossary` mode × 3 evaluation runs (aggregated in [SCORES.txt](SCORES.txt))

**Policy:**
- Structured output (`--schema`) judged unnecessary for direct translation output tasks, so unused
- `--summary glossary` adopted (to prevent terminology drift)
- `--no-think` applied to Qwen3/Gemma4-series models

**Results (32 models, sorted by score descending):**

| Model | Score | Notes |
|---|---|---|
| qwen3.6-27b | 97 | Repeated `Exactamente` (reduced lexical variety) |
| gemma4-31b | 97 | Typos (accents/quotes), inconsistent formality (`usted`/`hablarte`) |
| gemma4-26b | 97 | `en coulisses` → `de forma interna` (`entre bastidores` recommended) |
| llama4-scout | 96 | `bachoter` mistranslated (meaning reversed), eval-2 plunged to 89 |
| gemma3-27b | 96 | `antisèche` → `memoria auxiliar` (`chuleta` recommended) |
| aya-expanse-32b | 96 | Full-width exclamation typo, podcast name `Tech Relámpago` translated literally |
| qwen3.6-35b | 95 | `fine-tuning` inconsistently rendered as `afinamiento`/`ajuste fino` (flagged in all 3 runs) |
| qwen3-32b | 95 | eval-3 dropped to 92 (fluency=17, literal conversational phrases like `¿Es decir?`) |
| mistral-small3.2 | 95 | eval-3 dropped to 93 (fluency=17, `informaciones` French interference) |
| gemma4-e4b | 95 | Leftover `*prompt*` markup (eval-3), preference issue in `anclaje` term choice |
| gemma3-12b | 95 | `sus inmensas conocimientos` gender/number agreement error (eval-1 dropped to 93) |
| ministral-3-14b | 94 | eval-2 plunged to 88 (fluency=16, grammar errors, French interference) |
| gpt-oss-120b | 94 | eval-3 plunged to 76 (`¿Eso qué?` slang/false-friend issue) |
| gpt-oss-20b | 91 | High evaluation variance (88-97), fluency/terminology consistency issues |
| qwen3.5-27b | 90 | `informações` (Portuguese) mixed in, `muletilla` (mistranslation of `antisèche`) |
| ministral-3-8b | 89 | eval-2 plunged to 74 (inserted translator meta-notes, gender agreement errors, terminology issues) |
| gemma4-e2b | 88 | French interference (`levantar el velo`, etc.), `tras bambalée` (nonexistent expression) |
| llama3.3 | 84 | `haber nos escuchado` grammar error (flagged in all 3 runs), `afinizar` (coined word) |
| gemma3-4b | 84 | `bachoter` → `aprobar por nota` (meaning drift), literal translation of French idioms |
| qwen3.5-35b | 82 | `informaciones`/`informaciónes` (French interference), eval-2 dropped to 76 |
| aya-expanse-8b | 79 | `ICL` typo'd as `LCL`, `grounding` → `referenciación`/`ancraje` (non-standard) |
| gemma3n-e4b | 78 | Mixed formality (`tú`/`usted`/`vosotros`), typos (`pre-entrerenamiento`, etc.) |
| phi4 | 76 | `informaciones` French interference, `ancoraje` (non-standard), high evaluation variance (73-84) |
| command-r7b | 76 | `grounding` → `amarre` (mooring, mistranslation), inconsistent formality (`tú`/`usted` mixed) |
| qwen3.5-4b | 74 | `Solucionamos estas IAs` (mistranslation of `percibimos`), many literal French renderings |
| qwen3-14b | 74 | Numerous gender/number agreement errors (e.g. `Las conocimientos`), eval-3 plunged to 64 |
| command-r-35b | 72 | `cuando begins` (English mixed in), eval-3 plunged to 63 (fluency=7) |
| qwen3.5-9b | 70 | Systematic gender/number agreement errors (e.g. `las conocimientos`), `ajustamiento fino` (non-standard) |
| ministral-3-3b | 63 | eval-3 plunged to 52 (fluency=8, leftover French `bachotaje`, many gender agreement errors) |
| qwen3-4b | 40 | Capability limit reached (74 was the prior experiment's best). Mixed-language output, unstable terminology |
| gemma2-9b | 27 | Translates fine, but appends an extraneous message after every line |
| qwen3-30b | 0 | With no structured output, free-form generation output the CoT reasoning text as the "translation" |
| mixtral-8x7b | - | Interactive comments accumulated and amplified into errors |
| mixtral-8x22b | - | Failed to load (memory configuration issue) |

Top-tier LLM models reach the same level as the reference translation. The pattern of a uniform -1 in readability and fluency is common across all top models, suggesting **97 points is effectively the ceiling** for this evaluator. Models at 97 can be considered near-perfect.

**Main patterns:**

- **French interference**: `informaciones` (an uncountable noun in Spanish) appeared across multiple models (qwen3.5-27b, qwen3.5-35b, phi4, ministral-3-3b, etc.). Also `haber nos` (llama3.3), `tras bambalée` (gemma4-e2b), and others
- **Gender/number agreement errors**: `Las/sus conocimientos` (treated as feminine when it should be masculine) recurred in mid-to-low-scoring models (qwen3-14b, qwen3.5-9b, ministral-3-3b, etc.)
- **Terminology mistranslations**: `grounding` → `amarre` (mooring, command-r7b), `ICL` → `LCL` (aya-expanse-8b), and other structural errors
- **Mixed formality/person**: `tú`/`usted`/`vosotros` mixed within the same text (gemma3n-e4b, command-r7b, qwen3-14b, etc.)
- **Inserted translator meta-notes**: some models sporadically added annotations or comments to the translation output (main cause of ministral-3-8b's eval-2 plunge)

**Overall assessment:**

- **gemma4-26b** is the best choice overall. It has the highest score stability (range of 1), with deductions limited to idiom-choice preferences. Zero mistranslations, typos, or grammatical flaws. Matches gemma4-31b's score with fewer parameters.
- **qwen3.6-27b** comes next, but note the risk of self-evaluation bias since the evaluator is a model from the same family (`ollama:qwen3.6`).
- **llama4-scout** has a median of 96, but the `bachoter` mistranslation (which caused a plunge to 89) raises concerns about reliability if it recurs.

---

### Phase C: comparison with the old architecture

Compares each model's best score from the "practical settings list per model" in the old architecture ([experimental/01/qwen3.6/SCORES.md](../01/qwen3.6/SCORES.md)), without distinguishing `nt`.

| Model | Old best | New glossary | Difference |
|---|:---:|:---:|:---:|
| gemma3-27b | 98 | 96 | -2 |
| gpt-oss-120b | 98 | 94 | -4 |
| aya-expanse-32b | 97 | 96 | -1 |
| command-r-35b | 96 | 72 | **-24** |
| ministral-3-8b | 96 | 89 | -7 |
| mistral-small3.2 | 96 | 95 | -1 |
| qwen3-30b | 96 | 0 | **-96** |
| qwen3-32b | 96 | 95 | -1 |
| gemma3-12b | 95 | 95 | 0 |
| gpt-oss-20b | 95 | 91 | -4 |
| llama3.3 | 95 | 84 | -11 |
| llama4-scout | 95 | 96 | **+1** |
| ministral-3-14b | 95 | 94 | -1 |
| qwen3-14b | 95 | 74 | **-21** |
| gemma2-9b | 94 | 27 | **-67** |
| aya-expanse-8b | 93 | 79 | -14 |
| mixtral-8x22b | 93 | not run | — |
| gemma3n-e4b | 91 | 78 | -13 |
| phi4 | 91 | 76 | -15 |
| mixtral-8x7b | 85 | not run | — |
| gemma3-4b | 81 | 84 | **+3** |
| ministral-3-3b | 74 | 63 | -11 |
| qwen3-4b (nt) | 74 | 40 | **-34** |
| command-r7b | 71 | 76 | **+5** |

**Trends:**

- **Improved or comparable (within ±2 points):** gemma3-12b(0), aya-expanse-32b(-1), mistral-small3.2(-1), qwen3-32b(-1), ministral-3-14b(-1), llama4-scout(+1), gemma3-4b(+3), command-r7b(+5)
- **Slight decline (-3 to -15):** gpt-oss-120b(-4), gpt-oss-20b(-4), ministral-3-8b(-7), llama3.3(-11), ministral-3-3b(-11), gemma3n-e4b(-13), aya-expanse-8b(-14), phi4(-15)
- **Large decline (known issues):** command-r-35b(-24), qwen3-14b(-21), qwen3-4b(-34), gemma2-9b(-67), qwen3-30b(-96)

The old best represented "the highest score with an optimized configuration," whereas the new architecture reaches a comparable level with a single uniform setting (`--summary glossary`). Most large declines stem from known issues (qwen3-30b requires structured output, gemma2-9b appends "Let me know if you need anything else translated!" to every line).

**Qualitative terminology-drift check (gemma3-27b):**

Comparing the old [tr-0/gemma3-27b-0-20-a.txt](tr-0/gemma3-27b-0-20-a.txt) with the new [tr/gemma3-27b.txt](tr/gemma3-27b.txt).

| Term (original) | Old | New | Match |
|---|---|---|:---:|
| pré-entraînement | pre-entrenamiento | pre-entrenamiento | ✓ |
| fine-tuning | ajuste fino (fine-tuning) | ajuste fino (fine-tuning) | ✓ |
| aprendizaje por transferencia | aprendizaje por transferencia | aprendizaje por transferencia | ✓ |
| ICL | aprendizaje en contexto, o ICL (In-Context Learning) | aprendizaje en contexto, o ICL (In-Context Learning) | ✓ |
| grounding | anclaje (grounding) | anclaje (grounding) | ✓ |
| bachoter | memorizar para un examen | memorizar para un examen | ✓ |
| Transformers | los Transformers | los Transformers | ✓ |
| ventana de contexto | ventana de contexto | ventana de contexto | ✓ |

No terminology drift. Stylistically, the new version used multiple expressions that read more naturally in Spanish (consistent informal register, subject omission). Terminology consistency from `--summary glossary` matches or exceeds the old architecture.

**Terminology drift check (qwen3-32b):**

`--summary glossary` maintains within-document consistency, but the term choices sometimes diverge from the standard:

- `fine-tuning` → consistently rendered as "**afinamiento**" rather than "ajuste fino"
- `ICL` → consistently rendered with the non-standard abbreviation "**AEC**" instead of the standard one

The old architecture's terminology drift (translation shifting line by line) has been resolved, but model-specific term-choice issues remain. If forcing a particular term or seeding an initial glossary is needed, prompt-level measures are required.

---

## Lightweight model analysis: gemma4-e4b

Among lightweight models, gemma4-e4b (95 points) stood out, so we analyzed it in detail.

### Score by category

| Item | eval-1 | eval-2 | eval-3 |
|---|:---:|:---:|:---:|
| readability | 19 | 19 | 19 |
| fluency | 19 | 19 | 18 |
| terminology | **20** | 18 | 18 |
| contextual_adaptation | 19 | 19 | 19 |
| **information_completeness** | **20** | **20** | **20** |
| **Total** | **97** | **95** | **94** |

### Notable point: perfect information completeness across all 3 runs

`information_completeness` scored 20/20 in all three evaluations. Even top-tier large models sometimes drop to 19 in some evaluations, but this model maintained a rating of zero missing, added, or distorted information across every run.

### Points deducted

Deductions were almost entirely concentrated on term-choice issues, with zero structural flaws:

- **`anclaje` (translation of grounding)**: eval-2 and eval-3 noted that "NLP literature more often uses `fundamentación contextual` or keeps the English term." However, many top-tier large models made the same choice, so this is within the range of evaluator preference
- **`ajuste fino` (translation of fine-tuning)**: eval-3 noted that "in technical contexts, keeping the English `fine-tuning` is also common." Again a choice shared by top-tier models generally
- **fluency -2 (eval-3 only)**: a combination of leftover `*prompt*` markup and the above point cost 2 points

### Positioning as a lightweight model

| Model | Score |
|---|:---:|
| gemma4-e4b | **95** |
| gemma3-12b | 95 |
| gemma4-e2b | 88 |
| gemma3-4b | 84 |
| gemma3n-e4b | 78 |

gemma4-e4b ties gemma3-12b (which has several times the parameters). The nature of its deductions is no different from that of large models, and it shows none of the issues typical of "lightweight model limitations" (language mixing, structural collapse, information loss). It's a clear first choice for resource-constrained environments.
