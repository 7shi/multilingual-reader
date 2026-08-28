# trtools Reference

A command-line tool suite for translation, evaluation, and terminology management.

```
uv run trtools [--label LABEL] [--start START] <command> [options]
```

---

## Main Options

Options available across all subcommands, used to control progress bar display.

| Option | Description |
|---|---|
| `--label LABEL` | Label string shown in the progress bar (e.g. `bg: Bulgarian (2/10)`). Hidden if not specified |
| `--start START` | Batch start time (Unix timestamp). If specified, shows elapsed time for the whole batch |

If both `--label` and `--start` are omitted, the progress bar's `|` separator is also hidden.

---

## Design Philosophy

### translate: Summary Compression Approach

With a sliding-window approach (keeping only the last N entries), pushing out old history causes **terminology drift**, and since the start of the prompt changes every time, the **KV cache is invalidated**. To solve this, `translate` uses a **summary compression approach** that fixes the chat structure to `system + summary (latest one) + last keep entries`.

Every `--threshold` lines, the translation history is compressed into an English summary and combined with the last `--keep` pairs to rebuild the context. This keeps the KV cache stable and effective even for long documents while maintaining consistency.

Since the summary is output in English and does not depend on the target language (`to_lang`), it is pre-generated once per original text (topic) with the `summary` subcommand. It is saved as `{topic}-summary.jsonl` in the same directory as the original, and can be reused across all `to_lang` values and multiple `translate` runs for that topic. Neither `translate` nor `batch` auto-generates it — they only read the pre-generated cache and error if it is missing, so `summary` must be run beforehand.

`translate` writes to the output file incrementally, one translated line at a time. If it fails or is interrupted partway through, rerunning the same command skips existing translated lines and resumes from where it left off (chat_history is rebuilt using the same procedure from the pre-generated summary and the output file's existing lines). If a single line's translation result is empty or contains an internal newline, it is treated as invalid and retried up to 3 times; an exception is raised on failure.

### term extract/translate: Separation from the Translation Loop

Extracting terms inside the translation loop causes the extraction results to drift from run to run, leading to **inconsistent translated terms** (e.g. `affinage` -> `refinamiento` / `ajuste fino`). `term extract/translate` fixes and proofreads terms beforehand and shares them across all runs, eliminating this drift by design.

The term TSV needs proofreading after LLM generation. Local LLMs are prone to errors such as slash-separated alternatives, mistranslations, mixed-language contamination, and inflection mistakes. Injecting the proofread TSV via `trtools translate --terms-json/--terms-tsv` applies consistent terminology across all translation runs.

### eval/agg: Median of 3 Evaluation Runs

Since the evaluation model's output varies from run to run, a single score is unreliable. Running the evaluation 3 times on the same translation and taking the median with `agg` suppresses the evaluator's randomness.

The recommended evaluation model is **qwen3.6**. Its CoT-based logical verification correctly identifies technical defects. GPT-OSS 120B is not recommended, since its scores cap out at 92 points, making it hard to differentiate top-tier models. Evaluation is more reliable with CoT left enabled.

### Model Selection Guidelines

The recommended translation model is **gemma4-26b** (`ollama:gemma4:26b`). Being MoE, it is fast, has high score stability, and also avoids self-evaluation bias since it has a different architecture from the evaluator (qwen3.6).

In resource-constrained environments, **gemma4-e4b** (`ollama:gemma4:e4b`) is an alternative candidate. Using a proofread shared term glossary (`--terms-json`/`--terms-tsv`) improves its stability. However, it is more prone to grammatical issues such as inconsistent person, which needs to be tolerated.

Both models can occasionally drop the speaker tag on short acknowledgment lines or continuation lines that follow a speaker change, so checking after translation is necessary.

---

## Subcommand List

| Command | Overview |
|---|---|
| [`summary`](#summary) | Pre-generate a summary of the original text (cache for `translate`) |
| [`translate`](#translate) | Translate text line by line |
| [`review`](#review) | Polish a translation via third-party review |
| [`eval`](#eval) | Evaluate translation quality on 5 criteria |
| [`agg`](#agg) | Aggregate evaluation result JSON (median) |
| [`trend`](#trend) | Summarize per-language trends from evaluation logs |
| [`term extract`](#term-extract) | Extract technical terms from text |
| [`term translate`](#term-translate) | Translate extracted terms into a TSV |
| [`term show`](#term-show) | Show a term TSV filtered by language/key |
| [`term set`](#term-set) | Update a specific cell in a term TSV |
| [`term reorder`](#term-reorder) | Reorder term TSV columns into a given order |
| [`term merge`](#term-merge) | Merge multiple term TSVs by column |
| [`batch`](#batch) | Run translate -> evaluate -> aggregate in one go |

---

## summary

Pre-generates, from the original text alone, the summary used by `translate`'s summary compression approach. Since the summary is output in English and does not depend on `to_lang`, generating it once per original text (topic) lets it be reused across all `to_lang` values and multiple `translate` runs for that topic.

It is saved as `{topic}-summary.jsonl` in the same directory as the original (the topic name is the input filename with the `-<language code>` suffix removed, e.g. `finetuning-fr.txt` -> `finetuning-summary.jsonl`). Does nothing if the required checkpoints already exist.

```
uv run trtools summary <input_file...> -f <from_lang> -m <model> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `input_files` | Text files to summarize (multiple allowed). Processed in order, showing `[i/n]` per file |
| `-f`, `--from` | Source language. Language name (`French`) or language code (`fr`) |
| `-m`, `--model` | Summary generation model |

### Options

| Option | Default | Description |
|---|---|---|
| `--threshold` | `10` | Interval for summary generation, in lines. Match with `translate` |
| `--keep` | `5` | Number of lines to keep for checkpoint calculation. Match with `translate` |
| `--no-think` | false | Disable thinking (for Qwen3 models) |
| `-w`, `--retry-wait` | 3 | Retry wait time in seconds |

### Examples

```bash
# Single file
uv run trtools summary finetuning-fr.txt -f fr -m ollama:gemma4:26b

# Process multiple files together (shows progress as [1/2], [2/2])
uv run trtools summary finetuning-en.txt transformer-en.txt -f en -m ollama:gemma4:26b
```

---

## translate

Translates a text file line by line. Translates one line at a time while preserving empty lines, handling long documents through context compression. Requires a summary cache pre-generated with the `summary` subcommand (errors if not generated).

```
uv run trtools translate <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `input_file` | Text file to translate |
| `-f`, `--from` | Source language. Language name (`French`) or language code (`fr`) |
| `-t`, `--to` | Target language. Language name (`Spanish`) or language code (`es`) |
| `-o`, `--output` | Output filename |
| `-m`, `--model` | Translation model (e.g. `ollama:gemma4:26b`) |

### Options

| Option | Default | Description |
|---|---|---|
| `--threshold` | `10` | Interval for summary generation, in lines |
| `--keep` | `5` | Number of translation pairs to keep after compression |
| `--terms-json` | none | Output JSON file from `term extract` |
| `--terms-tsv` | none | Output TSV file from `term translate` |
| `--no-think` | false | Disable thinking (for Qwen3 models) |
| `-w`, `--retry-wait` | 3 | Retry wait time in seconds |
| `--fix` | false | Retranslate only the empty lines in the existing output. Normal mode determines resume position from line count alone, so it does not detect empty lines and simply continues; `--fix` rewrites the whole output file, retranslating only the empty spots |

### Examples

```bash
# Basic translation
uv run trtools translate finetuning-fr.txt -f fr -t es \
  -o finetuning-es.txt -m ollama:gemma4:26b --no-think

# With term injection
uv run trtools translate finetuning-fr.txt -f fr -t es \
  -o finetuning-es.txt -m ollama:gemma4:26b \
  --threshold 10 --keep 5 --no-think \
  --terms-json terms/finetuning-fr.json \
  --terms-tsv terms/finetuning-fr.tsv
```

---

## review

Polishes a translation file via LLM-based third-party review. Targets lines with a speaker name (`Speaker: Text` format) and improves translation quality through a two-stage analyze-then-improve prompt.

```
uv run trtools review --original <orig> --translation <tr> -f <from> -t <to> -o <output> -m <model> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `--original` | Original text file |
| `--translation` | Translation file to be polished |
| `-f`, `--from` | Source language code (e.g. `en`) |
| `-t`, `--to` | Target language code (e.g. `nl`) |
| `-o`, `--output` | Output filename after polishing |
| `-m`, `--model` | Model used for polishing |

### Options

| Option | Default | Description |
|---|---|---|
| `--history` | `10` | Number of preceding polished lines referenced as context |
| `--no-think` | false | Disable thinking |
| `--terms` | none | Term translation TSV file (used to convert speaker names) |

### Behavior

- Only lines with a speaker name (`Speaker: Text`) are polished; empty lines and lines without a speaker name are output unchanged
- Polishing has two stages: (1) analyze translation issues (skip improvement if `No issues`) -> (2) generate the improved translation
- Speaker names in the output are converted to the target language using the speaker-name column of the TSV passed via `--terms`

### Example

```bash
uv run trtools review \
  --original finetuning-en.txt \
  --translation tr/finetuning-nl.txt \
  -f en -t nl \
  -o reviewed/finetuning-nl.txt \
  -m ollama:gemma4:26b \
  --terms terms/finetuning-en.tsv
```

---

## eval

Evaluates translation quality on 5 criteria (20 points each, 100 points total). The evaluation result can be saved to a JSON file.

```
uv run trtools eval --original <orig> --translation <tr> -f <from> -t <to> -m <model> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `--original` | Original text file |
| `--translation` | Translated text file |
| `-f`, `--from` | Source language. Language name or language code |
| `-t`, `--to` | Target language. Language name or language code |
| `-m`, `--model` | Evaluation model (e.g. `ollama:qwen3.6`) |

### Options

| Option | Default | Description |
|---|---|---|
| `-o`, `--output` | none | Where to save the evaluation result JSON |
| `-w`, `--retry-wait` | 3 | Retry wait time in seconds |
| `--no-think` | false | Disable thinking |
| `--run` | `1` | Current evaluation run number (used for the progress bar) |
| `--runs` | `1` | Total number of evaluation runs (used for the progress bar) |

### Evaluation Criteria

1. **Readability & comprehensibility** (20 points)
2. **Fluency & naturalness** (20 points)
3. **Terminology appropriateness** (20 points)
4. **Contextual adaptation** (20 points)
5. **Information completeness** (20 points)

### Examples

```bash
# Single evaluation run
uv run trtools eval \
  --original finetuning-fr.txt \
  --translation finetuning-es.txt \
  -f fr -t es \
  -m ollama:qwen3.6 -w 3 \
  -o evals/finetuning-es-1.json

# 3 evaluation runs (shows x/3 in the progress bar)
for run in 1 2 3; do
  uv run trtools eval \
    --original finetuning-fr.txt \
    --translation finetuning-es.txt \
    -f fr -t es \
    -m ollama:qwen3.6 -w 3 \
    --run $run --runs 3 \
    -o evals/finetuning-es-$run.json
done
```

---

## agg

Aggregates the evaluation JSON files (3 runs) generated by `eval` and calculates the median for each criterion. Assumes filenames of the form `<base>-1.json`, `<base>-2.json`, `<base>-3.json`.

```
uv run trtools agg <json_files...> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `files` | Evaluation JSON files (multiple allowed, wildcards allowed) |

### Options

| Option | Default | Description |
|---|---|---|
| `-o`, `--output` | none | Where to save the aggregated result JSON |
| `--verbose` | false | Show the per-criterion median, mean, and standard deviation |

### Examples

```bash
# Aggregate all eval files and save to SCORES.txt
uv run trtools agg evals/*.json | tee SCORES.txt

# Detailed display
uv run trtools agg evals/*.json --verbose
```

---

## trend

Merges the evaluation JSON (3 runs) generated by `eval` per language, has the LLM summarize it, and generates a sentence for `README.md`'s "Trend Analysis" column. Intermediate results are appended to a JSONL, from which a Markdown table is built and written back into `README.md`.

```
uv run trtools trend <json_files...> -m <model> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `files` | Evaluation JSON files (multiple allowed, wildcards allowed). Not needed with `--render-only` |

### Options

| Option | Default | Description |
|---|---|---|
| `-m`, `--model` | none | Model used for summarization (not needed with `--render-only`) |
| `-o`, `--output` | `TRENDS.jsonl` | Intermediate result JSONL |
| `--sync` | none | Path of the `README.md` to write the table back into after generation |
| `--render-only` | false | Only output/sync the table from the JSONL, without generating |
| `--no-think` | false | Disable thinking |
| `-w`, `--retry-wait` | 3 | Wait time on retry, in seconds |
| `-l`, `--lang` | `en` | Output language of the summary (`en`/`ja`) |

### Behavior

Only the evaluation logs are passed to the LLM; the translated text itself is not. Passing the translated text would amount to redoing a 4th evaluation, undermining the stabilization gained from taking the median of 3 evaluation runs. Information that would confuse the summary — file paths, model names, per-criterion scores/reasoning — is withheld; only the per-run total score `total_score` and overall evaluation `overall_comment` are passed. A defect flagged in all 3 runs is more reliable than one flagged only once, which serves as a signal for the summary.

The prompt instructs the model to trust the evaluation results as given and not to add specifics not present in the logs (e.g., if a contaminating language isn't identified, keep the description generic rather than naming a language). It also explicitly forbids confusing the output language (specified via `-l`/`--lang`, default `en`) with the language being evaluated.

Since the output is a single item, structured output is not used; plain text is received instead. The prompt instructs the model not to add labels, quotation marks, a trailing period, or surrounding explanation, and on the receiving side, surrounding quotes, a trailing period, and newlines are stripped, and `|` is escaped since it clashes with the table cell separator. If the reply doesn't come back in the specified language, it is re-prompted and regenerated up to 3 times.

**Resuming after interruption**: Each generated language is appended to the JSONL as it completes, and at startup the JSONL is read to skip languages already present. An interruption loses at most one language's worth of work. To regenerate a specific language, delete its line and rerun.

**Table sync**: With `--sync` specified, the entire table in the target file whose header is `| 言語 | スコア | 傾向の分析 |` (`ja`) or `| Language | Score | Trend Analysis |` (`en`) is replaced. Only tables with a matching header are targeted, so other tables in the same file are unaffected. Since the header itself is generated according to `-l`/`--lang`, the existing table can be detected and replaced regardless of which language it was written in. Rows are sorted by score descending, then language code ascending, and language names use the `-l`/`--lang`-corresponding notation (`en`/`ja`) from `LANGUAGES` ([language.py](language.py)).

### Examples

```bash
# Generate trends for all languages and update the table in README.md
uv run trtools trend evals/*.json -m ollama:qwen3.6 --no-think --sync README.md

# Resume after interruption (only ungenerated languages are processed)
uv run trtools trend evals/*.json -m ollama:qwen3.6 --no-think --sync README.md

# Only re-output/sync the table from the existing JSONL
uv run trtools trend --render-only --sync README.md
```

---

## term extract

Extracts proper nouns and technical terms from a text file and saves them as JSON, chunk by chunk. Intended to be passed to the `translate` subcommand's `--terms-json`.

```
uv run trtools term extract <input_file> -f <from_lang> -m <model> -o <output.json> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `input_file` | Text file to extract terms from |
| `-f`, `--from` | Source language. Language name or language code |
| `-m`, `--model` | Model to use |
| `-o`, `--output` | Output JSON filename |

### Options

| Option | Default | Description |
|---|---|---|
| `--keep` | `5` | Chunk size, in lines |
| `-w`, `--retry-wait` | 3 | Retry wait time in seconds |
| `--no-think` | false | Disable thinking |

### Example

```bash
uv run trtools term extract finetuning-fr.txt \
  -f fr -m ollama:gemma4:31b \
  --keep 5 --no-think \
  -o terms/finetuning-fr.json
```

---

## term translate

Loads the JSON generated by `term extract` and writes out term translations for each language into a TSV file. If a common glossary TSV (`-c`) is given, matching terms are taken from it, skipping the LLM.

```
uv run trtools term translate <extract.json> -t <lang> [-t <lang> ...] -m <model> -o <output.tsv> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `extract_file` | Output JSON from `term extract` |
| `-t`, `--to` | Target language. Language name or language code (multiple allowed) |
| `-m`, `--model` | Model to use |
| `-o`, `--output` | Output TSV filename |

### Options

| Option | Default | Description |
|---|---|---|
| `-c`, `--common` | none | Common glossary TSV file (reuse existing translations) |
| `-w`, `--retry-wait` | 3 | Retry wait time in seconds |
| `--no-think` | false | Disable thinking |

### Examples

```bash
# French -> English, Spanish
uv run trtools term translate terms/finetuning-fr.json \
  -t en -t es \
  -m ollama:gemma4:31b --no-think \
  -c terms/common.tsv \
  -o terms/finetuning-fr.tsv

# English -> German, Japanese, Chinese
uv run trtools term translate terms/finetuning-en.json \
  -t de -t ja -t zh \
  -m ollama:gemma4:31b --no-think \
  -c terms/common.tsv \
  -o terms/finetuning-en.tsv
```

---

## term show

Shows a term TSV, filtered by language column and key, on standard output. Used as preprocessing before passing a wide TSV to an LLM, or to check items pending proofreading.

```
uv run trtools term show <tsv_file> [-l <lang> ...] [-k <key> ...]
```

### Arguments

| Argument | Description |
|---|---|
| `tsv_file` | Target TSV file |
| `-l`, `--lang` | Language column(s) to show. Language name or language code (multiple allowed; all columns if omitted) |
| `-k`, `--key` | Key(s) to show, i.e. values in the first column (multiple allowed; all rows if omitted) |

The key column (first column) is always output first regardless of the `-l` specification.

### Examples

```bash
# Show all rows, Japanese column only
uv run trtools term show terms/onde-en.tsv -l ja

# Show two columns, Japanese and German
uv run trtools term show terms/onde-en.tsv -l ja -l de

# Filter by key
uv run trtools term show terms/onde-en.tsv -l ja -k physics -k waves
```

---

## term set

Overwrites and saves a specific cell in a term TSV. Used for individual proofreading after LLM auto-translation.

```
uv run trtools term set <tsv_file> -k <key> -l <lang> -v <value>
```

### Required Arguments

| Argument | Description |
|---|---|
| `tsv_file` | Target TSV file |
| `-k`, `--key` | Key to change (value in the first column) |
| `-l`, `--lang` | Language column name to change. Language name or language code |
| `-v`, `--value` | New value |

### Example

```bash
uv run trtools term set terms/onde-en.tsv -k "physics" -l ja -v "物理学"
```

---

## term reorder

Reorders the columns of a term TSV into a given order and outputs it. A missing column is added as an empty column.

```
uv run trtools term reorder <tsv_file> -c <lang> [...] -o <output.tsv>
```

### Required Arguments

| Argument | Description |
|---|---|
| `tsv_file` | Target TSV file |
| `-c`, `--col` | Column name(s) to output. Language name or language code (multiple) |
| `-o`, `--output` | Output TSV file |

### Example

```bash
uv run trtools term reorder terms/finetuning-en.tsv \
  -c en -c fr -c es -c de -c ja -c zh \
  -o terms/finetuning-en-reordered.tsv
```

---

## term merge

Merges multiple term TSVs by column and outputs the result. If the key column (first column) is common, rows are matched by key value; without a key column, rows are matched by position. When the same column name exists in multiple files, non-empty values from later files overwrite cell by cell.

```
uv run trtools term merge <file1> <file2> [...] -o <output.tsv>
```

### Required Arguments

| Argument | Description |
|---|---|
| `FILE...` | Input TSV files (multiple) |
| `-o`, `--output` | Output TSV file |

### Example

```bash
# Add language columns from another file to an existing TSV
uv run trtools term merge terms/finetuning-en.tsv extra-langs.tsv \
  -o terms/finetuning-en-full.tsv
```

---

## batch

Runs translate -> evaluate -> aggregate in one go. Derives the source language from the filename's language code (e.g. `finetuning-fr.txt` -> `fr`) and organizes output into the directories given by `--tr-dir` and `--eval-dir`. Existing files are skipped.

Since `summary` is not auto-generated, `{topic}-summary.jsonl` must be generated with `trtools summary` for the target files before the translation phase. If not generated, that translation target errors and is skipped.

```
uv run trtools batch <files...> --langs <lang...> -m <model> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `files` | Input text files (e.g. `../finetuning-fr.txt`). The `-XX` suffix in the filename is used as the source language code |
| `--langs` | List of target language codes (e.g. `en es de`) |
| `-m`, `--model` | Translation model (not needed with `--eval-only`) |

### Options

| Option | Default | Description |
|---|---|---|
| `--evaluator` | none | Evaluation model (not needed with `--tr-only`) |
| `--tr-only` | false | Run translation only (skip evaluation and aggregation) |
| `--eval-only` | false | Run evaluation only (skip translation and aggregation) |
| `--no-agg` | false | Skip aggregation only (do not generate `SCORES.txt`) |
| `-f`, `--from` | auto-derived from filename | Source language (for manual override) |
| `--terms-dir` | none | Directory of term files (auto-searches for `<topic>-<from>.json/tsv`) |
| `--tr-runs` | `1` | Number of translation runs |
| `--eval-runs` | `3` | Number of evaluation runs |
| `--threshold` | `10` | Interval for summary generation, in lines |
| `--keep` | `5` | Number of translation pairs to keep after compression |
| `--no-think` | false | Disable CoT |
| `--tr-dir` | `tr` | Translation output directory |
| `--eval-dir` | `evals` | Evaluation output directory |
| `-w`, `--retry-wait` | `3` | Retry wait time in seconds |

### Output File Layout

With `--tr-runs 1` (default):

```
<tr-dir>/
  <topic>-<lang>.txt          # Translation result
<eval-dir>/
  <topic>-<lang>-1.json  # Evaluation result (per eval-run)
  <topic>-<lang>-2.json
  <topic>-<lang>-3.json
SCORES.txt                    # Aggregated score
```

With `--tr-runs 3`, filenames get a suffix (e.g. `<tr-dir>/finetuning-de-1.txt`, `<eval-dir>/finetuning-de-1-1.json`).

### Supported Language Codes

See [trtools/language.py](language.py). An unregistered language code is passed through as a capitalized language name (e.g. `xx` -> `Xx`).

Languages with confirmed quality (all 4 topics, gemma4-26b, adopted as reference translations in [examples/](../examples/)): `en` English, `ja` Japanese, `es` Spanish, `zh` Chinese, `de` German

Quality for other languages is unconfirmed. Always review and proofread generated results.

### Examples

```bash
# Pre-generate summaries (trtools batch does not auto-generate them)
uv run trtools summary ../finetuning-en.txt ../transformer-en.txt \
  -f en -m ollama:gemma4:26b --threshold 20

# Translation only (multiple files, multiple languages)
uv run trtools batch \
  ../finetuning-en.txt ../transformer-en.txt \
  --langs de ja zh \
  -m ollama:gemma4:26b \
  --terms-dir ../terms \
  --threshold 20 --no-think \
  --tr-only

# Translation + evaluation + aggregation
uv run trtools batch \
  ../finetuning-fr.txt ../transformer-fr.txt \
  --langs en es \
  -m ollama:gemma4:26b \
  --evaluator ollama:qwen3.6 \
  --terms-dir ../terms \
  --no-think

# Evaluation only (assuming translated files already exist, rerun just the evaluation)
uv run trtools batch \
  ../finetuning-en.txt \
  --langs de ja zh \
  --evaluator ollama:qwen3.6 \
  --eval-only

# Run aggregation separately
uv run trtools agg evals/*.json | tee SCORES.txt
```

---

## Typical Workflow

### 1. Prepare term files

```bash
# Extract terms
uv run trtools term extract topic-fr.txt \
  -f fr -m ollama:gemma4:31b --keep 5 --no-think \
  -o terms/topic-fr.json

# Translate terms
uv run trtools term translate terms/topic-fr.json \
  -t en -t es \
  -m ollama:gemma4:31b --no-think \
  -c terms/common.tsv -o terms/topic-fr.tsv
```

### 2. Pre-generate summaries

```bash
uv run trtools summary topic-fr.txt -f fr -m ollama:gemma4:26b
```

### 3. Run translation and evaluation in one go

```bash
uv run trtools batch topic-fr.txt \
  --langs en es \
  -m ollama:gemma4:26b \
  --evaluator ollama:qwen3.6 \
  --terms-dir terms \
  --no-think
```

### 4. Run translation, evaluation, and aggregation individually

```bash
# Translation (assumes summary topic-fr.txt has already been run)
uv run trtools translate topic-fr.txt -f fr -t en \
  -o tr/topic-en.txt -m ollama:gemma4:26b --no-think \
  --terms-json terms/topic-fr.json --terms-tsv terms/topic-fr.tsv

# Evaluation (3 runs)
for run in 1 2 3; do
  uv run trtools eval \
    --original topic-fr.txt --translation tr/topic-en.txt \
    -f fr -t en \
    -m ollama:qwen3.6 -w 3 \
    --run $run --runs 3 \
    -o evals/topic-en-$run.json
done

# Aggregation
uv run trtools agg evals/topic-en-*.json | tee SCORES.txt
```
