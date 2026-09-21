# Experiment 11: 50 Yes/Partial/No Items Evaluation Scheme

## 1. Background & Motivation

`trtools eval` originally scored translations across five broad criteria worth 20 points each. Because the rubric provided no concrete anchors separating intermediate scores (e.g., distinguishing 14 from 17), scoring was left entirely to evaluator model discretion. This created three major structural problems:

### 1. Severe Run-to-Run Instability
On the *same* translation evaluated by the *same* model (`qwen3.6`) across three runs, scores swung drastically:

| Translator | Language | Old scores (3 runs) | Old range | Old median |
|---|---|---|---:|---:|
| gpt-5.6-terra | Polish | 69, 81, 15 | 66 | 69 |
| gpt-oss | Interlingua | 89, 73, 34 | 55 | 73 |
| qwen3.8 | Japanese | 56, 78, 25 | 53 | 56 |
| gemini-3.5-flash-lite | Kannada | 29, 61, 80 | 51 | 61 |
| ox-alpha | Irish | 38, 68, 89 | 51 | 68 |
| qwen3.6-27b | Korean | 92, 42, 77 | 50 | 77 |
| gemini-2.5-flash | Russian | 91, 44, 86 | 47 | 86 |
| gemini-3-flash | Hindi | 91, 81, 45 | 46 | 81 |

The mean range across runs was **52.4 points** (mean stdev 22.16). A translation could swing from acceptable to failure on a coin toss.

### 2. High Inter-Evaluator Divergence
When swapping evaluator models (`qwen3.6` vs `gpt-oss:120b`), scores on the same translations diverged by a mean absolute difference of **21.6 points** (mean 49.6 vs 69.5). The models observed the exact same errors, but `qwen3.6` penalized defects punitively while `gpt-oss:120b` gave generous credit for surviving meaning. Evaluator scores could not be compared across different models.

### 3. Artificial Score Cliffs
The old prompt contained hard penalties (e.g., guideline 1: *if missing/incomplete, assign 0 points to ALL criteria*). When triggered by minor truncation, a translation scored 0/100 despite enthusiastic rationales (e.g., "highly natural, idiomatic" Basque scoring 0/20). In another run, a schema artifact resulted in empty rationales being recorded as 0 beside 95 and 90. These cliffs measured prompt threshold artifacts rather than translation quality.

### What the Old Scheme Got Right
The three problems above are all failures of *resolution*: they appear when a single translation's single run is read as a number. Aggregated, the old scheme carried real signal. Over the full [examples/tr/onde/](../../examples/tr/onde/) corpus -- 16 translators x 67 languages x 3 runs, all evaluated by `qwen3.6` -- the mean-of-medians ranking is sound:

| Old score | Translator | Size (as recorded in the corpus README) |
|---:|---|---|
| 90.3 | gpt-5.6-luna | commercial |
| 90.1 | union-alpha | commercial |
| 87.5 | gemini-3.7-flash | commercial |
| 85.7 | ox-alpha | 320B-A18B (glm-5.3-flash stealth) |
| 81.6 | gemini-2.5-flash | commercial |
| 78.1 | gemini-3-flash | commercial |
| 77.7 | gpt-5.6-terra | commercial |
| 68.2 | gemma4 | 26B-A4B |
| 66.7 | gemma4-31b | |
| 66.1 | gemini-3.5-flash-lite | commercial |
| 65.1 | gpt-oss | |
| 63.6 | muse-glimmer | |
| 63.0 | qwen3.6-27b | |
| 58.3 | qwen3.6 | 35B-A3B |
| 54.0 | qwen3.8 | 27B |
| **27.9** | **bonsai2-27b** | **27B, ternary-quantized qwen3.8 (PTQ1_0)** |

- **Capability ordering is preserved**: frontier commercial models at the top, local models in the 54-68 band, and `ox-alpha` (320B-A18B) placing above every local model.
- **The ordering is reproducible, not a one-off.** Splitting the 67 languages at random into two halves and ranking the 16 translators independently from each half gives a median Spearman of **0.947** across 200 splits (minimum 0.874). Independent halves of the corpus recover the same ordering.
- **The decisive case is the last row.** `bonsai2-27b` is `qwen3.8` 27B under ternary quantization, and the old scheme separates it from its own full-precision parent by 26 points (54.0 -> 27.9). Paired by language, `bonsai2-27b` scores lower in **62 of 67 languages** (mean difference -26.1), so this is not a few languages dragging an average. A metric that cleanly detects a deliberate degradation of a known model is not producing noise.
- **Active-parameter effects show up too**: `qwen3.6` (35B-A3B, 3B active) scores below `qwen3.6-27b` (27B dense).
- **Resolution is coarse, though.** Bootstrapping over languages gives 95% intervals roughly 5-14 points wide (e.g. `gemma4` 68.2 [61.9, 74.7], `gemma4-31b` 66.7 [59.3, 73.6]), so adjacent models are not separated. The old scheme supports tiers, not a leaderboard.

So the old scheme's defect is variance at the single-translation level, not absence of signal. This matters for reading the rest of this document: the 8 targets below were selected precisely *because* their old scores were unstable ([targets.tsv](targets.tsv) ranks by 3-run range), so they are the corpus's worst case for the old scheme, and old-vs-new comparisons on them should not be generalized into a claim that the old scheme measured nothing.

### The Proposed 50-Item Scheme
This experiment replaces the 5 subjective 20-point scales with **50 concrete, narrow checklist items** grouped into five categories:

| Group | Category | Focus Areas |
|---|---|---|
| **A** | Structural integrity | Speaker labels, line correspondence, truncation, degenerate repetition |
| **B** | Language purity | Target language purity, contamination, script consistency, CoT/metadata leakage |
| **C** | Semantic fidelity | Propositional content, omissions, additions, numbers, polarity, anaphora |
| **D** | Terminology | Standard domain terms, consistency, technical notation, transliteration |
| **E** | Fluency & naturalness | Grammar, syntax, natural register, orthography, calques |

All items are positively phrased (`yes` = good) and scored under a single unified ternary rubric:
- `yes` (2 pts): Property holds throughout; zero instances of defect.
- `partial` (1 pt): Mostly holds, with minor isolated exceptions (roughly 1–3 lines).
- `no` (0 pts): Frequent or structural failure (roughly 4+ lines).

Total score maps directly to 0–100, nominally preserving compatibility with existing quality bands without arbitrary score cliffs. (Section 4 finds that the band labels do not in fact survive the change for every evaluator.) The full item definitions are in [items.py](items.py).

---

## 2. Experimental Setup

The experiment runs alongside `trtools` without modifying the core codebase:

- **Targets**: The 8 most unstable translations from [examples/tr/onde/](../../examples/tr/onde/), selected across 8 translation models and distinct language families ([targets.tsv](targets.tsv)).
- **Evaluators**: three local models (`qwen3.6`, `gemma4:31b`, `gpt-oss:120b`, all via Ollama) and two commercial API models (`gpt-5.6-terra`, `gpt-5.6-luna`), 3 runs each = 120 evaluations per variant. The commercial pair was added to test whether the checklist's stability and agreement hold outside the local model family, and to get a reference point from models that are not themselves among the weaker translators being judged.
- **Variants Tested**:
  1. `evals/`: Baseline (Thinking ON, Evidence ON).
  2. `evals-nt/`: No-Think (Thinking OFF, Evidence OFF) — tests latency and whether explicit CoT is required.
  3. `evals-ne/`: No-Evidence (Thinking ON, Evidence OFF) — isolates the effect of writing citation evidence.
- **Modularity**: [eval50.py](eval50.py) supports `--split` (`none`, `group`, `item`) to evaluate all items in one prompt or step them down into smaller calls.
- **Adding evaluators**: [eval50.py](eval50.py) runs one evaluator (`-m/--model`, `-s/--slug`) under one condition (`--no-think`, `--no-evidence`) over [targets.tsv](targets.tsv). [batch.sh](batch.sh) is a thin loop over the evaluators (`EVALUATORS` plus `EVAL_ORDER`, which fixes the run order the associative array does not preserve) and all three variants. A further evaluator can also be added by invoking `eval50.py` directly, without touching `batch.sh` or waiting for it to finish.

---

## 3. Current Results

Detailed tables and per-item breakdowns are recorded in [SCORES.md](SCORES.md) (generated by [agg50.py](agg50.py)); the variant comparison against a reference evaluator that Discussion 5 draws on is in [VARIANTS.md](VARIANTS.md) (generated by [refcmp.py](refcmp.py)). All 120 calls in each of `evals/`, `evals-nt/`, and `evals-ne/` completed without schema failures.

### 1. Run-to-Run Wobble Radically Narrowed
Under the new scheme, score variation across runs collapsed dramatically across all targets:

| Translator | Language | New scores (`qwen3.6`, 3 runs) | New range | Range change vs Old |
|---|---|---|---:|---:|
| gpt-5.6-terra | Polish | 87, 72, 69 | 18 | -48 |
| gpt-oss | Interlingua | 80, 89, 80 | 9 | -46 |
| qwen3.8 | Japanese | 86, 89, 84 | 5 | -48 |
| gemini-3.5-flash-lite | Kannada | 81, 79, 95 | 16 | -35 |
| ox-alpha | Irish | 85, 92, 89 | 7 | -44 |
| qwen3.6-27b | Korean | 84, 93, 100 | 16 | -34 |
| gemini-2.5-flash | Russian | 96, 100, 95 | 5 | -42 |
| gemini-3-flash | Hindi | 97, 98, 98 | 1 | -45 |

- Under `qwen3.6`, mean range dropped from **52.4 to 9.6 points** (mean stdev 22.16 -> 4.17).
- Across all five evaluators, the average run-to-run range was **8.6 points** (mean stdev 3.72).
- Every single translation stabilized significantly; none regressed.
- **The commercial models are among the steadiest**: mean run-to-run range 7.1 (`gpt-5.6-terra`) and 8.2 (`gpt-5.6-luna`), against 6.8 (`gemma4:31b`), 9.6 (`qwen3.6`) and 11.1 (`gpt-oss:120b`). Stability under the checklist is therefore not an artifact of the local model family.

*Caveat: stability is not by itself validity.* Part of this collapse is the checklist doing its job, but part of it is the positively-phrased items supplying a `yes` default where the old rubric supplied nothing. An evaluator that cannot detect defects in a given target now returns a stable near-ceiling score instead of a noisy low one. Interlingua and Irish are the clearest cases: their old 3-run ranges were 55 and 51, and their new ranges under the local evaluators are 6-9 and 2-7 -- but the resulting scores (84-98) contradict both the commercial evaluators and the old scheme's own corpus-level ranking of those languages. See "The Local Evaluators Are Miscalibrated" below.

### 2. Inter-Evaluator Agreement Improved Locally, but Splits by Model Family
Comparing median scores across the five evaluators (local three first, commercial two after):

| Translator | Language | Old (`qwen3.6`) | `gemma4:31b` | `gpt-oss:120b` | `qwen3.6` | `gpt-5.6-luna` | `gpt-5.6-terra` | New Evaluator Spread |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-terra | Polish | 69 | 70 | 92 | 74 | 78 | 79 | 22 |
| gpt-oss | Interlingua | 73 | 94 | 88 | 84 | 56 | 50 | 44 |
| qwen3.8 | Japanese | 56 | 92 | 96 | 88 | 70 | 69 | 27 |
| gemini-3.5-flash-lite | Kannada | 61 | 89 | 49 | 87 | 65 | 71 | 40 |
| ox-alpha | Irish | 68 | 96 | 98 | 89 | 64 | 61 | 37 |
| qwen3.6-27b | Korean | 77 | 84 | 94 | 94 | 81 | 69 | 25 |
| gemini-2.5-flash | Russian | 85 | 98 | 98 | 97 | 93 | 93 | 5 |
| gemini-3-flash | Hindi | 81 | 98 | 92 | 98 | 92 | 81 | 17 |

- **Agreement is tight inside each family, not across them**: the local three land within 1.7 points of each other (`gemma4:31b` 90.1, `qwen3.6` 88.9, `gpt-oss:120b` 88.4) and the commercial two within 3.3 (`gpt-5.6-luna` 74.9, `gpt-5.6-terra` 71.6, mean absolute per-target difference 5.0). The two clusters sit **13–19 points apart**.
- **Spread widened once the families were mixed**: mean evaluator spread rose from 13.25 (local three) to **27.1** points, and only 1 of 8 targets (Russian, spread 5) still fits within 10 points. The checklist stabilized *runs*, not the choice of evaluator.
- **The gap concentrates in group E (fluency & naturalness)**, not across the board. Mean group subtotals (out of 20): E is 18.8/18.8/17.9 for `gemma4:31b`/`qwen3.6`/`gpt-oss:120b` against **12.4/12.2** for `gpt-5.6-luna`/`gpt-5.6-terra`; groups A and D differ by 1–4 points. The commercial models are reading naturalness defects the local models score as clean.
- **The widest disagreements are on Interlingua and Irish** (spread 44 and 37): `gemma4:31b` and `gpt-oss:120b` score them 88–98 while the commercial pair scores 50–64, again mostly through group E (E=20 local vs E=4–7 commercial). Constructed and low-resource targets are where "local evaluators see nothing wrong" is most visible.
- **Ceiling effect resolved for `gpt-oss:120b`**: In the old scheme, `gpt-oss:120b` never scored above 84. Under the 50-item checklist, it reached 96–98 when warranted — though the next section shows some of that headroom is misplaced.
- **The split is a difference in accuracy, not just in scale.** The next section checks one item against ground truth and finds the commercial pair exact and the local three wrong on half the targets.
- **No visible self-preference**: `gpt-5.6-terra` scoring its own Polish translation gave 79, between `qwen3.6`'s 74 and `gpt-oss:120b`'s 92, and one point above `gpt-5.6-luna`'s 78. That is a single data point, so it rules nothing out, but nothing in this run looks like self-favoring.

### 3. Which Family Is Right: A Ground-Truth Calibration Check

The 13–19 point offset raises the obvious question of which family is closer to correct. One item admits an objective answer. `a01_speaker_label_present` can be settled by counting: the source has speaker labels on all 99 lines, and the rubric's bands are mechanical (`yes` = 0 unlabeled lines, `partial` = 1–3, `no` = 4+). Counting unlabeled lines in each translation gives the reference column below, and each evaluator's median-of-3 verdict can be scored against it:

| | pl | ia | ja | kn | ga | ko | ru | hi | Exact | Bias |
|---|---|---|---|---|---|---|---|---|---:|---:|
| **Unlabeled lines** | 2 | 13 | 0 | 0 | 1 | 0 | 15 | 5 | | |
| **Correct verdict** | partial | no | yes | yes | partial | yes | no | no | | |
| `gemma4:31b` | *yes* | *yes* | yes | yes | *yes* | yes | no | no | 5/8 | **+0.50** |
| `gpt-oss:120b` | *yes* | no | yes | yes | *no* | yes | *partial* | *yes* | 4/8 | **+0.38** |
| `qwen3.6` | *no* | no | *no* | yes | partial | yes | no | *partial* | 5/8 | -0.25 |
| `gpt-5.6-luna` | partial | no | yes | yes | partial | yes | no | no | **8/8** | 0.00 |
| `gpt-5.6-terra` | partial | no | yes | yes | partial | yes | no | no | **8/8** | 0.00 |

*(Italics mark incorrect verdicts. Bias is the mean signed error with `yes`=2, `partial`=1, `no`=0; positive means scoring higher than the count warrants.)*

- **Both commercial evaluators are exactly right on all 8 targets; the local three are right on 4–5.** On this item the offset is not a difference of scale but a difference of accuracy, and it runs in the local evaluators' disfavor.
- **`gemma4:31b` and `gpt-oss:120b` err leniently** (+0.50, +0.38). `gemma4:31b` rated `gpt-oss / ia` as `yes` with 13 lines unlabeled.
- **`qwen3.6` errs in both directions.** Its -0.25 bias looks strict, but the underlying mistakes are `no` verdicts on `ja` and `pl`, whose labels are complete or near-complete: hallucinated defects, not severity. Local inaccuracy is not uniformly leniency.

The mechanism shows up in the raw verdict distribution over all 1,200 verdicts per evaluator in `evals/` (8 targets × 3 runs × 50 items):

| Evaluator | `yes` | `partial` | `no` | Evidence field filled |
|---|---:|---:|---:|---:|
| `gemma4:31b` | 88.2% | **2.2%** | 9.6% | 12.1% |
| `qwen3.6` | 84.1% | **8.3%** | 7.6% | 15.9% |
| `gpt-oss:120b` | 83.6% | **5.4%** | 11.0% | 15.7% |
| `gpt-5.6-luna` | 60.4% | **25.0%** | 14.6% | 39.9% |
| `gpt-5.6-terra` | 59.8% | **23.2%** | 17.0% | 40.2% |

- **The gap is entirely in the `partial` band.** `no` rates are comparable across families (7.6–17.0%); what separates them is that the local models resolve the 1–3 line band to `yes` and the commercial models actually use it. `gemma4:31b` is effectively binary, using `partial` on 2.2% of verdicts.
- **A worked example**: `gemini-2.5-flash / ru` drops the speaker label on 15 of 99 lines, all of them Camille's. The commercial evaluators return `no` on both `a01_speaker_label_present` and `a03_speaker_attribution` in all three runs. The local three all get `a01` right, then miss `a03`: `gemma4:31b` and `gpt-oss:120b` return `yes` in two runs of three (median `yes`) and `qwen3.6` lands on a median of `partial`. They hand the translation a median total of 97–98. A transcript where 15% of turns have no attributable speaker is not a 98.

*Caveat: this is one item of fifty, with n=8. It establishes that the local evaluators are miscalibrated on a mechanically checkable structural item; it does not by itself prove the whole 13–19 point offset is theirs, since the bulk of that offset sits in group E, where no comparable ground truth is available.*

### 4. Thinking Off (`evals-nt/`): High Speedup, Evaluator-Dependent Cost

| Evaluator | Mean Score (think) | Mean Score (no-think) | Call Time (think) | Call Time (no-think) | Run Range (think -> no-think) |
|---|---:|---:|---:|---:|---:|
| `qwen3.6` | 88.9 | 74.0 | 245s | 23s | 9.6 -> 13.6 |
| `gemma4:31b` | 90.1 | 89.8 | 798s | 110s | 6.8 -> 2.8 |
| `gpt-oss:120b`* | 88.4 | 87.9 | 160s | 160s | 11.1 -> 12.5 |
| `gpt-5.6-luna` | 74.9 | 73.1 | 42s | 43s | 8.2 -> 6.1 |
| `gpt-5.6-terra` | 71.6 | 71.5 | 43s | 39s | 7.1 -> 4.9 |

*\*Note: `gpt-oss:120b` ignores Ollama's `--no-think` flag and continues to emit internal reasoning; its row acts as a thinking-on / evidence-off control.*

- **`qwen3.6` requires thinking**: Dropping thinking caused a severe **14.9-point drop** in mean score and increased noise (range widened to 13.6). The 10x speedup came at the expense of evaluation validity. (This reading assumes the thinking-on score was the valid one. Discussion 5 re-examines it against a reference evaluator and reaches the opposite conclusion.)
- **`gemma4:31b` succeeds without thinking**: Mean score barely shifted (-0.4 points), run-to-run stability improved (6.8 -> 2.8), and call duration dropped by **~7x (798s -> 110s)**. For `gemma4:31b`, thinking can be safely disabled to achieve high throughput.
- **The commercial models are insensitive to the flag, in both score and time**: scores moved -1.8 and -0.1, within run-to-run noise, and call duration barely changed (42s -> 43s, 43s -> 39s). Their reasoning effort is set server-side, so `--no-think` is not the same lever it is on Ollama; these rows behave like the `gpt-oss:120b` control rather than a real no-think condition.
- **Throughput is where the commercial models dominate**: at 39–43s per call under every variant, they are 3–4x faster than `qwen3.6` with thinking and ~20x faster than `gemma4:31b`, with the steadiest run-to-run ranges of the five.

### 5. Evidence On vs Off (`evals-ne/`): Isolating What Thinking vs Evidence Each Cost

`evals-nt/` turned thinking and evidence off together, so `qwen3.6`'s 14.9-point drop there couldn't be attributed to either one alone. `evals-ne/` reruns the same targets and evaluators with thinking left ON and only `--no-evidence` set, isolating the evidence half:

| Evaluator | Mean score (evidence on) | Mean score (no evidence) | Score diff | Time (evidence on) | Time (no evidence) | Time diff |
|---|---:|---:|---:|---:|---:|---:|
| `qwen3.6` | 88.9 | 90.1 | +1.2 | 245s | 156s | -36% |
| `gemma4:31b` | 90.1 | 94.5 | +4.4 | 798s | 382s | -52% |
| `gpt-oss:120b`* | 88.4 | 87.3 | -1.1 | 160s | 124s | -23% |
| `gpt-5.6-luna` | 74.9 | 73.4 | -1.5 | 42s | 39s | -8% |
| `gpt-5.6-terra` | 71.6 | 69.8 | -1.9 | 43s | 34s | -21% |

*\*`gpt-oss:120b` ignores `--no-think` (see above), so its `evals-nt` and `evals-ne` rows are both thinking-on/evidence-off in practice. They land within a point of each other (87.9 vs 87.3, 160s vs 124s), which is the control this experiment was designed to provide: it confirms the model really is ignoring the flag rather than something else differing between the two variants.*

- **The `qwen3.6` drop is thinking's, not evidence's.** Removing evidence alone left `qwen3.6`'s mean score essentially unchanged (+1.2, within run-to-run noise) while removing thinking (`evals-nt`) cost 14.9 points. The two conditions `evals-nt` conflates now separate cleanly: thinking is what `qwen3.6` needs, not the evidence field.
- **Evidence removal buys real speed on its own.** Dropping evidence alone cut call time by 8-52% depending on evaluator, well short of the 7-10x from dropping thinking too, but a meaningful gain by itself, especially for `gemma4:31b` (798s -> 382s). The commercial models gain least in relative terms because they were already fast.
- **The commercial evaluators barely move either way.** Scores shifted -1.5 and -1.9, inside their run-to-run range; combined with the no-think result, neither knob changes what they report. Their 13-19 point offset from the local evaluators survives all three variants, so it is a property of how they read the rubric, not of the prompt configuration.
- **`gemma4:31b` scores slightly higher without evidence** (+4.4), the opposite direction from what padding-driven degradation would predict. Combined with `evals-nt` leaving its score flat (-0.4), this suggests evidence and no-thinking partially offset each other for this model rather than evidence being purely a tax on the verdict.
- **Verdicts move more than totals suggest.** Comparing per-item medians against `evals/`, a mean of 4.6-8.8 items (of 50) flipped verdict per combination (max 15), with the commercial evaluators moving the most (8.8 and 8.4) despite their totals being the most stable. Across all 40 combinations, 48/50 items moved at least once, including the two documented bad citations from the discussion below (`a01_speaker_label_present`: 7/40 combinations moved; `d01_standard_terms`: 6/40). Totals stayed close because these moves went in both directions and largely cancelled, not because the items were unaffected.

---

## 4. Discussion & Caveats

### 1. Dilution of Catastrophic Defects
In the 50-item additive scheme, a severe local failure is heavily diluted. For example, in a 99-line Kannada translation where 2 lines contain corrupted, mixed-script characters (Arabic/Odia), the matching item (`b05_script_consistency`) receives `partial` (costing 1 point out of 2). The remaining 99 points remain intact, giving an overall score of 99/100.
The old scheme harshly penalized the entire document for such corruption (scoring 26/100). The new scheme measures *average per-property adherence*, not *worst-case deployment reliability*.

### 2. Discrepancies in Inspection Scrutiny
In `gemini-3.5-flash-lite / Kannada`, `gpt-oss:120b` scored 49 while `qwen3.6` and `gemma4:31b` scored 87–89. Inspection of the rationales revealed that `gpt-oss:120b` performed meticulous line-level auditing (catching dropped sentences, trailing clauses, and line desynchronization), whereas the other two models evaluated holistic impressions. Concrete rubrics do not eliminate differences in how deeply an evaluator inspects the text. Note that depth of inspection is item-specific rather than a property of the model: the same `gpt-oss:120b` that audited Kannada line by line is the second most lenient evaluator on `a01_speaker_label_present` (see "Which Family Is Right").

### 3. Unreliable Evidence Line Numbers
Because prompts provide plain text without line numbers, models frequently hallucinated line references in the `evidence` field (e.g. citing lines 15 and 64 when real defects were on lines 15, 20, 72, 78, 90). `evals-ne/` (see "Evidence On vs Off" above) shows producing evidence is neither clearly harmful nor clearly beneficial to the verdict: dropping it left aggregate scores close to unchanged (within +/-4.4 points) while still moving several item-level verdicts per combination in both directions. The unreliable citations look like a harmless side output rather than something dragging scores down, but the underlying instability they're a symptom of (see "Where the remaining wobble sits") is unresolved either way.

### 4. The Local Evaluators Are Miscalibrated, Not Merely Milder
The two `gpt-5.6` evaluators are internally consistent (run-to-run range 7.1-8.2, agreeing with each other within 5.0 points on average) yet sit 13-19 points below the local three on the same translations, in every variant. The ground-truth check in "Which Family Is Right" above resolves the direction of that gap on the one item where it can be resolved: on `a01_speaker_label_present`, where the correct verdict follows from counting unlabeled lines, the commercial pair is exact on all 8 targets and the local three are exact on 4-5, with `gemma4:31b` and `gpt-oss:120b` erring leniently. The local evaluators are not applying a gentler scale to the same observations; they are missing the observations.

Two properties of the local verdicts explain how:

- **The `partial` band is unused.** `gemma4:31b` assigns `partial` on 2.2% of verdicts and `qwen3.6` on 8.3%, against 23-25% for the commercial pair, while `no` rates are comparable across families. The rubric's middle band exists precisely for the 1-3 line defects that dominate a mature translation, and the local models collapse it into `yes`. Because this applies uniformly across all 50 items, the resulting inflation is broad rather than concentrated, which is why it reads as a scale offset.
- **Ceiling verdicts on languages the evaluator models poorly.** The gap is concentrated in group E, where the local models award 17.9-18.8 of 20 on targets like Interlingua and Irish that the commercial models rate 4-7. A model asked to judge naturalness in a language it barely represents has little to go on and defaults to `yes`. The near-ceiling E subtotals across every target are consistent with that, and group E has no ground truth to check it against.

The old scheme provides an independent check on the second point, and it lands against the local evaluators. Under the old 5x20 rubric, the same `qwen3.6` ranked Interlingua 64th and Irish **last** of 67 languages, averaged over all 16 translators in the corpus:

| Language | Old scheme (`qwen3.6`, corpus mean, rank of 67) | New scheme, local three | New scheme, commercial two |
|---|---|---:|---:|
| ja | 85.6 (9th) | 88-96 | 69-70 |
| ru | 85.2 (10th) | 97-98 | 93 |
| pl | 83.7 (15th) | 70-92 | 78-79 |
| ko | 75.9 (25th) | 84-94 | 69-81 |
| hi | 70.4 (32nd) | 92-98 | 81-92 |
| kn | 58.2 (54th) | 49-89 | 65-71 |
| **ia** | **47.2 (64th)** | **84-94** | **50-56** |
| **ga** | **37.8 (67th)** | **89-98** | **61-64** |

*(Corpus figures are per-language means over 16 translators; new-scheme figures are the 8 single targets from this experiment, so the columns are not directly comparable in level. The ordering is the point.)*

On Interlingua and Irish the commercial evaluators land near where the old scheme put those languages, while the new scheme's local evaluators moved them to near-ceiling. The same evaluator model, `qwen3.6`, went from rating Irish worst-of-67 to scoring it 89.

This suggests the rubric change did more than stabilize `qwen3.6` -- **it changed the direction in which evaluator ignorance is expressed.** The old free-form rubric gave a model with no command of the target language nothing to anchor on, producing low and wildly variable scores (Interlingua's 3-run range on this experiment's target was 55, Irish's 51). The 50-item checklist supplies a default instead: every item is positively phrased, so an undetected defect is silently scored `yes`. Ignorance that used to surface as noise now surfaces as a stable high score, which is harder to notice and worse to act on.

`qwen3.6` is a separate failure of the same kind. Its mean signed error on `a01` is -0.25, which looks strict, but the errors are `no` verdicts on `ja` and `pl`, whose speaker labels are complete or near-complete. It invents defects where the lenient models miss them. Both are inaccuracy; only one direction inflates the total.

The practical consequences:

- **Scores remain comparable only within an evaluator family.** Mixing families into one leaderboard would rank translations by which evaluator happened to run them.
- **A near-ceiling local score should not be read as near-perfect.** `gemini-2.5-flash / ru` scores 97-98 from all three local evaluators while dropping the speaker label on 15 of 99 lines. The band labels inherited from the old scheme do not survive this evaluator, whatever they mean elsewhere.
- **The evidence-fill rate is a cheap miscalibration signal.** The local evaluators fill the `evidence` field on 12-16% of verdicts against 40% for the commercial pair. An evaluator that finds almost nothing to cite while scoring in the high 90s is worth distrusting before its number is used.


### 5. Which Variant to Run, Taking `gpt-5.6-terra` as Reference

Sections 3.4 and 3.5 report each variant on its own terms -- what it costs, how far it moves each evaluator's score -- but that cannot decide which variant to run. A variant that makes an evaluator steadier can equally be making it steadily wrong, and a score that barely moves says nothing about whether it was right to begin with.

This section settles the question under one explicit assumption: that `gpt-5.6-terra` is the closest thing available to correct. Discussion 4 is what earns it that role -- exact on all 8 targets of the one mechanically checkable item, using the `partial` band the local evaluators collapse, and tracking the old scheme's corpus ordering. The assumption is still an assumption, so every claim below is re-checked against `gpt-5.6-luna` as reference at the end. Figures are from [VARIANTS.md](VARIANTS.md) (generated by [refcmp.py](refcmp.py)), which also re-runs the whole report under `--reference`.

**The reference itself barely moves, so the comparison is well-posed.**

| | `evals` | `evals-nt` | `evals-ne` |
|---|---:|---:|---:|
| `gpt-5.6-terra` mean score | 71.6 | 71.5 | 69.8 |
| Run-to-run range | 7.1 | **4.9** | 7.1 |
| Call time | 43s | 39s | **34s** |
| `partial` share | 23.2% | 26.8% | 27.8% |

Its per-item medians do churn between variants (15.0% of 400 differ between `evals` and `evals-nt`), but the level, the ordering of targets and the use of the `partial` band survive all three. For the commercial family the variant is therefore close to a free choice, and `evals-nt` is the cheapest steady one.

**For the local evaluators the variant matters enormously, and `evals-nt` is the only one that helps.** Distance from the reference, same variant on both sides:

| Evaluator | Variant | Mean | MAD | Kendall | Recall | Precision | Item agreement |
|---|---|---:|---:|---:|---:|---:|---:|
| `gpt-5.6-luna` | `evals` | 74.9 | 5.0 | 0.78 | 81.1% | 86.0% | 80.5% |
| `gpt-5.6-luna` | `evals-nt` | 73.1 | 6.1 | 0.63 | 81.1% | 87.3% | 80.5% |
| `gpt-5.6-luna` | `evals-ne` | 73.4 | 6.9 | 0.36 | 82.5% | 86.9% | 81.2% |
| `qwen3.6` | `evals` | 88.9 | 18.5 | 0.26 | 35.8% | 90.5% | 65.5% |
| `qwen3.6` | **`evals-nt`** | **74.0** | **8.0** | **0.50** | **66.9%** | 72.9% | 66.2% |
| `qwen3.6` | `evals-ne` | 90.1 | 20.4 | 0.29 | 35.6% | 88.7% | 62.3% |
| `gpt-oss:120b` | `evals` | 88.4 | 22.2 | 0.04 | 22.6% | 63.2% | 61.8% |
| `gpt-oss:120b` | `evals-nt` | 87.9 | 19.9 | 0.56 | 30.2% | 69.9% | 61.0% |
| `gpt-oss:120b` | `evals-ne` | 87.2 | 24.2 | 0.33 | 27.1% | 73.8% | 56.8% |
| `gemma4:31b` | `evals` | 90.1 | 20.8 | 0.08 | 23.3% | 84.1% | 63.5% |
| `gemma4:31b` | `evals-nt` | 89.8 | 18.5 | 0.14 | 26.0% | 88.0% | 61.0% |
| `gemma4:31b` | `evals-ne` | 94.5 | 24.8 | 0.15 | **12.4%** | 91.7% | 58.2% |

*(Recall and precision are over the reference's non-yes item medians: recall is the share of the reference's defects the evaluator also reports, precision the share of its own reports the reference shares.)*

- **`qwen3.6` without thinking is a different evaluator, and a much better one.** Its mean lands on the reference (74.0 against 71.5), its detection of the reference's defects nearly doubles (35.8% -> 66.9%), the `partial` band goes from unused to used (8.3% -> 21.8%), and group E drops from 18.8/20 to 13.9 against the reference's 11.1 -- the near-ceiling naturalness verdicts Discussion 4 identifies as the local failure mode are largely gone. Against the old scheme's corpus mean, an independent reference, its correlation recovers from 0.07 to 0.67 (Pearson). It also costs 23s per call against 245s.
- **This reverses section 3.4's reading.** That section recorded the 14.9-point drop as a loss of validity. Against the reference it is a correction: thinking is what lets `qwen3.6` talk itself into a `yes`.
- **The gain is in detection, not only in level.** Item agreement with the reference stays flat (65.5% -> 66.2%), so `evals-nt` is not reproducing the reference verdict by verdict. What changes is that it stops missing defects, at the price of precision (90.5% -> 72.9%; false alarms 6 -> 42). It trades a silent miss for a noisy report, which is the better direction under a scheme that scores every miss as `yes`, but it is not accuracy.
- **`a01` does not improve.** `qwen3.6` is exact on 5/8 under both variants; its bias merely flips from -0.25 to +0.50. On the one item with ground truth, `evals-nt` buys nothing, which bounds how far the recall gain should be read.
- **`evals-ne` is the worst variant for every local evaluator.** Removing evidence while leaving thinking on inflates all three (`qwen3.6` 90.1, `gemma4:31b` 94.5) and drives `gemma4:31b`'s detection down to 12.4% with a 1.2% `partial` rate. Its ~50% speedup is a fraction of what `evals-nt` gives. Nothing in this comparison argues for running it.
- **`gemma4:31b` is not rescued by any variant** (recall 23-26%, Kendall 0.08-0.15). Section 3.4's "succeeds without thinking" holds only in the sense that its score does not move; it does not start seeing defects.
- **`gpt-oss:120b` improves modestly under `evals-nt`** (Kendall 0.04 -> 0.56, recall 22.6% -> 30.2%) at no change in cost, since it ignores the flag. What it responds to is the evidence field being dropped, not thinking.

**Robustness.** Re-running with `gpt-5.6-luna` as reference gives the same verdict, slightly stronger: `qwen3.6` under `evals-nt` reaches MAD 5.4, Kendall 0.78 and 70.1% recall, against 15.0 / 0.50 / 36.0% under `evals`. The two commercial evaluators are 80.5% in item-level agreement with each other, so this is not an independent confirmation; it does establish that the conclusion is not an artifact of which of the two was picked.

**What this does not establish.** n=8, one item of fifty has ground truth, and the reference is assumed rather than verified. If `gpt-5.6-terra` is itself systematically harsh -- Discussion 4 can only rule that out on `a01` -- then `evals-nt` is selected here for agreeing with a harsh evaluator, and `qwen3.6`'s extra 42 false alarms are the honest reading of what it does without thinking. Future Work 4 is what would settle it.

**Practical upshot**: run `evals-nt` (`--no-think --no-evidence`) for every evaluator. It is the cheapest variant for all five, it costs the commercial evaluators nothing measurable, it is the only variant under which a local evaluator approaches the reference, and the evidence field it drops was producing hallucinated line numbers anyway (Discussion 3). `evals` remains the variant to use when the evidence text is wanted for inspection rather than for scoring.

### 6. Provisional Position

Two findings from the comparison against the old scheme are stable enough to record, with their scope stated. Both are provisional: Future Work 3 and 6 could overturn either by showing the local failures are a rubric defect rather than a capability limit.

**1. The old scheme carried real signal about translator capability, at corpus scale.** Over 16 translators x 67 languages x 3 runs (all evaluated by `qwen3.6`), the ranking is reproducible from independent halves of the language set (split-half Spearman 0.947) and separates a ternary-quantized model from its own full-precision parent in 62 of 67 languages. Scope: this holds for *tiers*, not fine ranking -- bootstrap intervals over languages are 5-14 points wide and adjacent models overlap. It also says nothing about single translations, which is where the old scheme's documented instability lives and why this experiment exists.

**2. The commercial evaluators track the old scheme's ordering; the local three do not.** Score *level* is not the criterion here -- the two schemes need not share a range, only a trend -- so the comparison is by rank, against two references. The first is this experiment's 8 old 3-run medians; the second is the old scheme's per-language corpus mean over 16 translators, which is the better-verified reference (split-half Spearman 0.947, per finding 1).

Against the 8 old 3-run medians:

| Evaluator | Pearson | Spearman | Kendall | Concordant/discordant pairs (of 28) |
|---|---:|---:|---:|---|
| `gpt-5.6-luna` | 0.67 | 0.67 | **0.50** | 21/7 |
| `qwen3.6` | 0.54 | 0.60 | 0.43 | 20/8 |
| `gpt-5.6-terra` | 0.44 | 0.55 | 0.41 | 19/8 |
| `gemma4:31b` | 0.26 | 0.45 | 0.33 | 18/9 |
| `gpt-oss:120b` | 0.40 | 0.26 | 0.15 | 15/11 |

Against the old per-language corpus mean (the verified reference):

| Evaluator | Pearson | Spearman | Kendall | Concordant/discordant pairs (of 28) |
|---|---:|---:|---:|---|
| `gpt-5.6-terra` | **0.72** | 0.50 | 0.41 | 19/8 |
| `gpt-5.6-luna` | 0.68 | **0.64** | **0.43** | 20/8 |
| `gpt-oss:120b` | 0.25 | 0.36 | 0.31 | 17/9 |
| `qwen3.6` | 0.07 | 0.12 | 0.07 | 15/13 |
| `gemma4:31b` | **-0.35** | **-0.19** | **-0.19** | 11/16 |

- **Both commercial evaluators track both references** (Kendall 0.41-0.50 and 0.41-0.43). They are equivalent to each other on trend, so neither is "closest to the old scheme"; the split is between families, not between `gpt-5.6-terra` and `gpt-5.6-luna`.
- **`qwen3.6` collapses when the reference is changed** (Kendall 0.43 -> 0.07). Its apparent agreement with the 8 old medians does not reflect the language-difficulty trend the old scheme established over the whole corpus.
- **`gemma4:31b` is negatively correlated** with the verified reference (-0.19): it scores highest on the languages the old scheme ranked hardest. This is the same Interlingua/Irish inflation documented in Discussion 4, measured against an independent reference.

Scope: n=8, where Spearman needs about 0.71 and Kendall about 0.57 for p<0.05, so **no individual correlation here is significant**; these are comparisons among evaluators on a shared sample, not established effect sizes. The 8 targets also use 8 different translators, so language difficulty is confounded with translation quality -- the confound is identical for all five evaluators, which is what keeps the comparison fair but not what would make any single row meaningful.

*(Separately, and not as a criterion: `gpt-5.6-terra`'s mean over these 8 targets is 71.6 against the old scheme's 71.2, a bias of +0.4, where the local three run +17.1 to +18.9. The level match is mechanically coincidental -- the old scheme's low scores come from score cliffs (Background 3), `gpt-5.6-terra`'s from systematic use of the `partial` band -- and it is not what finding 2 rests on.)*

**What this does not establish.** It is tempting to read the two together as "the 50-item scheme requires a commercial evaluator of this class." The data does not support that as stated, for three reasons:

- **Scale does not predict accuracy within the local set.** `gpt-oss:120b` (116.8B total, MoE 128/4, MXFP4) is the largest local evaluator and the least accurate on `a01` (4/8); `gemma4:31b` (31.3B dense, by far the most active parameters of the three) is the most lenient (+0.50). A capability floor should produce some ordering by scale, and none appears.
- **The old scheme worked with a local evaluator.** The corpus ranking above, including the quantization detection, was produced entirely by `qwen3.6`. Local models can evaluate translation quality in aggregate; what fails is this particular rubric.
- **The commercial side is n=2 from one family.** `gpt-5.6-terra` and `gpt-5.6-luna` agree on 80.5% of item verdicts. No commercial model outside the `gpt-5.6` family has been run as an evaluator, so no class threshold has been located.

A sharper statement of what changed: the old rubric asked for an overall judgment, which averages over an evaluator's blind spots; the 50-item checklist asks for 50 independent detections and scores every miss as `yes`, which accumulates them in one direction. The burden moved from judgment to detection, and the averaging that rescued the old scheme is gone.

**Cheapest decisive test.** Run `bonsai2-27b` and `qwen3.8` over all 67 languages under the new scheme with `qwen3.6` as evaluator -- 134 calls, no commercial API, roughly an hour at the measured 23s per no-think call (Discussion 5 selects that variant for `qwen3.6`; the thinking-on variant would take about 9 hours at 245s). If the new scheme plus a local evaluator cannot reproduce the 26-point separation the old scheme found, "new scheme + local" is unusable even in aggregate, and the question above is settled without paying for a 67-language commercial run.

---

## 5. Future Work & Next Steps

1. **Implement Catastrophic Failure Gating**:
   - Introduce pre-screening hard gates (e.g. script corruption, line count mismatches, severe truncation) that cap or reject translations before checklist tallying.
2. **Line-Numbered Evaluation Prompts**:
   - Provide line-indexed text to the evaluator to verify if citation accuracy improves and whether it stabilizes verdicts for items with line-count thresholds.
3. **Fix the Local Evaluators' `partial` Band**:
   - The ground-truth check localizes the problem to the unused 1-3 line middle band. Give the rubric explicit counted anchors (e.g. "state the number of offending lines, then map 0 / 1-3 / 4+ to the verdict") and re-run `gemma4:31b` and `qwen3.6` to see whether `partial` usage and `a01` accuracy both move. Start from `--no-think`, not `evals/`: Discussion 5 finds that is already where `qwen3.6` uses the band, so the anchors have to improve on that, not on the thinking-on baseline.
4. **Extend Ground Truth Beyond `a01`**:
   - Several more items are mechanically checkable against the source (`a04_body_present`, `a05_line_correspondence`, `a07_no_duplication`, `c04_numeric_accuracy`, `b06_encoding_integrity`). Scoring evaluators against a computed reference on all of them would turn the single-item calibration check into a real accuracy benchmark, and would test whether the commercial pair's 8/8 generalizes.
5. **Adjudicate Group E on Interlingua and Irish**:
   - Group E holds most of the 13-19 point offset and admits no automatic ground truth. These two languages are where the old scheme (corpus ranks 64/67 and 67/67) and the commercial evaluators agree against the local ones, so hand-adjudicating them decides whether the local near-ceiling subtotals are the same failure `a01` exposes.
6. **Reconsider the Uniform `yes` Default**:
   - Every item is positively phrased, so an evaluator that cannot inspect a property scores it `yes`. That converts ignorance into a stable high score rather than visible noise. Options worth testing: an explicit `unable_to_assess` verdict excluded from the denominator, or requiring evidence to *support* a `yes` on items where the old scheme and the checklist disagree most.
7. **Run the Quantization Separation Test**:
   - Evaluate `bonsai2-27b` and `qwen3.8` over all 67 languages under the new scheme with `qwen3.6` as evaluator (134 calls, local only), under `--no-think --no-evidence` per Discussion 5. The old scheme separated them by 26 points in 62 of 67 languages; whether the new scheme plus a local evaluator reproduces that decides if "new scheme + local" is usable in aggregate. See "Provisional Position".
8. **Evaluate `--split` Modes**:
   - Test `--split group` (5 calls of 10 items) and `--split item` (50 calls) to determine if reducing per-prompt cognitive load improves inspection scrutiny (e.g. on Kannada).
9. **Mainline Integration into `trtools`**:
   - Migrate `trtools eval` from the legacy 5×20 scheme to the 50-item checklist architecture. Items 3-7 are prerequisites, not follow-ups: migrating as-is would replace a noisy metric with a confidently wrong one on exactly the low-resource languages the corpus exists to cover.

---

## 6. Reproducing

```bash
# 1. Pick unstable evaluation targets across translators
uv run experimental/11/pick_unstable.py --per-translator 1 --exclude gpt-5.6-luna/no -n 8 \
  > experimental/11/targets.tsv

# 2. Run batch evaluation (evals/, evals-nt/, evals-ne/)
bash experimental/11/batch.sh

# 3. Aggregate scores and generate comparisons
uv run experimental/11/agg50.py

# 4. Compare the three variants against a reference evaluator
#    (--reference re-runs the whole report under a different one)
uv run experimental/11/refcmp.py
```
