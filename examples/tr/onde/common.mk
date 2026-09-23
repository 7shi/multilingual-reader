# Shared definitions for each onde model directory
# Each Makefile defines only its model-specific part (TRANSLATOR) and includes this.

.PHONY: all translate evaluate jev scores scores-jev trends trends-jev

DIR = ../../..
include ../../common.mk

EVALUATOR  = ollama:qwen3.6
# Written out rather than following EVALUATOR: Jev writes no prose, so a summarizer
# that followed it once it becomes the evaluator would have nothing to write with.
SUMMARIZER = ollama:qwen3.6
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

# The trend column on the Jev scale, in its own file: TRENDS.jsonl stays the old scale's
# record. Takes the place of trends in all: when EVALUATOR switches over. TREND_SYNC=
# writes TREND-jev.jsonl without touching README.md, for generating ahead of the switch.
TREND_SYNC = --sync README.md

trends-jev:
	uv run trtools trend --jev jev.jsonl --original $(DIR)/onde-en.txt \
		-m $(SUMMARIZER) -o TREND-jev.jsonl $(TREND_SYNC)
