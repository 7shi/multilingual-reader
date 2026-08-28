# Memo

## Debug records

- **[`debug1/`](debug1/)**: Method selection. Ran 4 models (gemma3:27b, gpt-oss:120b, gemma4:31b, qwen3.6) × 4 variants (none, none-schema, glossary, glossary-schema). `--schema` was harmful for multiple models (notably gemma4:31b's glossary-schema=62 points), `--summary glossary` was counterproductive for gpt-oss:120b, and gemma4:31b (no-think) differed by only 1 point (97 vs 98) while other models were equal or better. Finalized the Phase B policy (no glossary/schema, Qwen3/Gemma4 use no-think).
- **[`debug2/`](debug2/)**: KV cache investigation. Identified that `llm7shi` was on an outdated version and `generate_with_schema` was failing to preserve roles, resolved by upgrading to v0.10.1 and passing `chat_history` through as-is. Measured KV cache effectiveness via `prefill duration`, confirming the fix keeps it around 0.2s even after summary generation.

---

## Hybrid mode (planned for experimental/03)

An advanced approach for CoT-capable models (Qwen3/Gemma4 series). Adds a `--hybrid` option so the translation loop runs without CoT while only summary generation uses CoT.

- Translation itself runs without CoT to ensure speed and stability
- Summary generation uses CoT to improve accuracy (since it's infrequent, the extra cost is limited)
- The summary's CoT is self-contained within that call, and only the summary text remains in the translation history, so it does not pollute the KV cache

**Operation flow (threshold=15, keep=5):**

```
Translate 1-10 (no CoT) → generate summary 1 (with CoT) → summary not included in history
Continue translating 11-15 (KV cache active, unaffected by the summary)
Compress context after 15: [summary 1, 11-15]
Translate 16-20 (no CoT) → generate summary 2 (with CoT) → summary removed from history
Continue translating 21-25
Compress context after 25: [summary 2, 21-25]
...
```

After generating a summary, it's removed from history before translation continues, which keeps the KV cache intact while avoiding the behavior where the summary's phrasing influences the translation. The summary is only injected into the context at compression time.

Since CoT-based summarization is costly, we're also considering widening the interval beyond the current `threshold - keep` (e.g., every 10 lines).
