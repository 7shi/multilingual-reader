# examples/tr/fr/

Directory for translating the French source text into English and Spanish and updating the reference translations in `examples/`.

## Flow

1. Run the translation with `make` (output goes to `tr/`)
2. Proofread the translation results
3. Replace the corresponding files in `examples/`

If evaluation is needed, add `--eval-runs 3` to `Makefile` and re-run `make` (outputs JSON to `evals/` and scores to `SCORES.txt`).

## Running

```bash
make
```

- Translation model: gemma4-26b
- Targets: finetuning, transformer, onde, momentum × FR→EN, FR→ES
- Settings: threshold=10, keep=5, no CoT, term-file injection (`../terms/*-fr.{json,tsv}`)
- Existing files are skipped, so it can be resumed partway through
