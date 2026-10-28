# examples/tr/onde/

Translates and evaluates the onde text with each model.

- [gemma4](gemma4/) (26B-A4B)
- [gemma4-31b](gemma4-31b/)
- [gemma4-12b](gemma4-12b/)
- [gemma4-e4b](gemma4-e4b/)
- [gemma4-e2b](gemma4-e2b/)
- [gpt-oss](gpt-oss/)
- [qwen3.5-9b](qwen3.5-9b/)
- [qwen3.5-4b](qwen3.5-4b/)
- [qwen3.6-27b](qwen3.6-27b/)
- [qwen3.6](qwen3.6/) (35B-A3B)
- [qwen3.8](qwen3.8/) (27B)
- [qwen3.8-flash-next](qwen3.8-flash-next/) (Qwen 3.8 Flash Next 125B-A6B MoE, GSQ-RCO IQ3_S)
- [bonsai2-27b](bonsai2-27b/) (Ternary Bonsai 2 27B PTQ1_0: ternary-quantized Qwen 3.8 27B)
- [saluki-27b](saluki-27b/) (Underdog Saluki 27B 1.0 IQ2-mix: quantized Qwen 3.8 27B)
- [muse-glimmer](muse-glimmer/)
- [mai-code-1.1-flash](mai-code-1.1-flash/) (Microsoft 138B-A5B MoE, Q2_XS, llama.cpp)
- [flint](flint/) (40B-A2.5B MoE)
- [ornith-1.5](ornith-1.5/) (122B-A10B MoE, tuned from Qwen3.5 122B-A10B)
- [gpt-5.6-luna](gpt-5.6-luna/)
- [gpt-5.6-terra](gpt-5.6-terra/)
- [gpt-6-luna](gpt-6-luna/)
- [gpt-6-astra](gpt-6-astra/)
- [gpt-6-sol](gpt-6-sol/)
- [gpt-6.1-sol](gpt-6.1-sol/)
- [gemini-3.5-flash-lite](gemini-3.5-flash-lite/)
- [gemini-2.5-flash](gemini-2.5-flash/)
- [gemini-3-flash](gemini-3-flash/)
- [gemini-3.7-flash](gemini-3.7-flash/)
- [deepseek-v4.1-flash](deepseek-v4.1-flash/)
- [haiku-5.5](haiku-5.5/)
- [glm-5.3](glm-5.3/) (744B-A40B)
- [nemotron-3.5-super-vl](nemotron-3.5-super-vl/) (120B-A12B MoE)
- [ox-alpha](ox-alpha/) (glm-5.3-flash stealth 320B-A18B)
- [union-alpha](union-alpha/) (Pareto 26.9 stealth, a router over several models)
- [space-bunny-alpha](space-bunny-alpha/) (stealth)

Every model is evaluated by TypeSafe's Jev, one run per language, into `{model}/jev.jsonl`; `SCORES-jev.txt` and the trend column (`TREND-jev.jsonl`) come from it. The evaluator was previously `ollama:qwen3.6` with the median of three runs, and its record remains beside them as `{model}/evals/`, `SCORES.txt`, and `TRENDS.jsonl`. `generate_compare_rows.py` and `plot_comparison.py` read that record unless given `--jev`, which `examples/tr/Makefile` passes. The evaluator is pinned to `jev-1.14.0`; each `{model}/jev-1.13.0/` keeps the same three files from `jev-1.13.0`, frozen. See [JEV.md](JEV.md) for the first run over the corpus and what it measured, and [JEV-1.14.md](JEV-1.14.md) for the move to `jev-1.14.0`.

"onde" means "wave" in French. Here it's used in the sense of "wave" as a physics term.

[TEMPLATE/](TEMPLATE/) is the template directory for adding a model (excluded from `make all`). See [ADD_MODEL.md](../ADD_MODEL.md) for the procedure for adding one.
