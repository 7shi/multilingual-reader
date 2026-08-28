# examples/tr/terms/

Directory holding the term files (JSON/TSV) used for translation in `examples/`. Generated with `trtools term extract/translate`, and only the proofread versions are kept here.

## File Layout

| File | Contents |
|---|---|
| `common.mk` | Defines `EXTRA_LANGS`, additional languages for `onde-en.tsv` |
| `common.tsv` | Proper nouns common to all topics (show titles, etc.); skips the LLM to fix the translation |
| `{topic}-fr.json` | Term chunk map extracted from the French source text (for FR→EN, FR→ES translation) |
| `{topic}-fr.tsv` | English/Spanish translation table for French terms |
| `{topic}-en.json` | Term chunk map extracted from the English source text (for EN→DE, EN→JA, EN→ZH translation) |
| `{topic}-en.tsv` | German/Japanese/Chinese translation table for English terms |

## Generating/Updating

```bash
make
```

Proofread the TSV after generating it. The LLM can produce slash-separated dual candidates, mistranslations, extraneous text, and typos (see [MEMO.md](../../MEMO.md) for details).

## Operational Notes

- `trtools term set` updates the TSV directly, so **never run it in parallel against the same file**. Always run `show` / `set` / re-check sequentially.
- If `trtools term show common.tsv -l xx` finds no such column, it displays only the `English` column with a warning. This means "that language column hasn't been created yet."

## TSV Proofreading Procedure

Since there are many columns, **always split by language into separate, independent tasks** when reviewing and fixing.

Additional notes when proofreading `common.tsv`:
- The titles "Tech Flash" and "Bridges in Physics" should be translated.
- Person names "Camille" and "Luc" should be transliterated in languages that use a distinct script.

### 1. Display filtered by language

```bash
# Show only a specific language column (also useful when pasting into an LLM for review)
uv run trtools term show onde-en.tsv -l ja
```

### 2. Fix a problematic cell

```bash
uv run trtools term set onde-en.tsv -k "physics" -l ja -v "物理学"
```

`-k` specifies the key (the value in the first column), `-l` the language code (e.g. `ja`), and `-v` the corrected value.

### 3. Check the result of the fix

```bash
uv run trtools term show onde-en.tsv -l ja -k physics
```

## Using in Translation

```bash
uv run trtools translate input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma4:26b \
  --terms-json {topic}-fr.json \
  --terms-tsv {topic}-fr.tsv
```

For `trtools batch`, point to this directory with the `--terms-dir` option.
