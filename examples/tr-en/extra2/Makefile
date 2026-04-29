.PHONY: all translate evaluate scores

DIR = ../..
include $(DIR)/terms/common.mk

TRANSLATOR1 = ollama:gpt-oss:120b
TRANSLATOR2 = openrouter:openai/gpt-oss-120b:free
EVALUATOR1 = ollama:qwen3.6
EVALUATOR2 = openrouter:qwen/qwen3.6-35b-a3b

TRANSLATE = uv run trtools batch \
	--terms-dir $(DIR)/terms \
	--threshold 20 \
	--no-think \
	$(DIR)/onde-en.txt \
	--langs $(EXTRA_LANGS)

all: translate evaluate scores

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR1)
	$(TRANSLATE) --tr-only -m $(TRANSLATOR2) --tr-dir tr-openrouter

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR1)
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR2) --eval-dir evals-openrouter

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
	uv run trtools agg evals-openrouter/*.json | tee SCORES-openrouter.txt
