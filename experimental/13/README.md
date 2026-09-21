# Experiment 13: The Corpus's Top Two, Every Language, One Run

## 1. What This Tests

Experiment 12 ends with a working evaluator and no idea whether it works. Its `degrees`
level set agrees with the old scheme's corpus reference at Spearman +0.64 and with
experiment 11's 50-item scheme at Pearson +0.90 — on **8 targets**, chosen for being the
8 the old scheme was *least* stable on. That is the worst possible sample to generalise
from, and [experiment 12's Next 1](../12/README.md) says so: the comparison that matters
is against the corpus, at a scale where a correlation means something.

This is that comparison, on the slice where it is hardest. `gpt-5.6-luna` and
`union-alpha` are the corpus's two best translators under the old scheme, and it puts
them **0.22 points apart** averaged over 67 languages:

| Translator | Old corpus mean |
|---|---:|
| gpt-5.6-luna | 90.31 |
| union-alpha | 90.09 |
| gemini-3.7-flash | 87.48 |
| … | |
| bonsai2-27b | 27.90 |

Three questions come out of that, and they are not the same question:

- **Does it track the reference per translation?** Within one translator, the 67 languages
  give a paired comparison with n=67 against the old scheme's own median for each
  translation. This is experiment 12 section 3.3 with an order of magnitude more data and
  a reference that is not drawn from a 52-point spread.
- **Does the top of the scale exist?** Experiment 12 section 3.4 found level 3 most
  probable in 100 of 120 judgments and level 4 in 5, and could not tell a correct level 3
  from a level 3 wide enough to swallow everything. These are the best translations in the
  corpus. If level 4 is reachable at all, it is reachable here.
- **Do the two translators come apart?** Worth reporting, but it cannot be scored. The old
  scheme has no opinion to check against — 0.22 points over 67 languages is a tie — so a
  gap under this scheme is a claim nothing available can confirm or refute.

A fourth question was added once the first run was in. Experiment 12 section 3.3 found the
five-criterion scheme and experiment 11's fifty-item scheme agreeing at **Pearson +0.90** —
the strongest agreement either experiment produced, and the one resting on the smallest
sample, those same 8 targets. [eval50_jev.py](eval50_jev.py) runs the fifty-item scheme
over these 134 translations too, so the two rubrics can be compared where neither is being
asked to generalise from eight numbers. Same targets, same model: whatever separates them
is the rubric.

The bottom of the scale is still untested after this. That needs its own targets, and the
corpus has them (`bonsai2-27b` at 27.90); it is a separate run.

---

## 2. Setup

- **Evaluators**: two, over the same targets.
  - [eval5_jev.py](eval5_jev.py) with [criteria.py](criteria.py), copied from experiment
    12 and frozen here — the old rubric's five criteria as five Score questions.
  - [eval50_jev.py](eval50_jev.py) with [items.py](items.py), copied from experiment 11
    and frozen here — fifty narrow properties as fifty Score questions, each judged
    `no`/`partial`/`yes`. Its imports from experiment 11's `eval50.py` were carried into
    the file rather than kept: that module drives a generative evaluator and has no place
    in a run that never calls one.

  Frozen copies rather than imports. Experiments 11 and 12 are finished records whose rubrics were
  the thing they tested, so importing from them would let a later edit change what the
  results here claim to mean. The cost is that the copies have to be diffed rather than
  trusted to agree.
- **Targets**: two translator directory names, `gpt-5.6-luna` and `union-alpha`, given on
  the command line. Every language each of them has under `tr/` is evaluated, which comes
  to 134 translations. There is no target list: a translator's `tr/` directory already
  states which languages it covers and this experiment takes all of them, so a list would
  be a copy of that with nothing added. Experiment 11 needed a file because its 8 targets
  encoded a selection; "every language this translator has" encodes nothing.
- **Runs**: 1. Experiment 12 section 3.1 measured this evaluator's run-to-run range at
  1.12 points and showed run 1 alone reproduces the median of three at Spearman 1.000;
  three runs would triple the cost and settle nothing.
- **Reference**: each translation's old-scheme score, the median of the three runs already
  in `examples/tr/onde/{translator}/evals/`, read in place. Never copied.
- **Output**: `evals-degrees/` for the five-criterion scheme, named for the level set that
  produced it, in `trtools eval`'s schema; `evals50/` for the fifty-item scheme, in
  experiment 11's schema. Each holds one subdirectory per translator, and one
  `<lang>.json` per translation — `evals50/union-alpha/uk.json`. Experiments 11 and 12
  put everything in one flat directory under a name that repeated the topic, the
  translator, the evaluator and a run number; at 134 files per scheme that stops being
  readable, and every one of those four is either constant here or already named by the
  directory. A second and later run appends `-N`, so an interrupted `--runs 3` can still
  tell which of its runs are on disk. Experiment 11's `agg50.py` and `refcmp.py` expect
  the flat names and would have to be pointed at this layout to read `evals50/`.

  A five-criterion file also records the level set and the level texts it was scored on,
  so a result never depends on a script to say what it means.
- **Cost**: 134 evaluations at roughly $0.0002 each for the five-criterion scheme, about
  **$0.03**; the fifty-item scheme sends about 12.7k input tokens per evaluation against
  5.8k, so roughly **$0.06**. Minutes, not hours, either way.

---

## 3. Results

134 evaluations, one run each, about $0.03. [agg13.py](agg13.py) generates every table
below, reading the corpus's own scores where they live.

### 1. The top of the scale exists

This is the question experiment 12 could not answer, and it answers cleanly. Over 670
judgments:

| | L0 | L1 | L2 | L3 | L4 |
|---|---:|---:|---:|---:|---:|
| Mean probability mass | 0.000 | 0.009 | 0.080 | 0.346 | **0.564** |
| Times most probable | 0 | 2 | 1 | 198 | **469** |

Experiment 12 section 3.4 found level 3 most probable in 100 of 120 judgments and level 4
in 5, and could not tell a correct level 3 from a level wide enough to absorb everything.
On the corpus's best translations level 4 wins **469 of 670**, and level 3 falls from 83%
of judgments to 30%. The scale was tracking translation quality, not saturating: the same
levels that sat on 3 for experiment 12's targets sit on 4 for these. Mean confidence rises
with it, from 0.55 to **0.65**.

That disposes of the second of the two readings experiment 12 left open. The first — that
its 8 targets really are level-3 translations — is what is left, and it is the one that
says the evaluator is working.

### 2. Agreement holds at n=67, and the offset is small

| Set | n | Pearson | Spearman | Kendall | Mean diff | Mean abs diff |
|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 67 | +0.63 | +0.67 | +0.50 | -4.1 | 6.4 |
| union-alpha | 67 | +0.63 | +0.69 | +0.54 | -3.3 | 5.7 |
| **pooled** | 134 | +0.62 | **+0.69** | +0.53 | **-3.7** | 6.0 |

Experiment 12 got Spearman +0.64 against the corpus reference on 8 targets, which was
suggestive and nothing more. At n=67 per translator, against a per-translation reference
rather than a per-language mean, it holds: **+0.69** pooled over 134.

The offset is the other half of it. This scheme reads **3.7 points below** the old one on
average, against 2.1 points below on experiment 12's eight targets — the same small
constant, on translations a full 17 points higher up the scale. The two schemes are close
to the same scale, which is what makes the correlation interpretable rather than an
artifact of two differently-shaped distributions.

### 3. It does not separate the two translators, and neither does the old scheme

| Translator | `jev` mean | Old mean |
|---|---:|---:|
| gpt-5.6-luna | 86.24 | 90.31 |
| union-alpha | **86.77** | **90.09** |

`jev` puts `union-alpha` ahead by 0.53 points; the old scheme puts `gpt-5.6-luna` ahead by
0.22. Both are ties, and they are ties in opposite directions. **Nothing here says which
translator is better**, and the experiment was not built to: the reference has no opinion
to check a verdict against. What can be read off it is that this evaluator does not
manufacture a separation where its reference sees none.

Per language the two schemes do line up:

| Scheme | gpt-5.6-luna | union-alpha | tied |
|---|---:|---:|---:|
| `jev` | 37 | 29 | 1 |
| old (3-run medians) | 31 | 23 | 13 |

Both take a side in 53 of the 67 languages, and pick the same translator in **37 of those
53 (70%)**. That is a real signal at the per-language level from an evaluator whose
corpus-level verdict is a tie — which is the shape you would expect if the two translators
are genuinely close and the per-language differences are genuinely there.

The 13 old ties against `jev`'s 1 are worth noting on their own. A 21-point integer scale
summed over five criteria collides constantly; a probability-weighted position does not.

### 4. The disagreements sit partly, but only partly, on the reference's noise

The largest disagreements look at first like the reference's fault:

| | Translator | Lang | `jev` | Old | Diff | Old 3 runs |
|---|---|---|---:|---:|---:|---|
| jev higher | union-alpha | ga | 72.3 | 31 | **+41.3** | 21, 42, 31 |
| jev higher | gpt-5.6-luna | tl | 83.2 | 62 | +21.2 | 70, 56, 62 |
| jev higher | gpt-5.6-luna | cy | 86.0 | 67 | +19.0 | 91, 67, 52 |
| jev lower | gpt-5.6-luna | el | 72.5 | 89 | -16.5 | — |
| jev lower | union-alpha | ne | 75.6 | 91 | -15.4 | — |

`union-alpha / ga` is scored 21, 42 and 31 by the old scheme — a 21-point spread around a
median of 31 — while the same scheme gives `gpt-5.6-luna` 83 for the same language. That
is not a reference that can adjudicate a 41-point disagreement.

But the general version of that excuse does not hold up, so it is stated rather than
leaned on. Bucketing all 134 translations by the spread of the three runs behind their
median:

| Old 3-run range | n | Pearson | Spearman | Mean abs diff |
|---|---:|---:|---:|---:|
| 0–9 (steady) | 93 | **+0.61** | **+0.57** | **5.4** |
| 10–19 | 27 | +0.35 | +0.51 | 5.8 |
| 20+ (noisy) | 14 | +0.41 | +0.37 | 10.3 |

Agreement is best where the reference is steadiest and the mean disagreement doubles in
the noisy bucket — but translation by translation, the size of the disagreement and the
old scheme's own range correlate at only Pearson **+0.20** (Spearman +0.05), and the noisy
bucket is n=14. So: some of the disagreement is the reference's instability, most of it is
not accounted for, and the reference's noise cannot be used to explain away an arbitrary
disagreement.

### 5. Fluency is the floor again

| Criterion (mean, 0–20) | gpt-5.6-luna | union-alpha |
|---|---:|---:|
| Readability | 18.01 | 18.11 |
| Fluency | **15.42** | **15.42** |
| Terminology | 17.36 | 17.49 |
| Contextual adaptation | 17.18 | 17.33 |
| Information completeness | 18.28 | 18.43 |

Fluency sits about 2.5 points below every other criterion and is the one figure identical
to two decimals across both translators. Experiment 12 found the same criterion moved
least when the levels were rewritten. Whether that is a real property of machine
translation at this quality level or a property of how this evaluator reads "natural and
smooth to native speakers" is not something either experiment can say.

### 6. The two rubrics agree at +0.90, but only before rounding

The fifty-item scheme over the same 134 translations, one run each. [cmp13.py](cmp13.py)
generates this section.

| Pair | Pearson | Spearman | Kendall |
|---|---:|---:|---:|
| 5 criteria vs 50 items, probability-weighted totals | **+0.90** | +0.89 | +0.73 |
| 5 criteria vs 50 items, rounded verdict totals | +0.72 | +0.74 | +0.71 |

**Experiment 12's +0.90 replicates exactly**, at n=134 instead of n=8. That was its
strongest result and the one resting on the fewest targets, and it survives the jump
without moving to two decimal places. Two rubrics that share no wording — five broad
criteria on a five-level severity scale against fifty narrow properties on
`no`/`partial`/`yes` — land on the same ordering of the same translations. What they do
share is the evaluator, which is the honest reading: this is a fact about Jev's judgments
being stable under a change of rubric, not evidence that either rubric is right.

The second row is the caveat, and it is not small. Rounding each judgment to its most
probable level costs 0.18 of correlation, because the fifty-item scheme's verdict total
is at the ceiling:

| Scheme | Total | Mean | Range | Mean confidence |
|---|---|---:|---:|---:|
| 5 criteria | probability-weighted | 86.51 | 72.1–94.7 | 0.65 |
| 5 criteria | rounded | 86.46 | 73.0–96.0 | |
| 50 items | probability-weighted | 86.01 | 66.8–91.8 | 0.61 |
| 50 items | **rounded** | **97.52** | 77.0–100.0 | |
| old scheme | 3-run median | 90.20 | 31.0–100.0 | |

96.1% of the 6,700 item verdicts are `yes`, against 2.7% `partial` and 1.1% `no`. That is
[experiment 11's diagnosed failure](../11/README.md) reproduced precisely — "a confident
near-ceiling score", where "every item is positively phrased, so a defect an evaluator
cannot see is silently scored `yes`" — and it is what experiment 11's Discussion 4 blames
for the local evaluators' inflation. The probability weighting is the entire difference
between a usable scale and a saturated one here: the same 134 translations spread over
66.8–91.8 weighted and over 77–100 rounded.

Note what that does *not* say about the five-criterion scheme, whose two totals are 86.51
and 86.46 — indistinguishable. Five levels of severity per criterion round harmlessly;
three levels per property do not. The resolution the fifty-item scheme buys is real, but
on this evaluator it lives entirely in the distribution and none of it in the verdict.

Against the old scheme the five-criterion scheme tracks better on every statistic:

| Scheme | Total | Pearson | Spearman | Kendall | Mean diff |
|---|---|---:|---:|---:|---:|
| 5 criteria | weighted | **+0.62** | **+0.69** | +0.53 | -3.7 |
| 50 items | weighted | +0.53 | +0.63 | +0.47 | -4.2 |
| 50 items | rounded | +0.47 | +0.55 | +0.50 | +7.3 |

**This does not settle which rubric is better.** The old scheme *is* the five-criterion
rubric, scored by a generative model; it shares a rubric with one of these schemes and not
the other, so a margin in that direction is what shared wording predicts regardless of
accuracy. What the table does say is that both track the corpus, and that the fifty-item
scheme's rounded total tracks it worst while sitting 7.3 points above it.

### 7. Which of the two to use

Measured over these 134 translations, one run each:

| | 5 criteria | 50 items | Ratio |
|---|---:|---:|---:|
| Input tokens, total | 943,916 | 1,860,476 | **×1.97** |
| Input tokens, per evaluation | 7,044 | 13,884 | |
| Output tokens, total | 11,122 | 131,052 | ×11.78 |
| Wall time, per evaluation | 0.27s | 0.33s | ×1.19 |

TypeSafe bills input, so the fifty-item scheme costs about twice as much. Time is not the
constraint — fifty questions and five questions go in one request either way, and the
state, which is most of the input, is billed once per request rather than once per
question.

**For ranking, use the five criteria.** The two weighted totals differ by a mean absolute
1.92 points, with 89 of 134 translations within 2 points and 126 within 5; against scale
standard deviations of 5.44 and 4.52, that is agreement well inside the noise anyone would
act on. The five-criterion scheme also rounds harmlessly, so its plain `total_score` is
usable as it stands, where the fifty-item scheme's saturates at 97.52 and only its
weighted total is worth reading. And it is in the corpus's own units, so it can be
compared against everything already accumulated. Paying twice as much for the same
ordering, reported on a scale that needs a caveat, is not a trade worth making.

**For diagnosis, use the fifty items.** What the extra tokens buy is not accuracy but
localisation. The 4% of verdicts that are not `yes` do not scatter:

| Item | `no` | `partial` |
|---|---:|---:|
| `e05_no_calque` | 8 | 95 |
| `b04_no_intraword_intrusion` | 32 | 5 |
| `b05_script_consistency` | 14 | — |
| `d04_notation_convention` | 11 | — |

Only 10 of the 50 items were ever scored `no` and 31 ever `partial`. Section 3.5's finding
that fluency sits 2.5 points below every other criterion is, in all likelihood, those 95
calque verdicts — and the five-criterion scheme cannot say that, because it collapses them
into one number per criterion.

The second thing lost is the ability to be checked. Experiment 11 could test Jev against
ground truth because `a01_speaker_label_present` is settled by counting unlabeled lines;
the five-criterion scheme has no item to count against, so nothing in it can be verified
rather than correlated. That is an argument for keeping the fifty-item scheme available,
not for running it by default.

---

## 4. Reproducing

```bash
# 1. Evaluate all 134 targets, one run each, under each scheme (needs TYPESAFE_API_KEY)
uv run experimental/13/eval5_jev.py    # 5 criteria  -> evals-degrees/
uv run experimental/13/eval50_jev.py   # 50 items    -> evals50/

# 2. Aggregate the five-criterion run against the corpus's own scores
uv run experimental/13/agg13.py

# 3. Compare the two rubrics against each other
uv run experimental/13/cmp13.py
```

Existing result files are skipped, so an interrupted run resumes where it stopped and
costs nothing for what is already on disk. `agg13.py` reports on whatever it finds, so it
can be run while the evaluation is still going.

Both scripts take translator directory names as positional arguments, so any other
selection from the corpus is a matter of naming it:

```bash
uv run experimental/13/eval5_jev.py qwen3.8 bonsai2-27b
uv run experimental/13/eval50_jev.py qwen3.8 bonsai2-27b
uv run experimental/13/agg13.py qwen3.8 bonsai2-27b
```

---

## 5. What Would Come Next

1. **The bottom of the scale.** Still untested, and now the obvious gap: level 4 dominates
   here, level 3 dominated experiment 12's targets, and nothing has been run where level 1
   or 2 should win. `bonsai2-27b` sits at 27.90 under the old scheme against `qwen3.8`'s
   53.96, and it is the same 134-evaluation shape as this run. That is also experiment
   11's Future Work 7 — whether a cheaper scheme still separates a ternary-quantized model
   from its full-precision parent, which the old scheme did by 26 points in 62 of 67
   languages — so one run answers both.
2. **The middle of the corpus.** Sections 2 and 4 rest on translations the old scheme
   scores in the 80s and 90s. Whether Spearman +0.69 survives on translators the old
   scheme puts at 60–70, where its own rankings are most contested, is what decides if
   this is usable as a general replacement rather than a check on good translations.
3. **Fluency.** Section 3.5 is either a finding about machine translation or a bias in one
   criterion's wording, and the two are distinguishable: the criterion descriptions are
   `trtools/evaluate.py`'s verbatim, so rewording only that one and re-running 134
   evaluations would say which.
4. **Why the offset is 3.7 points and not zero.** Small enough to ignore for ranking,
   large enough to matter for any absolute claim. It is one number and it has not been
   looked into.
5. **Whether the fifty-item verdicts can be rescued.** Section 3.7 recommends the
   five-criterion scheme for ranking on cost, which leaves the fifty-item one to justify
   itself as a diagnostic — and a diagnostic whose headline number is 96.1% `yes` is not
   yet one. The choice is to abandon the verdict in favour of the weighted total, which
   costs comparability with every generative evaluator experiment 11 ran, or to rewrite
   the three levels the way experiment 12 rewrote its five. Experiment 12 is the precedent
   that this is worth trying: there, the level wording moved the corpus mean by 15 points.
6. **Whether +0.90 says anything about the rubrics at all.** Two rubrics sharing nothing
   but an evaluator agree at +0.90; a third rubric asked of the same evaluator would say
   whether that is a property of the rubrics or of Jev. If everything Jev is asked
   correlates at +0.90, the number is about the model, and neither rubric is being
   validated by it.
