# Shared definitions for each onde model directory
# Each Makefile defines only its model-specific part (TRANSLATOR) and includes this.

.PHONY: all translate evaluate jev scores scores-jev trends

DIR = ../../..
include ../../common.mk

EVALUATOR  = ollama:qwen3.6
SUMMARIZER = $(EVALUATOR)
OPTIONS   ?= --no-think

# Target languages. Overridden by the caller when only a subset is needed, e.g. for past experiments.
LANGS = $(CORE_LANGS) $(EXTRA_LANGS)

TRANSLATE = uv run trtools batch \
	--terms-dir ../../terms \
	--threshold 20 \
	$(OPTIONS) \
	$(DIR)/onde-en.txt \
	--langs $(LANGS)

all: translate evaluate scores trends

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR)

# Jev evaluation, alongside evaluate: it writes jev.jsonl and leaves evals/ untouched.
# One run per language; the model version is pinned in trtools/jev.py.
jev:
	uv run trtools jev $(DIR)/onde-en.txt --langs $(LANGS)

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt

# Totals from jev.jsonl, beside SCORES.txt until EVALUATOR switches over.
scores-jev:
	uv run trtools agg --jev --prefix onde jev.jsonl | tee SCORES-jev.txt

trends:
	uv run trtools trend evals/*.json -m $(SUMMARIZER) --no-think --sync README.md
