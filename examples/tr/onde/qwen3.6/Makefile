TRANSLATOR = ollama:qwen3.6

include ../common.mk

# [Past experiment] Swapped the evaluator to a different model to compare self-evaluation
# vs. third-party evaluation scoring criteria.
# Translation reuses the shared tr/, so only evaluation and aggregation are run here.
# Not included in `all`; the target languages are fixed to the set used at the time of the experiment.
ALT = gpt-oss-120b
ALT_EVALUATOR = ollama:gpt-oss:120b

.PHONY: $(ALT)
$(ALT): LANGS = eo hi te kn tr et sr ko
$(ALT):
	$(TRANSLATE) --eval-only --evaluator $(ALT_EVALUATOR) --eval-dir $(ALT)/evals
	uv run trtools agg $(ALT)/evals/*.json | tee $(ALT)/SCORES.txt
