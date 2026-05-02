INPUT    := ../../examples/finetuning-fr.txt
EVAL_PY  := ../../experimental/evaluate_translation.py
AGG_PY   := ../../experimental/aggregate_evaluations.py
MODEL    := ollama:gemma3:27b
EVALUATOR:= ollama:qwen3.6
OPTS     := -f French -t Spanish -m $(MODEL) --summary glossary
EVAL_OPT := --original $(INPUT) -f French -t Spanish -m $(EVALUATOR) -w 3

.PHONY: all translate eval aggregate clean

all: SCORES.txt

# --- 翻訳 ---

glossary.txt:
	uv run ../translate.py $(INPUT) $(OPTS) \
	  -o $@ 2>/dev/null | tee glossary.log

glossary-no-hist.txt:
	uv run ../translate.py $(INPUT) $(OPTS) --no-summary-history \
	  -o $@ 2>/dev/null | tee glossary-no-hist.log

translate: glossary.txt glossary-no-hist.txt

# --- 評価（各3回）---

glossary-eval-1.json: glossary.txt
	uv run $(EVAL_PY) $(EVAL_OPT) --translation $< -o $@

glossary-eval-2.json: glossary.txt
	uv run $(EVAL_PY) $(EVAL_OPT) --translation $< -o $@

glossary-eval-3.json: glossary.txt
	uv run $(EVAL_PY) $(EVAL_OPT) --translation $< -o $@

glossary-no-hist-eval-1.json: glossary-no-hist.txt
	uv run $(EVAL_PY) $(EVAL_OPT) --translation $< -o $@

glossary-no-hist-eval-2.json: glossary-no-hist.txt
	uv run $(EVAL_PY) $(EVAL_OPT) --translation $< -o $@

glossary-no-hist-eval-3.json: glossary-no-hist.txt
	uv run $(EVAL_PY) $(EVAL_OPT) --translation $< -o $@

eval: glossary-eval-1.json glossary-eval-2.json glossary-eval-3.json \
      glossary-no-hist-eval-1.json glossary-no-hist-eval-2.json glossary-no-hist-eval-3.json

# --- 集約 ---

SCORES.txt: glossary-eval-1.json glossary-eval-2.json glossary-eval-3.json \
            glossary-no-hist-eval-1.json glossary-no-hist-eval-2.json glossary-no-hist-eval-3.json
	uv run $(AGG_PY) $^ | tee $@

# --- クリーンアップ ---

clean:
	rm -f glossary.txt glossary.log glossary-eval-*.json \
	      glossary-no-hist.txt glossary-no-hist.log glossary-no-hist-eval-*.json \
	      SCORES.txt
