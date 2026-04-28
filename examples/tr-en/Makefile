.PHONY: all translate evaluate scores

TRANSLATOR = ollama:gemma4:26b
EVALUATOR = ollama:qwen3.6

BATCH = uv run trtools batch \
	-m $(TRANSLATOR) \
	--terms-dir ../terms \
	--threshold 20 \
	--no-think

CORE_BASE = $(BATCH) \
	../finetuning-en.txt ../transformer-en.txt ../momentum-en.txt ../onde-en.txt \
	--langs de ja zh

EXTRA_BASE = $(BATCH) \
	../onde-en.txt \
	--langs eo hi te kn tr et sr

all: translate evaluate scores

translate:
	$(CORE_BASE) --translate-only
	$(EXTRA_BASE) --translate-only

evaluate:
	$(CORE_BASE) --evaluator $(EVALUATOR) --no-agg
	$(EXTRA_BASE) --evaluator $(EVALUATOR) --no-agg

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
