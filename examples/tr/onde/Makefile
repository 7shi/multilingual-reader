MODELS = gemma4 gpt-oss qwen3.6 qwen3.8 muse-glimmer ox-alpha gpt-5.6-luna gemini-3.5-flash-lite

.PHONY: all $(MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@
