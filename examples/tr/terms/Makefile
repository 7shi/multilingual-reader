include ../common.mk

MODEL       = ollama:gemma4:31b
#MODEL      = google:gemma-4-31b-it
#MODEL      = openrouter:google/gemma-4-31b-it:free
KEEP        = 5
TOPICS      = finetuning transformer onde momentum
CORE_FLAGS  = $(foreach l,$(CORE_LANGS),-t $(l))
EXTRA_FLAGS = $(foreach l,$(EXTRA_LANGS),-t $(l))
CMD         = uv run trtools term

.PHONY: all common core extra $(TOPICS)

all: common core extra

common:
	$(CMD) translate -o $@.tsv $@.json $(EXTRA_FLAGS) -m "$(MODEL)" --no-think

core: $(TOPICS)

$(TOPICS): %: ../../%-fr.txt ../../%-en.txt
	$(CMD) extract -o $@-fr.json ../../$@-fr.txt -f fr -m "$(MODEL)" --keep $(KEEP) --no-think
	$(CMD) translate -o $@-fr.tsv $@-fr.json -t en -t es -m "$(MODEL)" --no-think -c common.tsv
	$(CMD) extract -o $@-en.json ../../$@-en.txt -f en -m "$(MODEL)" --keep $(KEEP) --no-think
	$(CMD) translate -o $@-en.tsv $@-en.json $(CORE_FLAGS) -m "$(MODEL)" --no-think -c common.tsv

extra: onde-en.json
	$(CMD) translate -o onde-en.tsv $< $(EXTRA_FLAGS) -m "$(MODEL)" --no-think -c common.tsv
