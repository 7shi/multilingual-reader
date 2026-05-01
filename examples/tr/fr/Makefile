.PHONY: all

all:
	uv run trtools batch \
		../../finetuning-fr.txt ../../transformer-fr.txt ../../onde-fr.txt ../../momentum-fr.txt \
		--langs en es \
		-m ollama:gemma4:26b \
		--evaluator ollama:qwen3.6 \
		--terms-dir ../terms \
		--no-think
