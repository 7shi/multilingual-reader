.PHONY: help all core onde sync compare

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  all      core + onde"
	@echo "  core     build core examples"
	@echo "  onde     build onde examples"
	@echo "  sync     sync comparison table into README.md"
	@echo "  compare  generate comparison graphs/tables"

all: core onde

core:
	$(MAKE) -C core

onde:
	$(MAKE) -C onde

GEMINI35FL = -i gemini-3.5-flash-lite -l "Gemini 3.5 Flash Lite"
GEMINI25F  = -i gemini-2.5-flash -l "Gemini 2.5 Flash"
GEMMA4     = -i gemma4 -l "Gemma 4 26B-A4B"
GEMMA4_31B = -i gemma4-31b -l "Gemma 4 31B"
GEMINI3F   = -i gemini-3-flash -l "Gemini 3 Flash Preview"
QWEN36     = -i qwen3.6 -l "Qwen 3.6 35B-A3B"
QWEN36_27B = -i qwen3.6-27b -l "Qwen 3.6 27B"
QWEN38     = -i qwen3.8 -l "Qwen 3.8 27B"
GPT56LUNA  = -i gpt-5.6-luna -l "GPT-5.6 Luna"
GPT56TERRA = -i gpt-5.6-terra -l "GPT-5.6 Terra"
GPTOSS     = -i gpt-oss -l "GPT-OSS 120B"

sync:
	uv run generate_compare_rows.py compare --sync

compare:
	uv run generate_compare_rows.py graph
	uv run plot_comparison.py -o compare/gemini35fl.png $(GEMINI35FL) $(GEMINI25F) $(GEMMA4) $(GEMMA4_31B) $(GEMINI3F)
	uv run plot_comparison.py -o compare/gemini25f.png $(GEMINI25F) $(GEMINI35FL) $(GEMMA4) $(GEMMA4_31B) $(GEMINI3F)
	uv run plot_comparison.py -o compare/gemma4.png $(GEMMA4) $(GEMINI35FL) $(GEMINI25F) $(GEMMA4_31B) $(GEMINI3F)
	uv run plot_comparison.py -o compare/gemma4_31b.png $(GEMMA4_31B) $(GEMINI35FL) $(GEMINI25F) $(GEMMA4) $(GEMINI3F)
	uv run plot_comparison.py -o compare/gemini3f.png $(GEMINI3F) $(GEMINI35FL) $(GEMINI25F) $(GEMMA4) $(GEMMA4_31B)
	uv run plot_comparison.py -o compare/qwen38.png $(QWEN38) $(QWEN36) $(QWEN36_27B)
	uv run plot_comparison.py -o compare/gpt56luna.png $(GPT56LUNA) $(GPT56TERRA) $(GPTOSS)
