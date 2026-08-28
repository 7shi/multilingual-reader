# debug2: KV cache investigation

## Purpose

Measured whether `translate.py`'s KV cache was actually effective via `prompt_eval_duration` (prefill time), identified the problem, and fixed it.

---

## Investigation method

Extended `translate.py` to pull `prompt_eval_count` / `prompt_eval_duration` from the `call_llm` return value's `response.chunks[-1]` and log the prefill speed.

```
prefill: 844 tokens, 0.42s, 1986 tps
```

Whether the KV cache is working can be judged from **duration**. When the cache is effective, only the incremental tokens are computed, so it finishes within 0.5s. On a cache miss, all tokens must be recomputed, so duration scales with token count (3-5s for 800-1400 tokens).

Note that the displayed tps is computed from the total token count including cached tokens, so it looks larger than the actual compute amount on a cache hit. Computing from the incremental token count instead gives roughly 250 tps (the hardware's actual prefill speed).

---

## Problem found

Before the fix, `call_llm` stripped the role information from `chat_history` and extracted only the content strings:

```python
contents = [msg["content"] for msg in chat_history[1:]]
generate_with_schema(contents, system_prompt=system_content, ...)
```

The (old) `generate_with_schema` sent all `contents: List[str]` to Ollama as `role: user`. As a result:

- Translation responses (which should be `role: assistant`) were resent as `role: user` in the next request
- Ollama's token sequence changed, invalidating the KV cache
- Translation after summary generation always required full re-evaluation (3-5s)

### Log before the fix (slowdown after the summary)

```
[Generating summary after translation 10]
prefill: 1035 tokens, 0.68s   ← summary generation
prefill: 1129 tokens, 4.31s   ← i=11: full re-evaluation (KV cache invalid)
prefill: 1181 tokens, 4.43s   ← i=12: no recovery
...stays at 4-5s from here on
```

---

## Fix

Upgraded `llm7shi` to v0.10.1 and confirmed `generate_with_schema` can now accept `List[Dict[str, str]]` (OpenAI format). Changed the code to pass `chat_history` through as-is:

```python
# After the change
generate_with_schema(chat_history, ...)
```

The `system` / `user` / `assistant` roles are now passed to Ollama unchanged, matching the previous request's response token sequence, which activates the KV cache.

### Log after the fix

```
[Generating summary after translation 10]
prefill: 1035 tokens, 0.68s   ← summary generation
prefill: 1227 tokens, 0.22s   ← i=11: KV cache active (in the 0.2s range)
prefill: 1287 tokens, 0.32s   ← i=12: stays fast
...
[Compressing history after translation 15]
prefill:  786 tokens, 3.00s   ← cold start right after compression only (unavoidable due to prefix change)
prefill:  883 tokens, 0.31s   ← fast again from the next translation onward
```

---

## About the `--no-summary-history` option

During the investigation, we also implemented and compared a `--no-summary-history` option that "does not add the summary to `chat_history`."

With this option, the context shrinks after the summary is dropped, so Ollama can't match the prefix and full re-evaluation (3-5s) occurs every time right after a summary. Since the fixed regular glossary mode also stays at 0.2s right after a summary, we concluded this option is unnecessary.

---

## Evaluation results (gemma3:27b)

| Variant | Score (median of 3) |
|---|---|
| `glossary` | 95 points |
| `glossary-no-hist` | 96 points |

No difference in quality; `glossary` is superior in KV cache efficiency.

---

## Remaining cold start

Translation right after compression (the sliding step) always has a cold start (about 3.5s) since the prefix changes. This is a fixed architectural cost that cannot be avoided.
