.PHONY: all core onde compare

all: core onde

core:
	$(MAKE) -C core

onde:
	$(MAKE) -C onde

GEMINI35FL = -i gemini-3.5-flash-lite -l "Gemini 3.5 Flash Lite"
GEMINI25F  = -i gemini-2.5-flash -l "Gemini 2.5 Flash"
GEMMA4     = -i gemma4 -l "Gemma 4 26B-A4B"
GEMMA4_31B = -i gemma4-31b -l "Gemma 4 31B"

compare:
	uv run generate_compare_rows.py graph
	uv run plot_comparison.py -o compare/gemini35fl.png $(GEMINI35FL) $(GEMINI25F) $(GEMMA4) $(GEMMA4_31B)
	uv run plot_comparison.py -o compare/gemini25f.png $(GEMINI25F) $(GEMINI35FL) $(GEMMA4) $(GEMMA4_31B)
	uv run plot_comparison.py -o compare/gemma4.png $(GEMMA4) $(GEMINI35FL) $(GEMINI25F) $(GEMMA4_31B)
	uv run plot_comparison.py -o compare/gemma4_31b.png $(GEMMA4_31B) $(GEMINI35FL) $(GEMINI25F) $(GEMMA4)
