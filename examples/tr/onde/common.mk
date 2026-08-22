# onde 各モデルディレクトリの共通定義
# 各 Makefile では固有部分（TRANSLATOR）のみ定義してこれを include する。

.PHONY: all translate evaluate scores trends

DIR = ../../..
include ../../common.mk

EVALUATOR  = ollama:qwen3.6
SUMMARIZER = $(EVALUATOR)
OPTIONS   ?= --no-think

# 対象言語。過去実験など一部の言語だけを扱う場合はターゲット側で上書きする。
LANGS = $(CORE_LANGS) $(EXTRA_LANGS)

TRANSLATE = uv run trtools batch \
	--terms-dir ../../terms \
	--threshold 20 \
	$(OPTIONS) \
	$(DIR)/onde-en.txt \
	--langs $(LANGS)

all: translate evaluate scores trends

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

evaluate:
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR)

scores:
	uv run trtools agg evals/*.json | tee SCORES.txt

trends:
	uv run trtools trend evals/*.json -m $(SUMMARIZER) --no-think --sync README.md
