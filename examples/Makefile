# Pre-generate each topic's summary for use by trtools translate.
# Summaries are output in English and don't depend on to_lang, so generating
# once per topic is enough (trtools summary skips instantly if already generated).
# threshold matches the TRANSLATE definition in examples/tr/onde/common.mk.

TOPICS = finetuning momentum onde transformer

.PHONY: all

all:
	uv run trtools summary $(TOPICS:%=%-en.txt) -f English --threshold 20 -m ollama:qwen3.8
