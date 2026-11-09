# Procedure When Adding a Model to `plamo/`

Procedure for adding a model to [plamo/](plamo/), the set translated under PLaMo 3 Translate's conditions ([plamo/PLAN.md](plamo/PLAN.md)), and reflecting its results there. It follows [ADD_MODEL.md](ADD_MODEL.md) for onde/, with these differences:

- the target languages are PLaMo's (`PLAMO_LANGS` in [common.mk](common.mk)), not the corpus's;
- the whole text goes in one request per language, and `make` translates it, so the user runs the translation through `make` rather than placing the files by hand;
- the line alignment is not held, and its breaks are kept as part of the performance;
- the results go to [plamo/README.md](plamo/README.md), never to the main comparison in [README.md](README.md).

The same three steps apply.

1. Prepare under `plamo/`
2. User translates
3. Process the results

PLaMo 3 Translate translates with `trtools plamo`, and a general model, compared with it on the same request ([plamo/PLAN.md](plamo/PLAN.md)'s section 3), with `trtools whole`. A general model takes the name of its onde/ directory, so that its line-by-line counterpart is [onde/{model}/](onde/), unless it runs a different build of the model, which then takes a name of its own (`gemma4-26b`, the QAT build, beside onde/'s `gemma4`, Q4_K_M).

## 1. Preparing Under `plamo/`

`plamo/` has no template directory; an existing model directory such as [plamo/plamo-3-translate-2b/](plamo/plamo-3-translate-2b/) serves as one.

1. Create a directory named after the model, with a `Makefile` that includes `../common.mk` (the languages and the translation command come from [plamo/common.mk](plamo/common.mk)):
   - a general model sets `TRANSLATOR` and `OPTIONS` as in its onde/ `Makefile`, and translates with `trtools whole` by default, as [plamo/gpt-6-luna/](plamo/gpt-6-luna/) does:
     ```make
     TRANSLATOR = gpt-6-luna
     OPTIONS    =

     include ../common.mk
     ```
   - PLaMo 3 Translate sets `TRANSLATOR` and switches the command to `trtools plamo` after the include:
     ```make
     TRANSLATOR = llama.cpp:plamo-3-translate-2b-Q4_K_M

     include ../common.mk
     TRANSLATE_CMD = $(PLAMO_TRANSLATE)
     ```
2. Copy `README.md` from an existing directory of the same kind ([plamo/gpt-6-luna/](plamo/gpt-6-luna/) for a general model) and rewrite its title, model card link, model name, model file name and running conditions. Leave out the parts about the earlier model's results (line breaks, the language check), and empty the quality table, which `make` fills.
3. Add the directory name to `MODELS` in [plamo/Makefile](plamo/Makefile), and to the list in [plamo/README.md](plamo/README.md). `MODELS` is also what `generate_compare_rows.py` reads for plamo/'s tables and chart.

Check the Makefile with `make -n` in the new directory. Don't run `make` itself at this point.

## 2. User Translates

The user starts the model's server and runs `make` in `plamo/{model}/`, which translates every language and then evaluates.

- A general model: as in onde/, with the same server or API. On Ollama, set the context to 32,768 tokens (`OLLAMA_CONTEXT_LENGTH=32768` for the server), since the whole text and its translation go in one request.
- PLaMo 3 Translate: `llama-server -c 32768 --jinja --no-prefill-assistant`, reached with `OPENAI_BASE_URL` (e.g. `OPENAI_BASE_URL=http://host:8000/v1 make`). 32,768 tokens is the model card's training length for input and output combined; whether a larger model fits that much context on the machine is the user's to check.
- A language whose file exists in `tr/` is skipped, so an interrupted run can be resumed by running `make` again.
- `trtools plamo` and `trtools whole` warn when a translation's line count differs from the source's, or when the output stopped on repetition or length. The translation is saved either way; it is not retranslated.

## 3. Processing the Results

As in [ADD_MODEL.md](ADD_MODEL.md)'s section 3, done by Claude after the user's `make`, with the following differences.

### 3.1 Line Alignment

Compare each translation's line count with the source's 99 (`wc -l tr/*.txt`). Where it differs, or where a line runs far longer than the source's, find what happened, by setting the translation beside the source:

- a stretch skipped, with a natural ending after it;
- a loop on a word, a phrase or a few lines until the output stops;
- a stretch gone back to and translated again;
- a line split in two, two lines joined, or a line added.

These are not fixed, retranslated or excluded; they are kept as part of the model's performance under its intended use. Note each, by language and what happened, for 3.4.

### 3.2 Checking the Target Language

As in [ADD_MODEL.md](ADD_MODEL.md)'s 3.2, run in `plamo/{model}/`. Two cases recur here:

- **Traditional Chinese** (`zh-hant`) always comes out `review`, since the detector does not tell the two scripts apart. Read it for simplified characters, and settle it.
- **Serbian** may come out `review` with Croatian forms; read it for its script and forms, and settle it.

### 3.3 Checking Scores and Trends

As in [ADD_MODEL.md](ADD_MODEL.md)'s 3.3 and 3.4. A trend phrase that blames a break the translation does not have (e.g. "incomplete" for a full translation) is to be corrected, as in onde/.

### 3.4 Updating `plamo/{model}/README.md`

Add, as facts and without scores, the line-alignment breaks found in 3.1 and the language check's settlements from 3.2, in the form of the existing models' READMEs.

### 3.5 Updating `plamo/README.md`

- Run `make sync-plamo` in `examples/tr/`: it rewrites plamo/'s two tables in [plamo/README.md](plamo/README.md) (the stats per model and the scores per language), and leaves the main comparison, which the plamo/ models are not part of, untouched.
- Write the model's Notes in the stats table by hand, comparing it only with the other plamo/ models, on PLaMo's languages (e.g. Wilcoxon signed-rank against the neighbouring sizes, or a general model against the largest PLaMo). For a general model, also compare it with its onde/ counterpart on the corpus languages they share, which is the method's own effect.
- Update the text around the tables, such as the comparison between sizes and the line-alignment breaks, if the model changes them.
- Run `make compare-plamo` in `examples/tr/` to regenerate plamo/'s chart (`PLAMO.svg` and `compare/PLAMO.png`) without touching the main chart (`MODELS.svg`).
- Don't add the model to [README.md](README.md)'s model table, its comparison or its discussion.
