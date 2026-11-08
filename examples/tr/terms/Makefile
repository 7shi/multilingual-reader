include ../common.mk

MODEL       = ollama:gemma4:31b
#MODEL      = google:gemma-4-31b-it
#MODEL      = openrouter:google/gemma-4-31b-it:free
KEEP        = 5
TOPICS      = finetuning transformer onde momentum
CORE_FLAGS  = $(foreach l,$(CORE_LANGS),-t $(l))
EXTRA_FLAGS = $(foreach l,$(EXTRA_LANGS),-t $(l))
PLAMO_ONLY  = $(filter-out $(CORE_LANGS) $(EXTRA_LANGS),$(PLAMO_LANGS))
PLAMO_FLAGS = $(foreach l,$(PLAMO_ONLY),-t $(l))
CMD         = uv run trtools term

.PHONY: all common core extra plamo $(TOPICS)

all: common core extra plamo

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

# The languages PLaMo 3 Translate supports outside the corpus (../common.mk), for its
# glossary: common.tsv first, so that onde-en.tsv takes the shared names from it.
plamo: MODEL = gpt-6-luna
plamo: onde-en.json
	$(CMD) translate -o common.tsv common.json $(PLAMO_FLAGS) -m "$(MODEL)" --no-think
	$(CMD) translate -o onde-en.tsv $< $(PLAMO_FLAGS) -m "$(MODEL)" --no-think -c common.tsv
