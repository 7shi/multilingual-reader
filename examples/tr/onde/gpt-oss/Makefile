TRANSLATOR = ollama:gpt-oss:120b

include ../common.mk

# 【過去実験】ローカル（Ollama）とクラウド（OpenRouter）の実行環境の違いによる
# 挙動の差異を検証したもの。all には含めず、明示的に指定した場合のみ実行する。
# 対象言語は実験当時のセットに固定する。
.PHONY: openrouter

OR_TRANSLATOR = openrouter:openai/gpt-oss-120b:free
OR_EVALUATOR  = openrouter:qwen/qwen3.6-35b-a3b
OR = openrouter

openrouter: LANGS = eo hi te kn tr et sr ko
openrouter:
	$(TRANSLATE) --tr-only -m $(OR_TRANSLATOR) --tr-dir $(OR)/tr
	$(TRANSLATE) --eval-only --evaluator $(EVALUATOR) --tr-dir $(OR)/tr --eval-dir $(OR)/evals-ollama
	$(TRANSLATE) --eval-only --evaluator $(OR_EVALUATOR) --tr-dir $(OR)/tr --eval-dir $(OR)/evals
	uv run trtools agg $(OR)/evals-ollama/*.json | tee $(OR)/SCORES-ollama.txt
	uv run trtools agg $(OR)/evals/*.json | tee $(OR)/SCORES.txt
