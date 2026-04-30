.PHONY: all translate evaluate scores

DIR = ../..
include $(DIR)/terms/common.mk

TRANSLATOR = ollama:qwen3.6
EVALUATOR1 = ollama:qwen3.6
EVALUATOR2 = ollama:gpt-oss:120b

TRANSLATE = uv run trtools batch \
	--terms-dir $(DIR)/terms \
	--threshold 20 \
	--no-think \
	$(DIR)/onde-en.txt \
	--langs $(EXTRA_LANGS)

all: translate evaluate scores

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR1)
	#$(TRANSLATE) --eval-only --evaluator $(EVALUATOR2) --eval-dir gpt-oss-120b/evals

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
	#uv run trtools agg gpt-oss-120b/evals/*.json | tee gpt-oss-120b/SCORES.txt
