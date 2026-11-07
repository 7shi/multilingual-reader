.PHONY: all translate evaluate langcheck scores scores-jev

DIR = ../..
include ../common.mk

TRANSLATOR = ollama:gemma4:26b
TOPICS = finetuning transformer momentum

TRANSLATE = uv run trtools batch \
	--terms-dir ../terms \
	--threshold 20 \
	--no-think \
	$(foreach t,$(TOPICS),$(DIR)/$(t)-en.txt) \
	--langs $(CORE_LANGS)

all: translate evaluate langcheck scores-jev

translate:
	$(TRANSLATE) --tr-only -m $(TRANSLATOR)

# Jev, one run per language, pinned in trtools/jev.py. One file per topic, since a record
# names only its language. evals/ is the previous evaluator's record (ollama:qwen3.6,
# three runs each) and is no longer written.
evaluate:
	for t in $(TOPICS); do \
		uv run trtools jev $(DIR)/$$t-en.txt --langs $(CORE_LANGS) -o jev-$$t.jsonl || exit 1; \
	done

# Whether each translation is in its target language, appended to langcheck-{topic}.jsonl
# (experimental/15/PORT.md). A language found not to be in it totals 0 in scores-jev.
# LANGCHECK_OPTS=--force re-checks a file written on an earlier scheme.
langcheck:
	for t in $(TOPICS); do \
		uv run trtools langcheck $(DIR)/$$t-en.txt --langs $(CORE_LANGS) -o langcheck-$$t.jsonl $(LANGCHECK_OPTS) || exit 1; \
	done

# The previous evaluator's totals, from evals/. Kept beside SCORES-jev.txt as its record;
# not in all:, since evaluate no longer writes evals/.
scores:
	uv run trtools agg evals/*.json > SCORES.txt.tmp
	mv SCORES.txt.tmp SCORES.txt
	cat SCORES.txt

scores-jev:
	for t in $(TOPICS); do \
		uv run trtools agg --jev --prefix $$t --langcheck langcheck-$$t.jsonl jev-$$t.jsonl || exit 1; \
	done > SCORES-jev.txt.tmp
	mv SCORES-jev.txt.tmp SCORES-jev.txt
	cat SCORES-jev.txt
