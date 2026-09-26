MODELS = gemma4 gemma4-31b gemma4-12b gemma4-e4b gemma4-e2b gpt-oss \
		 qwen3.5-9b qwen3.5-4b qwen3.6-27b qwen3.6 qwen3.8 \
		 bonsai2-27b muse-glimmer \
		 gpt-5.6-luna gpt-5.6-terra gpt-6-luna \
		 gemini-3.5-flash-lite gemini-2.5-flash gemini-3-flash gemini-3.7-flash \
		 ox-alpha union-alpha space-bunny-alpha

.PHONY: all $(MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@
