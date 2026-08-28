# Experiment 09: Expanding third-party-evaluation revision to all languages

This directory expands the "third-party evaluation approach (separating the roles of translation and revision)" established in Experiment 07 to all 67 languages. For each language, we automatically select the highest-scoring baseline among multiple models' translation results, and have `qwen3.6` revise it line by line.

## Background and purpose

Experiment 07 verified, for two languages (Dutch and Czech), a method of revising `trtools` (gemma4) baseline translations with `qwen3.6`. Since this method was confirmed to be effective for improving quality in medium-resource languages, we now expand its application to all languages.

Also, whereas Experiment 07 fixed the revision baseline to `gemma4`, this experiment compares scores across `gemma4`, `gpt-oss`, and `qwen3.6`, automatically selecting the highest-scoring translation for each language. Since some languages — such as Czech (`cs`) — score highest with a model other than gemma4, we can start revision from a higher-quality baseline.

## Script structure

- **`find_best.py`**:
  Compares the `SCORES.txt` files of all models under `examples/tr/onde/`, selects the highest-scoring translation file for each language code, and outputs a TSV (language code, score, file path, language name) to standard output. Language names are obtained from `trtools.language.LANG_NAMES`.

- **`review.py`**:
  An extension of Experiment 07's `review.py` for this experiment. Main changes from Experiment 07: added a feature to convert speaker names to the target language using a terminology TSV; converted `-f`/`-t` to accept language codes (instead of language names); migrated from `tqdm` to `rich`, with enhanced status bars (overall language progress / batch elapsed time, plus per-line progress bar / elapsed time).

- **`batch.sh`**:
  After generating the TSV with `find_best.py`, this fully automates revision with `review.py`, evaluation with `trtools eval`, and aggregation with `trtools agg` for each language. Running all 67 languages took about 38 hours.

- **`compare.py`**:
  Compares `best.tsv` (pre-revision scores) with `SCORES.txt` (post-revision scores), and outputs to standard output, in Markdown format: two tables (sorted by language code, and sorted descending by post-revision score), summary statistics, a breakdown in 5-point buckets, and a list of languages for which revision was effective. Run `uv run compare.py > SCORES.md` to generate the output.

## Results

See [SCORES.md](SCORES.md) for a comparison of post-revision scores against pre-revision scores across all 67 languages.

The results showed 30 languages improved, 32 languages degraded, and 5 languages unchanged (average change: -1.2 points). Low- and medium-resource languages such as Basque (+42), Slovene (+22), and Estonian (+29) showed large improvements, while quality dropped for Telugu (-31), Albanian (-26), and Nepali (-28).

### Discussion: conditions under which revision is effective

Organizing the results shows that the effectiveness of revision strongly depends on the "state" of the baseline translation.

- **Effective cases**: Improvement is pronounced when the baseline translation is "semantically sound but roughly expressed." Effects tend to appear at moderate pre-revision scores in the 70-85 range, such as Bulgarian (80→97) and Hungarian (83→96). There were also cases of large improvement even from low pre-revision scores, as long as the translation's structure was preserved, such as Basque (45→87) and Estonian (53→82).
- **Counterproductive cases**: For languages with high pre-revision scores (Japanese 97→80, Armenian 91→75), the revision model made unnecessary changes that degraded quality.
- **No-effect cases**: For translations that failed to accurately capture the structure of the original — such as Bengali (54→39), Khmer (54→33), and Telugu (64→33) — revision could not improve them and, if anything, tended to make them worse.

Because revision functions as "refinement of expression" rather than "correction of errors," it cannot be expected to help when the baseline translation is semantically broken.

## How batch.sh works

1. **Baseline selection**
   - Runs `find_best.py` and saves the result to `best.tsv`
   - TSV format: `language_code\tscore\tfile_path\tlanguage_name`

2. **Running the revision**
   - **Input**: Original text `examples/onde-en.txt` and the baseline translation selected in `best.tsv`
   - **Revision model**: `ollama:qwen3.6` (`--no-think`)
   - **Output**: `tr/onde-{lang}.txt`

3. **Evaluation**
   - **Evaluation model**: `ollama:qwen3.6`
   - Runs `trtools eval` 3 times for each language's revised translation
   - **Output**: `evals/onde-{lang}-{1,2,3}.json`

4. **Aggregation**
   - Aggregates the median across all evaluation files with `trtools agg`, outputting to `SCORES.txt`
