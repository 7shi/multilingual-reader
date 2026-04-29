.PHONY: all translate evaluate scores

DIR = ../..
TRANSLATOR = ollama:gemma4:26b
EVALUATOR = ollama:qwen3.6

TRANSLATE = uv run trtools batch \
	--terms-dir $(DIR)/terms \
	--threshold 20 \
	--no-think \
	$(DIR)/finetuning-en.txt $(DIR)/transformer-en.txt $(DIR)/momentum-en.txt $(DIR)/onde-en.txt \
	--langs de ja zh

all: translate evaluate scores

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR)

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
