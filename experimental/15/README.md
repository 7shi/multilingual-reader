# Experiment 15: Does the Evaluator Notice the Wrong Language?

A translation asked for in French that comes back in English, or in Spanish, should score 0.
This checks whether Jev's scores do that, and when they do not, what can say which language
a text is in reliably enough to zero a score on.

**Answer: Jev's five-criterion scoring does not, and a separate Jev `Choice` does.** Over
a fixed set of options — the target, the languages it can be confused with, English and
`Other` — the target's probability separates every wrong-language text tried from every
right one, at a threshold of 0.5.

**Status**: frozen, 2026-11-08. The port into `trtools` is [PORT.md](PORT.md).

## 1. Setup

The scoring scheme ([trtools/jev_criteria.py](../../trtools/jev_criteria.py)) tells Jev the
target language in `build_state` (`target_language`, and the `task` line), and its lowest
level mentions "no usable target-language text". Nothing else checks the language.

[mislabel.sh](mislabel.sh) builds `mislabel/tr/` from existing `gpt-6-sol` translations
copied under another language's code; `trtools jev` takes the target from the file name,
so Jev is told the wrong target:

| Labelled | Actually | What it tests |
|---|---|---|
| fr | the English original | untranslated output |
| de | `gpt-6-sol`'s French | fluent, wrong language |
| pt | `gpt-6-sol`'s Spanish | close language |
| zh | `gpt-6-sol`'s Japanese | shared script |
| sr | `gpt-6-sol`'s Croatian | near-identical (this corpus writes Serbian in Latin) |

The correctly labelled controls are the same model's own files.

## 2. Jev's Scores Ignore the Language

`trtools jev` over the five ([results/score-mislabel.jsonl](results/score-mislabel.jsonl),
[results/SCORES-mislabel.txt](results/SCORES-mislabel.txt)), against the same text under
its correct label:

| Labelled | Actually | Score | Correct label's score |
|---|---|---:|---:|
| de | French | **93.3** | 92.8 (fr) |
| sr | Croatian | 85.0 | 90.0 (hr) |
| zh | Japanese | 82.4 | 91.8 (ja) |
| pt | Spanish | 81.4 | 91.2 (es) |
| fr | English | 35.4 | — |

French scored as German comes out *higher* than as French; every criterion sits at level
3.7–3.9. The other foreign languages lose 5–10 points, mostly on fluency and contextual
adaptation. English is noticed — fluency falls to level 0.89 — but readability and
information completeness stay near level 2, since the text is readable and complete, so it
keeps 35 points.

Compare [experiment 13's FLOOR.md](../13/FLOOR.md), where `bonsai2-27b`'s `fi` (six lines
of the English source, then bare speaker names) scored 3.8: that case is carried by its
collapse, not by its language.

## 3. Asking Directly, on the Ten

The five mislabelled texts plus the five correct controls, asked of each judge with the
whole text attached:

| Labelled | Actually | qwen3.6 yes/no | Jev `Noul` p(yes) | Jev `Choice` P(English) |
|---|---|---|---:|---:|
| fr | English | no | **0.57** | **0.62** |
| de | French | no | 0.12 | 0.74 |
| pt | Spanish | no | 0.07 | 0.12 |
| zh | Japanese | no | 0.03 | 0.19 |
| sr | Croatian | yes ✗ | 0.82 | 0.01 |
| 5 correct | | yes | 0.88–0.99 | 0.00 |

- qwen3.6 ([ask_qwen_yesno.py](ask_qwen_yesno.py), no thinking, temperature 0): "Is the
  following text written in X? Answer only yes or no."
- `Noul` ([ask_jev_noul.py](ask_jev_noul.py)): state `{claimed_language, text}`, "Is `text`
  written in `claimed_language`?". No original is passed.
- `Choice` ([ask_jev_choice.py](ask_jev_choice.py)): state `{text}` only, options English
  and the target.

**Jev cannot say that plain English is English.** Both of its forms leave the English
original near 0.6, the one case qwen3.6 found easiest. With the `Choice`, a text in
neither option drifts to English (French labelled German: 0.74), so its English
probability reads as "not the target" rather than as English. Raw outputs are in
`results/probe-*.txt`.

## 4. False Rejections Over 67 Correct Translations

A gate zeroes scores, so a correct translation it rejects is the costly error.
[check_all.py](check_all.py) runs over all of `gpt-6-sol`'s translations, correctly
labelled, and asks a rejected text which language it is:

| Judge | Rejected | Time |
|---|---|---:|
| qwen3.6 yes/no | ar, da, sv | 3m53s |
| qwen3.6, pick a name from all 68 ([choose_qwen.py](choose_qwen.py)) | ia → Esperanto | 3m53s |
| Jev `Choice`, English or target | none, P(English) = 0.00 for all 67 | 13s |

- **qwen3.6's yes/no is biased toward no.** Asked which language the three rejected texts
  are, it names each correctly (Arabic, Danish, Swedish): it can tell the languages, the
  yes/no framing is what fails.
- **Picking from a list does better but not well enough.** The `ia` text is plainly
  Interlingua ("Salute a totes, e benvenite a «Pontes in Physica»…"). It does return
  English for the English original, and never answers outside the list.
- **Jev's `Choice` makes no false rejections**, and its English probability is exactly
  0.00 for every correct text against 0.12–0.74 for the wrong ones in section 3, except
  `sr`.

## 5. Narrowed Choices With `Other`

Offering all 68 languages every time is wasteful, so [calibrate_jev.py](calibrate_jev.py)
asks once per text over all 67 targets + English + `Other` (69 options) and derives a
candidate list per target ([results/calib-jev-gpt-6-sol.jsonl](results/calib-jev-gpt-6-sol.jsonl)).
For target A, another language B is ranked by the larger of

- P(B | A's text): what A's text is mistaken for, and
- P(A | B's text): which texts are mistaken for A.

The second is the one the gate needs: a B text labelled A is only caught if B is an
option, otherwise its probability can land on A.

**Most languages have nothing to be confused with.** The API reports probabilities in 0.01
steps, and 48 of 67 targets drew 0.00 for every other language. A fixed top 5 filled with
alphabetical ties (Afrikaans, Arabic, …); the candidate list was changed to keep only
languages at 0.01 or above ([results/candidates-gpt-6-sol.json](results/candidates-gpt-6-sol.json)):

| Target | Added |
|---|---|
| hr | Serbian, Slovene |
| sl | Croatian, Latvian |
| ia | Esperanto, Italian |
| sr | Croatian |
| eo, it | Interlingua |
| lv | Slovene |
| da/no, es/fr, id/ms, fa/ur, kn/te, lo/th | each other |

The English original, over all 69, comes out **French 0.63, English 0.36** — the weakness
of section 3 again.

[gate_jev.py](gate_jev.py) then asks with the target's candidates + English + `Other`, and
flags P(target) < 0.5:

| Texts | Flagged | Lowest P(target) among the unflagged |
|---|---|---|
| the five mislabelled | all five | — |
| `bonsai2-27b`, 67 languages | `fi` only (English 1.00) | sr 0.64 (Croatian 0.30), de 0.73 (`Other` 0.27) |
| `gpt-6-sol`, 67 languages | none | sr 0.83 (Croatian 0.13), ia 0.87 (`Other` 0.10) |

- **`Other` takes what is not on the list.** French labelled German, Spanish labelled
  Portuguese and Japanese labelled Chinese, each asked over three options, go to `Other`
  at 1.00.
- **`sr`/`hr` is separated once Croatian is an option**: Croatian 0.96 for the text
  labelled Serbian. Every earlier form missed it.
- **The English original is caught, weakly**: English 0.66, French 0.32.
- **A collapsed translation is not a wrong-language one.** `bonsai2-27b`'s `cy`, gibberish
  that only looks Welsh (Jev score 3.4), is Welsh 1.00 here; the low score is the
  scoring's job. Its `fi`, which is the English source, is the one flagged.
- `bonsai2-27b`'s `sr` at 0.64 is the closest to the threshold on either side. Whether its
  text mixes in Croatian forms was not checked.

The first gate pass, with the padded top-5 lists, is kept as `results/gate-*-top5.jsonl`;
its results are the same (all five flagged, `fi` only). The padded list is not
reproducible from the current `calibrate_jev.py`.

## 6. Side Finding: ollama Ignores `format` Without Thinking

On ollama 0.30.6 with `qwen3.6`, a request with `"think": false` and a JSON schema in
`format` comes back as prose; the schema is ignored, streaming or not. With thinking on,
the schema is honoured. That is why [choose_qwen.py](choose_qwen.py) lists the options in
the prompt and reads a plain-text answer instead.

## 7. What Carries Forward

- **The check is a separate request**, not a sixth question in the scoring request: adding
  one changes `SCHEME_ID` and with it every score on disk.
- **Jev `Choice`**, options from `results/candidates-gpt-6-sol.json` + English + `Other`,
  flag below P(target) 0.5. Over 67 languages it costs seconds.
- **Untranslated output can also be caught without a model**, by comparing each line with
  the original's; it is the case Jev is weakest on, and the one that should certainly
  score 0.

Open:

1. Where it goes: a record per language beside `jev.jsonl`, and `trtools agg --jev`
   zeroing flagged languages — or only reporting them at first. Existing sets have no
   check results and need a pass over all of them.
2. The candidate table comes from one translator's texts. A pair that only shows up in
   another translator's output would be missing from it.
3. `bonsai2-27b`'s `sr` (0.64) and `de` (0.73) have not been read.

## 8. Files and Reproduction

Run from the repository root; `bash experimental/15/mislabel.sh` first, for the scripts
that read `mislabel/tr/` (gitignored, rebuilt from the corpus).

| File | Run as | Output |
|---|---|---|
| — | `uv run trtools jev examples/onde-en.txt --langs fr de pt zh sr --tr-dir experimental/15/mislabel/tr -o experimental/15/results/score-mislabel.jsonl` | `score-mislabel.jsonl` |
| [ask_qwen_yesno.py](ask_qwen_yesno.py) | `uv run python experimental/15/ask_qwen_yesno.py` | `probe-qwen-yesno.txt` (stdout) |
| [ask_jev_noul.py](ask_jev_noul.py) | `uv run python experimental/15/ask_jev_noul.py` | `probe-jev-noul.txt` (stdout) |
| [ask_jev_choice.py](ask_jev_choice.py) | `uv run python experimental/15/ask_jev_choice.py` | `probe-jev-choice.txt` (stdout) |
| [check_all.py](check_all.py) | `uv run python experimental/15/check_all.py {qwen,jev} [model]` | `check-{qwen,jev}-gpt-6-sol.jsonl` |
| [choose_qwen.py](choose_qwen.py) | `uv run python experimental/15/choose_qwen.py [model]` | `choose-qwen-gpt-6-sol.jsonl` |
| [calibrate_jev.py](calibrate_jev.py) | `uv run python experimental/15/calibrate_jev.py [model] [--agg]` | `calib-jev-gpt-6-sol.jsonl`, `candidates-gpt-6-sol.json` |
| [gate_jev.py](gate_jev.py) | `uv run python experimental/15/gate_jev.py <tr dir>` | `gate-{mislabel,bonsai2-27b,gpt-6-sol}.jsonl` |
| [narrow_qwen.py](narrow_qwen.py) | `uv run python experimental/15/narrow_qwen.py` | `narrow-qwen.jsonl` ([PORT.md](PORT.md) section 3.4) |
| [variants_jev.py](variants_jev.py) | `uv run python experimental/15/variants_jev.py [--table]` | `variants-jev.jsonl` ([PORT.md](PORT.md) section 3.5) |

Outputs are in [results/](results/). Jev is `jev-1.14.0` throughout; qwen3.6 runs on ollama
0.30.6 without thinking, at temperature 0.
