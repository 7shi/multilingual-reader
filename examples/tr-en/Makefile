.PHONY: all translate evaluate scores

OTHERS_BASE = uv run trtools batch \
	../finetuning-en.txt ../transformer-en.txt ../momentum-en.txt \
	--langs de ja zh \
	-m ollama:gemma4:26b \
	--terms-dir ../terms \
	--threshold 20 \
	--no-think

ONDE_BASE = uv run trtools batch \
	../onde-en.txt \
	--langs de ja zh eo hi \
	-m ollama:gemma4:26b \
	--terms-dir ../terms \
	--threshold 20 \
	--no-think

all: translate evaluate scores

translate:
	$(OTHERS_BASE) --translate-only
	$(ONDE_BASE) --translate-only

evaluate:
	$(OTHERS_BASE) --evaluator ollama:qwen3.6 --no-agg
	$(ONDE_BASE) --evaluator ollama:qwen3.6 --no-agg

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt
