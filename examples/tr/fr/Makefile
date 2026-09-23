.PHONY: all translate evaluate scores-jev

DIR = ../..
TOPICS = finetuning transformer onde momentum
LANGS = en es

all: translate evaluate scores-jev

translate:
	uv run trtools batch \
		$(foreach t,$(TOPICS),$(DIR)/$(t)-fr.txt) \
		--langs $(LANGS) \
		-m ollama:gemma4:26b \
		--terms-dir ../terms \
		--no-think \
		--tr-only

# Jev, one run per language, pinned in trtools/jev.py. One file per topic, since a record
# names only its language. evals/ and SCORES.txt are the previous evaluator's record
# (ollama:qwen3.6, three runs each) and are no longer written.
evaluate:
	for t in $(TOPICS); do \
		uv run trtools jev $(DIR)/$$t-fr.txt -f French --langs $(LANGS) -o jev-$$t.jsonl || exit 1; \
	done

scores-jev:
	for t in $(TOPICS); do \
		uv run trtools agg --jev --prefix $$t jev-$$t.jsonl || exit 1; \
	done > SCORES-jev.txt.tmp
	mv SCORES-jev.txt.tmp SCORES-jev.txt
	cat SCORES-jev.txt
