MODELS = plamo-3-translate-0.8b plamo-3-translate-2b plamo-3-translate-8b plamo-3-translate-31b \
		 gemma4-e2b gemma4-e4b gemma4-12b gemma4-26b gemma4-31b \
		 gpt-6-luna gpt-6-astra gemini-4-argon gemini-3.8-flash

.PHONY: all langcheck $(MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@

langcheck: $(MODELS:%=langcheck-%)

langcheck-%:
	$(MAKE) -C $* langcheck
