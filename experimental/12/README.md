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
- **Levels**: five ordered severity bands, taken from that script's own CRITICAL GUIDELINES 3–6. Twenty-one levels would put the "what separates 14 from 17" question straight back into the rubric; five anchored levels plus the probability weighting answer it instead.

  | Level | Band | Old scale |
  |---:|---|---:|
  | 0 | Missing, empty, or not in the target language | 0 |
  | 1 | Critical: mixed languages, markup fragments, meta-commentary | 0–5 |
  | 2 | Major: grammatical errors, untranslated passages | 6–12 |
  | 3 | Minor: occasional awkwardness only | 13–17 |
  | 4 | Clean: natural and accurate throughout | 18–20 |

  A level maps to the 0–20 scale at **5 points each**, which puts each level at the top of its band and within a point of the middle of the two bands wide enough to have one.
- **What is deliberately *not* carried over**: the old prompt's guideline 1, "if missing or incomplete, assign 0 points to ALL criteria". That is the score cliff experiment 11's background blames for 0/100 totals sitting beside enthusiastic rationales, and it cannot be expressed as a per-criterion level anyway. Level 0 covers the same situation without propagating it sideways.
- **Targets**: experiment 11's [targets.tsv](../11/targets.tsv), read where it lives. Those 8 are the corpus's worst case for the old scheme — ranked by 3-run range — so they are where a replacement evaluator has to be checked first.
- **Runs**: 3, which is what makes the run-to-run range comparable with the old scheme's 52.4.
- **Model**: `jev-1.13.0`, pinned by version and re-checked against every response.
- **Output**: `evals/`, in `trtools eval`'s schema, so [trtools/aggregate.py](../../trtools/aggregate.py) and [trtools/trend.py](../../trtools/trend.py) read it unchanged. `reasoning` and `overall_comment` are empty — Jev emits no text — and neither is read by the aggregation. The distribution behind each score, the per-criterion confidence and the unrounded total are kept in fields those scripts ignore.
- **Cost**: five questions over one state, about 5,000 input tokens and under a second per evaluation (~$0.0002). The 8 targets × 3 runs come to roughly $0.005.

---

## 3. Results

24 evaluations (8 targets × 3 runs), about 30 seconds and 5,800 input tokens per call.

### 1. The instability was the evaluator's, not the rubric's

| Target | `jev` 3 runs | Range | Old 3 runs (`qwen3.6`) | Old range |
|---|---|---:|---|---:|
| gpt-5.6-terra / pl | 30, 30, 30 | **0** | 69, 81, 15 | 66 |
| gpt-oss / ia | 52, 52, 51 | 1 | 89, 73, 34 | 55 |
| qwen3.8 / ja | 57, 58, 59 | 2 | 56, 78, 25 | 53 |
| gemini-3.5-flash-lite / kn | 50, 49, 50 | 1 | 29, 61, 80 | 51 |
| ox-alpha / ga | 68, 69, 67 | 2 | 38, 68, 89 | 51 |
| qwen3.6-27b / ko | 58, 58, 59 | 1 | 92, 42, 77 | 50 |
| gemini-2.5-flash / ru | 59, 58, 57 | 2 | 91, 44, 86 | 47 |
| gemini-3-flash / hi | 57, 56, 56 | 1 | 91, 81, 45 | 46 |

Mean range **1.25**, against the old scheme's **52.4** on these same 8 targets — a factor of 42, with the rubric untouched and only the mechanism changed. It is also below experiment 11's 50-item Jev run (2.25), which is the expected direction: five judgments carry fewer independent sources of noise than fifty.

**This answers the question the experiment was built for.** The old scheme's run-to-run instability was a property of asking a generative model to write a number into a 21-point scale, not of the five criteria or of the scale's width. Experiment 11's diagnosis — that the old rubric's fault was leaving the intermediate scores to model discretion — is confirmed, and its remedy of deleting the scale turns out not to have been the only one available.

### 2. But the levels are not being read as written

Everything else about this run is wrong, and it is wrong in a way that points at the rubric text rather than at the model.

| | Mean total | Mean confidence |
|---|---:|---:|
| This experiment | 53.8 | 0.52 |
| Old scheme, 3-run medians | 71.4 | — |
| Experiment 11, 50-item Jev | 80.5 | 0.33 |

The level usage shows the mechanism. Over all 120 judgments:

| Level | 0 (missing) | 1 (critical) | 2 (major) | 3 (minor) | 4 (clean) |
|---|---:|---:|---:|---:|---:|
| Mean probability mass | 0.000 | 0.268 | 0.375 | 0.295 | **0.061** |
| Times it was the most probable | 0 | 17 | 56 | 47 | **0** |

**The clean level never won once.** Probability is compressed into levels 1–3, which is what drags the totals down by roughly 18 points relative to the old scheme.

The clearest single case is Polish, scored **30/100** with every criterion landing near level 1 ("the text is structurally damaged, with mixed languages, JSON or markup fragments, or meta-commentary left in the body") at probability 0.87 and confidence 0.85. Checking the file mechanically finds nothing of the kind: all 99 lines are in Polish orthography, with no markup, no untranslated English and no meta-commentary. The same model's 50-item run scores `b06_encoding_integrity` as `yes` with confidence 0.81 on the same file. The verdict is simply wrong, and it is wrong confidently, which rules out the "Jev is unsure about this task" reading that experiment 11's mean confidence of 0.33 invited.

Rank correlations are correspondingly flat or negative:

| Reference | Pearson | Spearman | Kendall |
|---|---:|---:|---:|
| Old 3-run medians | +0.10 | +0.12 | +0.14 |
| Old per-language corpus mean | **-0.38** | +0.05 | +0.07 |
| Experiment 11, 50-item Jev | +0.26 | +0.35 | +0.28 |
| `gpt-5.6-terra` (experiment 11) | -0.17 | -0.11 | -0.11 |

So the level is wrong *and* the ordering is not recovered. Stability alone bought nothing here — which is the caveat experiment 11 attaches to its own stability finding, arriving from the other direction.

### 3. The likely cause: level descriptions are not comparable to each other

The five levels in [criteria.py](criteria.py) are asymmetric in two ways, both introduced by copying the old prompt's guidelines faithfully:

- **Levels 1 and 2 name concrete defects; levels 3 and 4 state vague absolutes.** "Mixed languages, JSON or markup fragments" is something a text can be matched against; "no fault on this criterion" and "natural and accurate throughout" are conditions almost nothing satisfies outright. A Score places mass on the level whose description fits, so any imperfection is pulled toward the specific wording and away from the absolute one.
- **The defect taxonomy does not apply evenly across the five criteria.** Level 1 is about structural damage, which is not what "readability" or "contextual adaptation" is asking about. Each criterion is nonetheless offered the same ladder, so for three of the five the bottom rungs describe something off-topic.

Notably, the 50-item scheme's levels have neither property: `no` / `partial` / `yes` are purely degrees, identical across all 50 items, and defined by line counts rather than defect kinds. That is a plausible part of why experiment 11's Jev run reads sanely and this one does not.

**This is unresolved.** Rewriting the levels as pure degrees would likely fix it, but it trades away the fidelity to the old prompt's anchors that section 2 argues for, so the two goals are in conflict and the choice has not been made. The results above are what the faithful version produces.

---

## 4. Reproducing

```bash
# 1. Evaluate experiment 11's 8 unstable targets, 3 runs each (needs TYPESAFE_API_KEY)
uv run experimental/12/eval5_jev.py

# 2. Any other target set, in the same TSV format
uv run experimental/12/eval5_jev.py --targets path/to/targets.tsv
```

---

## 5. What Would Come Next

1. **Rewrite the levels as pure degrees and re-run.** Section 3.3 is the blocker for everything below it: until the clean level can win, no comparison against any reference means anything. Keeping the old prompt's severity ordering while dropping its defect taxonomy is the obvious candidate, and the run costs about 30 seconds and half a cent, so the old levels should be kept as a control rather than overwritten — "how specifically a Score level is worded moves its probability mass" is a general finding about the primitive, and the comparison is nearly free.
2. **Then compare against the verified corpus reference.** The old scheme's per-language mean over 16 translators, which experiment 11 treats as its better-verified reference. Unlike the 50-item scheme, this one is in the same units, which is the whole reason for the experiment.
3. **Run the quantization separation test.** Experiment 11's Future Work 7 asks whether a cheaper scheme still separates `bonsai2-27b` from its full-precision parent `qwen3.8`, which the old scheme did by 26 points in 62 of 67 languages. At 5 questions per evaluation that is 134 evaluations for a few cents — the cheapest decisive test available, and the one that says whether this is usable in aggregate. It is only worth paying for after step 1.
4. **Decide between 5 criteria and 50 items for Jev.** Both now exist. The 50-item scheme buys resolution and a ground-truth check on structural items; the 5-criterion scheme buys direct comparability with everything already accumulated. They are not the same trade-off they were for a generative evaluator, because neither is limited by what the evaluator can hold together in one prompt. On the evidence so far the 50-item scheme is ahead on everything except run-to-run range, but its rubric has been through experiment 11 and this one's has not.
