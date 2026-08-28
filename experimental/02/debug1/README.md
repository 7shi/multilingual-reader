# debug1: method selection

## Purpose

Run 4 models × 4 variants (none, none-schema, glossary, glossary-schema) to narrow down Phase B to a single method.

| Model | Options |
|---|---|
| `gemma3:27b` | |
| `gpt-oss:120b` | |
| `gemma4:31b` | `--no-think` |
| `qwen3.6` | `--no-think` |

---

## Execution

```bash
bash batch.sh
```

Existing files are skipped, so the run can be resumed from any point. Results are output to `{model}/SCORES.txt`.

The script splits into three phases: translation, evaluation, and aggregation. To avoid the overhead of switching models, translation for all models is run first, keeping the translation model and the evaluation model (qwen3.6) each running continuously, before moving on to evaluation.

---

## Background

During the initial functional check (gemma3:27b's none/glossary), scores changed as follows before and after the `llm7shi` v0.10.1 update:

| Variant | Before update | After update |
|---|---|---|
| `none` | 98 points | 95 points |
| `glossary` | 96 points | 98 points |

`llm7shi` v0.10.1 fixed a role-conversion issue (details in `../debug2/README.md`), confirming that `glossary` now outperforms `none`. This directory also verifies the effect of enabling/disabling schema.

---

## Results and conclusion

All work complete. See `../README.md` (debug1 section) for the scores and the resulting method-selection conclusion.
