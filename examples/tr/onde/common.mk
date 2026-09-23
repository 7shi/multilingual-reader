# Shared definitions for each onde model directory
# Each Makefile defines only its model-specific part (TRANSLATOR) and includes this.

.PHONY: all translate evaluate scores scores-jev trends-jev

DIR = ../../..
include ../../common.mk

# The evaluator is Jev, pinned in trtools/jev.py. The trend column's writer is a
# generative model of its own, since Jev writes no prose.
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

all: translate evaluate scores-jev trends-jev

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

# Jev, one run per language, appended to jev.jsonl. evals/ and TRENDS.jsonl are the
# previous evaluator's record (ollama:qwen3.6, three runs each) and are no longer written.
evaluate:
	uv run trtools jev $(DIR)/onde-en.txt --langs $(LANGS)

# The previous evaluator's totals, from evals/. Kept beside SCORES-jev.txt as its record;
# not in all:, since evaluate no longer writes evals/.
scores:
	uv run trtools agg evals/*.json > SCORES.txt.tmp
	mv SCORES.txt.tmp SCORES.txt
	cat SCORES.txt

scores-jev:
	uv run trtools agg --jev --prefix onde jev.jsonl > SCORES-jev.txt.tmp
	mv SCORES-jev.txt.tmp SCORES-jev.txt
	cat SCORES-jev.txt

# The trend column, in its own file so the old scale's TRENDS.jsonl is never appended to.
trends-jev:
	uv run trtools trend --jev jev.jsonl --original $(DIR)/onde-en.txt \
		-m $(SUMMARIZER) -o TREND-jev.jsonl --sync README.md
