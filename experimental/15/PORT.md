# Port: The Language Check into `trtools`

A companion to [README.md](README.md). The README is what experiment 15 measured; this is
how the check is to go into `trtools`, including the flow it was asked to have — Jev
first, qwen3.6 when Jev cannot decide.

**Status**, 2026-11-08: step 0 is measured and dropped the qwen3.6 fallback (section
3.4); step 1 is implemented as `trtools langcheck` without it. Steps 2-4 are open.

---

## 1. What It Does

Per language of one set, before its score is used:

1. **Copy check** (no model). Compare the translation line by line with the original. If
   most non-empty lines are identical after stripping the speaker label, the verdict is
   `wrong` (detected: the source language). This is the case Jev is weakest on — the
   English original came out English 0.66 at best — and the one most certainly worth 0.
2. **Jev**. A `Choice` over the target, its confusable languages (section 4), the source
   language and `Other`, with only the translation in the state. P(target) decides:
   pass, `wrong`, or undecided (section 3).
3. ~~**qwen3.6**, only when Jev is undecided.~~ Dropped after step 0 (section 3.4): an
   undecided Jev answer is `review`.
4. Append one record to the set's check file (section 2.2).

`trtools agg --jev` and `trtools trend --jev` then read that file: `wrong` totals 0,
`review` keeps its score and is reported (section 5).

## 2. Interface

### 2.1 Command line

A subcommand of its own, `trtools langcheck`, not a flag on `trtools jev`:

- It is a different question with a different state (no original, no criteria), and its
  records must not enter `jev.jsonl`, whose every line is checked against `SCHEME_ID`.
- It has to run alone over every existing set; nothing about the scores needs redoing.

```
uv run trtools langcheck ORIGINAL --langs fr es ... [--tr-dir tr] [-o langcheck.jsonl]
    [-f English] [-m jev-1.14.0] [--force]
```

Arguments mirror `trtools jev`'s (`--langs`, `--tr-dir`, `-o`, `-f`, `--attempts`,
`--timeout`, `--force`), and so does resuming: languages already in the output are skipped,
and a line from another check scheme or another Jev version stops the run.

### 2.2 Record

`langcheck.jsonl` beside `jev.jsonl` (in `core/` and `fr/`, `langcheck-{topic}.jsonl` beside
`jev-{topic}.jsonl`):

```json
{"lang": "sr", "scheme": "langcheck@1a2b3c4d", "model": "jev-1.14.0",
 "verdict": "ok", "stage": "jev", "detected": "Serbian",
 "p_target": 0.83, "copy_share": 0.0,
 "probabilities": {"Serbian": 0.83, "Croatian": 0.13, ...}, "usage": {...}, "seconds": 1.2}
```

- `verdict`: `ok`, `wrong` or `review`.
- `stage`: which step decided — `copy` or `jev`. A `copy` record has no `model`,
  `p_target` or `probabilities`; `detected` is the source language.
- `scheme`: a hash, like `SCHEME_ID`, over the instructions, option texts, thresholds and
  the candidate table. Changing any of them changes verdicts, so it must be detectable.

## 3. Jev, Then qwen3.6

### 3.1 When Jev is undecided

Two thresholds on P(target): at or above `HIGH` passes, below `LOW` is `wrong`, between
goes to qwen3.6. What experiment 15 has to set them by:

| Texts | P(target) |
|---|---|
| Wrong language, not English (de, pt, zh, sr mislabelled; `bonsai2-27b` fi) | 0.00–0.02 |
| The English original labelled French | 0.32 |
| Correct, lowest four of 134 | 0.64 (`bonsai2-27b` sr), 0.73 (`bonsai2-27b` de), 0.83 (`gpt-6-sol` sr), 0.87 (`gpt-6-sol` ia) |
| Correct, all others | 0.89 and above |

`LOW = 0.2`, `HIGH = 0.8` would send three texts in 139 to qwen3.6: the English original
(which the copy check catches first) and `bonsai2-27b`'s sr and de. Raising `HIGH` to 0.9
adds `gpt-6-sol`'s sr and ia.

### 3.2 Is qwen3.6 the right referee there?

**Only partly, and the measurements so far point in opposite directions.**

- **Where it is stronger than Jev**: English. It named the English original as English
  every time it was asked, where Jev never got above 0.66. But the copy check covers the
  fully untranslated case without a model, so what is left for qwen3.6 here is a text that
  is *partly* English, which experiment 15 did not test.
- **Where it is weaker**: the languages that make Jev hesitate are close or constructed —
  sr/hr, ia — and those are qwen3.6's own errors. Choosing from all 68, it named the
  Interlingua text Esperanto; asked yes/no, it accepted Croatian as Serbian and rejected
  correct Arabic, Danish and Swedish. Sending `ia` at 0.87 to qwen3.6 would have turned a
  pass into a false `wrong`.

So the band is where the two judges are *both* least reliable, except for English. A
second opinion there is worth having, but not as a tie-breaker that can zero a score.

### 3.3 Decision rule (as planned; dropped in 3.4)

| Jev | qwen3.6 says | Verdict |
|---|---|---|
| P(target) ≥ `HIGH` | — | `ok` |
| P(target) < `LOW` | — | `wrong` |
| between | the target | `ok` |
| between | the language Jev ranks first (not the target) | `wrong` |
| between | anything else | `review` |

`wrong` needs both judges to name the same other language, or one of them to be
unequivocal. A disagreement is `review`: the score stands, and a person reads the text.
With `--no-fallback`, everything in the band is `review`.

qwen3.6 is asked over the same options Jev had, not all 68: it is a narrower question,
and the one that went wrong in experiment 15 (`ia` → Esperanto) was asked over all 68.
Whether narrowing fixes it is step 0.

**Alternative considered: no fallback at all.** `review` for the band, read by a person.
On experiment 15's data that is two texts in 134 correct ones, plus whatever the corpus
turns up. It is simpler — no ollama dependency in a step that otherwise only needs the
Jev API — and loses nothing qwen3.6 has been shown to get right in the band. The fallback
earns its place only if step 0 shows it right on the band's cases.

### 3.4 Step 0: the fallback is dropped

[narrow_qwen.py](narrow_qwen.py) asked qwen3.6 with the gate's options listed in the
prompt (plain text, no thinking, temperature 0;
[results/narrow-qwen.jsonl](results/narrow-qwen.jsonl)). It sometimes echoed the option's
description after the name ("German: The text is written in German."); the answer is read
up to the colon.

| Set | Label | Actually | qwen3.6 | Right |
|---|---|---|---|---|
| `bonsai2-27b` | sr | sr | Serbian | ✓ |
| `bonsai2-27b` | de | de | German | ✓ |
| `bonsai2-27b` | sk | sk, line 6 English | Slovak | ✓ |
| `bonsai2-27b` | fi | English | English | ✓ |
| `gpt-6-sol` | sr | sr | Serbian | ✓ |
| `gpt-6-sol` | ia | ia | Interlingua | ✓ (Esperanto over all 68) |
| mislabel | sr | hr | Serbian | ✗ |
| mislabel | fr | English | English | ✓ |
| mislabel | de | fr | German | ✗ (`Other` expected) |
| mislabel | pt | es | Portuguese | ✗ (`Other` expected) |
| mislabel | zh | ja | `Other` | ✓ |

Narrowing fixed `ia`, and every correct text in the band was named correctly. But three of
five wrong-language texts were named as the label, where Jev gave the label 0.00-0.02.
Under section 3.3's rule a "the target" answer passes the text, so in the band qwen3.6
would pass exactly the texts the check exists for; its "the target" carries no
information. Its one strength, English, is already covered by the copy check. So: no
fallback, and the band is `review`.

## 4. Candidate Table

The options per target are frozen data, [trtools/langcheck_candidates.py](../../trtools/langcheck_candidates.py), copied from
[results/candidates-gpt-6-sol.json](results/candidates-gpt-6-sol.json): the target plus
the languages that drew 0.01 or more either way in the 69-option pass. Source language
and `Other` are added at run time, so the same table serves `fr/` (French source).

- A language missing from the table gets the target alone.
- The table is part of the check scheme's hash.
- Rebuilding it is `experimental/15/calibrate_jev.py`; it stays there rather than
  becoming a subcommand, since it runs once per change of language list or Jev version.
- It comes from one translator's texts (README section 7, open item 2). Running the
  69-option pass over a second translator before freezing the table would show whether
  pairs are missing; it is about 70 Jev requests.

## 5. Consumers

### 5.1 Scores

`aggregate_jev` in [trtools/aggregate.py](../../trtools/aggregate.py) takes the check file
as an optional argument: `wrong` sets `total` to 0 and records `verdict` and `detected`
beside it; `review` leaves the total and records the verdict. Everything downstream of it
then follows without changes of its own:

- `trtools agg --jev --langcheck FILE` → `SCORES-jev.txt`, with a line on stderr per
  `wrong` and `review` language.
- `trtools trend --jev ... --langcheck FILE` → `TREND-jev.jsonl` score, and through it the
  README tables, `plot_comparison.py` and the comparison table in
  [examples/tr/README.md](../../examples/tr/README.md).

A language missing from the check file is an error, as a language missing from `tr/` is
for `trtools jev`, so a set cannot be totalled half-checked.

### 5.2 Trend phrase

For a `wrong` language, `trtools trend --jev` writes no LLM phrase: a fixed one such as
"Not in the target language (detected: English)". Describing the five criteria of a text
in the wrong language would describe the wrong thing.

### 5.3 Makefiles

A `langcheck` target before `scores-jev` in [examples/tr/onde/common.mk](../../examples/tr/onde/common.mk),
`core/Makefile` and `fr/Makefile` (per topic), and the reference translations in
`examples/evals/`. `scores-jev` and `trends-jev` pass the file.

## 6. Order of Work

0. **Measure the fallback** — done, section 3.4: dropped. qwen3.6 with narrowed
   options, plain text, on the cases the band would send it and the ones it got wrong:
   `bonsai2-27b` sr and de, `gpt-6-sol` sr and ia, Croatian labelled Serbian, and a
   partly English text (e.g. `bonsai2-27b` sk, line 6 left in English).
1. `trtools/langcheck.py`, `langcheck_candidates.py`, the subcommand, and the copy check
   — done. The copy check counts content lines (speaker label stripped) found verbatim in
   the original, `wrong` at half or more: the English original labelled French is 1.00,
   the correct translations tried 0.00-0.10.
   Run over the five mislabelled texts and `bonsai2-27b`'s sr, de, fi, sk, cy, ia: every
   verdict as expected — fr `wrong` by copy; de, pt, zh `wrong` (`Other` 1.00); sr `wrong`
   (Croatian 0.95); fi `wrong` (English 1.00); `bonsai2-27b` sr `review` (0.61), de
   `review` (0.76); sk, cy, ia `ok`. Against gate_jev.py's run, sr and de moved by 0.03.
   `langcheck` targets are in the Makefiles (`onde/common.mk`, `core/`, `fr/`), outside
   `all:` until step 3.
2. Run over the whole corpus **in report-only mode**: write the check files, total
   nothing differently. Read every `wrong` and `review`. This is the first look at whether
   the corpus has real wrong-language translations.
3. `--langcheck` on `agg` and `trend`; Makefile targets; regenerate `SCORES-jev.txt`,
   `TREND-jev.jsonl` and the README tables for sets with a `wrong` language.
4. Docs: [trtools/README.md](../../trtools/README.md) (`langcheck` section, `agg`/`trend`
   options), [examples/tr/README.md](../../examples/tr/README.md) (what a 0 means).

Step 2 is a corpus-wide run and is for the user to start; steps 0 and 1 are not.
