.PHONY: all translate evaluate scores

DIR = ../..
TRANSLATOR = ollama:qwen3.6
EVALUATOR1 = ollama:qwen3.6
EVALUATOR2 = ollama:gpt-oss:120b

TRANSLATE = uv run trtools batch \
	--terms-dir $(DIR)/terms \
	--threshold 20 \
	--no-think \
	$(DIR)/onde-en.txt \
	--langs eo hi te kn tr et sr

all: translate evaluate scores

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR1)
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR2) --eval-dir evals-gpt-oss-120b

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
	uv run trtools agg evals-gpt-oss-120b/*.json | tee SCORES-gpt-oss-120b.txt
