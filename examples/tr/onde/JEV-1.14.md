# Jev 1.14.0

`jev-1.14.0` replaced `jev-1.13.0` as `DEFAULT_MODEL` in
[trtools/jev.py](../../../trtools/jev.py) on 2026-10-17. Every set evaluated by 1.13.0 was
evaluated again on the same scheme (`degrees@f518286e`), so the two versions differ only in
the model. [JEV.md](JEV.md) is the record of the first run, under 1.13.0.

## Layout

Each set keeps its previous version's files, frozen, in a `jev-1.13.0/` directory beside
the current ones:

| Set | Moved into `jev-1.13.0/` |
| --- | --- |
| `onde/{model}/` | `jev.jsonl`, `SCORES-jev.txt`, `TREND-jev.jsonl` |
| [core/](../core/README.md), [fr/](../fr/README.md) | `jev-{topic}.jsonl`, `SCORES-jev.txt` |
| [examples/evals/](../../evals/README.md) | `jev-{topic}-{src}.jsonl`, `SCORES-jev.txt` |

The current file names always mean the pinned version, so nothing that reads them changed:
the Makefiles, `generate_compare_rows.py` and `plot_comparison.py` follow the new version
as they are. The archive is not evaluated again; it is the record of what 1.13.0 said, and
the comparison with 1.14.0 is made once, on identical translations. `trtools agg --jev`
still reads it, e.g. `uv run trtools agg --jev --prefix onde gemma4/jev-1.13.0/jev.jsonl`.

`trtools jev` now refuses a file holding another version's records. Before this, it
checked only the scheme, so bumping `DEFAULT_MODEL` alone would have counted every language
as done and left the old judgments in place.

## Run

| Set | Evaluations | Input | Output | `seconds` 1.13 → 1.14 |
| --- | ---: | ---: | ---: | ---: |
| `onde/` (29 models × 67 languages) | 1,943 | 13,518,850 | 161,269 | 538.0 → 424.0 |
| `core/` | 15 | 74,730 | 1,245 | 4.4 → 3.0 |
| `fr/` | 8 | 39,816 | 664 | 2.4 → 1.9 |
| `examples/evals/` | 20 | 103,499 | 1,660 | 6.0 → 4.4 |
| Total | 1,986 | 13,736,895 | 164,838 | 550.8 → 433.4 |

Billed $0.5769, input only (about $0.042 per million tokens), matching the 44 `usage.jsonl`
entries of the run. Wall time 9m15s for the whole batch, including aggregation, the trend
rebuild and `make sync compare`. Input and output tokens are identical to 1.13.0's record
for record: the inputs did not change, and neither did their tokenization.

## Agreement with 1.13.0

Agreement is on the most probable level of each criterion, five per evaluation.

| Set | Level agreement | Up | Down | Total change, mean (sd) | Pearson | Mean confidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `onde/` | 8,344/9,715 (85.9%) | 908 | 463 | +0.69 (2.50) | 0.991 | 0.586 → 0.555 |
| `core/` | 65/75 (86.7%) | 9 | 1 | +0.54 (1.23) | 0.972 | 0.628 → 0.624 |
| `fr/` | 37/40 (92.5%) | 2 | 1 | +1.35 (2.63) | 0.942 | 0.662 → 0.658 |
| `examples/evals/` | 88/100 (88.0%) | 9 | 3 | −0.42 (1.55) | 0.843 | 0.707 → 0.693 |

Almost every change is one level, mostly between 2, 3 and 4; on `onde/` 3 → 4 (477) and
2 → 3 (290) lead. By criterion, contextual adaptation gains most (+0.65 points on `onde/`)
and information completeness follows (+0.35); readability, fluency and terminology move by
less than 0.2.

- **The scale is compressed, not shifted.** On `onde/` the change falls with the old score:
  +2.39 below 60, +0.82 at 60–70, +0.55 at 70–80, +0.40 at 80–85, −0.47 at 85–90 and −1.33 at
  90 and above. Languages at 90+ drop from 170 to 121, and those below 60 from 423 to 393.
- **The per-language change is larger than run-to-run noise.** Its sd of 2.50 points is
  well above the 1.12-point range experiment 12 measured for 1.13.0 between runs, and 417
  of the 1,943 languages move by more than 3 points. A single score is therefore not
  compared across versions.
- **The model order barely moves.** The 29 model means correlate at 0.9985. The top eight
  and the bottom eleven keep their places; the swaps are between neighbours less than about
  a point apart (glm-5.3 / gpt-5.6-terra, gemma4 / gemma4-31b, and gemini-2.5-flash
  dropping from 13th to 16th among four models within about 1.5 points of each other). By model the
  mean change runs from −0.99 (ox-alpha) to +2.65 (gemma4-12b), in line with the
  compression: the stronger models lose a little and the weaker gain.
- **Some readings of the comparison changed**, all recorded in
  [examples/tr/README.md](../README.md) as 1.14.0's: `gpt-6.1-sol` is now separated from
  `gpt-5.6-luna` and `union-alpha` by the paired test (p = 0.001 and 0.010, from 0.046 and
  0.017) and has the narrowest spread of any model; `haiku-5.5` is no longer clearly below
  `ox-alpha` (p = 0.06, from 0.005); `deepseek-v4.1-flash` trails `gemini-3-flash` (p =
  0.001) instead of sitting level; and `glm-5.3`, in the languages without its doubled
  lines, is level with `ox-alpha` rather than about a point behind. Greek and Interlingua rise
  more than the compression alone would, and Telugu falls by 2.8 on average, in 22 of 29
  models.
- **The reference translations** (`examples/evals/`) keep their language order except
  Chinese and Spanish, whose averages are within a point; see
  [examples/evals/README.md](../../evals/README.md).

## Trend Column

The trend phrases were not written again. [rescore_trend.py](rescore_trend.py) rebuilt each
model's `TREND-jev.jsonl` from the phrases in `jev-1.13.0/TREND-jev.jsonl` and the totals in
the new `jev.jsonl`, and synced the table in its `README.md`. The phrase is a short
description of the tendency, written by qwen3.6 from 1.13.0's levels; where 1.14.0 moves a
language's score, the phrase still describes the 1.13.0 reading, which matters most for
the languages that moved by more than 3 points. Models added after this
migration get phrases written from 1.14.0 by `make trends-jev` as usual.

## Procedure

1. Move each set's files into `jev-1.13.0/` with `git mv`.
2. Set `DEFAULT_MODEL = "jev-1.14.0"`.
3. Evaluate: `bash batch.sh` in `examples/evals/`, `make evaluate scores-jev` in `core/`,
   `fr/` and each `onde/{model}/`. Not `make` or `make all` in `onde/`: their
   `trends-jev` would write every phrase anew.
4. `uv run rescore_trend.py {models}` in `onde/`, then `make sync compare` in `examples/tr/`.
