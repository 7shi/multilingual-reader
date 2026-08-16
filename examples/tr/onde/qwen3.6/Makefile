TRANSLATOR = ollama:qwen3.6

include ../common.mk

# 【過去実験】評価者を他モデルに替え、自己評価と他者評価の採点基準を比較したもの。
# 翻訳は共通の tr/ を再利用するため、評価と集計のみ行う。
# all には含めず、対象言語は実験当時のセットに固定する。
ALT = gpt-oss-120b
ALT_EVALUATOR = ollama:gpt-oss:120b

.PHONY: $(ALT)
$(ALT): LANGS = eo hi te kn tr et sr ko
$(ALT):
	$(TRANSLATE) --eval-only --evaluator $(ALT_EVALUATOR) --eval-dir $(ALT)/evals
	uv run trtools agg $(ALT)/evals/*.json | tee $(ALT)/SCORES.txt
