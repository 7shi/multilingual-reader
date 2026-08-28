# Term Pre-Extraction Translation Experiment

Building on the hybrid mode from [experimental/03](../03/), this experiment directory verifies an approach that **extracts terms and proper nouns from the full text before translation begins, and fixes their translations up front**.

## Background and Motivation

Through experimental/03, the summary (glossary) was accumulated incrementally within the translation loop. With this approach, a mistranslation in the early lines gets locked into the glossary and propagates through everything that follows — the "early-accumulation drift" problem (this was the main cause of the sharp score drop seen in experimental/03).

In experimental/04:

- **Scan the full text before translation starts to extract terms** (chunk by chunk)
- **Batch-translate the extracted terms** to fix the glossary
- **Inject a term list scoped to the target range on every reorganization**

This aims to eliminate early-accumulation drift while ensuring terminology consistency across the entire translation. By including proper nouns (person names, place names) in the extraction target, this also addresses **unifying transliteration** (keeping a once-decided spelling consistent throughout).

## Translation System

Always use `uv run` to run the scripts.

### translate.py

```bash
uv run translate.py <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**Options:**

| Option | Default | Description |
|---|---|---|
| `--threshold` | 10 | Interval (in translation pairs) for generating a summary |
| `--keep` | 5 | Number of translation pairs kept between a summary and the next reorganization |
| `--terms` | `<output_base>-terms.json` | Path to the term file. If it already exists, extraction is skipped and it is loaded instead |
| `--terms-only` | none | Run only term extraction and translation generation, then exit (no translation is performed) |

The `--no-think` option present in experimental/03 has been removed; CoT is now fixed to disabled (translation, summarization, extraction, and translation generation all run with think=False).

### Behavior Specification (threshold=10, keep=5)

#### Phase 0: Term Extraction and Translation Generation (preprocessing)

1. Split the input into chunks of `keep` lines (43 lines → 9 chunks)
2. Extract source-language terms and proper nouns from each chunk via structured output (no CoT)
3. Merge and deduplicate terms across all chunks
4. Generate translations for all terms in a single batched structured output call
5. Save to the term file (default `<output_base>-terms.json`)

If the term file already exists, it is simply loaded (saving time on re-runs of the experiment). If there is an issue with a term or its translation, you can edit the JSON directly and re-run — only the translation step is re-run, without redoing extraction.

#### Phase 1: Translation Loop

Translation follows the same threshold+keep cycle as experimental/03. The difference is the context structure at reorganization time:

| Timing | chat_history |
|---|---|
| Initial | `[system, terms(1〜threshold+keep)]` |
| Translations 1–10 | Extended incrementally |
| Right after translation 10 | Summary generated → removed from history |
| Translations 11–15 | Extension continues |
| Right after translation 15 (reorganization) | `[system, terms(16〜30), latest_summary, last 5 pairs]` |
| Translations 16–25 | Extension continues |
| Right after translation 25 | Summary generated → removed from history |
| ... | ... |

- The scope for term injection is "the threshold+keep lines to be translated in the next cycle"
- Because term extraction is done chunk by chunk (keep lines), range filtering is possible

### Term File Format (JSON)

```json
{
  "from": "French",
  "to": "Spanish",
  "chunks": [
    {"index": 1, "start": 1, "end": 5, "terms": ["Aurélien Géron", "TensorFlow"]},
    {"index": 2, "start": 6, "end": 10, "terms": ["fine-tuning", "LoRA", "TensorFlow"]}
  ],
  "glossary": {
    "Aurélien Géron": "Aurélien Géron",
    "TensorFlow": "TensorFlow",
    "fine-tuning": "ajuste fino",
    "LoRA": "LoRA"
  }
}
```

- `chunks`: extracted terms per chunk. `start`/`end` are 1-indexed line numbers in the input file
- `glossary`: source-language → target-language mapping (used for range filtering at reorganization time)

### batch.sh

```bash
bash batch.sh
```

For the two models in [MODELS.txt](MODELS.txt) (gemma4-26b, gemma4-e4b), this runs **3 translations × 3 evaluations**. Same conditions as experimental/03/10-nt; the only difference is whether terms are pre-extracted.

**File naming:**

```
tr/<model>-<trrun>.txt              e.g. tr/gemma4-26b-1.txt
tr/<model>-<trrun>-terms.json       e.g. tr/gemma4-26b-1-terms.json
evals/<model>-<trrun>-eval-<evrun>.json
```

## Target Models

Narrowed down to gemma4-26b, whose stable operation was confirmed in experimental/03, and gemma4-e4b as a lower-resource alternative. qwen3.6-27b is excluded, since experimental/03 identified it as having a risk of sharp score drops and inefficient KV-cache usage.

| Model | experimental/03/10-nt median | Reason for selection |
|---|:---:|---|
| gemma4-26b | 96 / 100 / 96 | No sharp drops in any run, most stable |
| gemma4-e4b | 95 / 96 / 85 | Alternative for resource-constrained settings |

## Evaluation System

Uses the same pipeline as [experimental/03](../experimental/03/).

- Evaluator: `ollama:qwen3.6`
- 5 criteria × 20 points = 100 points total
- Aggregation: median of 3 evaluations

## Trials

| Trial | threshold | Result |
|---|:---:|---|
| [tr/](tr/) | 10 | gemma4-26b: 96/96/99, gemma4-e4b: 95/96/92 |

## Comparison Results

Comparison against experimental/03/10-nt (no term extraction) — the only difference is whether terms are pre-extracted:

| Model | experimental/03/10-nt | experimental/04 |
|---|:---:|:---:|
| gemma4-26b run 1 | 96 | 96 |
| gemma4-26b run 2 | 100 | 96 |
| gemma4-26b run 3 | 96 | 99 |
| gemma4-e4b run 1 | 95 | 95 |
| gemma4-e4b run 2 | 96 | 96 |
| gemma4-e4b run 3 | **85** (sharp drop) | **92** (drop lessened) |

**Observations:**

- **gemma4-e4b's sharp drop is lessened**: 85 → 92 points. The drop itself still occurs, but the damage is substantially reduced. This confirms the effect of pre-extracting terms
- **gemma4-26b remains stable**: no sharp drop. Run 3 improved slightly, 96 → 99
- **Run-to-run glossary drift persists**: the translation of `affinage` splits between `refinamiento` and `ajuste fino` depending on the run, showing that the term extraction phase itself has stochastic variance. This essentially just moved the early-accumulation drift from the translation loop to the term extraction phase
- **Contamination with general vocabulary**: non-technical words such as `mathématiques`, `physicien`, `anglais` get extracted. There is room to improve the extraction prompt
