# Evaluation Update Procedure When Adding a Language

Procedure for reflecting evaluation results in each directory's `README.md` after adding a language and running translation and evaluation (`make`).

## 1. Checking and Updating Evaluations in the `onde/` Directory

For each model directory under `onde/` (see `all` in `onde/Makefile`), do the following.

### 1.1 Checking Scores and Evaluation Logs
- Check the output scores (`SCORES.txt`).
- Read the translations (text files under `tr/`) and evaluation logs (JSON files under `evals/`) to understand the specific issues noted for each language (terminology accuracy, unnatural literal translation, garbled text, hallucinations such as system-prompt or other-language contamination, etc.).

### 1.2 Updating `README.md`
Update each directory's `README.md` as follows.
- **Reflect the target language**: insert the target language (e.g. `Korean`) into the target-language list at the top of the file, in the manner of insertion sort.
- **Check the "Trend Analysis" column**: this column is auto-generated from the evaluation logs by `make` (the `trends` target) via `trtools trend --sync`, so no manual entry is needed. Check that the generated content is appropriate according to the writing policy ([1.2.1](#121-writing-policy-for-trend-analysis)).
- **Unify notation**: make sure the target language's notation is consistent throughout the file, avoiding inconsistencies with existing mentions (e.g. spelling variants of the same language).

#### 1.2.1 Writing Policy for "Trend Analysis"

For the "Trend Analysis" column in the per-language table in each model directory's `README.md`, **do not write what can already be seen from the score**. Ranking or quality level (words like "high quality", "close") are just paraphrases of the number, so use that space for concrete symptoms instead.

- **What to write**: what actually happens in the translation that the score number alone doesn't reveal. Describe concretely what happened: speaker-tag dropout, contamination with another language or Han characters, coined/nonexistent words, orthography breakdown, generation loops, output cutting off partway through, mistranslation of specific terms, etc.
- **What not to write**: evaluative words that just restate the score's magnitude, like "high quality", "close", "relatively good", "collapsed".
- **If there's nothing to write, leave it as is**: for languages with no notable symptoms reported (e.g. stable languages), don't force an entry — keep the existing text.

## 2. Updating the Consolidated Results (`examples/tr/README.md`)

Once all directories have been updated, update the top-level `examples/tr/README.md` to summarize.

- `uv run examples/tr/generate_compare_rows.py compare` outputs the "Comparison Between Translation Models" table (header row, separator row, body rows). With `--sync`, it directly rewrites the entire table following the line starting with `| Language | ` in README.md.
- `uv run examples/tr/generate_compare_rows.py core` outputs the score rows for "Evaluation Results for Core Languages (core)".
- In `core` mode, rows are ordered by descending average; ties are stabilized by ascending language code.

### 2.1 Updating the Comparison Table
- Reflect the target language's row in the table under "Comparison Between Translation Models".
- Enter each model's representative score (the number recorded in the base `SCORES.txt`), and bold (`**`) the **cell with the maximum score** in that row. If the maximum is tied, bold all tied cells.
- The comparison table is updated by running `uv run examples/tr/generate_compare_rows.py compare --sync`. The header row (each model name links to `onde/{model}/README.md`), separator row, and body rows are all rewritten together, so no manual pasting is needed.
- Columns (models) are automatically read from `MODELS` in `onde/Makefile`. There's no need to add or edit columns manually in the table.
- This script reads `onde/{each model}/SCORES.txt`, internally builds a **tuple of each language's scores sorted in descending order within the row**, and determines row order by **comparing those tuples in descending order**. Ties on the same tuple are stabilized by ascending language code.
- Language names are output in their English form (`LANG_NAMES`).

### 2.2 Updating the Trend Analysis Section
- **Stability items**: if the target language's results back up an item (such as "gemma4's stability on minor languages"), add the language name (e.g. `Korean`) into the text as a concrete example.
- **Hallucination items**: add any peculiar phenomenon found for the target language.
- **Don't distinguish old from new**: avoid phrasing like "the newly added ~" even in the discussion or notes of the consolidated `README.md`; integrate it naturally as part of the overall comparison across languages.
- **Unify notation**: also check the consolidated `README.md` for inconsistent notation of the target language (e.g. mentions in past hallucination examples) and unify it.

---

Following the above procedure lets you accurately maintain a record of per-language differences in model performance and characteristic hallucination tendencies for comparative verification.
