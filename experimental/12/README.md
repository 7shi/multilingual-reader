# Experiment 12: The Old 5×20 Scheme, Judged by a System One Model

## 1. What This Tests

Experiment 11 established two things about the old `trtools eval` rubric — five criteria worth 20 points each — and they point in opposite directions:

- **It is unusable on a single translation.** The same evaluator (`qwen3.6`) on the same translation swings by a mean of **52.4 points** across three runs (mean stdev 22.16), because the rubric supplies no anchors separating a 14 from a 17.
- **It carries real signal at corpus scale.** Over 16 translators × 67 languages × 3 runs the ranking is reproducible from independent halves of the language set (split-half Spearman **0.947**), and it separates a ternary-quantized model from its own full-precision parent in 62 of 67 languages.

Experiment 11's response was to replace the rubric: 50 narrow yes/partial/no items. Its [Discussion 6](../11/README.md) closes on a diagnosis of what that traded away:

> the old rubric asked for an overall judgment, which averages over an evaluator's blind spots; the 50-item checklist asks for 50 independent detections and scores every miss as `yes`, which accumulates them in one direction. The burden moved from judgment to detection, and the averaging that rescued the old scheme is gone.

That framing leaves a question nobody has asked: **how much of the old scheme's instability was the rubric's, and how much was the generative evaluator's?** Every run of the old scheme was produced by a model writing a number into a schema. This experiment keeps the rubric exactly and changes only the mechanism.

[eval5_jev.py](eval5_jev.py) asks each of the five criteria as one TypeSafe System One **Score** question. Two properties follow, neither of them a change to what is being judged:

- **The intermediate scores stop being discretionary.** A Score returns the probability-weighted position across its levels, so a value between "minor issues" and "clean" comes out of the distribution rather than out of a model choosing a number. That is exactly the gap the old rubric left open, and which the 50-item scheme closed by deleting the scale.
- **The five judgments are independent.** Each question is scored on its own against the same state, so a weak reading of one criterion cannot pull the other four along.

### Why not just use experiment 11's 50-item Jev run

Experiment 11 [section 3.6](../11/README.md) already runs Jev, and found it the steadiest evaluator on the panel (mean run-to-run range 2.3) and exact on the one item with ground truth — but also negatively rank-correlated with two of its three references, on n=8. The ceiling on that result is the comparison set: the 50-item scheme can only be checked against the old one on 8 targets, and 8 old 3-run medians are the weaker of the two available references.

A 5-criterion evaluator has no such ceiling. It produces the old scheme's own units, so it can be compared against the whole of [examples/tr/onde/](../../examples/tr/onde/) — the reference with split-half Spearman 0.947 behind it — for a few cents.

---

## 2. Setup

- **Rubric**: the five criteria of [trtools/evaluate.py](../../trtools/evaluate.py), verbatim, in [criteria.py](criteria.py).
- **Levels**: five ordered severity levels — and *how those levels are worded* turned out to be a variable rather than a detail, so [criteria.py](criteria.py) holds two sets and `--levels` selects between them. They differ in nothing else. Twenty-one levels would put the "what separates 14 from 17" question straight back into the rubric; five levels plus the probability weighting answer it instead.

  | Level | `bands` — the old prompt's CRITICAL GUIDELINES 3–6 | `degrees` — extent only | Old scale |
  |---:|---|---|---:|
  | 0 | Missing, empty, or not in the target language | Not met anywhere | 0 |
  | 1 | Critical: mixed languages, markup fragments, meta-commentary | Fails across most of the document | 0–5 |
  | 2 | Major: grammatical errors, untranslated passages | Fails repeatedly, or over ~4 lines or more | 6–12 |
  | 3 | Minor: occasional awkwardness only | Mostly met; shortfalls confined to ~1–3 lines | 13–17 |
  | 4 | Clean: natural and accurate throughout | Met throughout; not a single place it falls short | 18–20 |

  `bands` was written first, as the faithful transcription of the old prompt, and it is what section 3 finds wrong. `degrees` is the replacement: each level says only *how much* of the document falls short, never what kind of defect is responsible. Levels 2–4 of it are experiment 11's own working anchor transplanted — [eval50.py](../11/eval50.py)'s `no`/`partial`/`yes`, which are degrees, identical across all 50 items and pinned to line counts — with levels 0 and 1 extending the same ladder down to cover the old prompt's critical band.

  A level maps to the 0–20 scale at **5 points each** under both sets, which puts each level at the top of its `bands` band and within a point of the middle of the two bands wide enough to have one. That the two sets share the mapping is what makes their scores comparable.
- **What is deliberately *not* carried over**: the old prompt's guideline 1, "if missing or incomplete, assign 0 points to ALL criteria". That is the score cliff experiment 11's background blames for 0/100 totals sitting beside enthusiastic rationales, and it cannot be expressed as a per-criterion level anyway. Level 0 covers the same situation without propagating it sideways.
- **Targets**: experiment 11's [targets.tsv](../11/targets.tsv), read where it lives. Those 8 are the corpus's worst case for the old scheme — ranked by 3-run range — so they are where a replacement evaluator has to be checked first.
- **Runs**: 3 for the results below, which is what makes the run-to-run range comparable with the old scheme's 52.4. The default is now **1** — see section 3.1 — and `--runs 3` restores it for re-checking a new model version.
- **Model**: `jev-1.13.0`, pinned by version and re-checked against every response.
- **Output**: one directory per level set — `evals/` for `bands`, `evals-degrees/` for `degrees` — in `trtools eval`'s schema, so [trtools/aggregate.py](../../trtools/aggregate.py) and [trtools/trend.py](../../trtools/trend.py) read it unchanged. `reasoning` and `overall_comment` are empty — Jev emits no text — and neither is read by the aggregation. The distribution behind each score, the per-criterion confidence, the unrounded total and the level set the run was scored on are kept in fields those scripts ignore.
- **Cost**: five questions over one state, about 5,000 input tokens and under a second per evaluation (~$0.0002). The 8 targets × 3 runs come to roughly $0.005, which is what makes a second level set affordable as a controlled comparison rather than a replacement.

---

## 3. Results

48 evaluations: 8 targets × 3 runs under each level set, about 30 seconds and $0.005 per set. [cmp_levels.py](cmp_levels.py) generates every table below, reading both result directories and all four references where they live.

### 1. The instability was the evaluator's, not the rubric's

| Target | Old 3 runs (`qwen3.6`) | Old range | `bands` 3 runs | Range | `degrees` 3 runs | Range |
|---|---|---:|---|---:|---|---:|
| gpt-5.6-terra / pl | 69, 81, 15 | 66 | 30, 30, 30 | **0** | 74, 73, 73 | 1 |
| gpt-oss / ia | 89, 73, 34 | 55 | 52, 52, 51 | 1 | 61, 60, 61 | 1 |
| qwen3.8 / ja | 56, 78, 25 | 53 | 57, 58, 59 | 2 | 75, 75, 74 | 1 |
| gemini-3.5-flash-lite / kn | 29, 61, 80 | 51 | 50, 49, 50 | 1 | 67, 67, 68 | 1 |
| ox-alpha / ga | 38, 68, 89 | 51 | 68, 69, 67 | 2 | 72, 72, 72 | **0** |
| qwen3.6-27b / ko | 92, 42, 77 | 50 | 58, 58, 59 | 1 | 74, 72, 72 | 2 |
| gemini-2.5-flash / ru | 91, 44, 86 | 47 | 59, 58, 57 | 2 | 68, 68, 67 | 1 |
| gemini-3-flash / hi | 91, 81, 45 | 46 | 57, 56, 56 | 1 | 66, 66, 68 | 2 |
| **Mean** | | 52.4 | | **1.25** | | **1.12** |

Mean range **1.25** and **1.12**, against the old scheme's **52.4** on these same 8 targets — a factor of 42 and 47, with the rubric untouched and only the mechanism changed. Both are below experiment 11's 50-item Jev run (2.25), which is the expected direction: five judgments carry fewer independent sources of noise than fifty.

**This answers the question the experiment was built for.** The old scheme's run-to-run instability was a property of asking a generative model to write a number into a 21-point scale, not of the five criteria or of the scale's width. Experiment 11's diagnosis — that the old rubric's fault was leaving the intermediate scores to model discretion — is confirmed, and its remedy of deleting the scale turns out not to have been the only one available.

**A practical consequence: three runs are no longer worth paying for.** Run 1 alone reproduces the median of three at Pearson 0.998 and Spearman 1.000 under `degrees` (mean absolute difference 0.22 points, maximum 0.80), all three runs agree on the most probable level in 38 of 40 criterion-target pairs, and no correlation in section 3.3 moves by more than 0.02 when the other two runs are dropped. Three runs were necessary exactly once, to measure the range that made this section's finding; repeating them triples the cost of everything in section 5 and settles nothing. `--runs` defaults to 1 accordingly, and 3 is the right setting only when the pinned model version changes and the range has to be re-established.

Note also that stability is indifferent to whether the judgment is any good: the two level sets are equally steady and, as the next section shows, they are not scoring the same thing at all. A run-to-run range near zero says the mechanism is deterministic, and nothing more.

### 2. How specifically a level is worded moves its probability mass

This is the result the second run was for, and it is a finding about the Score primitive rather than about this rubric. Over 120 judgments per set:

| Level | 0 (not met) | 1 (critical / most) | 2 (major / wide) | 3 (minor / scattered) | 4 (clean / throughout) |
|---|---:|---:|---:|---:|---:|
| `bands` mean mass | 0.000 | 0.268 | 0.375 | 0.295 | **0.061** |
| `bands` times most probable | 0 | 17 | 56 | 47 | **0** |
| `degrees` mean mass | 0.004 | 0.069 | 0.246 | **0.505** | 0.175 |
| `degrees` times most probable | 0 | 3 | 12 | **100** | 5 |

Under `bands` the clean level never won once, and probability piled into levels 1–2, the two that name concrete defects. Under `degrees` the mass moves up by roughly a level and a half: level 1 collapses from 17 wins to 3, and the top level becomes reachable. Nothing about the model, the criteria, the texts or the run count differs between the two rows.

| | Mean total | Mean confidence |
|---|---:|---:|
| `bands` | 53.8 | 0.52 |
| `degrees` | **69.2** | 0.55 |
| Old scheme, 3-run medians | 71.4 | — |
| Experiment 11, 50-item Jev | 80.5 | 0.33 |

The 18-point deficit against the old scheme is almost entirely gone — 53.8 → 69.2 against 71.4 — and it closed without a single word of the five criteria changing.

**The Polish case is the clearest single reading.** Under `bands` it scored 30/100, every criterion landing on level 1 ("mixed languages, JSON or markup fragments, or meta-commentary left in the body") at probability 0.86–0.91 with confidence up to 0.89, while a mechanical check of the file finds all 99 lines in Polish orthography, no markup, no untranslated English and no meta-commentary. Under `degrees` the same file, same model, scores **74/100** against an old median of 69, with mass on levels 3–4 and terminology's most probable level being 4 at 0.47. The confident false verdict was produced by the level text, not by the model's reading of the translation.

Per-criterion, the shift is uniform rather than concentrated in the criteria the `bands` taxonomy fit worst:

| Criterion (mean, 0–20) | `bands` | `degrees` |
|---|---:|---:|
| Readability & comprehensibility | 10.74 | 14.20 |
| Fluency & naturalness | 10.32 | 11.85 |
| Terminology appropriateness | 11.37 | 15.60 |
| Contextual adaptation | 10.49 | 13.59 |
| Information completeness | 10.70 | 14.14 |

So section 3.3's first diagnosis is confirmed and its second is not. Levels 1 and 2 naming matchable defects while 3 and 4 stated unmatchable absolutes is what drove the mass down — removing that asymmetry lifts every criterion. The second guess, that the structural taxonomy hurt `readability` and `contextual_adaptation` specifically because it was off-topic for them, predicted an uneven recovery; `fluency` moves least (+1.5) and `terminology` most (+4.2), which is not that pattern.

### 3. Agreement with the references

Correlated on the probability-weighted total, medianed over the 3 runs (n=8):

| Reference | `bands` | | | `degrees` | | |
|---|---:|---:|---:|---:|---:|---:|
| | Pearson | Spearman | Kendall | Pearson | Spearman | Kendall |
| Old per-language corpus mean | -0.38 | +0.05 | +0.07 | **+0.47** | **+0.64** | **+0.57** |
| Experiment 11, 50-item Jev | +0.28 | +0.41 | +0.36 | **+0.90** | **+0.74** | **+0.60** |
| `gpt-5.6-terra` (experiment 11) | -0.16 | -0.10 | -0.07 | +0.31 | +0.10 | +0.14 |
| Old 3-run medians | +0.10 | +0.12 | +0.14 | **-0.33** | **-0.31** | -0.21 |

Three of the four references flip from flat-or-negative to positive, and the two best-verified ones — the corpus mean over 16 translators, and the 50-item Jev run that experiment 11 found exact on its one ground-truth item — go from nothing to a clear ordering. The Pearson of +0.90 against the 50-item scheme is the strongest agreement anything in either experiment has shown, and it is between two schemes that share only their evaluator.

**The fourth row runs the other way and should not be explained away.** Against the old 3-run medians `degrees` is negatively correlated where `bands` was weakly positive. Those medians are the one reference whose unreliability is measured rather than assumed: these 8 targets were *selected* for having the widest 3-run spread in the corpus (66 to 46 points), so each median is one draw from a distribution wide enough to swallow the entire ranking. Experiment 11's Discussion 6 already calls them the weaker of its two references. Agreeing with the corpus mean and disagreeing with a median drawn from a 52-point spread is the expected shape if `degrees` is the better evaluator — but a reference that noisy cannot confirm that, only fail to refute it. n=8 throughout, so none of these correlations is individually decisive.

### 4. What is still open: level 3 absorbs almost everything

`degrees` wins on every comparison above, and it has an obvious remaining weakness: level 3 is the most probable level in **100 of 120** judgments, and level 4 in 5. The scale has not collapsed — the underlying mass is spread (0.505 on level 3, 0.175 on level 4, 0.246 on level 2) and the unrounded totals separate the targets by 14 points — but the discrete verdict is nearly constant, and most of the discrimination now lives in the probability weighting rather than in which level wins.

Two readings, which this run cannot separate:

1. It is correct. All 8 targets are competent translations with scattered small faults, which is what level 3 describes; the old scheme's own 3-run medians put every one of them between 56 and 86.
2. Level 3's "roughly one to three lines" is simply wide enough to catch nearly everything, in a way `partial` is not when it is applied to one narrow property at a time rather than to a whole criterion.

The second reading is the one that would matter, and this target set cannot test it: all 8 land between 61 and 75, while the corpus reference spans 37.8 (`ga`) to 85.6 (`ja`) at the language level. Nothing here sits where level 2 ought to be winning outright. These 8 were selected for the old scheme's *instability* on them, not for being bad translations, so the bottom of the scale has simply never been exercised.

---

## 4. Reproducing

```bash
# 1. Evaluate experiment 11's 8 unstable targets (needs TYPESAFE_API_KEY).
#    The default level set writes to evals-degrees/; --levels bands writes to evals/.
#    --runs 3 reproduces the results above; the default of 1 is what section 3.1 argues for.
uv run experimental/12/eval5_jev.py --runs 3
uv run experimental/12/eval5_jev.py --runs 3 --levels bands

# 2. Compare the two level sets against each other and against the four references
uv run experimental/12/cmp_levels.py

# 3. Any other target set, in the same TSV format
uv run experimental/12/eval5_jev.py --targets path/to/targets.tsv
```

Existing result files are left alone, so a re-run fills in only what is missing and costs nothing for what is already there.

---

## 5. What Would Come Next

1. **Compare against the verified corpus reference at scale.** Section 3.3 gets Spearman +0.64 against the old scheme's per-language mean on 8 targets, which is suggestive and nothing more. The corpus is 16 translators × 67 languages and this evaluator costs $0.0002 per translation, so the comparison that experiment 11 could never afford — the same rubric, the same units, over enough languages for the correlation to mean something — is now the obvious next spend.
2. **Run the quantization separation test.** Experiment 11's Future Work 7 asks whether a cheaper scheme still separates `bonsai2-27b` from its full-precision parent `qwen3.8`, which the old scheme did by 26 points in 62 of 67 languages. At 5 questions per evaluation and one run each that is 134 evaluations for a few cents — the cheapest decisive test available, and the one that says whether this is usable in aggregate. It is also a direct test of section 3.4: two models of known and unequal quality either land on different levels or they do not.
3. **Probe the bottom of the scale.** Section 3.4 cannot tell a correct level 3 from a level 3 wide enough to absorb everything. Running a handful of targets the corpus scores in the 30s and 40s would say which, and it is the precondition for trusting any aggregate result from step 1.
4. **Decide between 5 criteria and 50 items for Jev.** Both now exist, and they agree at Pearson +0.90, which is new information: the case for preferring one on accuracy grounds is weaker than it looked when this experiment's only run was the `bands` one. The 50-item scheme buys resolution and a ground-truth check on structural items; the 5-criterion scheme buys direct comparability with everything already accumulated, at a tenth of the questions and a lower run-to-run range (1.12 against 2.25).
5. **Carry the level-wording finding back to the 50-item scheme.** Section 3.2 is a property of Score, not of this rubric: a level that names a matchable defect attracts mass away from one that states an absolute. Experiment 11's three levels are already pure degrees, which is why they were transplanted here — but its 50 *item* descriptions are not, and whether the same asymmetry is quietly at work in them has not been checked.
