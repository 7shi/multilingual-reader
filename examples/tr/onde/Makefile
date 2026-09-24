MODELS = gemma4 gemma4-31b gpt-oss qwen3.6-27b qwen3.6 qwen3.8 \
		 bonsai2-27b muse-glimmer \
		 gpt-5.6-luna gpt-5.6-terra \
		 gemini-3.5-flash-lite gemini-2.5-flash gemini-3-flash gemini-3.7-flash \
		 ox-alpha union-alpha

.PHONY: all $(MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@
