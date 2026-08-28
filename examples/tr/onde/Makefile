MODELS = gemma4 gemma4-31b gpt-oss qwen3.6-27b qwen3.6 qwen3.8 \
		 muse-glimmer ox-alpha \
		 gpt-5.6-luna \
		 gemini-3.5-flash-lite gemini-2.5-flash gemini-3-flash

.PHONY: all $(MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@
