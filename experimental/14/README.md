# Experiment 14: Writing the Trend Column Without an Evaluator's Prose

What the trend column is to be under Jev, and why. The design is settled. [PLAN.md](PLAN.md)
is the ledger of the fourteen runs that reached it, what each settled and what changed after
it, kept separate so that a design changing does not edit a result. [PORT.md](PORT.md) is
how it goes into `trtools`.

The question came from [experiment 13](../13/README.md), which chose Jev as the corpus
evaluator: Jev returns no prose, so the column had nothing to summarise.

---

## 1. The Problem

`examples/tr/onde/{model}/TRENDS.jsonl` holds three keys per language — `lang`, `score`,
`analysis` — and the model READMEs render it as the "Translation quality overview" table.
`score` comes from the evaluation; `analysis` is one short phrase describing the
translation.

Under Jev, `score` falls straight out of `jev.jsonl`. `analysis` has no source.
`trtools/trend.py` builds it by handing an LLM the `overall_comment` of three evaluation runs
and asking for a summary; Jev is a System One model that returns typed judgments and no
prose, so there is nothing to summarise.

**The phrase has to describe Jev's score.** A phrase that is a second, independent verdict
on the translation would be no reason to replace the column that exists.

## 2. The Design

The old pipeline, rebuilt around Jev's scores: two calls to `ollama:qwen3.6`, both without
thinking, sharing no history.

**Stage 1 writes the evaluator's comment.** It is `trtools/evaluate.py`'s prompt — the
original, the translation and the guidelines with their point bands — with the closing
sentence replaced. Where evaluate.py asked for five scores, this hands over Jev's:

```
The translation has already been scored on each criterion:
- Readability & comprehensibility: 19.3/20
- Fluency & naturalness: 17.0/20
...
Total score: 92.2/100

Do not re-score it. Write an overall comprehensive evaluation comment about the translation
quality as a whole, based on the ENTIRE document, that accounts for these scores.
Write the comment in English — not in Danish.
```

Jev's five criteria are evaluate.py's verbatim, and a Jev level times `POINTS_PER_LEVEL` is a
score out of 20, so the numbers land on the scale the prompt's point bands are written on.
The comment is plain text rather than the old schema, and English is required because a
comment in the target language would make the evaluation of a Hindi translation depend on how
well the model writes Hindi.

**Stage 2 summarises it.** It is `trtools/trend.py`'s prompt, made singular, handed the one
comment with the Jev total in the block header, and never the translation. Two sentences are
added. One says to state the shortfall the comment names rather than praise:

```
IMPORTANT: If the evaluation names any shortcoming, however minor, state the most prominent
one rather than praising the translation. Praise it only if the evaluation names no
shortcoming at all.
```

The other gives Jev's own words (`jev_criteria.LEVELS`, verbatim) for the level of the
weakest criterion — for level 3, `The places where it falls short are scattered and confined
to roughly one to three lines.` Stage 1 reads the scores through evaluate.py's point bands,
where 17–19 of 20 is "high quality", and without these two sentences two thirds to three
quarters of the level-3 phrases at 89 and over are praise alone, although every comment
behind them names a shortfall. With them, praise is left to the rows Jev found nothing wrong
with.

## 3. What It Produces

Over 21 targets spanning all five levels, drawn four times (runs 13 and 14):

- **The old column's form.** Median five words, no quoted strings, no line numbers. The high
  rows read `Slight stiffness in conversational fillers`, the low ones `Severe garbling and
  repetition errors`; the severity follows the score as the old column's did.
- **Praise only at level 4.** No level-3 phrase is praise alone; the old column had praise
  alone on about a tenth of its rows.
- **Findings in the lower rows are real** — the collapse of amplitude and width into one Greek
  word, a stray Chinese character in Nepali, English inside Interlingua, a Thai translation cut
  off at the end — and the higher rows are mostly not checkable, which is the old column's
  nature too.
- **A phrase is as right as the comment behind it.** Stage 2 invents nothing; every claim is
  already in the comment. Stage 1's errors pass through at the same rate as its findings: an
  invented speaker swap, a real register shift called a gender problem.
- **About 12 seconds a phrase**, nearly all of it stage 1 — about 3.5 hours for a pass over
  the corpus's 1,072 translations.

**The one failure that has survived every design** is faulting the translation for the
original's own wording or notation — `implacable`, `delta x`, `NSOM`. No rule has ever
reduced it.

## 4. Already Decided

[PLAN.md](PLAN.md) section 16 holds the evidence for the ones that rest on a corpus
measurement, and the run sections for the ones that rest on output.

- **Record format**: `TREND-jev.jsonl`, the same three keys as `TRENDS.jsonl` and nothing
  more. No provenance field for the writer, no criterion breakdown, and not the comment.
  Kept in a separate file from `TRENDS.jsonl` so that two scales never share one
  ([PORT.md](PORT.md) section 4).
- **`score` is one decimal place, not an integer.** `trend.py` stores `int(median)`; on the
  Jev scale that ties most of a model's languages and collapses the table's sort order.
- **All 16 models are refreshed, and the score column is not frozen.** The model README
  table and `SCORES.txt` are the same numbers, so leaving the table on the old scale while
  [experiment 13's PORT.md](../13/PORT.md) regenerates `SCORES.txt` would contradict
  itself inside one file.
- **The existing `analysis` text is not carried over.** Its severity wording is calibrated
  to the old evaluator, and half the corpus changes tier under the new scale.
- **Every language gets a phrase.** No threshold restricting generation to the tail.
- **Two calls, not one.** Runs 1–12 had one call read the translation and write the phrase,
  with the level steering it and the reasoning standing in for the comment. It needed
  thinking on to follow its own wording — 35 hours a pass — and was no more accurate for it
  ([PLAN.md](PLAN.md) section 13).
- **No thinking in either stage.**
- **Jev reaches both stages**: its five scores in stage 1, its total and its weakest level in
  stage 2. Without them the phrase does not describe the score.
- **The comment is in English.**
- **The writer is `ollama:qwen3.6`**, a mixture of experts, chosen for speed. A commercial
  writer is ruled out on input tokens — [PLAN.md](PLAN.md) section 10 — and the other local
  writers are not compared.
- **The summarizer stays generative and is decoupled from the evaluator.** `common.mk`
  line 10 reads `SUMMARIZER = $(EVALUATOR)` ([PORT.md](PORT.md) section 2).

[PORT.md](PORT.md) is how this goes into `trtools trend --jev`.

## 5. Not Tested Here

- Whether `analysis` and `score` disagreeing in a row is a problem to solve. Left to be read
  off the first full run.
- Anything about `examples/tr/core/` or `examples/tr/fr/`, which pin the same evaluator and
  are out of scope for now ([experiment 13's PORT.md](../13/PORT.md) section 8 item 3).
- Whether stage 1 can be made more accurate. The phrase inherits its errors, and nothing
  here tried to reduce them.
- Whether faulting the translation for the original's own wording can be ruled out. It is a
  known residue, not an open experiment.

## 6. Running It

[trend14.py](trend14.py) writes phrases for a set of targets; [batch.sh](batch.sh) is every
run in order, and skips a run whose directory already holds results.

```
bash experimental/14/batch.sh                                    # the runs not already done
uv run experimental/14/trend14.py --two-stage --show-prompt      # stage 1 and stage 2's prompts
uv run experimental/14/trend14.py --comments experimental/14/run13 \
    --shortfall-rule --jev-level -v level -d DIR                 # stage 2 alone, over saved comments
```

```
experimental/14/
├── README.md        # this file: the problem, the design, the decisions
├── PLAN.md          # the ledger of the runs, and what each one settled
├── PORT.md          # how the design goes into `trtools trend --jev`
├── trend14.py       # the writer; every wording tried is reachable through a flag
├── batch.sh         # one section per run, each writing to its own runX/
└── runX/            # one <variant>.jsonl per variant
```

Run 13's records carry the stage-1 comment beside the phrase, and run 14's name the comment
file they summarised, so any phrase can be traced to the stage that made it. Nothing under
`examples/` is written.
