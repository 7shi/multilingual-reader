# Experiment 14: Writing the Trend Column Without an Evaluator's Prose

What is being built, what was measured from `examples/tr/onde/{model}/jev.jsonl` to arrive
at that design, and what still has to be settled before
[experimental/13/PLAN.md](../13/PLAN.md)'s step 3 can regenerate the model READMEs.
[PLAN.md](PLAN.md) is the ledger of the runs — twelve so far, what each settled and what
changed after it — kept separate so that a design changing does not edit a result.

This is [PORT.md](../13/PORT.md) section 7 item 1 and
[experiment 13's PLAN.md](../13/PLAN.md) section 5.1. The specification is settled. The
wording is now settled too; what is not is **which writer**, which run 9 turned from a
question for afterwards into part of the port itself — the phrases differ by more between
two writers than they ever did between two wordings.

---

## 1. The Problem

`examples/tr/onde/{model}/TRENDS.jsonl` holds three keys per language — `lang`, `score`,
`analysis` — and the model READMEs render it as the "Translation quality overview" table.
`score` comes from the evaluation; `analysis` is one short phrase describing the
translation.

Under Jev, `score` falls straight out of `jev.jsonl`. `analysis` has no source.
`trtools/trend.py:198-250` builds it by handing an LLM the `overall_comment` of three
evaluation runs and asking for a summary; Jev is a System One model that returns typed
judgments and no prose, so there is nothing to summarise.

The replacement writes the phrase from the translation itself, with Jev's per-criterion
breakdown steering what the writer looks for. That makes the two columns independent:
`score` is Jev's judgment, `analysis` is a generative model's reading of the same text.

## 2. Why the Breakdown Steers Rather Than Appears

[Experiment 13's PORT.md](../13/PORT.md) section 5 recorded three options for the column,
and measuring the corpus ruled two of them out before anything was run.
[PLAN.md](PLAN.md) section 1 is the measurement; the conclusions are:

- **A fixed sentence derived from the five scores would be nearly constant.** The lowest
  criterion is `fluency` in 960 of 1,072 translations, and in all 67 languages of four
  models.
- **Replacing the prose with the five scores would add almost nothing to `score`.** Each
  criterion correlates with the total at Pearson 0.88–0.99.
- **But a number is usable as an instruction rather than as output.** An instruction is not
  read by anyone, so its being identical in most cases costs nothing, and the rest is
  exactly where it is worth having.

Of the two numbers tried as instructions, only one survived. The *level* of the weakest
criterion steers the phrase; the *identity* of that criterion was tried over two runs and
changed nothing, for the reason the correlations above already give.

## 3. The Design

The column being replaced is a *characterisation*, not a location. Measuring its 1,072
entries says so plainly:

> median 5 words, longest 11; a quotation mark in 23 entries of 1,072, always around a
> single word; a line number in none.

It reads `<severity> <kind of defect>` about the translation as a whole — `Minor stylistic
phrasing issues`, `Severe structural corruption and gibberish` — and its severity word
tracks the score almost monotonically: `Severe` at a median of 32, `Critical` 57, `Notable`
74, `Minor` 91, `Exceptional` 97.

Runs 1–6 asked instead for the lines that fall short and what is wrong with them, and every
failure they turned up was a failure at pointing. Run 7 changed the genre and runs 1–6 are
behind `--locate`. [PLAN.md](PLAN.md) sections 2–7 are that history; what follows is the
design as it now stands.

### The writer's own reasoning stands in for the evaluator's prose

`trtools/trend.py` hands an LLM the `overall_comment` of three evaluation runs and asks it
to summarise them. Its writer never saw the translation; the phrase is a summary of someone
else's verdict. Under Jev there is no verdict, so the equivalent has to come from the writer
itself — which is why this genre runs with **thinking on**, where every run before 9 ran
without it. The reasoning plays the part of the `overall_comment` and the phrase is its
summary, in the same relation the old pipeline had.

This is not a preference, and [PLAN.md](PLAN.md) section 13 measures it: the same writer,
wording and targets with the thinking off. What it buys is **obedience, not accuracy**. The
false rate is identical either way, 7 phrases in 84; what changes is whether the wording is
followed. With the reasoning the ban on pointing below holds at 0–5% and the adopted
variant is the stable one. Without it the ban is ignored at 19–29% and `--summary` is the
variant that comes apart, 11 of 21. The reasoning costs 117 seconds a phrase against 2.1 —
about 35 hours for a corpus pass against 37 minutes — and that is what it is bought with.

The closing line and the output format are `trend.py`'s own sentences, carried over:

```
Summarize the single most notable characteristic of this translation in one short phrase.
If defects exist, state the most prominent one concretely. If the translation is sound,
state that briefly.
```

Asking for *the single most notable characteristic* is also what makes the phrase stable:
run 8's wording said what kind of thing to name and left which one open, and the repeats
disagreed on ten of 21 rows. This says which of the several to pick.

The 8-word ceiling is the old prompt's too, and it is what recovers the length. Runs 7 and 8
asked for about five words and got four, a third of their answers at three or fewer; the
ceiling puts the median back on the old column's five to six without any instruction about
magnitude.

### The level of the weakest criterion supplies the extent, and only that

`jev_criteria.py`'s five levels say how much of the document falls short, deliberately not
what is wrong with it. That is exactly the part a writer cannot infer from the text alone,
and it is well spread across the corpus:

| Level | Records | What the writer is told |
| ---: | ---: | --- |
| 4 | 12 | Nothing in this translation falls short |
| 3 | 625 | A small part falls short, and the rest is sound |
| 2 | 335 | A substantial part falls short, or one problem runs through the whole text |
| 1 | 88 | Most of the translation falls short |
| 0 | 12 | Nothing meets the criteria, and there may be no usable target-language text |

`SUMMARY_LEVELS` is that and nothing more, standing in for the old prompt's `Trust these
evaluations as given`. It carries no task and no register word: the task is the closing
line's, and the register the old prompt never supplied either, its writer taking severity
from the evaluations' prose. Taking the extent from the level also removes the need to
police severity adjectives — the prose lands on the same scale as the score because the
instruction put it there.

**Nothing asks the writer how much.** Run 7 asked twice over, in the closing line and in the
no-pointing rule, and got it answered with a number nobody had supplied: eleven of 66 phrases
carried one, `gpt-oss/sv` was told it has three unlabelled lines when it has eight. Both
clauses are gone and both are behind `--extent-clause`.

### The ban on pointing is kept

`--summary-free` drops it; `--summary` keeps it, and `--summary` is what is adopted:

```
IMPORTANT: Do not point at a place. No line numbers, and no strings quoted from either
text. The phrase says what kind of thing is wrong; an instance of it is not what the
column holds.
```

The measurement is the quote rate against the old column's 2%. With the ban: 0–5%. Without
it: 19–33% on the commercial writer. The rule also buys stability — in run 10 every one of
the five rows where the repeats disagreed was a row where one of them reached for a specific
string.

The argument against it was that naming the string is what makes a claim checkable, and six
of run 9's seven checked findings were `summary-free`'s. [PLAN.md](PLAN.md) section 12
removes it: on the local writer `summary-free` reaches for two strings in 21 and both carry
a false or mis-framed claim rather than a finding.

### The focus sentence, tried and dropped

A second sentence pointed the writer at whichever criteria sat more than 0.3 levels below
the record's own mean — relative to the record rather than absolute, so a uniformly weak
translation would still report what was weakest within itself. It changed nothing that two
runs of the same prompt did not change by more, including over `FOCUS_TARGETS`, the target
set built to give it its best chance. [PLAN.md](PLAN.md) sections 3 and 4 are the
comparison; `--axis-b` still switches it on. The level alone steers it.

## 4. What the Experiment Has to Settle

The wording, judged on output over a sample spanning all five levels and several models,
and — since run 9 — the writer with it. [PLAN.md](PLAN.md) is where each answer was reached
and which run reached it.

| | Question | Verdict |
|---|---|---|
| 1 | Is the phrase the same genre as the column it replaces? | Yes, from run 7. Median words and quote rate both match |
| 2 | Does the focus sentence change the output at all? | No, twice. Dropped |
| 3 | Is the phrase stable between runs? | On the commercial writer, 16–17 of 21. On the local one with thinking, 13–14; without it, 10 |
| 4 | Does the writer invent a defect where there is none? | Not on the commercial writer — two false phrases in 84 and 63. On the local one, seven in 84 |
| 5 | Keep the ban on pointing, or drop it? | Keep. It holds the quote rate at the old column's 2% and costs nothing the local writer was going to give |
| 6 | Does the reasoning have to be on? | Yes for `--summary`: without it the ban on pointing stops being obeyed and the variant destabilises. Not for accuracy — the false rate is the same |
| 7 | Which writer? | Open. Commercial is out on cost; `ollama:qwen3.6` is the only local one measured |

**Cost** has turned out to be two different constraints. On a commercial writer it is
tokens: every phrase sends the whole original and the whole translation, about 4,190 input
tokens, and a pass over the corpus is 1,072 of them — roughly 4.5M input tokens, which is
what rules `gpt-5.6-terra` out. On a local writer nothing is billed and the constraint is
the clock: run 11 took 163m58.240s for 84 phrases with thinking on, 117 seconds each, which
puts a full pass near 35 hours. That is why run 12 carries all four of run 11's variants —
the two runs have to be the same size for their times to mean anything.

**The one failure that has survived every genre** is faulting the translation for the
original's own wording — `implacable`, `its square amplitude`, `uh...` rendered as `ehm...`.
It was the notation demands of run 6 and the back-translation judgements of run 5, and it is
still here at two phrases in 84. No rule has ever reduced it.

## 5. Running It

[trend14.py](trend14.py) writes one phrase per target and prints it beside the one currently
in `TRENDS.jsonl`; [batch.sh](batch.sh) is every run in order.

```
bash experimental/14/batch.sh                     # the runs not already done
MODEL=... bash experimental/14/batch.sh           # the same, for a section with a commercial writer
uv run experimental/14/trend14.py --show-prompt   # the instructions, without calling
uv run experimental/14/trend14.py --focus-targets  # the set built for the focus sentence
uv run experimental/14/trend14.py --slight-targets # level 3's top tenth
```

```
experimental/14/
├── README.md        # this file: the problem, the design, the decisions
├── PLAN.md          # the ledger of the runs, and what each one settled
├── trend14.py       # the writer -- the wording under test is the block at the top
├── batch.sh         # one section per wording, each writing to its own runX/
└── runX/            # one directory per wording: one <variant>.jsonl per variant
```

The writer is `WRITER` in [batch.sh](batch.sh), pinned to `ollama:qwen3.6`, except in the
sections that take it from `MODEL` in the environment — runs 9 and 10, whose writer is a
commercial one and is named by whoever runs it rather than by the file.

A section whose directory already holds results is skipped, so the script is safe to re-run
and does only what is left; to redo one, move its directory aside. A run directory belongs
to one wording, because a phrase only means something against the prompt that produced it,
and every superseded wording is reachable from the current `trend14.py` through `--locate`,
`--no-line-rule`, `--strict-level3`, `--axis-b`, `--extent-clause`, `--no-magnitude` and
`--no-original` — though the phrases will not come back identical, since the writer is not
deterministic.

Each section is a single call. `trend14.py` loops the targets on the outside and the
variants on the inside, so every variant of a target sends the same original and translation
one after another and that prefix stays in the server's cache — which is worth 25% of the
input on a first run and 99.9% on a second over the same targets. `runX/` gets one
`<variant>.jsonl` per variant and nothing else. The console output — the variants grouped
under their target, beside the phrase currently in `TRENDS.jsonl` — is for watching a run go
past and is not kept. Runs 1–12 teed it to `runX/batch.log`; nothing was ever read out of
one that the JSONL did not already hold, and they have been deleted.

The wording under test is the block at the top of `trend14.py`; everything below it is
plumbing. Nothing under `examples/` is written.

## 6. Already Decided

Recorded here so the experiment does not reopen them. [PLAN.md](PLAN.md) section 14 holds
the evidence for the ones that rest on a corpus measurement, and the run sections for the
ones that rest on output.

- **Record format**: `TREND-jev.jsonl`, the same three keys as `TRENDS.jsonl` and nothing
  more. No provenance field for the writer, and no criterion breakdown. Kept in a separate
  file from `TRENDS.jsonl` so that two scales never share one
  ([experiment 13's PLAN.md](../13/PLAN.md) section 5.3).
- **`score` is one decimal place, not an integer.** `trend.py` stores `int(median)`; on the
  Jev scale that ties most of a model's languages and collapses the table's sort order.
- **All 16 models are refreshed, and the score column is not frozen.** The model README
  table and `SCORES.txt` are the same numbers, so leaving the table on the old scale while
  step 3 regenerates `SCORES.txt` would contradict itself inside one file.
- **The existing `analysis` text is not carried over.** Its severity wording is calibrated
  to the old evaluator, and half the corpus changes tier under the new scale.
- **Every language gets a phrase.** No threshold restricting generation to the tail.
- **The level alone steers it.** The focus sentence is dropped and `--no-original`
  rejected; both stay as flags so the rejections can be re-run.
- **The phrase characterises, it does not point.** No line numbers and no quoted strings:
  `--summary` is adopted over `--summary-free`, on the quote rate against the old column's
  2% and on what the strings turned out to carry (section 3).
- **Praise is allowed; invention is not.** The ban on general assessments bought about a
  tenth of the level-3 band and cost fabricated defects on the rows it did not buy. The
  permission went unused for six runs and is taken from run 11 on.
- **Nothing in the prompt asks how much.** The level says it; a number from the writer is
  a guess, and run 7 is eleven of 66 phrases carrying one.
- **Thinking is on.** It is what stands in for the `overall_comment` the old pipeline
  summarised, and [PLAN.md](PLAN.md) section 13 is what turning it off does to the wording's
  central rule. It is the experiment's most expensive decision — 35 hours a pass against
  37 minutes — and section 13's closing paragraph is the one reading that would reopen it.
- **The writer is a local model.** A commercial one is ruled out on input tokens alone —
  4,190 per phrase times 1,072 languages — regardless of how well it writes.
  [PLAN.md](PLAN.md) section 10 is the measurement.
- **The summarizer stays generative and is decoupled from the evaluator.** `common.mk`
  line 10 reads `SUMMARIZER = $(EVALUATOR)`
  ([experiment 13's PLAN.md](../13/PLAN.md) section 5.1). **Which** local model it is, is
  the one thing this experiment still owes; `ollama:qwen3.6` is the only candidate
  measured.

## 7. Not Tested Here

- Whether `analysis` and `score` disagreeing in a row is a problem to solve. They now come
  from two judges, and a visible disagreement is honest rather than broken. Left to be read
  off the first full run.
- Anything about `examples/tr/core/` or `examples/tr/fr/`, which pin the same evaluator and
  are out of scope for the same reason as in [PLAN.md](../13/PLAN.md) section 4 item 3.
- Whether faulting the translation for the original's own wording can be ruled out. It has
  survived every genre and every rule tried, at two phrases in 84. It is a known residue,
  not an open experiment.
- Whether the full pass's wall-clock cost is acceptable. Section 4 has the number for the
  one local writer measured; it is a scheduling question for the port, not a wording one.
