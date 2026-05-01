.PHONY: all translate evaluate scores

DIR = ../../..
include ../../common.mk

TRANSLATOR = ollama:gemma4:26b
EVALUATOR = ollama:qwen3.6

TRANSLATE = uv run trtools batch \
	--terms-dir ../../terms \
	--threshold 20 \
	--no-think \
	$(DIR)/onde-en.txt \
	--langs $(CORE_LANGS) $(EXTRA_LANGS)

all: translate evaluate scores

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR)

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
