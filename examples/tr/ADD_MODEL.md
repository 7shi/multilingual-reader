# Evaluation Update Procedure When Adding a Model

Procedure for reflecting a newly added translation model in the comparison table and discussion after creating a benchmark set for it. The translation work itself is done manually by the user, so proceed through the following 3 steps.

1. Prepare under `onde/`
2. User translates
3. Process the results

## 1. Preparing Under `onde/`

When adding a new model to the benchmark, duplicate [onde/TEMPLATE/](onde/TEMPLATE/) as the base structure. `TEMPLATE/` is a directory reserved for the template and is not included in the `make all` target.

1. Copy `TEMPLATE/` to a directory named after the target model
2. In the copy's `Makefile`, change `TRANSLATOR` to the target model (everything else uses the common definitions in [onde/common.mk](onde/common.mk). The evaluator is fixed to `ollama:qwen3.6` to keep the scoring criteria consistent. `TRANSLATOR` isn't used by automated runs — it's a value for recording which model did the translation)
3. Rewrite the `TODO` spots (title, translation model name) in the copy's `README.md`
4. Add the target model's directory name to `MODELS` in the parent [onde/Makefile](onde/Makefile), and also add it to the directory list in [onde/README.md](onde/README.md) (`MODELS` is also the source data `generate_compare_rows.py` reads automatically for the comparison table's model columns)

Don't run `make` at this point (running it before the translations are in place will attempt translation via the target model's API and fail).

## 2. User Translates

Using the target model, manually create `onde/{model}/tr/onde-{lang}.txt` for each target language (`CORE_LANGS` + `EXTRA_LANGS`, defined in [onde/common.mk](onde/common.mk)).

- The source text is [onde-en.txt](onde-en.txt). Translate line by line, keeping blank lines as-is (matching `trtools translate`'s output format).
- Place translation files for all target languages before proceeding to the next step. If any language is missing its file, the next `make` run will attempt an API call to the target model for that language only, and fail.

## 3. Processing the Results

### 3.1 Running `make`

Run `make` in `onde/{model}/`. If translated files are already in place in `tr/`, the translation phase is entirely skipped, and only evaluation, aggregation, and trend generation (`evaluate` → `scores` → `trends`) run. Evaluation logs are output to `evals/`, and scores to `SCORES.txt`.

### 3.2 Checking Scores and Evaluation Logs
- Check the output scores (`SCORES.txt`).
- Read the translations (text files under `tr/`) and evaluation logs (JSON files under `evals/`) to understand the specific issues noted for each language (terminology accuracy, unnatural literal translation, garbled text, hallucinations such as system-prompt or other-language contamination, etc.).

### 3.3 Updating `README.md`
Update `onde/{model}/README.md` as follows.
- **Check the "Translation Quality Overview"**: this table is auto-generated from the evaluation logs by `make` (the `trends` target) via `trtools trend --sync`, so no manual entry is needed. Check that the generated trend for each language is appropriate (see [ADD_LANG.md's 1.2.1](ADD_LANG.md#121-writing-policy-for-trend-analysis) for the writing policy).
- **Unify notation**: make sure the language notation is consistent throughout the file, avoiding inconsistencies with existing mentions (e.g. spelling variants of the same language).

### 3.4 Updating the Consolidated Results (`examples/tr/README.md`)

Once all directories have been updated, update the top-level `examples/tr/README.md` to summarize.

- Add the added model's full name (parameter scale, whether it's MoE, etc.) to the model abbreviation list at the top.
- Insert a link to the added directory into the `onde/` description list.
- Running `make sync` in `examples/tr/` updates the "Comparison Between Translation Models" table (header row, separator row, body rows) all at once.

#### 3.4.1 Updating the Comparison Table
- Reflect the added model's column in the table under "Comparison Between Translation Models". Columns follow the order of `MODELS` in `onde/Makefile`, so if you added it to `MODELS` in step 1.4, no manual column editing is needed on the table side.
- Enter each model's representative score (the number recorded in the base `SCORES.txt`), and bold (`**`) the **cell with the maximum score** in that row. If the maximum is tied, bold all tied cells.
- Update the comparison table by running `make sync` in `examples/tr/`. The header row (each model name links to `onde/{model}/README.md`), separator row, and body rows are all rewritten together.
- Then run `make compare` in `examples/tr/` to regenerate the per-model score-distribution boxplot (`compare/MODELS.png`).
- See [ADD_LANG.md's 2.1](ADD_LANG.md#21-updating-the-comparison-table) for details on the generation process, including the row-ordering algorithm.

#### 3.4.2 Updating the Trend Analysis Section
- **Stability items**: if the added model's results back up or overturn an existing trend, add the model name into the text as a concrete example.
- **Hallucination items**: add any peculiar phenomenon found for the added model.
- **Don't distinguish old from new**: avoid phrasing like "the newly added ~" even in the discussion or notes of the consolidated `README.md`; integrate it naturally as part of the overall comparison across models.
- **Unify notation**: also check the consolidated `README.md` for inconsistent notation of the model name and unify it.

---

Following the above procedure lets you accurately maintain a record of per-model differences in translation quality and characteristic hallucination tendencies for comparative verification.
