# Memo

Separate from the experiment setup and results overview in [examples/tr/README.md](examples/tr/README.md), this file keeps only decision notes and future considerations.

## Key findings

Model-by-model trends, comparisons between Google's models, and language classification are consolidated in [examples/tr/README.md](examples/tr/README.md).

### Hypotheses on the underlying behavior

- Translation quality seems to depend more strongly on training data volume and the richness of standardized digital resources than on the language's structure itself
- The same model can locally break down for just one specific language; this seems more naturally explained as crosstalk within that model's internal representation space than as a general difficulty of the language
- Bigger models aren't always better — for low-to-mid resource languages, a smaller but more stable model can sometimes be more practical
- There's an asymmetry between evaluation ability and generation ability — a model that's strong at reading isn't necessarily strong at writing

### Trends in the revision (peer-review) approach

We ran an experiment (experiment 09) across all 67 languages where `qwen3.6` revised each language's highest-scoring baseline line by line. The result was 30 languages improved, 32 degraded, and 5 unchanged (average change −1.2 points), showing that the effect of revision depends heavily on the language and the state of the base score.

**Languages where revision worked well** (delta of +6 or more, and 80+ points after revision): Bulgarian (97:+17), Hungarian (96:+13), Slovene (95:+22), Azerbaijani (91:+13), Czech (89:+9), Basque (87:+42), Estonian (82:+29), Latvian (82:+17), Macedonian (82:+6), Belarusian (81:+12)

**Conditions and caveats for when revision works** (from experiments 09 and 10):

- Revision functions as "refining the expression," so it's effective on **translations that are understandable but rough in phrasing**
- If a translation is **structurally broken**, revision tends to fail to improve it and can make it worse
- If the baseline is **already highly polished**, unnecessary changes can sometimes backfire (bg: 88 points → −1 point)
- **Even when the base score is low**, if the semantic skeleton is intact, revision can bring about large improvements (experiment 10: eu 17→59, hu 26→89, sl 56→83, et 30→51)

Because of this asymmetric effect, whether to apply revision can't be judged from the score alone.

### Operational decisions

- Purely on quality, `gpt-5.6-luna` (closed) is the most generally capable, but `gemma4` remains a reasonable baseline if open-weight operation is desired. `ox-alpha` is a time-limited test stealth model, and its production release is expected to be 500B+ parameters, which would be hard to self-host — so if going to the cloud anyway, the more efficient `gpt-5.6-luna` is a more sensible choice
- Keeping the evaluation "ruler" fixed to `qwen3.6` makes comparisons easier
- For low-resource languages, weight not just "is the meaning conveyed" but also whether speaker tags are preserved and whether other languages leak in
- Revision (`trtools review`) is especially effective for mid-resource languages, but backfires when the baseline is structurally broken or already too polished. Don't judge by score alone — check the translation's structural soundness before applying it
- Differences between models matter more than differences between providers, but there are environment-specific differences in how JSON breaks or how generation stops, so automation needs to handle that separately

## ROCm/Vulkan backend trends

After the evaluator (`qwen3.6`) started misbehaving on the ROCm backend, we compared switching the backend used for translation and for evaluation separately (`examples/tr/onde/qwen3.8/`, `examples/tr/onde/muse-glimmer/`).

- **Evaluation is unusable on ROCm**: running `qwen3.6` as the evaluator on ROCm produces hallucinated reports of language contamination that isn't actually there, or output claiming the source/translation text was never passed to the prompt (i.e. the context itself is corrupted), and scores collapse. Switching evaluation back to Vulkan resolves these anomalies and restores reasonable scoring aligned with the actual translation content. Evaluation should always be pinned to Vulkan.
- **The impact of ROCm on translation depends on the model**: with evaluation fixed to Vulkan, comparing only the translation backend (ROCm/Vulkan) shows behavior that varies by model.
  - `qwen3.8`: with ROCm translation, some languages (Spanish, Galician, Romanian) stop partway through generation and score 0. Right up until it cuts off, the grammar and vocabulary look natural, suggesting a generation-completion failure rather than a capability shortfall.
  - `muse-glimmer`: no 0-score languages occur even with ROCm translation, and score differences stay within normal variance (some languages like Malay swing ±20-40 points, but the swings go both up and down with no consistent bias).
- Operationally: always pin evaluation to Vulkan, and when translating on ROCm, check each model individually for 0-score languages (generation stopping partway through).

**Suspected cause**: this problem didn't occur on ROCm at the time of the initial evaluation (May 2026) using Gemma 4, GPT-OSS 120B, and Qwen 3.6. The only major change to Ollama since then is the complete removal of its own inference engine in `v0.30.0` (June 2026) in favor of consolidating on the upstream `llama-server` (llama.cpp), along with the new compatibility layer (`llama/compat/`) that came with it — this change is suspected to be the cause of the broken inference / corrupted context on the ROCm backend.

The compatibility layer dynamically converts the metadata and tensor names of legacy Ollama-format GGUF files into the format upstream `llama-server` expects. Models released after this consolidation (Qwen 3.8, Muse Glimmer) are natively compatible and don't need this conversion, while older models predating the consolidation (Qwen 3.6, Gemma 4) depend on it. This distinction matches the observed result that only the former work correctly on ROCm while only the latter break.

## Using GPT-OSS 120B outside of evaluation

`gpt-oss` shows a ceiling effect on evaluation tasks, so it isn't used as a primary evaluator. On the other hand, it seems well-suited to auxiliary tasks that take advantage of its fast inference.

- Terminology checks: enumerating candidate translations, validating the soundness of existing translations
- Background knowledge supplementation: explaining proper nouns and cultural context
- Preliminary research: surfacing points to consider before translation

## Future considerations

The current experiments target podcast scripts under 100 lines, but the eventual goal is to also handle long-form translation like a full novel. At that scale, new mechanisms will likely be needed.

- Hierarchical context management: keep detail granularity varied — a detailed summary for the nearby span, a rough outline for distant spans
- Long-range reference support: a single summary tends to lose foreshadowing and character relationships, so some mechanism to dynamically pull in related chunks will likely be needed
- Consistency of terminology and style: how to manage cross-chapter term consistency, per-character speech patterns, and maintaining narrative tone
- Rethinking evaluation design: for long-form text, we'll want to look beyond line-level evaluation to chapter-level coherence and narrative comprehension as well

The operational decisions being solidified in the current experiments — term extraction, summary compression, and so on — are expected to become the foundation for that next stage.
