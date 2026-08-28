TRANSLATOR = ollama:gpt-oss:120b

include ../common.mk

# [Past experiment] Verified behavioral differences between local (Ollama) and cloud
# (OpenRouter) execution environments. Not included in `all`; only runs when
# explicitly specified. The target languages are fixed to the set used at the time of the experiment.
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
