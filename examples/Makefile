# 各トピックの要約を trtools translate 用に事前生成する。
# 要約は英語で出力され to_lang に依存しないため、トピックごとに1回生成すればよい
# （生成済みなら trtools summary 側で即座にスキップされる）。
# threshold は examples/tr/onde/common.mk の TRANSLATE 定義に合わせている。

TOPICS = finetuning momentum onde transformer

.PHONY: all

all:
	uv run trtools summary $(TOPICS:%=%-en.txt) -f English --threshold 20 -m ollama:qwen3.8
