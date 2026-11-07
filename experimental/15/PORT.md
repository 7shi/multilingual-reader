# Port: The Language Check into `trtools`

A companion to [README.md](README.md). The README is what experiment 15 measured; this is
how the check is to go into `trtools`, including the flow it was asked to have — Jev
first, qwen3.6 when Jev cannot decide.

**Status**, 2026-11-08: step 0 dropped the qwen3.6 fallback (section 3.4); step 1 is
`trtools langcheck` without it; step 2's corpus run showed Jev's verdicts cannot zero a
score (section 3.5); fastText's lid.176 does (section 3.6). Step 1 is redone around it
(section 3.7), which supersedes sections 1, 2.2 and 4, and step 2 is rerun on it: 4
`wrong`, 1 `review`, all of them real. Steps 3 and 4 are done: `agg --jev` and
`trend --jev` take `--langcheck`, the Makefiles pass it and run `langcheck` in `all:`, and
the four `wrong` translations total 0 in `SCORES-jev.txt`, `TREND-jev.jsonl`, the model
READMEs and the comparison in examples/tr/README.md. The reference translations in
examples/evals/ are checked too (`batch.sh`): all 20 `ok` by fastText alone.
`review` is settled by reading the text after the run (Claude, at the user's direction)
and recording it with `trtools langcheck --resolve`; `gemma4-e2b`'s ia, Latin like
`gemma4-e4b`'s, was the first, and is now 0 too.

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

### 3.5 Step 2: the corpus run, and why Jev cannot zero a score

The check over the corpus (2435 texts, `langcheck@be2794c4`, committed beside each
`jev.jsonl`) gave 2379 `ok`, 51 `review`, 5 `wrong`. Of the five, two are right
(`bonsai2-27b` fi, the English source; `nemotron-3.5-super-vl` my, romanised Burmese then
English, by copy) and three are **correct German** sent to `Other` at 0.81-0.87
(`gemini-2.5-flash`, `gemma4-e2b`, `qwen3.5-4b`). The 51 `review` are mostly sr/hr against
each other, es against French, zh against `Other`, and the `fr/` set's en and es against
the French source; `fr/`'s transformer `en`, plain English, came out French 0.72.
Experiment 15's one-translator calibration ("correct texts are 0.64 and above") did not
hold over the corpus.

[variants_jev.py](variants_jev.py) asked 14 of those texts and 5 wrong-language controls
in six variants ([results/variants-jev.jsonl](results/variants-jev.jsonl)); P(label):

| Text | base | no labels | no `Other` | neither | brief `Other` | no labels, brief |
|---|---:|---:|---:|---:|---:|---:|
| German, three false `wrong` | 0.07-0.21 | 0.03-0.32 | 0.82-0.85 | 0.79-0.91 | 0.07-0.17 | 0.02-0.25 |
| Chinese, two | 0.30-0.48 | 0.01-0.03 | 0.93-0.95 | 0.48-0.66 | 0.29-0.65 | 0.02-0.07 |
| Spanish vs French, two | 0.34-0.53 | 0.73-0.86 | 0.41-0.63 | 0.73-0.86 | 0.54-0.56 | 0.75-0.84 |
| hr, sr | 0.60-0.62 | 0.65-0.67 | 0.63-0.68 | 0.76-0.80 | 0.59-0.67 | 0.66-0.71 |
| ia | 0.33 | 0.37 | 0.75 | 0.73 | 0.34 | 0.28 |
| `fr/` en (plain English) | 0.27 | 0.18 | 0.32 | 0.22 | 0.28 | 0.17 |
| Controls: fr, es, ja under another label | 0.00 | 0.00 | **0.23-0.77** | **0.26-0.72** | 0.00 | 0.00 |
| Controls: hr as sr; English as fi | ≤0.02 | ≤0.01 | ≤0.03 | ≤0.02 | ≤0.02 | ≤0.01 |

- **`Other` is both what catches a wrong language and what takes correct German, Chinese
  and Interlingua.** Without it the controls pass (Spanish labelled Portuguese 0.69); with
  it, in either wording, correct texts lose. Its wording makes no difference.
- **The speaker labels pull toward French**, as suspected (Camille, Luc): stripping them
  lifts Spanish to 0.73-0.86. But it sends Chinese to `Other` at 0.96-0.99 — the
  translated labels (卡米尔：) were what held it — and does nothing for the `fr/` English.
- **Jev calls plain English French**, labels or not. That is section 3's weakness on
  English again, now on a correct text, where it decides the verdict.

No variant separates the corpus's correct texts from the controls with one threshold. A
Jev P(target) is evidence for a person, not grounds for a 0: until something better is
found, only the copy check may set `wrong`, and Jev's low answers are `review`.

### 3.6 fastText's lid.176 does what Jev could not

[lid_fasttext.py](lid_fasttext.py) runs fastText's language identifier (`fasttext-predict`,
a dev dependency; the model in `lid/`, gitignored) over the same 2435 texts and the five
controls, locally, in about ten seconds ([results/lid-ftz.jsonl](results/lid-ftz.jsonl),
[results/lid-bin.jsonl](results/lid-bin.jsonl)). The whole text, speaker labels stripped,
is one prediction.

- **Where Jev failed, it is sure.** The lowest P(label) over correct German is 0.99,
  Chinese 0.997, Spanish 0.96; `fr/` (en, es from French) 0.94, `core/` 0.96.
- **Its absolute probability is not usable for close languages.** hr and sr split with
  `sh` (Serbo-Croatian) and `bs`, landing at 0.31-0.41 on every correct text; ms loses to
  Indonesian (0.26-0.38) on every one; ia sits at 0.23-0.41. What works is the **top
  language**: whether it lies outside the target's group (hr/sr/sh/bs, ms/id, no/da).
- **The top-language rule flags only real problems.** Correct texts whose top language
  falls outside the group, either model:

  | Text | Top | What it is |
  |---|---|---|
  | `bonsai2-27b` fi | en 0.96 / 0.47 | the English source |
  | `nemotron-3.5-super-vl` my | en 0.86 / 0.87 | romanised Burmese, then English |
  | `saluki-27b` eu | en 0.65 / 0.61 | English lines, then collapse |
  | `gemma4-e2b`, `gemma4-e4b` ia | la 0.48-0.56 | **Latin**, not Interlingua ("Ego sum Camille", "Haec sunt") |
  | `bonsai2-27b` ia (ftz only) | it 0.27 | Interlingua mixed with Spanish and Italian, collapsing |
  | `bonsai2-27b` th (bin only) | es 0.45 | collapse ("คา:BBBB…") |

  Jev had the two Latin texts at `Other` 0.60-0.64 — right, but no more confident than it
  was about correct German.
- **Controls**: French, English, Spanish and Japanese under another label are caught at
  0.94-1.00. Croatian labelled Serbian is not — they share a group — and that is the case
  Jev gets right (Croatian 0.95-0.97 in every variant of section 3.5).
- **Per-line reading** (lines of 30 characters or more) finds partial English: `bonsai2-27b`
  th 68% of lines, `nemotron-3.5-super-vl` ka 39%, `saluki-27b` ga 29%, all collapsing
  texts. As a share of the target it is noise (gl→pt/es, ne→hi, sk→cs, sw→eo on every
  model's correct text), so only the English share is worth reading.

So the division of labour is: **fastText for "which language family is this",** where it
is fast, local and sure; **Jev only between the members of a group,** where fastText
cannot tell and Jev can, without `Other`. Copy check becomes redundant with fastText for
the untranslated case, but costs nothing.

### 3.7 The revised check: fastText first, Jev where it is unsure

[trtools/langcheck.py](../../trtools/langcheck.py), scheme `langcheck@<8 hex>` over the
lid model's sha256, the thresholds, the groups and the option wording:

1. **copy** — half or more of the content lines verbatim from the original: `wrong`.
2. **fasttext** — lid.176 over the whole text (speaker labels stripped):
   - top language is the target, and the target has no group: `ok`;
   - top language outside the target's group at P ≥ 0.5: `wrong`;
   - otherwise Jev.
3. **jev** — a `Choice`:
   - target in a group (hr/sr, ms/id, da/no), whatever fastText's top: the corpus's
     members of the group only, no source, no `Other`;
   - fastText unsure outside the group: target, fastText's top three (named, e.g.
     Latin), the source and `Other`.

   P(target) < 0.3 `wrong`, < 0.5 `review`, else `ok`.

Each record keeps fastText's top three, its P(target), the copy share and the share of
long lines read as English (recorded, not used: in the corpus it marks collapsing texts).

Routed offline over the corpus (2435 texts, `lid.176.ftz`): 2213 `ok` by fastText; `wrong`
by copy for `nemotron-3.5-super-vl` my and by fastText for `bonsai2-27b` fi,
`gemma4-e4b` ia (Latin 0.51), `saluki-27b` eu; 216 to Jev within a group and 2 outside
(`bonsai2-27b` ia, `gemma4-e2b` ia with Latin offered). The candidate table of section 4
is gone; the groups replace it.

**The corpus run on `langcheck@38bab564`** (committed beside each `jev.jsonl`): 2430
`ok`, 4 `wrong`, 1 `review`, routed exactly as the offline count above.

- `wrong`: `bonsai2-27b` fi (English, fastText), `gemma4-e4b` ia (Latin 0.51, fastText),
  `saluki-27b` eu (English 0.65, fastText), `nemotron-3.5-super-vl` my (copy 0.59).
- `review`: `gemma4-e2b` ia, Jev Latin 0.49, Interlingua 0.35. The same kind of text as
  `gemma4-e4b`'s, which fastText settled at 0.51; this one fell at 0.48 and Jev, with
  Latin on the list, leaned the same way without reaching 0.3.
- Within the groups Jev separated cleanly without `Other`: correct sr 0.64 and above, hr
  0.67 and above (0.54 with `Other`, section 3.5); ms, id, da, no 0.97 and above. The
  correct German, Chinese and Spanish Jev had sent to `Other` never reached it.
- 218 Jev requests for the whole corpus.

The model is read from `--lid-model`, else `$TRTOOLS_LID_MODEL`, else
`.cache/lid.176.ftz` at the project root (gitignored). `LANGCHECK_OPTS=--force` on the Makefile targets re-checks
files written on an earlier scheme.

## 4. Candidate Table (superseded by 3.7)

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
