MODELS = gemma4 gpt-oss qwen3.6 qwen3.8 muse-glimmer ox-alpha

.PHONY: all $(MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@
