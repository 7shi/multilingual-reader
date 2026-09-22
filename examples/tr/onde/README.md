# examples/tr/onde/

Translates and evaluates the onde text with each model.

- [gemma4](gemma4/) (26B-A4B)
- [gemma4-31b](gemma4-31b/)
- [gpt-oss](gpt-oss/)
- [qwen3.6-27b](qwen3.6-27b/)
- [qwen3.6](qwen3.6/) (35B-A3B)
- [qwen3.8](qwen3.8/) (27B)
- [bonsai2-27b](bonsai2-27b/) (Ternary Bonsai 2 27B PTQ1_0: ternary-quantized Qwen 3.8 27B)
- [muse-glimmer](muse-glimmer/)
- [ox-alpha](ox-alpha/) (glm-5.3-flash stealth 320B-A18B)
- [union-alpha](union-alpha/)
- [gpt-5.6-luna](gpt-5.6-luna/)
- [gpt-5.6-terra](gpt-5.6-terra/)
- [gemini-3.5-flash-lite](gemini-3.5-flash-lite/)
- [gemini-2.5-flash](gemini-2.5-flash/)
- [gemini-3-flash](gemini-3-flash/)
- [gemini-3.7-flash](gemini-3.7-flash/)

Every model has also been evaluated by TypeSafe's Jev, in one pass over all 67 languages, with the results in `{model}/jev.jsonl`. The corpus's published scores are unaffected; see [JEV.md](JEV.md) for that run and what it measured.

"onde" means "wave" in French. Here it's used in the sense of "wave" as a physics term.

[TEMPLATE/](TEMPLATE/) is the template directory for adding a model (excluded from `make all`). See [ADD_MODEL.md](../ADD_MODEL.md) for the procedure for adding one.
