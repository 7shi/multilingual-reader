MODELS = gemma4 gemma4-31b gpt-oss qwen3.6-27b qwen3.6 qwen3.8 \
		 bonsai2-27b \
		 muse-glimmer ox-alpha union-alpha \
		 gpt-5.6-luna gpt-5.6-terra \
		 gemini-3.5-flash-lite gemini-2.5-flash gemini-3-flash gemini-3.7-flash

# Jev evaluation for every model, one directory at a time. `jev-<model>` runs one of
# them; the model is the outer loop either way, so a run is a sequence of whole
# directories rather than an interleaving nothing could resume cleanly.
JEV_MODELS = $(MODELS:%=jev-%)

# TREND-jev.jsonl for every model, the same way. README.md is not synced: its table
# moves to the Jev scale together with SCORES.txt, so each directory's own
# `make trends-jev` does that at the switch, skipping the languages already written.
TREND_JEV_MODELS = $(MODELS:%=trends-jev-%)

.PHONY: all jev trends-jev $(MODELS) $(JEV_MODELS) $(TREND_JEV_MODELS)

all: $(MODELS)

$(MODELS):
	$(MAKE) -C $@

jev: $(JEV_MODELS)

$(JEV_MODELS): jev-%:
	$(MAKE) -C $* jev

trends-jev: $(TREND_JEV_MODELS)

$(TREND_JEV_MODELS): trends-jev-%:
	$(MAKE) -C $* trends-jev TREND_SYNC=
