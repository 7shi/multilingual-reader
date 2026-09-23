# Experiment 13: Both Ends of the Corpus, Every Language, One Run

This file is the experiment record: what was run, what it measured, and what that
does and does not support. What was *decided* on the strength of it — replacing the
corpus evaluator — is [PLAN.md](PLAN.md), and what is left to do about it, with the
blockers in the way, is [PORT.md](PORT.md); both are kept separate so a plan changing does
not edit a result.

**Status**: frozen, 2026-09-23. Section 7 item 1's remainder is closed by
[FLOOR.md](FLOOR.md); the items still open are kept in
[examples/tr/README.md](../../examples/tr/README.md) ("Scope of the Comparison and Open
Questions").

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
corpus has them (`bonsai2-27b` at 27.90); it was run separately, and **section 4** is that
run. Everything in section 3 is the top two and stands as first written.

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
  Section 4 runs the same shape over `qwen3.8` and `bonsai2-27b`, a second 134,
  into the same two output directories.
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

*Settled afterwards, from data already on disk: **section 5.1**. The second reading is
refuted — the fifty-item scheme's own fluency group and the old generative evaluator, over
all 16 translators, put fluency lowest too. Section 5.2 adds that it is the criterion that
discriminates most at the top of the corpus.*

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

## 4. The Bottom of the Scale

Section 3 leaves two things open that the same run answers: nothing had been evaluated
where levels 1 and 2 should win, and experiment 11's Future Work 7 — whether a scheme this
cheap still separates a ternary-quantized model from its full-precision parent — had no
result. `qwen3.8` (old corpus mean 53.96) and `bonsai2-27b` (27.90), its ternary
quantization, are the corpus's answer to both. Same two schemes, same 67 languages each,
134 translations, one run, nothing above rewritten:

```bash
uv run experimental/13/eval5_jev.py  qwen3.8 bonsai2-27b
uv run experimental/13/eval50_jev.py qwen3.8 bonsai2-27b
uv run experimental/13/agg13.py qwen3.8 bonsai2-27b
uv run experimental/13/cmp13.py qwen3.8 bonsai2-27b
```

The quantization pair is the one target in this corpus where the answer is close to known
in advance. `bonsai2-27b` is not a different translator from `qwen3.8`; it is the same
model with its weights crushed, so a scheme that cannot tell them apart is not measuring
translation quality. That is why this section can say more than section 3.3 could.

### 1. Levels 0, 1 and 2 exist as well

| | L0 | L1 | L2 | L3 | L4 |
|---|---:|---:|---:|---:|---:|
| Mean probability mass | 0.086 | 0.253 | 0.236 | 0.289 | 0.135 |
| Times most probable | **46** | **191** | **156** | 219 | 58 |

Section 3.1 found level 4 winning 469 of 670 judgments on the corpus's best translations,
and experiment 12 found level 3 winning 100 of 120 on its mid-range targets. Here levels 0
through 2 take **393 of 670 (59%)**, and level 0 — never once the most probable level on
the top two — wins 46 times. Level 3 is still the largest single bucket at 219, but
at 33% of judgments rather than 83%.

Three runs, three different modes, ordered the way the targets are:

| Targets | Old-scheme mean | Modal level | L4 mass | Mean confidence |
|---|---:|---|---:|---:|
| experiment 12's 8 | — | L3, 100/120 | 0.175 | 0.55 |
| top two (section 3) | 90.20 | **L4**, 469/670 | 0.564 | 0.65 |
| this pair | 40.93 | L3, 219/670 — but L0–L2 take 393 | 0.135 | 0.59 |

Experiment 12's targets have no comparable old-scheme mean: they were selected for having
the widest 3-run spread in the corpus, so their medians are not a position on the scale.

That is the full scale in use. Section 3.1 could rule out saturation at the top; this rules
it out at the bottom, and the two together say the level set spans the corpus rather than
covering one end of it.

### 2. Agreement is far stronger here — and most of that is range

| Set | n | Pearson | Spearman | Kendall | Mean diff | Mean abs diff |
|---|---:|---:|---:|---:|---:|---:|
| qwen3.8 | 67 | +0.93 | +0.94 | +0.80 | +12.5 | 15.3 |
| bonsai2-27b | 67 | +0.92 | +0.95 | +0.85 | +12.3 | 13.9 |
| **pooled** | 134 | +0.92 | **+0.96** | +0.84 | **+12.4** | 14.6 |
| *(top two, section 3.2)* | *134* | *+0.62* | *+0.69* | *+0.53* | *-3.7* | *6.0* |

Spearman +0.96 against +0.69 looks like the evaluator working far better down here, and
that reading should be resisted. The reference's own spread is **3.2× wider** on this pair
— standard deviation 27.93 against 8.72, interquartile range 21–59 against 88–96 — and
correlation rises with range whatever the evaluator is doing. Restriction of range alone
predicts most of the difference, and nothing in this run separates that from a real gain in
accuracy. What can be said is the weaker claim in both directions: **the scheme tracks the
reference at both ends of the corpus**, and it does not fall apart where the reference's
own scores do.

The mean absolute difference moves the other way — 14.6 points here against 6.0 at the top
— which is the same fact seen from the other side.

### 3. The offset is not an offset

Section 3.2 reported the scheme reading 3.7 points **below** the old one, and
[section 7 item 4](#7-what-would-come-next) asked why it was 3.7 and not zero. Here it
reads **12.4 points above**. A constant does not change sign, so it was never a constant.
Fitting all 268 translations from both runs:

```
jev = 0.69 × old + 24.7        (crossover at old = 79.6)
```

| Set | n | Slope of `jev` on old | Old mean | `jev` mean |
|---|---:|---:|---:|---:|
| top two | 134 | 0.39 | 90.20 | 86.51 |
| this pair | 134 | 0.75 | 40.93 | 53.34 |
| both | 268 | **0.69** | 65.57 | 69.93 |

The scheme is **compressed** against the old one: it pulls bad translations up and good
ones down, crossing the old scale around 80. The -3.7 of section 3.2 and the +12.4 here are
the same slope read at two points, not two offsets. For ranking this changes nothing —
compression is monotone, and the Spearman figures are what section 3.7's recommendation
rests on — but any absolute claim, or any comparison of a `jev` score against a corpus
number, has to go through the slope rather than through a constant.

### 4. Quantization: the cheap scheme separates them, slightly more cleanly

| | `jev` | Old (3-run medians) |
|---|---:|---:|
| qwen3.8 corpus mean | 66.49 | 53.96 |
| bonsai2-27b corpus mean | 40.18 | 27.90 |
| **Gap** | **+26.31** | **+26.06** |
| Languages separated (of 67) | **66** | 62 |
| Separated by ≥10 points | **60** | 53 |
| Same winner where both take a side | 61/66 (92%) | |

This is experiment 11's Future Work 7, answered. The old scheme separated the quantized
model from its parent by 26 points in 62 of 67 languages; the five-criterion scheme
reproduces the gap to within **0.25 points** and separates **66 of 67** — one more clean
than the reference, at half the input tokens of the fifty-item scheme and a fraction of the
old scheme's three generative runs. The single exception is not a reversal worth the
name: `jev` puts `bonsai2-27b` ahead in one language by **0.1 points**.

The reason it separates more of them is at the floor. The old scheme scores
`bonsai2-27b` a flat **0 in 10 of its 67 languages** (`cs cy fi hr ia id sk sl sw th`), and
15 at 10 or below: below some quality threshold a 21-point integer scale summed over five
criteria has nothing left to say. On those same 10 translations `jev` returns 2.6 to 31.2,
an ordering where the reference has a single value. This is section 3.3's point about the
old scheme's 13 ties, seen at the other end of the scale — and here it costs the reference
real information, because a quantization this severe fails by degrees.

Whether that ordering inside the floor is *correct* is not something this run can check;
[FLOOR.md](FLOOR.md) checks it by reading the ten, and it holds as a coarse order.
What it establishes is that the cheap scheme is usable for the one question quantization
work actually asks — did this hurt, and where — and that the old scheme stops answering it
first.

### 5. The fifty-item verdicts are not saturated here

Section 3.6 found 96.1% of item verdicts `yes` and rounding costing 0.18 of correlation.
Over these 134 translations:

| Verdict | Top two (section 3.6) | This pair |
|---|---:|---:|
| `yes` | 96.1% | 64.5% |
| `partial` | 2.7% | 11.4% |
| `no` | 1.1% | **24.1%** |
| Items ever scored `no` | 10 of 50 | **49 of 50** |
| Items ever scored `partial` | 31 of 50 | 47 of 50 |

And the rounding penalty goes with it:

| Pair | Top two | This pair |
|---|---:|---:|
| 5 criteria vs 50 items, weighted | +0.90 | +0.95 |
| 5 criteria vs 50 items, **rounded** | +0.72 | **+0.94** |

**The saturation section 3.6 diagnosed is a property of the targets, not of the rubric.**
The fifty items discriminate perfectly well when there is something to discriminate; what
they cannot do is tell two near-perfect translations apart, because a positively-phrased
item has nowhere above `yes` to go. That narrows [section 7 item 5](#7-what-would-come-next)
considerably: the three levels do not need rewriting for the corpus at large, they need a
ceiling for its top. Experiment 11's diagnosis stands, with its scope corrected.

Two things do not improve. The fifty-item scheme's mean confidence falls to **0.38** here
(0.61 on the top two) against the five-criterion scheme's 0.59, and its inflation against
the old scheme is much the larger:

| Scheme | Total | Pearson | Spearman | Mean diff |
|---|---|---:|---:|---:|
| 5 criteria | weighted | **+0.92** | **+0.96** | **+12.4** |
| 5 criteria | rounded | +0.92 | +0.96 | +12.4 |
| 50 items | weighted | +0.90 | +0.92 | +23.4 |
| 50 items | rounded | +0.88 | +0.92 | +29.3 |

Section 3.7's recommendation is unchanged and, on this evidence, stronger: the
five-criterion scheme tracks the reference better and sits half as far above it, at half
the cost.

Where the two rubrics disagree is systematic and worth recording. The five largest
residuals in each direction are all `bonsai2-27b` on one side — the fifty items rate
badly-broken translations far higher (`fi` 3.8 against 49.6) — and good translations of
`zh`, `ar`, `fr` on the other. Fifty narrow properties scored independently cannot
register that a translation has failed as a whole; most of them are still satisfied by
text that is unusable.

### 6. Spread, per translator and per scheme

All four translators measured so far, 67 languages each, one run each. Median and standard
deviation are across languages, not across runs — every translation here was evaluated
once.

**Probability-weighted totals**, which is what each scheme is recommended on:

| Translator | n | 5 criteria | sd | 50 items | sd | Old (3-run median) | sd |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 67 | 88.00 | 5.82 | 87.08 | 4.97 | 93.00 | 8.15 |
| union-alpha | 67 | 87.15 | 5.06 | 86.84 | 4.04 | 92.00 | 9.31 |
| qwen3.8 | 67 | 70.10 | 15.18 | 74.34 | 11.77 | 52.00 | 25.38 |
| bonsai2-27b | 67 | **38.45** | **21.10** | **56.27** | **13.40** | 24.00 | 24.15 |

**Rounded verdict totals**, for what rounding costs each scheme:

| Translator | 5 criteria | sd | 50 items | sd |
|---|---:|---:|---:|---:|
| gpt-5.6-luna | 88.00 | 5.67 | **99.00** | 4.18 |
| union-alpha | 87.00 | 4.99 | **99.00** | 2.43 |
| qwen3.8 | 71.00 | 15.10 | 86.00 | 15.98 |
| bonsai2-27b | 39.00 | 20.97 | 58.00 | 18.67 |

Three things come out of this that the pooled statistics above do not show.

**The five-criterion scheme keeps more spread, and the gap opens downward.** On the top two
the two schemes are indistinguishable (88.00/5.82 against 87.08/4.97). On `bonsai2-27b` the
five-criterion scheme reads 18 points lower with **1.6× the standard deviation**. The
fifty-item scheme's compression against the old scale, which section 4.3 measured for the
five-criterion scheme at a slope of 0.69, is steeper still.

That makes the five-criterion scheme easier to compare translators with, and it is worth
being careful about what that does and does not mean. A wider spread is not by itself
better: the two schemes are not on the same scale, and spreading the same ordering over
more points adds nothing. **What matters is spread against the scheme's own noise**, and
both figures were measured on other targets — experiment 12 section 3.1 put the
five-criterion scheme's mean run-to-run range at **1.12** and experiment 11's fifty-item
Jev run at **2.25**. Taking those as indicative:

| Translator | 5 criteria, sd ÷ 1.12 | 50 items, sd ÷ 2.25 |
|---|---:|---:|
| gpt-5.6-luna | 5.2 | 2.2 |
| union-alpha | 4.5 | 1.8 |
| qwen3.8 | 13.6 | 5.2 |
| bonsai2-27b | 18.8 | 6.0 |

The five-criterion scheme has roughly **2–3× the spread per unit of its own noise**, at
every quality level. That is a stronger statement than "wider range", and it is the one the
cost argument in section 3.7 was missing — but the two noise figures come from different
experiments on different targets, so this is an indication and not a measurement. Measuring
it properly means three runs of both schemes on one target set, which nothing so far has
paid for.

**The standard deviations are themselves ordered by quality** — 5.82, 5.06, 15.18, 21.10.
A good translator is uniformly good across languages; a broken one fails language by
language. The old scheme shows the same shape with one exception, and the exception is
informative: its sd **falls** from 25.38 to 24.15 between `qwen3.8` and `bonsai2-27b`, the
one place the ordering breaks, because 10 of `bonsai2-27b`'s translations are pinned to 0
and a floor truncates variance. Section 4.4 reads that floor off the separation counts;
here it shows up as the reference's dispersion going the wrong way.

**Rounding is a fifty-item problem, confirmed per translator.** The five-criterion scheme's
two tables are the same to within a point everywhere (88.00 against 88.00, sd 5.82 against
5.67). The fifty-item scheme's rounded total sits at a median of **99.00** for both top
translators, with `union-alpha`'s standard deviation collapsing to **2.43** — its 67
languages take only 10 distinct values, and **57 of them fall in 97–100**. Section 3.6 measured that as a loss of 0.18 of
correlation; this is the same fact as a distribution.

### 7. Cost is the same ratio

| | 5 criteria | 50 items | Ratio |
|---|---:|---:|---:|
| Input tokens, total | 925,334 | 1,841,894 | **×1.99** |
| Input tokens, per evaluation | 6,905 | 13,745 | |
| Output tokens, total | 11,122 | 131,052 | ×11.78 |
| Wall time, per evaluation | 0.25s | 0.32s | ×1.28 |

Within 2% of section 3.7's input-token figures, which is expected: the state is the same
size whatever the translation says. Output is identical to the token — 11,122 either time —
because a five-question structured response has a fixed shape.

---

## 5. The Corpus as a Yardstick

Everything above asks whether this scheme measures translation quality. That is not quite
the question the corpus exists to answer. The corpus exists to say **how many languages a
model can translate acceptably**, which is a different instrument with different
requirements: it needs to rank models, to survive being pointed at new ones, and to say
which languages fail — not to be right in the abstract about any single translation.

This section is what fell out of reading the existing measurements against that use. No new
evaluations were run for it: sections 5.1 through 5.4 are computed from data already on
disk, which is why several questions section 7 had listed as open turn out to be answered.

### 1. Fluency is real, and section 3.5's second reading is dead

Section 3.5 found fluency about 2.5 points below every other criterion and could not say
whether that was machine translation or how this evaluator reads "natural and smooth to
native speakers". The corpus already contains two independent checks.

**The fifty-item scheme has its own fluency group** — `e`, ten narrow properties
(`e03_syntax`, `e05_no_calque`, `e07_spoken_register`, `e10_orthography`, …) sharing no
wording with the five-criterion description:

| Group (mean, 0–20) | gpt-5.6-luna | union-alpha | qwen3.8 | bonsai2-27b |
|---|---:|---:|---:|---:|
| a Structural integrity | 18.72 | 18.83 | 16.66 | 13.77 |
| b Language purity | 16.97 | 17.13 | 15.20 | 12.38 |
| c Semantic fidelity | 17.93 | 18.06 | 14.67 | 11.16 |
| d Terminology | 16.44 | 16.50 | 14.01 | 11.35 |
| **e Fluency and naturalness** | **15.69** | **15.77** | **11.67** | **7.73** |

Lowest in all four, and per translation the two schemes' fluency figures correlate at
**+0.91, +0.92, +0.97, +0.91**.

**The old generative evaluator says the same thing over all 16 translators.** Per-criterion
means from `examples/tr/onde/*/evals/`, a different model on a different mechanism:

| Criterion (mean over 16 translators, 0–20) | |
|---|---:|
| Information completeness | 15.64 |
| Terminology | 14.08 |
| Contextual adaptation | 14.03 |
| Readability | 13.74 |
| **Fluency** | **12.76** |

Fluency is the lowest criterion in **16 of 16 translators**, without exception.

Two rubrics, two evaluator models, two granularities, one direction. **The "bias in one
criterion's wording" reading is refuted**, and section 7 item 3's proposed test — reword
that criterion and re-run — would not have been decisive anyway, since experiment 12
already established that level wording moves scores.

What is left is narrower than the original question. All of this is 67 translations of one
document, a spoken dialogue about physics, so a fluency floor specific to *this source
text* is not excluded; a second source in another genre would settle it. And no human has
checked any of it — three evaluators agreeing is not ground truth. Item-level evidence
gives at least a mechanism: `e05_no_calque` is the most-failed item in both runs (95
`partial` on the top two, 91 `no` on the bottom pair), and calque is the documented failure
mode of machine translation.

### 2. Fluency is also the criterion that discriminates at the top

Across all 16 translators the five criteria are near-identical in spread, so none of them
is obviously carrying the ranking:

| Criterion | min | max | range | sd |
|---|---:|---:|---:|---:|
| Readability | 5.48 | 18.01 | 12.54 | 3.25 |
| Fluency | 4.72 | 17.18 | 12.46 | 3.31 |
| Terminology | 6.03 | 17.75 | 11.72 | 3.09 |
| Contextual adaptation | 5.31 | 18.22 | 12.91 | 3.40 |
| Information completeness | 6.43 | 19.25 | 12.82 | 3.25 |

Restricted to the four best translators, they are not:

| Criterion | spread among the top 4 |
|---|---:|
| **Fluency** | **1.22** |
| Contextual adaptation | 0.99 |
| Readability | 0.96 |
| Terminology | 0.93 |
| **Information completeness** | **0.43** |

Information completeness reaches 19.25/20 at the top and is nearly a constant there;
fluency is the one criterion still separating models. **Rewording fluency upward would
remove the most informative signal the rubric has at the top of the corpus**, which is
where new models arrive. Section 7 item 3 is withdrawn on that basis rather than merely
answered.

### 3. The mean hides coverage, and the tail is unusable with the old evaluator

For "how many languages does this model handle", the corpus mean is the wrong summary.
Counting languages at or above 80 — `generate_compare_rows.py`'s existing `practical range`
boundary — reorders it:

| Translator | Old mean | ≥80 | % | the three single runs | 70–90 band |
|---|---:|---:|---:|---|---:|
| union-alpha | 90.09 | **63** | 94 | 60, 62, 60 | 17 |
| gpt-5.6-luna | 90.31 | 61 | 91 | 55, 61, 59 | 20 |
| gemini-3.7-flash | 87.48 | 58 | 87 | 55, 59, 54 | 21 |
| ox-alpha | 85.73 | 52 | 78 | 50, 53, 54 | 24 |
| gemini-3-flash | 78.09 | **48** | 72 | 44, 44, 43 | 37 |
| gpt-5.6-terra | 77.66 | 40 | 60 | 41, 46, 35 | 23 |
| gemini-2.5-flash | **81.61** | **39** | 58 | 43, 33, 42 | 40 |
| gemma4-31b | 66.72 | 32 | 48 | 32, 34, 30 | 15 |
| gemma4 | 68.16 | 29 | 43 | 32, 30, 27 | 19 |
| gemini-3.5-flash-lite | 66.10 | 24 | 36 | 23, 21, 24 | 22 |
| muse-glimmer | 63.64 | 19 | 28 | 19, 19, 18 | 25 |
| qwen3.6 | 58.28 | 17 | 25 | 16, 19, 16 | 19 |
| gpt-oss | 65.07 | 15 | 22 | 19, 20, 12 | 24 |
| qwen3.6-27b | 63.00 | 14 | 21 | 18, 18, 16 | 20 |
| qwen3.8 | 53.96 | 14 | 21 | 13, 17, 15 | 14 |
| bonsai2-27b | 27.90 | 5 | 7 | 5, 4, 5 | 2 |

`gemini-2.5-flash` has the higher mean (81.61 against 78.09) and nine fewer usable
languages than `gemini-3-flash`. A few strong languages lift a mean; they do not widen
coverage. The top two also swap: the mean puts `gpt-5.6-luna` ahead by 0.22, the count puts
`union-alpha` ahead 63 to 61.

**But the count is more noise-sensitive than the mean**, because languages pile up near the
boundary — `gemini-2.5-flash` has 40 of its 67 in the 70–90 band. Recomputed from each
single run rather than the 3-run medians, the count moves by a mean of **4.4 languages** and
as much as **11** (`gemini-2.5-flash`: 43, 33, 42). The last column doubles as an error bar.

The minimum is worse still and should not be used at all under the current evaluator. The
three runs behind each translator's worst language spread by a mean of **15.1 points**:

| Translator | worst lang | median | the three runs | spread |
|---|---|---:|---|---:|
| gemini-3.7-flash | ia | 54 | 23, 59, 54 | 36 |
| gemini-2.5-flash | lo | 49 | 42, 72, 49 | 30 |
| gemini-3.5-flash-lite | si | 20 | 8, 20, 32 | 24 |
| union-alpha | ga | 31 | 21, 42, 31 | 21 |

Averaging 67 languages suppresses evaluator noise; taking a minimum amplifies it. **The
statistics that measure multilingual coverage are exactly the ones the current evaluator's
52.4-point swing destroys** — the mean was the only one robust to it. That is a sharper
argument for [PLAN.md](PLAN.md)'s migration than the one it was resting on, and it comes
from this use of the corpus rather than from the evaluator's accuracy.

### 4. What the migration does to the existing chart and tiers

`generate_compare_rows.py` ranks by `(median, pstdev)` and draws a boxplot per model. On the
four translators measured under both schemes:

| Translator | scale | min | q1 | median | q3 | max | pstdev |
|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | old | 62 | 88.0 | 93.0 | 96.0 | 100 | 8.13 |
| gpt-5.6-luna | jev | 72 | 82.7 | 88.0 | 91.0 | 95 | 5.77 |
| union-alpha | old | **29** | 88.0 | 92.0 | 95.0 | 98 | 9.39 |
| union-alpha | jev | **72** | 84.2 | 87.2 | 90.7 | 94 | 5.02 |
| qwen3.8 | old | 14 | 30.0 | 53.0 | 77.0 | 98 | 25.34 |
| qwen3.8 | jev | 38 | 54.8 | 70.1 | 78.1 | 94 | 15.07 |
| bonsai2-27b | old | 0 | 12.0 | 24.0 | 34.0 | 96 | 23.98 |
| bonsai2-27b | jev | 3 | **25.4** | 38.5 | **52.4** | 90 | 20.94 |

The box narrows as section 4.3's compression predicts. The **whisker** is where the change
matters: `union-alpha`'s left whisker moves from 29 to 72, and 29 is the `ga` translation
whose three old runs were 21, 42 and 31. The chart's most visually striking feature is
currently its least reliable one. At the other end the compression runs backwards —
`bonsai2-27b`'s box *widens*, because the old scheme's pile-up at 0 truncates its variance.

**Honest negative: the median does not separate the top pair any better.** 93 against 92
becomes 88.0 against 87.2. Whatever the migration buys, it is not top-end discrimination on
this statistic, and the two remaining top-four translators would have to be measured to say
more.

The tier boundaries do not survive unchanged. Under `jev = 0.69 × old + 24.7`:

```
old 60 -> jev 66.1
old 80 -> jev 79.9      <- the practical-range boundary, essentially unmoved
old 90 -> jev 86.8
```

Only 80 lands where it started, at the crossover. Left at 90/80/60 the tiers re-bucket
substantially — `gpt-5.6-luna` goes from 44 languages at 90+ to 24, and from 17 in 80–89 to
35 — without any change in translation quality. The boundaries are rough guides and the one
that defines "practical" is the one that holds, so this is recorded rather than treated as
a problem; see [PORT.md](PORT.md) section 5.2.

### 5. The reference has two definitions, and this experiment uses the other one

`SCORES.txt`, the comparison table and the chart all come from `trtools agg`, which totals
the **five criteria's medians** (`trtools/aggregate.py:67`). [agg13.py](agg13.py) uses the
**median of the three total scores**, which is what experiments 11 and 12 used. They are not
the same statistic, and `agg13.py`'s docstring claimed they were.

Over all 1,072 corpus translations they agree on **60%**, differ by a mean absolute **0.60
points**, and never by more than 7. Refitting section 4.3's compression against
`SCORES.txt` instead:

| Reference | Fit | Crossover |
|---|---|---:|
| median of totals (used here) | `jev = 0.690 × old + 24.7` | 79.6 |
| sum of criterion medians (`SCORES.txt`) | `jev = 0.688 × old + 24.8` | 79.4 |

Nothing in this experiment turns on the choice. The docstring is corrected and the
reference is left as the median of totals, for continuity with experiments 11 and 12.

---

## 6. Reproducing

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

All four scripts take translator directory names as positional arguments, so any other
selection from the corpus is a matter of naming it. Section 4 is that command, and the
results live beside these under the same two directories:

```bash
uv run experimental/13/eval5_jev.py  qwen3.8 bonsai2-27b
uv run experimental/13/eval50_jev.py qwen3.8 bonsai2-27b
uv run experimental/13/agg13.py qwen3.8 bonsai2-27b
uv run experimental/13/cmp13.py qwen3.8 bonsai2-27b
```

The two aggregators must be given the same names. `evals-degrees/` and `evals50/` hold one
subdirectory per translator and accumulate across runs, so without the argument they report
on their own default pair and a later run over different targets would otherwise be
averaged silently into the wrong table.

---

## 7. What Would Come Next

1. ~~**The bottom of the scale.**~~ **Done — section 4.** Levels 0–2 take 59% of judgments
   on `qwen3.8` and `bonsai2-27b`, and the five-criterion scheme reproduces the old
   scheme's 26-point quantization gap to within 0.25 points while separating 66 of 67
   languages against its 62. What it turned up instead is section 4.3: the scheme is
   compressed against the old one at a slope of 0.69, so the -3.7 offset of section 3.2 is
   not a constant. **What was left of this one** — whether the ordering `jev` produces
   inside the old scheme's floor, 10 translations it scores a flat 0, spread over 2.6 to
   31.2 here, is real or invented — **is answered in [FLOOR.md](FLOOR.md): real, as a
   coarse order.** It follows how much of the dialogue each translation carries before it
   collapses; between translations of similar coverage the gap is not an order.
2. **The middle of the corpus.** **Compared — [REPORT.md](REPORT.md) section 3:** all 16
   translators went through `trtools jev` on 2026-09-22
   ([JEV.md](../../examples/tr/onde/JEV.md)). The middle band is not specially weak: per
   translation, agreement inside every ten-point band of the old score is low, the top band
   included, and the corpus-wide +0.81 is mostly range; per translator, the middle of the
   ranking reorders because of lost speaker labels (REPORT.md section 4), not the band. As
   written before that run: now the
   only untested part of it, and the sharper question for having both ends. Section 3.2
   rests on translations the old scheme scores in the 80s and 90s (Spearman +0.69) and
   section 4.2 on ones it scores 0–98 (+0.96), and section 4.2 says most of that difference
   is range rather than accuracy. A translator the old scheme puts at 60–70, where its own
   rankings are most contested, has a narrow range *and* a contested reference — so it is
   the case where the two explanations come apart, and it is what decides whether this is a
   general replacement rather than a check on translations at the extremes. Section 4.3's
   slope predicts a near-zero mean difference there, which is a second thing to check
   against.
3. ~~**Fluency.**~~ **Withdrawn — sections 5.1 and 5.2.** The wording reading is refuted by
   two independent measurements that were already on disk, and the proposed test would not
   have been decisive regardless, since experiment 12 had already shown level wording moves
   scores. Worse, section 5.2 finds fluency is the criterion that separates the top four
   translators best (spread 1.22 against information completeness's 0.43), so rewording it
   upward would remove signal where the corpus most needs it. **What is left** is narrower:
   every measurement is 67 translations of one spoken-dialogue document, so a fluency floor
   specific to this source text is not excluded. A second source in another genre settles
   it, and nothing else will.
4. ~~**Why the offset is 3.7 points and not zero.**~~ **Answered, and it was the wrong
   question — section 4.3.** It is not an offset: the same scheme reads 12.4 points
   *above* the old one on this pair, and all 268 translations fit `jev = 0.69 × old +
   24.7`. What is left is why the slope is 0.69 — whether five ordered levels simply
   cannot reach the ends of a 100-point scale the way a generative model's free-hand
   numbers do, or whether the level wording is doing it — and whether it is stable enough
   to invert. If it is, corpus scores and `jev` scores can be put on one scale; if the
   slope moves with the translator, section 3.7's "ranking only" restriction is permanent.
5. **Whether the fifty-item verdicts can be rescued.** Narrowed by section 4.5: the
   96.1% `yes` is a ceiling effect on good translations, not a broken scale. On this pair
   the same items return 24.1% `no`, 49 of 50 fire at least once, and rounding costs
   0.01 of correlation instead of 0.18. So the rewrite that was being considered for the
   whole rubric is needed only at the top — a positively-phrased item has nowhere above
   `yes` to go, and that is where the resolution disappears. The cheaper fix is now worth
   trying first: keep the three levels and reword only their top, against the top two's
   134 translations where the failure is measurable. Experiment 12 is still the precedent
   — there, level wording moved the corpus mean by 15 points.
6. **Whether +0.90 says anything about the rubrics at all.** Two rubrics sharing nothing
   but an evaluator agree at +0.90 on the top two and +0.95 on this pair; a third rubric
   asked of the same evaluator would say whether that is a property of the rubrics or of
   Jev. If everything Jev is asked correlates at +0.90, the number is about the model, and
   neither rubric is being validated by it. Section 4.5 is a partial argument that it is
   not pure model artifact — the two rubrics disagree systematically on `bonsai2-27b`,
   where fifty independent properties cannot see that a translation has failed as a whole
   — but that is one direction of disagreement, not a test.
7. **Spread per unit of noise, measured rather than borrowed.** Section 4.6 finds the
   five-criterion scheme carrying 2–3× the spread per unit of its own run-to-run noise at
   every quality level, which is the sharpest form of section 3.7's recommendation — and
   it rests on 1.12 and 2.25, two figures measured in different experiments on different
   8-target sets. Three runs of both schemes over one target set would replace it with a
   measurement. At $0.09 per pair of 134 and the ranges already known to be small, this is
   the cheapest open question here, and it is the one the choice between the two schemes
   actually turns on.
8. **Whether `jev` separates the top of the corpus.** **Compared — [REPORT.md](REPORT.md)
   section 2:** `gemini-3.7-flash` and `ox-alpha` went through `trtools jev` with the rest
   of the corpus on 2026-09-22 ([JEV.md](../../examples/tr/onde/JEV.md)). Into two pairs,
   not within them: `gpt-5.6-luna` and `union-alpha` stay tied as under the old scheme, and
   are taken as even ([PORT.md](PORT.md) section 8 item 2). As written before that run:
   section 5.4's honest
   negative: the median moves from 93/92 to 88.0/87.2 on the top pair, so nothing yet says
   this scheme discriminates better where new models actually arrive. `gemini-3.7-flash` and
   `ox-alpha` are the other two of the corpus's top four and are not measured under `jev`.
   That is 134 evaluations, and it is the question a yardstick lives or dies on.
9. **A second source text.** Sections 5.1 and 5.3 both end at the same limit: everything
   the corpus knows is 67 translations of one document. Whether the fluency floor, the
   language difficulty ordering, and the per-model coverage counts survive a different
   genre is untested, and it is the largest unexamined assumption in the whole corpus —
   larger than anything about the evaluator. **Accepted as a choice:** the source is
   deliberately spoken in form and technical in content, which is hard to translate and
   chosen to make translators differ; the scores are not meant as a general-purpose
   measure ([PORT.md](PORT.md) section 8 item 4).
