# Report: The Corpus on the Jev Scale

Step 2 of [PORT.md](PORT.md) section 7: all 16 translators × 67 languages on the Jev scale,
set beside the published old-evaluator numbers. It answers the questions that step was
set, and the slope's stability, and it turns up one thing none of them asked about: **Jev
penalises dropped speaker labels heavily, and the old evaluator barely notices them.**
That, not the middle band, is what moves the ranking.

**Status**: frozen, 2026-09-23. Section 4's question of size is not pursued: the deduction
for a lost label is accepted as it stands, as the corpus's speaker-tag policy
([examples/tr/README.md](../../examples/tr/README.md)) takes it.

Every number here comes from [report.py](report.py); its full output is the appendix.

```bash
uv run experimental/13/report.py
```

The old side is each model's `SCORES.txt`, whose totals are the sum of the five criteria's
medians ([PLAN.md](PLAN.md) section 7). The Jev side is `jev.jsonl` read through
`trtools agg --jev` and rounded to one decimal, as `SCORES-jev.txt` is.

## 1. Short Answers

| Question (PORT.md section 7, step 2) | Answer |
|---|---|
| Does Jev separate the top four? | **Into two pairs, not within them.** `gpt-5.6-luna` and `union-alpha` stay tied; `gemini-3.7-flash` drops to the bottom of the four |
| Does the middle band hold? | **Per translation, no band holds, and the middle is not the worst.** Per translator, the middle of the ranking reorders, and the cause is speaker labels (section 4) |
| Is the 0.69 slope stable enough to invert? | **No.** Over all 1,072 it is 0.508 fitted one way and 0.718 the other; the four-translator 0.69 falls between them |

## 2. The Top Four

Under the old evaluator the four sit within 2 median points (93 / 92 / 91 / 91). Under Jev,
`gpt-5.6-luna`, `union-alpha` and `ox-alpha` sit within 1.7 (88.1 / 87.6 / 86.4) and
`gemini-3.7-flash` is 3.7 behind them at 82.7.

Per language, pair by pair (Wilcoxon p on the paired differences):

| Pair | old | Jev |
|---|---|---|
| luna vs union | tie, p = 0.64 | tie, p = 0.52 |
| luna vs gemini-3.7 | luna, p = 0.0009 | luna, p = 1e-6 |
| union vs gemini-3.7 | union, p = 0.002 | union, p = 1e-7 |
| luna vs ox | luna, p = 5e-6 | luna, p = 0.003 |
| union vs ox | union, p = 3e-6 | union, p = 0.0002 |
| gemini-3.7 vs ox | gemini-3.7, p = 0.07 | **ox**, p = 0.02 |

- **luna vs union is a tie under both**, as README section 3.3 found. On the pair that
  matters most, the answer is no (PORT.md section 8 item 2).
- Jev separates both of them from `gemini-3.7-flash` more strongly than the old evaluator
  (dz +0.58 / +0.76 against +0.38 / +0.31), and from `ox-alpha` about as strongly or less.
- **The bottom pair swaps.** Part of `gemini-3.7-flash`'s fall is section 4: 23 of its
  translations lose a speaker label, against `ox-alpha`'s 5.

## 3. The Middle Band

**Per translation.** Spearman between the two scales, inside bands of the old score:

| Old band | n | Spearman | sd old | sd jev |
|---|---:|---:|---:|---:|
| all | 1072 | +0.81 | 25.5 | 15.4 |
| 0–59 | 308 | +0.75 | 14.5 | 15.9 |
| 60–69 | 91 | +0.21 | 2.9 | 6.3 |
| 70–79 | 138 | +0.07 | 2.8 | 6.6 |
| 80–89 | 205 | +0.18 | 3.1 | 7.3 |
| 90–100 | 330 | +0.39 | 2.5 | 6.8 |

Inside any ten-point band of the old score the two evaluators barely agree — and that
includes the top band, whose range is as narrow as the middle's. README section 4.2's
warning generalises: the corpus-wide +0.81 is mostly range. The middle is not uniquely
worse, which is the question PORT.md asked; but nothing here says which evaluator's
within-band ordering is right, and the answer is not "the middle holds" either.

**Per translator.** The ranking moves in the middle (Spearman over the 16 means +0.84):

| Translator | old mean | Jev mean | rank old → Jev (by median) |
|---|---:|---:|---|
| gemini-2.5-flash | 81.67 | 71.65 | 7 → 12 |
| gemini-3-flash | 78.07 | 69.54 | 5 → 13 |
| gpt-5.6-terra | 77.79 | 75.95 | 6 → 8 |
| gpt-oss | 64.97 | 64.52 | 12 → 15 |
| gemma4-31b | 66.69 | 75.60 | 8 → 5 |
| gemma4 | 68.22 | 75.65 | 9 → 6 |
| muse-glimmer | 63.63 | 70.89 | 13 → 7 |

Jev compresses the scale towards its middle, so the top falls and the bottom rises. Against
that, `gemini-2.5-flash` and `gemini-3-flash` fall far further than the top four (−10.0 and
−8.5 in mean, against −1.1 to −4.9), `gpt-5.6-terra` loses 11 points of median, and
`gpt-oss`, which the compression should lift, does not move. These four are the ones whose
`information_completeness` falls furthest (−2.2 to −4.1 points out of 20, against −0.6 to
−1.7 for the top four), and section 4 is why.

## 4. Speaker Labels

Every line of the original starts with `Camille:` or `Luc:`, and the label is not left to
the translator: `examples/tr/terms/onde-en.tsv` gives both names in every language, and
the translators were handed it. A missing or wrong label is a translation defect, not a
matter of interpretation. Some translators drop it anyway, mostly on short turns:

```
Luc: Okay.          ->  Ok.             (gpt-oss, it, line 14)
Camille: That's the irrefutable experimental proof. ...
                    ->  Das ist der unwiderlegbare experimentelle Beweis. ...
                                        (gemini-3.7-flash, de, line 25)
```

The second one is not cosmetic: the line before is Luc's, so without the label the
reader gives Camille's line to Luc.

Each line is checked against the speaker of the original's line *i* and the glossary's
name for that speaker, and falls in one of four classes:

| Class | What the line does | Speaker |
|---|---|---|
| `dropped` | starts with no label at all | lost |
| `swapped` | names the other speaker | wrong |
| `mixed-script` | a label whose name mixes writing systems: `Λυկ:` in Greek, `קמիլ:` in Hebrew | readable |
| `off-glossary` | a label spelled otherwise than the glossary: `Camille:` in Hindi, `Камил:` where it says `Camille` | readable |

Against `information_completeness`, splitting each translator's languages by whether any
line is `dropped` or `swapped`:

| Translator | languages | dropped | swapped | IC old | IC Jev | Jev, intact | Jev, lost |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 0 | 0 | 0 | 19.3 | 18.2 | 18.2 | — |
| union-alpha | 1 | 1 | 0 | 19.2 | 18.5 | 18.5 | 15.3 |
| gemini-3.7-flash | 23 | 22 | 5 | 18.9 | 17.3 | 18.4 | 15.0 |
| ox-alpha | 5 | 7 | 0 | 18.8 | 18.2 | 18.4 | 15.5 |
| gemini-2.5-flash | 65 | 700 | 11 | 18.1 | 14.0 | 18.7 | 13.8 |
| gemini-3-flash | 66 | 358 | 5 | 17.0 | 13.1 | — | 13.1 |
| gpt-5.6-terra | 41 | 58 | 6 | 17.0 | 14.8 | 16.5 | 13.8 |
| gpt-oss | **67** | 998 | 13 | 15.1 | 12.2 | — | 12.2 |

- **The four translators that fall are the four that lose labels in most languages.**
  Over the 1,071 aligned translations, the number of lost labels correlates with Jev's IC
  at Spearman −0.57 and with the old evaluator's at −0.12.
- **Within a translator, one lost label costs about three IC points.** `union-alpha`,
  `gemini-3.7-flash` and `ox-alpha` lose one or two lines where they lose any, and their
  IC falls from about 18.4 to about 15.3. The gap is inside each translator, so it is not
  good translators against bad.
- Pooled, the old evaluator's IC is 15.7 with lost labels and 15.6 without: it does not
  see them. Jev's is 13.1 and 16.2.
- **`off-glossary` is not what Jev penalises.** `qwen3.6-27b` writes 360 of its lines
  under names the glossary does not give (`Kamija:`, `Kamili:`, `Камил:`) and loses
  none; its IC rises by 1.1 like its neighbours'. Jev is not shown the glossary —
  `build_state` holds the two texts and nothing else — so it could not know the
  prescribed spelling if it tried.

So Jev's direction is right, and the only open question is size: whether three points out
of twenty is proportionate for one line in 99. That is a calibration question, not a
defect, and it does not need settling before step 3. **Not pursued:** the deduction is
accepted as it stands.

The glossary check is also a better yardstick for this than any evaluator: it is exact
for `dropped` and `swapped`, costs nothing, and sees `off-glossary`, which Jev cannot.
Its limits: a label spelled in some way the translation does not use consistently can
only be `off-glossary` or `mixed-script`, never `swapped`, and a handful of one-word
Armenian sentences (`Ճշտորեն.`, "exactly") read as labels because Armenian separates
names with a full stop. `gemini-3-flash`'s 18-line `eu` is left out, since its lines no
longer align with the original's.

## 5. The Other Direction

The largest divergences the other way — old far below Jev — are the old evaluator's
floor, which PORT.md section 8 item 3 already flags. One was checked:
`gpt-5.6-terra`'s `hr` scores **9** under the old evaluator and **66.7** under Jev. Its
line 23 is leaked model reasoning (`Camಿಕೆassistant to=python? no. Need translate …`);
the other 98 lines are clean. The old evaluator's three runs gave it all zeros once and
1–4 per criterion twice. Jev's score is closer to one bad line in 99. One case, not a
pattern — but it is the same kind of case as `union-alpha`'s `ga`, which README
section 5.4 traces to three old runs of 21, 42 and 31.

## 6. Spread

Four translators barely vary under Jev: `gpt-oss`, `gemini-3-flash`, `gemini-2.5-flash`
and `gpt-5.6-terra` have pstdev 5.5–6.3, and 52–63 of their 67 languages land in 60–79.
All four are section 4's label droppers; a penalty that applies to nearly every language
pins them in a band. For a yardstick whose point is the tail ([PLAN.md](PLAN.md)
section 1), this hides which of their languages are weak for other reasons. The glossary
check separates the two: it counts the labels, so the Jev score need not be read for
them.

## 7. The Slope and the Tiers

Least squares over all 1,072 gives `jev = 0.508 × old + 37.1` (r = 0.84); regressing the
other way and inverting gives 0.718. The two bracket any symmetric fit, and the
four-translator 0.69 falls between them. PORT.md section 5.2's mapped cuts (86.8 / 79.9 / 66.1)
depend on which fit is chosen, so they should not be quoted as a conversion. The decision
it rests on — keep 90 / 80 / 60 — does not depend on them.

What the unchanged cuts do: at 90+, the top four go from 37–48 languages to 13–22; the
tier counts per translator are in the appendix.

## 8. For Step 3

Nothing here blocks step 3.

One change belongs to step 3 itself: `generate_compare_rows.py` parses `SCORES.txt` as
integers (`LINE_RE`, `int()`), and must accept one decimal before step 3 switches the file
over.

---

## Appendix: `report.py` Output
Computed from `SCORES.txt` and `jev.jsonl` for 16 translators x 67 languages = 1072 translations.

### Per Translator

Five-number summary as `generate_compare_rows.py graph` draws it (whiskers at 1.5 IQR), and the tier counts at the unchanged 90 / 80 / 60 cuts.

| Translator | scale | mean | min | q1 | median | q3 | max | pstdev | 90+ | 80-89 | 60-79 | <60 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gemma4 | old | 68.22 | 9.0 | 51.5 | 76.0 | 91.0 | 100.0 | 26.04 | 19 | 10 | 17 | 21 |
|  | jev | 75.65 | 54.5 | 72.3 | 78.5 | 86.1 | 94.3 | 14.69 | 4 | 27 | 29 | 7 |
| gemma4-31b | old | 66.69 | 11.0 | 34.0 | 77.0 | 93.5 | 98.0 | 29.61 | 26 | 6 | 11 | 24 |
|  | jev | 75.60 | 37.2 | 65.2 | 80.6 | 88.2 | 94.7 | 15.52 | 11 | 24 | 20 | 12 |
| gpt-oss | old | 64.97 | 23.0 | 52.0 | 67.0 | 79.5 | 98.0 | 19.10 | 7 | 10 | 25 | 25 |
|  | jev | 64.52 | 50.7 | 60.9 | 65.2 | 67.8 | 77.8 | 5.50 | 0 | 0 | 56 | 11 |
| qwen3.6-27b | old | 62.97 | 25.0 | 39.5 | 68.0 | 77.5 | 99.0 | 22.02 | 10 | 4 | 28 | 25 |
|  | jev | 71.47 | 46.2 | 64.3 | 72.9 | 79.9 | 92.9 | 11.08 | 1 | 16 | 38 | 12 |
| qwen3.6 | old | 58.27 | 18.0 | 34.5 | 55.0 | 79.0 | 97.0 | 24.24 | 8 | 9 | 16 | 34 |
|  | jev | 69.88 | 42.1 | 60.9 | 71.5 | 79.7 | 93.0 | 12.76 | 1 | 15 | 36 | 15 |
| qwen3.8 | old | 53.88 | 14.0 | 30.5 | 53.0 | 77.0 | 98.0 | 25.34 | 8 | 6 | 12 | 41 |
|  | jev | 66.47 | 38.0 | 55.5 | 69.8 | 77.6 | 94.2 | 15.06 | 3 | 10 | 29 | 25 |
| bonsai2-27b | old | 27.97 | 0.0 | 12.5 | 24.0 | 33.0 | 59.0 | 23.98 | 4 | 1 | 1 | 61 |
|  | jev | 40.16 | 2.6 | 26.1 | 38.5 | 53.1 | 90.2 | 21.05 | 1 | 0 | 12 | 54 |
| muse-glimmer | old | 63.63 | 16.0 | 44.0 | 67.0 | 82.0 | 96.0 | 21.51 | 6 | 13 | 22 | 26 |
|  | jev | 70.89 | 40.6 | 64.4 | 74.1 | 80.6 | 93.1 | 13.74 | 3 | 14 | 36 | 14 |
| ox-alpha | old | 85.90 | 62.0 | 80.0 | 91.0 | 94.5 | 97.0 | 11.51 | 38 | 14 | 13 | 2 |
|  | jev | 84.79 | 70.8 | 81.5 | 86.4 | 89.4 | 95.9 | 6.46 | 14 | 38 | 15 | 0 |
| union-alpha | old | 90.18 | 78.0 | 88.0 | 92.0 | 95.0 | 98.0 | 9.39 | 48 | 15 | 3 | 1 |
|  | jev | 86.86 | 75.6 | 84.5 | 87.6 | 90.5 | 94.6 | 5.10 | 18 | 43 | 6 | 0 |
| gpt-5.6-luna | old | 90.39 | 79.0 | 88.0 | 93.0 | 96.0 | 100.0 | 8.13 | 44 | 17 | 6 | 0 |
|  | jev | 86.16 | 71.2 | 82.3 | 88.1 | 90.9 | 93.0 | 5.79 | 22 | 37 | 8 | 0 |
| gpt-5.6-terra | old | 77.79 | 41.0 | 71.0 | 85.0 | 91.5 | 98.0 | 20.15 | 27 | 13 | 15 | 12 |
|  | jev | 75.95 | 63.4 | 71.5 | 74.0 | 79.7 | 91.5 | 6.33 | 5 | 10 | 52 | 0 |
| gemini-3.5-flash-lite | old | 65.94 | 20.0 | 49.0 | 69.0 | 85.5 | 97.0 | 22.40 | 12 | 12 | 19 | 24 |
|  | jev | 71.09 | 54.2 | 67.4 | 71.3 | 76.4 | 84.5 | 7.57 | 1 | 6 | 53 | 7 |
| gemini-2.5-flash | old | 81.67 | 60.0 | 76.5 | 84.0 | 89.5 | 97.0 | 10.34 | 17 | 25 | 23 | 2 |
|  | jev | 71.65 | 61.7 | 67.5 | 71.2 | 75.1 | 85.1 | 5.73 | 1 | 3 | 63 | 0 |
| gemini-3-flash | old | 78.07 | 60.0 | 75.0 | 85.0 | 90.0 | 98.0 | 19.95 | 19 | 29 | 10 | 9 |
|  | jev | 69.54 | 57.8 | 67.1 | 69.9 | 73.8 | 79.3 | 5.77 | 0 | 0 | 61 | 6 |
| gemini-3.7-flash | old | 87.52 | 63.0 | 81.5 | 91.0 | 95.0 | 98.0 | 10.12 | 37 | 21 | 8 | 1 |
|  | jev | 82.62 | 64.8 | 77.5 | 82.7 | 89.4 | 94.5 | 7.53 | 13 | 29 | 25 | 0 |

### Ranking

By `(median, pstdev)`, the order `generate_compare_rows.py` sorts the chart in.

| # | old | median | jev | median |
|---:|---|---:|---|---:|
| 1 | gpt-5.6-luna | 93.0 | gpt-5.6-luna | 88.1 |
| 2 | union-alpha | 92.0 | union-alpha | 87.6 |
| 3 | gemini-3.7-flash | 91.0 | ox-alpha | 86.4 |
| 4 | ox-alpha | 91.0 | gemini-3.7-flash | 82.7 |
| 5 | gemini-3-flash | 85.0 | gemma4-31b | 80.6 |
| 6 | gpt-5.6-terra | 85.0 | gemma4 | 78.5 |
| 7 | gemini-2.5-flash | 84.0 | muse-glimmer | 74.1 |
| 8 | gemma4-31b | 77.0 | gpt-5.6-terra | 74.0 |
| 9 | gemma4 | 76.0 | qwen3.6-27b | 72.9 |
| 10 | gemini-3.5-flash-lite | 69.0 | qwen3.6 | 71.5 |
| 11 | qwen3.6-27b | 68.0 | gemini-3.5-flash-lite | 71.3 |
| 12 | gpt-oss | 67.0 | gemini-2.5-flash | 71.2 |
| 13 | muse-glimmer | 67.0 | gemini-3-flash | 69.9 |
| 14 | qwen3.6 | 55.0 | qwen3.8 | 69.8 |
| 15 | qwen3.8 | 53.0 | gpt-oss | 65.2 |
| 16 | bonsai2-27b | 24.0 | bonsai2-27b | 38.5 |

Over the 16 translators' means: Spearman +0.835, Kendall +0.700.

### The Top Four, Pairwise

Per language, first minus second. `agree` counts the languages where both scales take a side and it is the same side.

| Pair | scale | mean Δ | median Δ | win / loss / tie | sign p | Wilcoxon p | dz | agree |
|---|---|---:|---:|---|---:|---:|---:|---|
| gpt-5.6-luna vs union-alpha | old | +0.21 | +0.0 | 32 / 22 / 13 | 0.22 | 0.64 | +0.02 |  |
|  | jev | -0.70 | -0.3 | 31 / 36 / 0 | 0.63 | 0.52 | -0.17 | 38 / 54 |
| gpt-5.6-luna vs gemini-3.7-flash | old | +2.87 | +2.0 | 39 / 16 / 12 | 0.0027 | 0.00087 | +0.38 |  |
|  | jev | +3.53 | +2.3 | 54 / 13 / 0 | 4.5e-07 | 1e-06 | +0.58 | 41 / 55 |
| gpt-5.6-luna vs ox-alpha | old | +4.49 | +2.0 | 48 / 13 / 6 | 7.7e-06 | 5.1e-06 | +0.62 |  |
|  | jev | +1.36 | +1.4 | 46 / 21 / 0 | 0.0031 | 0.0028 | +0.27 | 46 / 61 |
| union-alpha vs gemini-3.7-flash | old | +2.66 | +2.0 | 40 / 20 / 7 | 0.013 | 0.002 | +0.31 |  |
|  | jev | +4.24 | +2.8 | 51 / 16 / 0 | 2.2e-05 | 1.4e-07 | +0.76 | 42 / 60 |
| union-alpha vs ox-alpha | old | +4.28 | +2.0 | 46 / 14 / 7 | 4.2e-05 | 2.6e-06 | +0.44 |  |
|  | jev | +2.07 | +1.1 | 44 / 21 / 2 | 0.0059 | 0.00016 | +0.51 | 40 / 58 |
| gemini-3.7-flash vs ox-alpha | old | +1.63 | +1.0 | 36 / 24 / 7 | 0.16 | 0.073 | +0.18 |  |
|  | jev | -2.17 | -0.8 | 27 / 39 / 1 | 0.18 | 0.019 | -0.35 | 39 / 60 |

### Agreement by the Old Score's Band

Translation level, pooled over every translator. `sd` is the population standard deviation of each scale inside the band: correlation falls with range whatever the evaluator is doing (README section 4.2).

| Old band | n | Pearson | Spearman | Kendall | sd old | sd jev |
|---|---:|---:|---:|---:|---:|---:|
| all | 1072 | +0.841 | +0.811 | +0.631 | 25.53 | 15.41 |
| 0-59 | 308 | +0.788 | +0.753 | +0.569 | 14.45 | 15.88 |
| 60-69 | 91 | +0.231 | +0.207 | +0.147 | 2.91 | 6.27 |
| 70-79 | 138 | +0.075 | +0.065 | +0.046 | 2.82 | 6.57 |
| 80-89 | 205 | +0.199 | +0.176 | +0.131 | 3.14 | 7.33 |
| 90-100 | 330 | +0.362 | +0.387 | +0.284 | 2.51 | 6.83 |

### Agreement per Translator

| Translator | old mean | Pearson | Spearman | Kendall | sd old | sd jev |
|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 90.39 | +0.634 | +0.688 | +0.507 | 8.13 | 5.79 |
| union-alpha | 90.18 | +0.642 | +0.707 | +0.546 | 9.39 | 5.10 |
| gemini-3.7-flash | 87.52 | +0.554 | +0.560 | +0.410 | 10.12 | 7.53 |
| ox-alpha | 85.90 | +0.653 | +0.755 | +0.584 | 11.51 | 6.46 |
| gemini-2.5-flash | 81.67 | +0.494 | +0.517 | +0.372 | 10.34 | 5.73 |
| gemini-3-flash | 78.07 | +0.773 | +0.655 | +0.490 | 19.95 | 5.77 |
| gpt-5.6-terra | 77.79 | +0.529 | +0.627 | +0.460 | 20.15 | 6.33 |
| gemma4 | 68.22 | +0.848 | +0.828 | +0.655 | 26.04 | 14.69 |
| gemma4-31b | 66.69 | +0.892 | +0.889 | +0.713 | 29.61 | 15.52 |
| gemini-3.5-flash-lite | 65.94 | +0.754 | +0.784 | +0.582 | 22.40 | 7.57 |
| gpt-oss | 64.97 | +0.680 | +0.640 | +0.470 | 19.10 | 5.50 |
| muse-glimmer | 63.63 | +0.879 | +0.879 | +0.713 | 21.51 | 13.74 |
| qwen3.6-27b | 62.97 | +0.852 | +0.855 | +0.681 | 22.02 | 11.08 |
| qwen3.6 | 58.27 | +0.875 | +0.898 | +0.717 | 24.24 | 12.76 |
| qwen3.8 | 53.88 | +0.930 | +0.942 | +0.799 | 25.34 | 15.06 |
| bonsai2-27b | 27.97 | +0.912 | +0.940 | +0.812 | 23.98 | 21.05 |

### Per Criterion

Mean points out of 20 over all languages; Δ is Jev minus old.

| Translator | readability old | jev | Δ | fluency old | jev | Δ | terminology old | jev | Δ | contextual old | jev | Δ | information old | jev | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 18.0 | 18.0 | -0.0 | 17.2 | 15.4 | -1.8 | 17.7 | 17.4 | -0.4 | 18.2 | 17.2 | -1.0 | 19.3 | 18.2 | -1.0 |
| union-alpha | 18.0 | 18.1 | +0.1 | 17.1 | 15.4 | -1.7 | 17.7 | 17.5 | -0.2 | 18.2 | 17.3 | -0.9 | 19.2 | 18.5 | -0.7 |
| gemini-3.7-flash | 17.4 | 17.2 | -0.2 | 16.5 | 14.7 | -1.8 | 17.0 | 17.0 | -0.0 | 17.7 | 16.4 | -1.2 | 18.9 | 17.3 | -1.7 |
| ox-alpha | 17.1 | 17.7 | +0.6 | 16.0 | 14.8 | -1.1 | 16.8 | 17.2 | +0.4 | 17.2 | 16.9 | -0.3 | 18.8 | 18.2 | -0.6 |
| gemini-2.5-flash | 16.0 | 14.9 | -1.1 | 15.0 | 12.6 | -2.3 | 16.3 | 16.0 | -0.3 | 16.3 | 14.1 | -2.2 | 18.1 | 14.0 | -4.1 |
| gemini-3-flash | 15.1 | 14.3 | -0.7 | 14.4 | 12.6 | -1.8 | 15.9 | 15.9 | -0.0 | 15.8 | 13.7 | -2.1 | 17.0 | 13.1 | -3.9 |
| gpt-5.6-terra | 14.5 | 15.7 | +1.2 | 14.0 | 14.1 | +0.1 | 16.3 | 16.3 | +0.0 | 15.9 | 15.0 | -1.0 | 17.0 | 14.8 | -2.2 |
| gemma4 | 13.4 | 15.7 | +2.3 | 12.3 | 13.0 | +0.7 | 13.4 | 15.8 | +2.4 | 13.6 | 14.9 | +1.3 | 15.6 | 16.3 | +0.7 |
| gemma4-31b | 13.2 | 15.6 | +2.4 | 12.2 | 13.0 | +0.8 | 13.3 | 15.8 | +2.5 | 13.2 | 14.8 | +1.5 | 14.8 | 16.5 | +1.7 |
| gemini-3.5-flash-lite | 12.7 | 14.8 | +2.1 | 11.7 | 12.8 | +1.1 | 13.8 | 15.5 | +1.7 | 13.2 | 13.8 | +0.6 | 14.6 | 14.2 | -0.3 |
| gpt-oss | 12.2 | 13.2 | +1.0 | 11.5 | 11.2 | -0.3 | 13.4 | 15.4 | +2.1 | 12.8 | 12.6 | -0.2 | 15.1 | 12.2 | -2.9 |
| muse-glimmer | 12.3 | 14.6 | +2.3 | 11.0 | 11.6 | +0.6 | 12.7 | 15.2 | +2.6 | 12.6 | 13.9 | +1.3 | 15.0 | 15.5 | +0.4 |
| qwen3.6-27b | 12.4 | 15.0 | +2.5 | 11.1 | 12.0 | +0.9 | 12.6 | 15.1 | +2.5 | 12.4 | 13.9 | +1.5 | 14.4 | 15.5 | +1.1 |
| qwen3.6 | 11.4 | 14.4 | +3.0 | 10.3 | 11.6 | +1.3 | 11.6 | 14.8 | +3.2 | 11.4 | 13.6 | +2.2 | 13.6 | 15.5 | +1.9 |
| qwen3.8 | 10.7 | 13.8 | +3.1 | 9.3 | 11.0 | +1.7 | 10.8 | 14.3 | +3.5 | 10.5 | 12.8 | +2.3 | 12.5 | 14.5 | +1.9 |
| bonsai2-27b | 5.5 | 8.0 | +2.6 | 4.7 | 6.0 | +1.3 | 6.0 | 9.7 | +3.6 | 5.3 | 7.4 | +2.1 | 6.4 | 9.0 | +2.6 |

### Speaker Labels

Every line of the original starts with `Camille:` or `Luc:`, and the translators were given each language's rendering of both names in `examples/tr/terms/onde-en.tsv`. Lines per class over all languages; a language counts under `languages` if any of its lines is dropped or swapped. IC is `information_completeness` in points out of 20, and the last two columns split Jev's by the same test, within one translator.

| Translator | languages | dropped | swapped | mixed-script | off-glossary | unaligned | IC old | IC jev | IC Δ | IC jev, intact | IC jev, lost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 0 | 0 | 0 | 1 | 0 | 0 | 19.3 | 18.2 | -1.0 | 18.2 |  |
| union-alpha | 1 | 1 | 0 | 0 | 0 | 0 | 19.2 | 18.5 | -0.7 | 18.5 | 15.3 |
| gemini-3.7-flash | 23 | 22 | 5 | 0 | 0 | 0 | 18.9 | 17.3 | -1.7 | 18.4 | 15.0 |
| ox-alpha | 5 | 7 | 0 | 0 | 1 | 0 | 18.8 | 18.2 | -0.6 | 18.4 | 15.5 |
| gemini-2.5-flash | 65 | 700 | 11 | 0 | 93 | 0 | 18.1 | 14.0 | -4.1 | 18.7 | 13.8 |
| gemini-3-flash | 66 | 358 | 5 | 0 | 0 | 1 | 17.0 | 13.1 | -3.9 |  | 13.1 |
| gpt-5.6-terra | 41 | 58 | 6 | 28 | 12 | 0 | 17.0 | 14.8 | -2.2 | 16.5 | 13.8 |
| gemma4 | 7 | 53 | 0 | 0 | 297 | 0 | 15.6 | 16.3 | +0.7 | 16.7 | 12.8 |
| gemma4-31b | 0 | 0 | 0 | 0 | 0 | 0 | 14.8 | 16.5 | +1.7 | 16.5 |  |
| gemini-3.5-flash-lite | 37 | 28 | 45 | 3 | 132 | 0 | 14.6 | 14.2 | -0.3 | 15.4 | 13.2 |
| gpt-oss | 67 | 998 | 13 | 0 | 369 | 0 | 15.1 | 12.2 | -2.9 |  | 12.2 |
| muse-glimmer | 21 | 16 | 27 | 0 | 216 | 0 | 15.0 | 15.5 | +0.4 | 16.5 | 13.1 |
| qwen3.6-27b | 0 | 0 | 0 | 0 | 360 | 0 | 14.4 | 15.5 | +1.1 | 15.5 |  |
| qwen3.6 | 1 | 1 | 0 | 0 | 573 | 0 | 13.6 | 15.5 | +1.9 | 15.6 | 9.1 |
| qwen3.8 | 12 | 309 | 5 | 0 | 1 | 0 | 12.5 | 14.5 | +1.9 | 15.1 | 11.9 |
| bonsai2-27b | 6 | 60 | 1 | 0 | 216 | 0 | 6.4 | 9.0 | +2.6 | 9.5 | 4.6 |

Over the 1071 aligned translations, Spearman between lost labels and IC: old -0.121, Jev -0.570.
- intact: n = 719, IC old 15.62, Jev 16.23
- lost: n = 352, IC old 15.71, Jev 13.12

### The Slope

Least squares over all 1072: `jev = 0.508 × old + 37.05`, r = 0.841. The old tier cuts map to 60 -> 67.5, 80 -> 77.7, 90 -> 82.7.
Regressing the other way and inverting gives slope 0.718; the two bracket the line a symmetric fit would draw, and differ because r < 1.

### Largest Divergences

The 15 translations whose old score most exceeds its Jev score, then the 15 the other way.

| Translator | lang | old | jev | old − jev |
|---|---|---:|---:|---:|
| gpt-oss | it | 95 | 65.6 | +29.4 |
| gpt-oss | ca | 96 | 69.4 | +26.6 |
| gpt-oss | vi | 93 | 67.0 | +26.0 |
| gpt-5.6-terra | hu | 96 | 70.8 | +25.2 |
| gpt-oss | pt | 90 | 65.3 | +24.7 |
| gemini-2.5-flash | pt | 94 | 69.4 | +24.6 |
| gemini-3-flash | bg | 94 | 70.3 | +23.7 |
| gpt-5.6-terra | af | 95 | 71.5 | +23.5 |
| gemini-3-flash | ca | 98 | 74.8 | +23.2 |
| gpt-5.6-terra | es | 97 | 74.0 | +23.0 |
| gemini-3-flash | hu | 89 | 66.1 | +22.9 |
| gpt-oss | ja | 94 | 71.2 | +22.8 |
| gemini-3-flash | vi | 97 | 74.2 | +22.8 |
| gemini-3-flash | pt | 95 | 72.2 | +22.8 |
| gemini-2.5-flash | ka | 92 | 69.2 | +22.8 |
| gpt-5.6-terra | hr | 9 | 66.7 | -57.7 |
| gpt-5.6-terra | nl | 24 | 72.5 | -48.5 |
| gemma4 | my | 34 | 79.2 | -45.2 |
| gemma4-31b | eo | 40 | 84.1 | -44.1 |
| union-alpha | ga | 29 | 71.7 | -42.7 |
| gemma4 | si | 32 | 73.8 | -41.8 |
| gemma4 | eo | 31 | 72.4 | -41.4 |
| gemma4 | th | 46 | 87.1 | -41.1 |
| gemma4-31b | ml | 17 | 57.0 | -40.0 |
| gemini-3.5-flash-lite | si | 20 | 59.8 | -39.8 |
| gpt-5.6-terra | cy | 32 | 71.4 | -39.4 |
| gemini-3-flash | bn | 16 | 55.1 | -39.1 |
| gemini-3-flash | ga | 27 | 66.0 | -39.0 |
| qwen3.6-27b | et | 32 | 70.5 | -38.5 |
| gemma4-31b | ka | 12 | 50.4 | -38.4 |
