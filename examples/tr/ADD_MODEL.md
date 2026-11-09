# Evaluation Update Procedure When Adding a Model

Procedure for reflecting a newly added translation model in the comparison table and discussion after creating a benchmark set for it. For [plamo/](plamo/), the set under PLaMo 3 Translate's conditions, see [ADD_PLAMO.md](ADD_PLAMO.md) instead. The translation work itself is done manually by the user, so proceed through the following 3 steps.

1. Prepare under `onde/`
2. User translates
3. Process the results

## 1. Preparing Under `onde/`

When adding a new model to the benchmark, duplicate [onde/TEMPLATE/](onde/TEMPLATE/) as the base structure. `TEMPLATE/` is a directory reserved for the template and is not included in the `make all` target.

1. Copy `TEMPLATE/` to a directory named after the target model
2. In the copy's `Makefile`, change `TRANSLATOR` to the target model (everything else uses the common definitions in [onde/common.mk](onde/common.mk). The evaluator is Jev, pinned in `trtools/jev.py` and the same for every model to keep the scoring criteria consistent. `TRANSLATOR` isn't used by automated runs — it's a value for recording which model did the translation)
3. Rewrite the `TODO` spots (title, translation model name) in the copy's `README.md`
4. Add the target model's directory name to `MODELS` in the parent [onde/Makefile](onde/Makefile), and also add it to the directory list in [onde/README.md](onde/README.md) (`MODELS` is also the source data `generate_compare_rows.py` reads automatically for the comparison table)

Don't run `make` at this point (running it before the translations are in place will attempt translation via the target model's API and fail).

## 2. User Translates

Using the target model, manually create `onde/{model}/tr/onde-{lang}.txt` for each target language (`CORE_LANGS` + `EXTRA_LANGS`, defined in [onde/common.mk](onde/common.mk)).

- The source text is [onde-en.txt](onde-en.txt). Translate line by line, keeping blank lines as-is (matching `trtools translate`'s output format).
- Place translation files for all target languages before proceeding to the next step. If any language is missing its file, the next `make` run will attempt an API call to the target model for that language only, and fail.

## 3. Processing the Results

### 3.1 Running `make`

Run `make` in `onde/{model}/`. If translated files are already in place in `tr/`, the translation phase is entirely skipped, and only evaluation, the language check, aggregation, and trend generation (`evaluate` → `langcheck` → `scores-jev` → `trends-jev`) run. Jev's evaluations are output to `jev.jsonl`, the language check to `langcheck.jsonl`, scores to `SCORES-jev.txt`, and the trend column to `TREND-jev.jsonl`. `evaluate` calls TypeSafe's API, which is billed; `langcheck` calls it only for the languages fastText cannot settle (see [trtools langcheck](../../trtools/README.md#langcheck)).

The user runs this step; the rest of section 3 is done by Claude afterwards.

### 3.2 Checking the Target Language

Jev's scores do not notice a translation that is not in its target language, so the language check decides that separately. Each language comes out `ok`, `wrong` (totals **0** in `SCORES-jev.txt`, with the fixed trend "Not in the target language (detected: …)"), or `review` (undecided; keeps its score until settled). Go through the run's report before looking at the scores:

- **`wrong`**: read the translation and confirm that it really is not in the target language (English left from the source, a neighbouring language, collapse into repetition, etc.), and note what it is for 3.5. A `wrong` cannot be overridden: if the text turns out to be in the target language, the check itself is at fault, so stop and report it instead of going on.
- **`review`**: `langcheck` ends by listing these ("to read and settle with --resolve"), and `agg` notes each on stderr as well. Read each translation, decide whether it is in the target language, and record it in `onde/{model}/` with `uv run trtools langcheck --resolve <lang> {ok|wrong} --reason "<what the text is>"`. The decision goes to `langcheck-resolved.jsonl`, survives a re-run of the check, and stops `agg` if the check of that language later changes (the text has to be read again).
- After any `--resolve`, rerun `make scores-jev trends-jev` in `onde/{model}/`. A language settled as `wrong` gets the fixed trend, so no LLM is called for it.

### 3.3 Checking Scores and Evaluation Logs
- Check the output scores (`SCORES-jev.txt`).
- Jev returns scores without prose, so there are no evaluation logs to read. Read the translations (text files under `tr/`) alongside each language's per-criterion levels in `jev.jsonl` and its trend column to understand the specific issues (terminology accuracy, unnatural literal translation, garbled text, speaker-tag dropout, hallucinations such as system-prompt or other-language contamination, etc.). `trends-jev` prints the comment each trend phrase was written from while it runs; it is not saved.

### 3.4 Updating `README.md`
Update `onde/{model}/README.md` as follows.
- **Check the "Translation Quality Overview"**: this table is auto-generated from Jev's scores by `make` (the `trends-jev` target) via `trtools trend --jev --sync`, so no manual entry is needed. Check that the generated trend for each language is appropriate (see [ADD_LANG.md's 1.2.1](ADD_LANG.md#121-writing-policy-for-trend-analysis) for the writing policy).
- **Unify notation**: make sure the language notation is consistent throughout the file, avoiding inconsistencies with existing mentions (e.g. spelling variants of the same language).

### 3.5 Updating the Consolidated Results (`examples/tr/README.md`)

Once all directories have been updated, update the top-level `examples/tr/README.md` to summarize.

- Add the added model's full name (parameter scale, whether it's MoE, etc.) to the model abbreviation list at the top.
- Insert a link to the added directory into the `onde/` description list.
- Running `make sync-onde` in `examples/tr/` updates the "Comparison Between Translation Models" table (header row, separator row, body rows) all at once.

#### 3.5.1 Updating the Comparison Table
- Add the model to the model table at the top of `examples/tr/README.md` (model name linked to `onde/{model}/README.md`, and a description). The comparison table lists each language's top three scores and their models, so it needs no manual editing; models are read from `MODELS` in `onde/Makefile`.
- Update the comparison table by running `make sync-onde` in `examples/tr/`. The header row, separator row, and body rows are all rewritten together.
- Then run `make compare-onde` in `examples/tr/` to regenerate the per-model score-distribution boxplot (`MODELS.svg` and `compare/MODELS.png`).
- See [ADD_LANG.md's 2.1](ADD_LANG.md#21-updating-the-comparison-table) for details on the generation process, including the row-ordering algorithm.

#### 3.5.2 Updating the Trend Analysis Section
- **Stability items**: if the added model's results back up or overturn an existing trend, add the model name into the text as a concrete example.
- **Hallucination items**: add any peculiar phenomenon found for the added model.
- **Language check**: if any of the added model's translations is `wrong` (3.2), add it to the list of translations at 0 under "Checking the target language" (and update the count before the list), with what the text is instead (e.g. mostly English, written in Latin).
- **Don't distinguish old from new**: avoid phrasing like "the newly added ~" even in the discussion or notes of the consolidated `README.md`; integrate it naturally as part of the overall comparison across models.
- **Unify notation**: also check the consolidated `README.md` for inconsistent notation of the model name and unify it.

---

Following the above procedure lets you accurately maintain a record of per-model differences in translation quality and characteristic hallucination tendencies for comparative verification.
