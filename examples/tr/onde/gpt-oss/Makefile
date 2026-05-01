.PHONY: all translate evaluate scores

DIR = ../../..
include ../../common.mk

TRANSLATOR1 = ollama:gpt-oss:120b
TRANSLATOR2 = openrouter:openai/gpt-oss-120b:free
EVALUATOR1 = ollama:qwen3.6
EVALUATOR2 = openrouter:qwen/qwen3.6-35b-a3b

TRANSLATE = uv run trtools batch \
	--terms-dir ../../terms \
	--threshold 20 \
	--no-think \
	$(DIR)/onde-en.txt \
	--langs $(CORE_LANGS) $(EXTRA_LANGS)

all: translate evaluate scores

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR1)
	#$(TRANSLATE) --tr-only -m $(TRANSLATOR2) --tr-dir openrouter/tr

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR1)
	#$(TRANSLATE) --eval-only --evaluator $(EVALUATOR1) --tr-dir openrouter/tr --eval-dir openrouter/evals-ollama
	#$(TRANSLATE) --eval-only --evaluator $(EVALUATOR2) --tr-dir openrouter/tr --eval-dir openrouter/evals

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
	#uv run trtools agg openrouter/evals-ollama/*.json | tee openrouter/SCORES-ollama.txt
	#uv run trtools agg openrouter/evals/*.json | tee openrouter/SCORES.txt
