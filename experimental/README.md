# Course of the Experiments

This document records the trajectory of the experiments in this directory, each section covering one stretch of it. The early ones set out to improve context retention and terminology consistency in long-form translation, as well as processing efficiency (e.g., KV cache optimization); the later ones turn on the evaluation method itself, once it became the thing standing in the way.

Starting from the initial "sliding window" approach, the process progressively refines toward a "summary compression" approach that retains context by summarizing it, a "hybrid mode" that dynamically switches reasoning (CoT) on and off, and a "term pre-extraction" approach, converging into the current stable translation pipeline of `trtools` — after which the question becomes whether the scores that guided all of it can be trusted.

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

Translation and evaluation tools reflecting the findings from 01–05 were implemented and consolidated into the `trtools` package.

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

## Questioning the Evaluation Scale Itself

- **[11/](11/)**: Tested replacing `trtools eval`'s 5 criteria × 0–20 scoring with 50 narrow yes/partial/no items, to see whether a score can be made to stop depending on the run and on which model evaluates. Grew over several rounds: three local evaluators first, then two commercial ones, three prompt variants, a ground-truth calibration check, and finally a System One model.
  - Under the old scheme, the same translation's score swings by a mean range of 52.4 points across runs, and by a mean absolute 21.6 points when the evaluator model is swapped (qwen3.6 vs gpt-oss:120b)
  - **Runs stabilized; the choice of evaluator did not.** Run-to-run range fell to a mean of 8.6 points over the five generative evaluators, but evaluator spread *rose* to 27.1 points once commercial models were added, and only 1 of 8 targets still fits within 10 points
  - **The evaluators split cleanly by family, 13–19 points apart**, agreeing tightly within each: local three at 88.4–90.1, commercial two at 71.6–74.9. Most of the gap sits in group E (fluency & naturalness)
  - **The split is accuracy, not scale.** On the one item that can be settled by counting (are speaker labels present), the commercial pair is exact on 8/8 targets and the local three on 4–5. The local models collapse the rubric's 1–3 line `partial` band into `yes`, using it on 2.2–8.3% of verdicts against the commercial 23–25%
  - So the old scheme's failure was noise and the new scheme's is a confident near-ceiling score: every item is positively phrased, so a defect an evaluator cannot see is silently scored `yes`. Ignorance stopped being visible
  - **Thinking matters, evidence does not.** Dropping thinking cost qwen3.6 14.9 points and 10× the speed; dropping the evidence field alone moved no evaluator more than 4.4. Measured against a reference evaluator, the no-think variant is the only one under which a local evaluator approaches it, which reverses the first reading of that drop
  - The evidence field itself produced hallucinated line numbers throughout, since the prompt carries no line numbers to cite
  - **A System One model (`jev`) was added last** and is the steadiest evaluator on the panel (run-to-run range 2.3, ~1s and $0.0005 per evaluation), exact on the ground-truth item, and the only one whose total reflects a transcript losing 15% of its speaker labels — but it does not reproduce any reference's ordering, and its probability-weighted total is markedly better than its rounded verdicts
  - Wobble that remained was spread across 49 of the 50 items rather than concentrated in a few badly worded ones
  - gemma4:31b was markedly slower per call with thinking on (median ~9 minutes) than qwen3.6 or gpt-oss:120b (~2.5–3.5 minutes); the commercial pair ran at ~40 seconds under every variant
  - Kept deliberately outside `trtools`; not folded back into production, and its own README lists the fixes that would have to come first

- **[12/](12/)**: Keeps the old 5 criteria × 0–20 rubric unchanged and replaces the evaluator instead, asking each criterion as one typed Score question of a System One model (Jev). Experiment 11 replaced the rubric; this asks how much of the old instability was ever the rubric's fault.
  - Run-to-run range collapsed from a mean of 52.4 points to **1.25** on the same 8 targets, with the rubric untouched. The old scheme's instability was the generative evaluator's, not the scoring scale's
  - The 21-point scale is not asked for directly: five anchored severity levels are, and the probability-weighted position between them supplies the intermediate values the old rubric left to model discretion
  - **How those five levels are worded turned out to matter more than anything else in the experiment**, so both wordings are kept and selectable. Copying the old prompt's guidelines verbatim gave levels that name concrete defects at the bottom of the scale and state unmatchable absolutes at the top; the clean level then won none of 120 judgments, totals ran 18 points low, and a structurally sound Polish translation was placed in the "mixed languages, markup fragments" level with probability 0.87
  - Rewriting the levels to say only *how much* of the document falls short — degrees rather than defect kinds, which is the one property experiment 11's working anchor has — moved the corpus mean from 53.8 to **69.2** against the old scheme's 71.4, made the top level reachable, and took that Polish translation to 74 against an old median of 69. Not a word of the five criteria changed
  - Agreement flipped positive on three of four references, reaching **Pearson +0.90** against experiment 11's 50-item Jev run. It did not flip against the old 3-run medians, which are the one reference drawn from the targets selected for having the widest spread in the corpus
  - A guess that did not survive: the borrowed defect taxonomy was expected to hurt the criteria it was off-topic for, which predicted an uneven recovery. Every criterion rose, and fluency rose least
  - **One run is enough.** Run 1 alone reproduces the median of three at Spearman 1.000, so three runs are worth paying for only when the pinned model version changes and the range has to be re-measured
  - Still open: level 3 is the most probable level in 100 of 120 judgments, and 8 targets chosen for instability cannot say whether that is correct or whether the level is simply wide enough to absorb everything

- **[13/](13/)**: Runs the System One evaluator over the corpus's top two translators (`gpt-5.6-luna`, `union-alpha`) in all 67 languages, one run each, against the old scheme's own scores for the same translations. Experiments 11 and 12 both rest on the same 8 targets, picked for being the ones the old scheme handled worst; this is the same comparison at n=67 per translator, on the slice where separation is hardest — the old scheme ranks the pair 0.22 points apart. Both rubrics are carried here as frozen copies rather than imports, since each was the variable its own experiment tested.
  - **The top of the scale exists.** Experiment 12's open question was whether level 3 winning 100 of 120 judgments meant the level was correct or merely wide enough to absorb everything. On the corpus's best translations level 4 wins **469 of 670** and level 3 drops from 83% of judgments to 30%, so the levels were tracking quality rather than saturating
  - **Agreement survives the jump from n=8 to n=134**: Spearman **+0.69** pooled, +0.67 and +0.69 within each translator, against a per-translation reference rather than a per-language mean. The scheme reads a constant 3.7 points below the old one, against 2.1 points on experiment 12's much lower-scoring targets
  - It does not separate the two translators (`union-alpha` +0.53) and neither does the old scheme (`gpt-5.6-luna` +0.22) — ties in opposite directions, on a pair nothing available can adjudicate. Per language, where both schemes take a side, they pick the same translator in **37 of 53**
  - The old scheme ties 13 of 67 languages and this one ties 1: a 21-point integer scale summed over five criteria collides constantly, a probability-weighted position does not
  - The largest disagreements sit partly on the reference's own noise — `union-alpha / ga` is scored 21, 42, 31 by the old scheme — but only partly, and the README says so: agreement is best where the reference is steadiest (Pearson +0.61, n=93), yet disagreement size and the old 3-run range correlate at only +0.20
  - Fluency comes out ~2.5 points below every other criterion for both translators, the same criterion that moved least when experiment 12 rewrote the levels
  - **Experiment 11's 50-item scheme was run over the same 134 translations, and experiment 12's Pearson +0.90 between the two rubrics replicates exactly** — its strongest result and the one that rested on the fewest targets, now at n=134. Two rubrics sharing no wording land on the same ordering; what they share is the evaluator, so this says Jev's judgments are stable under a change of rubric, not that either rubric is right
  - That holds only before rounding. The 50-item scheme's verdict total is at the ceiling — **96.1% of 6,700 item verdicts are `yes`**, mean 97.52 — which is experiment 11's own diagnosis reproduced, and rounding costs 0.18 of the correlation (+0.90 → +0.72). Its probability-weighted total is fine (66.8–91.8), so the resolution lives entirely in the distribution. The 5-criterion scheme's two totals are indistinguishable (86.51 / 86.46): five severity levels round harmlessly, three do not
  - The 5-criterion scheme tracks the old scheme better on every statistic (+0.62 vs +0.53 Pearson), but the old scheme *is* the 5-criterion rubric scored generatively, so it cannot referee between them and the README says so
  - **For ranking, the 5 criteria win on cost**: the 50-item scheme needs ×1.97 the input tokens (TypeSafe bills input) for weighted totals that differ by a mean absolute 1.92 points, and its rounded total needs a caveat where the 5-criterion one does not. What the extra tokens buy is localisation, not accuracy — the 4% of non-`yes` verdicts concentrate in a few items (`e05_no_calque` 95 `partial`, `b04_no_intraword_intrusion` 32 `no`), which is very likely what the 5-criterion scheme's low fluency score is made of. It is also the only one of the two that can be checked against ground truth rather than correlated. So: 5 criteria by default, 50 items when the question is *why*
  - **The bottom of the scale works too**, on `qwen3.8` and its ternary quantization `bonsai2-27b`: levels 0–2 take 59% of judgments there, and the scheme separates the pair in 66 of 67 languages against the old scheme's 62. What it turned up instead is compression — every one of the 268 translations fits `jev = 0.69 × old + 24.7`, so the 3.7-point gap at the top was never a constant offset. The 10 translations the old scheme scores a flat 0 come back spread over 2.6–31.2, which no reference can confirm
  - **Read as a yardstick for how many languages a model handles**, the case gets sharper: counting languages at 80 or above moves by a mean of 4.4 languages between single runs of the old evaluator, and the three runs behind each translator's worst language spread by 15.1 points. The statistics coverage needs are the ones its noise destroys, which is the argument the migration now rests on
  - **The migration was decided and its first step taken**: `trtools jev` evaluated the whole corpus — 16 translators, 1,072 evaluations, $0.3165 and 5m22.6s — reproducing this experiment's own runs at Pearson 0.9995. `PLAN.md` is frozen as the record of the decision
  - Still open, in `PORT.md`: `trtools agg --jev`; the comparison on the Jev scale, which is what says whether it separates the top four and holds in the middle of the corpus; and the switch

- **[14/](14/)**: Fourteen runs, 1,054 phrases, and a design that is settled. `trtools trend` writes each language's one-line trend phrase by summarizing three generative evaluations' `overall_comment`, and the System One evaluator returns no prose, so the column has no source once experiment 13's migration lands. The phrase also has to describe the Jev score beside it, or there is no reason to replace the column that exists
  - **Runs 1–12 had one call read the translation and write the phrase**, steered by the level of the weakest criterion. The genre was wrong for six of them — asking for the lines that fall short produced fabricated locations, while the column being replaced never pointed at all: median five words, a quotation mark in 2%, a line number in none. A commercial writer served as a yardstick and was ruled out on input tokens, ~4.5M for a pass
  - **Thinking bought obedience, not accuracy**: turning it off left the false rate at 7 phrases in 84 but stopped the ban on quoting being applied. It cost 35 hours a pass against 37 minutes
  - **Runs 13–14 went back to the old pipeline's two calls**, both on `ollama:qwen3.6` without thinking: `trtools/evaluate.py`'s prompt is handed Jev's five scores and writes the comment that accounts for them, in English, and `trtools/trend.py`'s prompt summarizes that comment. The old column's form comes back with no quotes, at 12 seconds a phrase — 3.5 hours a pass
  - **Stage 1 reads the scores on the old evaluator's point bands**, where 17–19 of 20 is "high quality", so level-3 rows at 89 and over came out as praise in 64–73% of phrases although every comment behind them named a shortfall. Telling stage 2 to state the shortfall the comment names, and giving it Jev's own words for the weakest level, took that to none: praise is left to level 4, which is what the scale says
  - **A phrase is as right as the comment behind it.** Stage 2 invents nothing, and stage 1's errors pass through at the same rate as its findings. Faulting the translation for the original's own wording survives every design tried
  - `PLAN.md` is frozen as the ledger; the port into `trtools trend --jev` is `PORT.md`, and waits on experiment 13's comparison and its `build_state` fix, since either can change whether or with what scores the column is written
