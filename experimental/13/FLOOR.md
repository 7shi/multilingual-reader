# Floor: Is Jev's Ordering Below the Old Scheme's Zero Real?

Closes [README.md](README.md) section 7 item 1 and [PORT.md](PORT.md) section 8 item 3. The
old evaluator scores 10 of `bonsai2-27b`'s translations a flat 0; Jev spreads them out.
This checks whether that spread is information or invention by reading the ten
translations against the source.

**Answer: real, as a coarse order.** Jev's order follows how much of the dialogue each
translation carries before it collapses, and the one pair out of order trades length for
accuracy. Between translations that carry about the same amount, the gap is not an order.

## The Ten

The Jev column is the corpus run's `SCORES-jev.txt` (section 4.4 quotes the experiment's own
run, which put `id` at 31.2). "Usable lines" counts source lines, of 99, that the
translation renders in the target language with the meaning recognisably intact, errors
allowed, by reading.

| Lang | Jev | Usable lines | What the file is |
|---|---:|---:|---|
| cy | 2.6 | 0 | Welsh-looking words without meaning from line 1; repetition loops (`i'n gyfner`, `i'n gyntaf`) from line 6; bare speaker names from line 14 |
| fi | 3.8 | 0 | No Finnish at all: lines 1–6 are the English source, the last of them cut mid-sentence; bare speaker names after that |
| sw | 9.6 | 5 | Lines 1–4 and 6 translated with errors, a fragment of line 9; bare speaker names after that |
| th | 13.3 | 5 | Lines 1, 3, 4, 6 and 12, then one- or two-syllable stubs; from line 63 every line is a run of about 500 `B`s, which is the file's size |
| sl | 14.9 | 17 | Lines 1–17 with errors, some of them Czech (`Jsem`); fragments to line 27 |
| sk | 17.1 | 23 | Lines 1–25 with one left in English (line 6); fragments to line 37 |
| ia | 18.1 | 28 | Lines 1–28 in Interlingua heavily mixed with Italian, Spanish and French forms; fragments to line 56 |
| cs | 23.7 | 40 | Lines 1–43 with light errors, the last few cut short; stubs to line 48 |
| hr | 26.6 | 55 | Lines 1–59, with more lexical errors than `cs` and one Cyrillic word; stubs to line 78 |
| id | 30.7 | 43 | Lines 1–42 and 56, the cleanest of the ten; nothing else |

## Reading It

- **The order is coverage.** Sorted by usable lines, the ten fall into the same order as
  Jev's, except `hr` and `id`. Jev reads every one of these as a failure — no criterion
  averages above level 2 — and ranks the failures by how far they get.
- **`hr` against `id` is a trade, not an error.** `hr` carries more of the dialogue and
  `id` carries less but renders it better; Jev weights accuracy here, a reader weighting
  coverage would swap them. Either order is defensible, and the 4-point gap is small.
- **Between translations of similar coverage, the gap is not an order.** `cy` and `fi`
  both carry nothing in the target language, one as gibberish and the other as the
  untranslated source, and sit 1.2 apart. `sw` and `th` carry the same few lines, and the gap between
  them is 3.7. `sl`, `sk` and `ia` step by 2 and 1 points over 17, 23 and 28 lines, which
  is monotone but thin.
- **What it does not show** is anything above the floor: this is one translator's
  collapses, where the differences are large and visible without knowing the language
  well. It supports reading Jev's order among collapsed translations as a coverage order,
  not reading a 1-point difference among them.

## How It Was Checked

Read by Claude, not by native speakers. That is enough here because what separates these
translations is coarse — whether a line is in the target language and carries the source's
meaning at all — not the fine judgments the evaluator makes above the floor.
