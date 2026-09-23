# examples/tr/fr/

Directory for translating the French source text into English and Spanish and updating the reference translations in `examples/`.

## Flow

1. Run the translation with `make` (output goes to `tr/`)
2. Proofread the translation results
3. Replace the corresponding files in `examples/`

`make` also evaluates the translations with TypeSafe Jev (`jev-1.13.0`, one run per language), writing `jev-{topic}.jsonl` (one per topic, since a record names only its language) and the scores to `SCORES-jev.txt`. `evals/` and `SCORES.txt` are the previous evaluator's record (qwen3.6, median of three runs) and are no longer written.

## Running

```bash
make
```

- Translation model: gemma4-26b
- Evaluation model: TypeSafe Jev (`jev-1.13.0`)
- Targets: finetuning, transformer, onde, momentum × FR→EN, FR→ES
- Settings: threshold=10, keep=5, no CoT, term-file injection (`../terms/*-fr.{json,tsv}`)
- Existing files are skipped, so it can be resumed partway through
