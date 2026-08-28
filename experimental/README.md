# Course of the Experiments

This document records the trajectory of a series of experiments (01–10) conducted to improve context retention and terminology consistency in long-form translation, as well as processing efficiency (e.g., KV cache optimization).

Starting from the initial "sliding window" approach, the process progressively refines toward a "summary compression" approach that retains context by summarizing it, a "hybrid mode" that dynamically switches reasoning (CoT) on and off, and a "term pre-extraction" approach, before finally converging into the current stable translation pipeline of `trtools`.

## translate.py: Origin of the Experimental Series

[translate.py](../obsolete/translate.py), originally at the repository root, is the starting point of the experimental series. It implemented reasoning levels 0–2 with structured output (`generate_with_schema` + Pydantic) and managed context using a sliding window of the last 5 entries.

## Early Trials (OBSOLETE)

The stage where `translate-exp.py`, `translate2.py`, and `translate3.py` were built on the results of `translate.py`, attempting multi-model collaboration (Phase 2a). 👉[Details](01/OBSOLETE.md)

**Evaluation language selection**:
- **English↔Western European languages** have the richest LLM training data, so top accuracy is "a given," making them unsuitable as an evaluation axis since differences between models rarely show up
- **Between Romance languages** (fr↔es), the linguistic distance is moderately close, so differences readily appear in terminology, idioms, and cultural localization. Fine-grained differentiation is possible even in the 97–100 point range
- **French→Spanish** (fr→es) was adopted as the baseline axis for the translation task

**Approaches tried**:
- Phase 1: Initial translation with gemma3n:e4b
- Phase 2a: Quality check and correction combined in one pass with qwen2.5:7b
- Ultimately, `translate3.py` (a single end-to-end version) became the top recommendation at "92 points"

**Reasons for hitting a dead end and starting over**:
- Evaluation was a single subjective pass by Claude Code, with no scoring criteria or rubric
- The basis for evaluation was unclear, casting doubt on the reliability of the scores
- Systematic comparison was difficult due to the accumulation of ad hoc methods
- → Led to redesigning from the evaluation method up, as the `experimental/` series

## Narrowing Down the Architecture

- **[01/](01/)**: Systematically analyzed the impact of reasoning level (0–4) on translation quality. Overhauled the evaluation method into 5 criteria across multiple passes.
  - Level 0 (direct translation) was the most stable and highest quality. Level 1 (structured reasoning) had the lowest median score overall at 59 points; CoT was counterproductive for translation
  - With sliding history, terminology drifted once older history was pushed out, and changes at the start of the prompt invalidated the KV cache
  - Adopted qwen3.6 as the evaluator (GPT-OSS 120B was retired due to a ceiling effect)

- **[02/](02/)**: Validated a summary-compression architecture to solve 01's issues (terminology drift, KV cache invalidation).
  - Enabled the KV cache with a fixed structure of `system + summary + last N entries`. `--no-think` and dropping structured output became the default settings
  - In a full-scale experiment across 34 models (Phase B), top models achieved 95–97 points (effectively the ceiling under the qwen3.6 evaluator)
  - **gemma4-26b** was the best performer: highest score stability (range of 1), zero structural defects

- **[03/](03/)**: Implemented a hybrid mode that excludes summaries from the translation history, avoiding style interference while maintaining KV cache efficiency.
  - The translation itself runs without CoT; only summary generation uses CoT. gemma4-26b showed no sharp drops across all runs (96/100/96 points)
  - Sharp drops occurred stochastically due to drift in the initial glossary accumulation, independent of configuration
  - Recommended settings: threshold=10, no CoT (shortest processing time, no quality degradation)

- **[04/](04/)**: Implemented a term pre-extraction approach that fixes and allows proofreading of the glossary before translation, enabling a human-intervention workflow.
  - gemma4-26b: 96/96/99 points (remained stable), gemma4-e4b: 95/96/92 points (sharp drop reduced from 85→92 points)
  - Terminology drift persisted across runs (e.g., the translation of `affinage` split between `refinamiento` / `ajuste fino`)

- **[05/](05/)**: Split term extraction out as `trtools term` for separate proofreading, eliminating drift across runs by having every run reference a shared glossary.
  - The shared glossary resolved gemma4-e4b's sharp drops (stabilized at 94–95 points); gemma4-26b remained stable at 95–97 points
  - qwen3.6's evaluation accuracy had limits (missed speaker loss in 2 of 3 cases)

Translation and evaluation tools reflecting the findings from 01–04 were implemented and consolidated into the `trtools` package.

- `trtools translate`: Based on 03's recommended settings (threshold=10, no CoT, summary compression), implementing term injection and skip-aware blank line preservation. Legacy designs such as structured output and sliding history were dropped
- `trtools term extract/translate`: Split term extraction and translation-fixing out of the translation loop. Sharing a proofread TSV across all runs eliminates terminology drift between runs
- `trtools eval / agg`: Median aggregation over 5 criteria × 20 points, 3 evaluation passes
- `trtools batch`: Runs translation → evaluation → aggregation in one pass. Input files are listed as bare positional arguments, with topic and language code auto-derived from the filename. Moved into production use, invoked from `examples/tr-fr/Makefile`

## Expansion to Medium-Resource Languages and Establishing a Third-Party-Review Refinement Process

- **[06/](06/)**: Applied two-stage translation (refinement) to medium-resource languages (Dutch, Czech) where direct translation plateaus, to test whether it improves quality.
  - Dutch: baseline 78 points → draft translation 86 points → 94 points after refinement (reached the target 90s)
  - Czech: baseline 78 points → draft translation 56 points (context collapsed under simple sliding) → 72 points after refinement
  - Practical use requires integration with the summary-compression approach and term injection

- **[07/](07/)**: Separated the roles of translation and refinement, testing a third-party-review approach where qwen3.6 refines trtools' high-quality baseline line by line.
  - From a baseline of 78 points, Dutch improved substantially to 97 points and Czech to 94 points (both reached the 90s)
  - Separating a high-quality baseline (context retention) from a separate model skilled at evaluation (refinement) proved effective for medium-resource languages

- **[08/](08/)**: Tested consolidating experiment 07's two-step approach into a single step using CoT, to optimize it.
  - CoT enabled (single step): nl 96 points, cs 86 points. Czech produced empty output, and without the analysis persisting in chat history, context consistency dropped
  - CoT disabled (single step): nl 75 points, cs 59 points. Did not function as refinement, with frequent language mixing
  - Fallback verification: discovered a `meteen` (Dutch interference) problem in the Czech baseline. The fallback further lowered the score (86→74 points)
  - **Conclusion**: The two-step approach, which accumulates analysis results in chat history, is essential for refinement. Adopted experiment 07's approach as the final refinement process

- **[09/](09/)**: Expanded experiment 07's third-party-review approach to all 67 languages. For each language, automatically selects the highest-scoring baseline among gemma4, gpt-oss, and qwen3.6 to refine. See [09/SCORES.md](09/SCORES.md) for detailed scores.
  - `find_best.py` compares `SCORES.txt` across all models and outputs the highest-scoring file per language as a TSV
  - Refinement was extended from experiment 07's `review.py` (speaker-name conversion, language-code handling, enhanced status bar via Rich)
  - 30 languages improved, 32 declined, 5 unchanged (average change −1.2 points). Large gains in Basque (+42), Estonian (+29), Slovene (+22), and others
  - Refinement functions as "polishing expression," so it is effective for translations that make sense but are rough in expression. When a translation is structurally broken, refinement tends to fail to improve it and can make it worse; when quality is already high, unnecessary changes can also backfire
  - Cases where refinement was effective (delta of +6 or more and post-refinement score of 80 or above): Bulgarian (97:+17), Hungarian (96:+13), Slovene (95:+22), Azerbaijani (91:+13), Czech (89:+9), Basque (87:+42), Estonian (82:+29), Latvian (82:+17), Macedonian (82:+6), Belarusian (81:+12)

Building on the results of experiments 06–09, the third-party-review approach was integrated into `trtools` as `trtools review`.

- **[10/](10/)**: Verifies the full translate → eval → review → eval pipeline (roughly 3.5 hours of run time) on the 5 languages (bg, eu, et, sl, hu) where refinement was most effective in experiment 09.
  - Ported `review.py` to a subcommand style, and consolidated `ConsoleStream` and `StatusLine` into shared modules
  - `translate`, `eval`, and `review` now share a unified progress bar via the `--label` / `--start` main options
  - Confirmed that refinement works effectively even when the base score is low (eu: 17→59, hu: 26→89, sl: 56→83, et: 30→51)
  - bg, which had a high base score (88 points), saw a slight decline (-1). Consistent with the finding from experiment 09 that refinement tends to backfire on already-high scores
