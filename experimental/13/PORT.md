# Port: Experiment 13's Evaluator into `trtools`, Writing `jev.jsonl`

Working document, and a companion to [PLAN.md](PLAN.md). PLAN.md section 5.2 records the
decision to give the corpus a Jev evaluation path of its own rather than a backend inside
`trtools`; this file is the design of that path, at the level of detail the implementation
needs. It lives here because everything it ports comes from this directory, and it should
move or be retired once `trtools/jev.py` exists.

**Scope: producing `examples/tr/onde/{model}/jev.jsonl`, and nothing else.** `TRENDS.jsonl`,
each model's `README.md`, `SCORES.txt` and the switch of `EVALUATOR` are PLAN.md's step 3
and are deliberately not settled here. Section 9 records the one deferred question that the
generation design nonetheless has to be aware of.

**Status**: design agreed, not implemented.

---

## 1. Where the Results Go

`examples/tr/onde/{model}/jev.jsonl`, one line per language, 67 lines, **beside `evals/`
rather than replacing it**. The old-scale record survives as its own thing, which is what
PLAN.md section 5.3 asks for, and the two directories never mix.

One file per model rather than one file per language. At the size below a model's whole
evaluation is 60 KB, appending is resumable, and a reader opens one file instead of 67.

## 2. The Record

```json
{"lang":"ja","model":"jev-1.13.0","rubric":"degrees@f518286e",
 "scores":{"readability":3.09,"fluency":2.61,"terminology":3.24,
           "contextual_adaptation":2.91,"information_completeness":3.11},
 "confidence":{"readability":0.73,"fluency":0.59,"terminology":0.61,
               "contextual_adaptation":0.73,"information_completeness":0.65},
 "probabilities":{"readability":[0.0,0.01,0.11,0.68,0.2], "…":[]},
 "usage":{"input_tokens":6878,"output_tokens":83},"seconds":0.3}
```

Section 3 defines the `rubric` value; `degrees@f518286e` is what the frozen code in this
directory produces today.

Measured over the four converted translators: 678 bytes a line, **44 KB per model and
roughly 0.7 MB for all 16**, against the 16 MB the three-run `evals/` directories
currently occupy. Section 8 breaks the saving down. `eval5_jev.py`'s per-language
file is 2,538 bytes, of which 637 are the level texts repeated in every one of them.

### What is kept, and why

| Field | Recoverable elsewhere? | |
|---|---|---|
| `probabilities` | primary data | kept |
| `confidence` | **no** — returned by the API, not computed | kept |
| `scores` | **no** — see below | kept |
| `usage` | no | kept; this is a paid API and the record is the only receipt |
| `seconds` | no | kept; see below |

`seconds` is the processing time for that language: `time.monotonic()` taken when the
language's processing starts and subtracted when it ends. It therefore covers the request
and everything around it, which is what a run costs. `monotonic` rather than `time.time()`
so a clock adjustment mid-run cannot produce a negative figure. It sits outside `usage`
because `usage` is the API's own report and this is measured locally.

With the token counts, it is what lets a finished corpus answer PLAN.md section 2's
reasons 2 and 3 -- "one run replaces three", "cost and wall time stop being design
constraints" -- from the record rather than from an estimate. The per-line figures do not
sum to the run's wall time, so the run prints its own total and this document is where
that total is written down once it exists.

`port.py` fills `seconds` with what the frozen files hold, which is **not the same
measurement**: `eval5_jev.py` timed `evaluate()` alone, so those values are request time
and a lower bound on the processing time the corpus records. The field is filled anyway so
that the two files have the same shape and can be diffed line by line; nothing should
compare the two `seconds` columns against each other.

`scores` cannot be recomputed from `probabilities`. The API returns probabilities rounded
to two decimals (some rows sum to 0.99), while the score comes from the full-precision
distribution. Over 400 criterion-judgments on disk, `Σ p·i × 5` differs from the recorded
`expected_scores` by a mean absolute **0.044** and a maximum of **0.20**. The score is the
primary number and the distribution is corroboration, not the other way round.

### What is dropped

`total_score`, `expected_total_score`, `evaluation.*.score` (all derivable by summation or
rounding), `evaluation.*.reasoning` and `overall_comment` (always empty under Jev),
`original_file`, `source_language` and `model_requested` (constant across the corpus), and
`target_language` and `translation_file` (implied by `lang`). The full `levels` text is
replaced by section 3's identifier.

Dropping them is only possible because `trtools` gets a reader of its own (section 5). As
long as the corpus was to be read by `trtools eval`'s existing path, the `evaluation.*.score`
shape was load-bearing — `aggregate.py:51` reads it directly — and this compression was
rejected for that reason. The decision to add `trtools jev` and `trtools agg --jev` is what
released it.

### Scores are levels, not points

`scores` holds the position on the five levels, `0.0`–`4.0`, not the 0–20 points that
`POINTS_PER_LEVEL = 5.0` maps it to. The level is what Jev answers; the point scale is a
presentation choice inherited from the old rubric. Storing the level means a later change
to that mapping does not invalidate anything already on disk.

### `model` and `rubric` repeat on every line

Hoisting them into a header record would save a few kilobytes of a 60 KB file. Repeating
them keeps the file honest if the pinned version or the rubric changes midway through a
resumed run: the record then says what each line was actually scored by. `trtools agg --jev`
asserts that all lines in a file agree, and a mixed file is an error rather than a silent
average.

## 3. `SCHEME_ID`

```
sha256(judge + scope + the five criterion descriptions + the five level texts
       + the state's key order)[:8]
```

recorded as `"rubric": "degrees@<hash>"`. The frozen code in this directory hashes to
**`degrees@f518286e`** ([port.py](port.py)`.scheme_id`), and `trtools/jev_criteria.py` has
to reproduce it.

Hashing only the level texts is not enough. What the model is asked is
`build_questions`'s `instructions` — `judge`, `criterion`, `scope` — together with the
levels, and what it is asked *about* is `build_state`'s named keys. Any of them can be
reworded without touching `LEVEL_SETS`, and the scores would shift with nothing in the data
to show it. This is the same failure mode as PLAN.md section 5.3's silent seam in
`TRENDS.jsonl`, at the level of the rubric rather than the file.

## 4. What Is Ported

| New file | Contents |
|---|---|
| `trtools/jev.py` | the `jev` subcommand; registered in `trtools/__main__.py` |
| `trtools/jev_criteria.py` | `CRITERIA`, `LEVELS`, `POINTS_PER_LEVEL`, `SCHEME_ID` |

Ported from `eval5_jev.py`: `build_state`, `build_questions`, `read_answers`, the version
pin and its check. Ported from `criteria.py`: the `degrees` level set and the five criterion
descriptions.

**Not ported**: the `bands` level set and the `--levels` switch, `EVAL_DIRS`, `--eval-dir`,
and `--runs`. Production is one rubric and one run. Experiment 12's README section 3.1
measured the run-to-run range at 1.12 points, with run 1 alone reproducing the median of
three at Pearson 0.998; there is nothing left for a second run to settle.

**`experimental/13/` is not touched.** Its copies stay frozen, which is the property
PLAN.md section 5.2 chose option A to preserve: a later edit to the corpus evaluator must
not change what experiment 13 claims to mean.

## 5. Command Line

```
uv run trtools jev ../../../onde-en.txt --langs $(LANGS) --tr-dir tr -o jev.jsonl
```

Run from a model directory. `--langs` takes `common.mk`'s `LANGS` (`CORE_LANGS +
EXTRA_LANGS`) exactly as the other targets do, rather than discovering languages from
`tr/`: the language list is the corpus's definition of what should exist, and a missing
translation should be an error, not a silently shorter run.

Defaults: `--model jev-1.13.0` (a version, never the `jev-latest` alias), `--from English`,
`--tr-dir tr`, `-o jev.jsonl`, `--attempts 3`, `-w/--retry-wait 3`.

`common.mk` gains a `jev:` target for this, separate from `evaluate:`. `EVALUATOR` and
`SUMMARIZER` are left alone — switching them is PLAN.md step 3.

### Aggregation needs a flag, and the reason is not obvious

`trtools agg jev.jsonl` cannot work as things stand, and would fail in the worst way.
`find_evaluation_groups` (`aggregate.py:11`) matches only `^(.+)-([123])\.json$` and then
keeps **only groups where all three runs are present** (`aggregate.py:27`). A one-run corpus
matches nothing and is discarded with no error and no warning. `trtools trend` shares the
same function (`trend.py:9,168,200`).

Hence `trtools agg --jev`, reading `jev.jsonl` directly. This is a fourth item for PLAN.md
section 5: section 5.2 states that the output being in `trtools eval`'s schema means `agg`
and `trend` read it as it stands, which is true of the schema and false of the file
discovery.

## 6. Resume and Failure

On start, read `jev.jsonl` and skip every `lang` already present. Append and flush one line
per language, so an interruption loses at most one — the same discipline as `trend.py:252`.

A malformed line **aborts**; it is never skipped. Silently dropping input that does not
parse is exactly the failure described in section 5, and it should not be reintroduced here.

A served model version other than the pinned one aborts the run instead of being retried:
the alias having moved is not a transient failure. Other errors retry up to `--attempts`.

## 7. Usage Accounting

One `usage.jsonl` entry per model directory, summing the run's 67 requests, matching
`eval5_jev.py`'s `evaluate_target`. `usage.jsonl` is shared account-level state; 67 entries
per model would make it unreadable.

## 8. All Sixteen Are Generated, Including the Four Already Evaluated

The four translators in `experimental/13/evals-degrees/` could be converted rather than
re-run: every field `jev.jsonl` needs is in those 268 files, and [port.py](port.py) does
it for nothing. That is not the plan.

**All 16 translators go through `trtools jev`, so the production path's wall time and cost
are measured end to end.** PLAN.md section 2 puts the full corpus at 1,072 evaluations,
roughly $0.21 and five minutes, and reasons 2 and 3 of that section rest on those figures
-- but they are extrapolated from 268 evaluations run by a different script. Converting
the four would leave the estimate unchecked at exactly the scale the decision depends on,
and save $0.05.

Re-running them also validates the port better than conversion could. The same languages
have been scored twice by the same pinned model on the same rubric, once by
`eval5_jev.py` and once by `trtools/jev.py`, so the two sets can be compared directly.
Experiment 12's README section 3.1 measures this evaluator's run-to-run range at 1.12
points; agreement inside that band means the port asks Jev the same question, and a
systematic shift means it does not. Equal `SCHEME_ID`s say the wording matches, which is
necessary but proves nothing about the rest of the request.

`port.py` is kept for that comparison -- it renders the frozen experiment files in this
exact format, so the old and new runs can be diffed line by line -- and as the fallback if
the paid path is ever unavailable. It is not part of the migration.

It writes to `experimental/13/jsonl-old/<translator>.jsonl`, never to the corpus: the
corpus file belongs to `trtools jev`, and this output exists to be compared against it
rather than to stand in for it. **`jsonl-old/` is gitignored.** It is a mechanical
re-rendering of `evals-degrees/`, which is committed, so the two would be the same
judgments stored twice; the conversion runs in under a second whenever the comparison is
wanted. What that costs is the ability to see the rendering change in a diff, which is
what `SCHEME_ID` and this document are for instead.

The rendering compresses by a measured **73.3%** -- 680,202 bytes over 268 files becomes
181,759 over four, or 2,538 bytes a file against 678 a line, consistent to within 0.2
points across all four translators. On disk the gain is larger, 1.1 MB against 196 KB,
because 268 files of 2.5 KB each occupy a 4 KB block apiece. Roughly 710 KB for all 16
translators, against the 16 MB the three-run `evals/` directories hold. Where it comes
from, per record: the level texts 637 bytes, `indent=2` about 580, the derivable
`evaluation` / `total_score` / `expected_total_score` about 290, and the constant or
implied fields about 185.

The four translators' 268 requests took **70 seconds** of request time in total, 16.7 to
18.9 per translator, or 0.26 seconds a language. That is a lower bound on a run of
`trtools jev` and nothing more: it excludes everything around the calls, which is exactly
the part section 2's `seconds` was added to measure.

## 9. Deferred: `TRENDS.jsonl`

Out of scope, and recorded so it is not lost.

`TRENDS.jsonl` is `{"lang", "score", "analysis"}`. The `score` column falls straight out of
`jev.jsonl`. The `analysis` column does not: `trend.py:198-250` builds it by passing three
runs' `reasoning` text to a generative model, and **Jev returns no `reasoning` at all**, so
for a newly added model the input to that step does not exist. PLAN.md section 5.1 says to
leave the summarizer on a generative model, which is necessary but not sufficient — there
would be nothing to feed it.

Models already evaluated have their Qwen-written `analysis` and keep it; whether their
`score` column is also kept, or refreshed to the Jev scale, is part of the deferred
question.

**Current idea for new models**: pass the translation itself and its Jev scores to
Qwen 3.6 and have it write the one-line summary — the summary then rests on the text plus
the numbers rather than on an evaluator's prose. To be worked out separately, along with
what the other options cost: deriving a fixed sentence from the five criterion scores
(free and deterministic, but unable to name a defect kind, since the `degrees` levels judge
only how much of the document falls short and deliberately not what is wrong with it —
`criteria.py:83-91`), or replacing the prose column with the five criterion scores.
