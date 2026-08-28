# translate-json.py

A script that translates JSON-format transcription text using an LLM.

## Features

- Retains translation history as context to achieve consistent translation
- **Two summary methods**:
  - `patterns`: extract translation patterns (emphasizes consistency of proper nouns/terminology)
  - `summary`: summarize the content in English (emphasizes expressive variety)
- **Cache-efficiency optimization**:
  - Never fully deletes history; always keeps the most recent 5-15 entries
  - Optimizes summary-generation timing to maximize cache hit rate
- **Cumulative summary**: merges past summaries with new history to maintain consistency
- Can translate between any language pair
- Lets you specify which LLM model to use
- Outputs a JSON file containing both the original text and the translation

## Usage

```bash
python translate-json.py INPUT_FILE -o OUTPUT_FILE -s SOURCE_LANG -t TARGET_LANG [-m MODEL] [--threshold N] [--keep K] [--summary TYPE] [--no-think]
```

## Arguments and options

### `INPUT_FILE` (required)
Path to the input JSON file to translate

### `-o, --output OUTPUT_FILE` (required)
Path to the output JSON file to save the translation results

### `-s, --source-lang SOURCE_LANG` (required)
Specifies the source language.

- Examples: `-s French`, `-s English`, `-s Japanese`

### `-t, --target-lang TARGET_LANG` (required)
Specifies the target language.

- Examples: `-t Japanese`, `-t English`, `-t French`

### `-m, --model MODEL`
Specifies the LLM model to use for translation.

- Default: `gpt-oss:120b`
- Examples: `-m gpt-oss:20b`, `-m gemma3`, `-m llama3`

### `--threshold N`
Specifies the interval (in translation pairs) between summary generations.

- Default: `10`
- The translation history is summarized by the LLM at this interval
- Example: `--threshold 20` summarizes every 20 pairs

### `--keep K`
Specifies the number of translation pairs between a summary and reorganization.

- Default: `5`
- History is reorganized after K translations following a summary (history is never reduced to zero)
- Example: `--keep 8` reorganizes history after 8 translations following a summary

### `--summary TYPE`
Specifies the summary generation method.

- Default: unspecified (no summary generated, fastest)
- Choices:
  - `patterns`: extract translation patterns
    - Proper-noun-to-translation mappings
    - Translations of technical terms
    - Each speaker's tone-of-voice patterns
    - Expressions that should remain consistent
    - **Pros**: high consistency of proper nouns/terminology
    - **Cons**: expression patterns can also become fixed, potentially making the style uniform
  - `summary`: summarize the content in English
    - Focuses only on the translated content and context
    - Does not extract translation patterns or tone
    - **Pros**: preserves expressive variety
    - **Cons**: may slightly reduce proper-noun consistency
- Usage examples: `--summary patterns` or `--summary summary`

### `--no-think`
Disables thinking mode.

- Default: thinking mode enabled (`think=True`)
- Passes `think=False` to `generate_content` when this flag is specified
- Use this to skip the thought process and speed up the response
- Usage example: `--no-think`

## Examples

### Run with default settings (French → Japanese)
```bash
python translate-json.py proust-duras.json -o proust-duras-translated.json -s French -t Japanese
```
- Source language: French
- Target language: Japanese
- Model: `gpt-oss:120b`
- Summary interval: 10 pairs
- Kept entries: 5 pairs
- Summary: none (fastest mode)

### Run in patterns mode (emphasizes consistency of proper nouns/terminology)
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --summary patterns
```
- Extracts translation patterns
- High consistency for proper nouns and technical terms
- Expressions may become uniform

### Run in summary mode (emphasizes expressive variety)
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --summary summary
```
- Summarizes the content in English
- Preserves expressive variety
- Proper-noun consistency may be slightly reduced

### Translate from English to Japanese
```bash
python translate-json.py input.json -o output.json -s English -t Japanese
```

### Run with a smaller model
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese -m gpt-oss:20b
```

### Change the compression threshold (compress every 20 pairs)
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --threshold 20
```

### Increase the number of kept entries (keep 8 pairs)
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --keep 8
```

### Custom settings (compress every 20 pairs, keep 8 pairs)
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --threshold 20 --keep 8
```

### Specify model and all settings
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese -m gemma3 --threshold 25 --keep 10 --summary summary
```

### Disable thinking mode for speed
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --no-think
```

### Disable thinking mode + summary
```bash
python translate-json.py proust-duras.json -o output.json -s French -t Japanese --summary summary --no-think
```

## Input/output

### Input file format
```json
{
  "transcriptions": [
    {
      "time": "00:20",
      "speaker": "Narrator",
      "transcription": "Text in the source language"
    }
  ]
}
```

### Output file format
```json
{
  "transcriptions": [
    {
      "time": "00:20",
      "speaker": "Narrator",
      "original": "Text in the source language",
      "translation": "Translation in the target language"
    }
  ]
}
```

## How it works

### Basic flow

1. Read the transcription text from the JSON file
2. Translate each entry in order
3. Add each translation to history
4. For each subsequent translation, send system prompt + summary (if any) + history + current request to the LLM
5. Perform compression once the message pair count reaches the threshold
6. Once all translations are done, save the results to a JSON file

### How history compression works

**With default settings (threshold=10, keep=5):**

```
Translations 1-15:   history grows from 0 to 15 pairs (maximum cache efficiency)
Translation 16 done: compression executed
            - the first 10 pairs (20 messages) are summarized by the LLM
            - translation patterns, proper nouns, terminology, tone, etc. are extracted
            - the most recent 5 pairs are kept in full
            Context: [system, summary, 5 pairs]

Translations 17-26:  history grows from 5 to 15 pairs (cache efficiency maintained)
Translation 27 done: re-compression
            - existing summary + first 10 pairs are cumulatively summarized
            - the most recent 5 pairs are kept in full
            Context: [system, cumulative summary, 5 pairs]

From here on:       compression repeats every 10 rounds (16, 26, 36, 46, ...)
```

**Key points:**
- History never reaches zero (always keeps the most recent 5-15 pairs)
- The summary is updated cumulatively (past information is never lost)
- Cache efficiency is maintained (prefix changes are minimized)

### Context management

**Components:**
- `system_message`: the system prompt (always included)
- `compressed_summary`: the compressed past translation patterns (added after compression)
- `messages`: the most recent translation history (5-15 pairs, in full)

**Sent to the LLM:**
```python
[system_message] + [compressed_summary] + messages + [current_user_message]
```

**Summary content:**

For `--summary patterns`:
- Proper-noun translation patterns (people, places, work titles)
- Key technical terms and their translations
- Each speaker's tone-of-voice patterns
- Expressions/style that should remain consistent

For `--summary summary`:
- An English summary of the translated content
- Topics and context discussed
- Does not include translation patterns or tone

### Code structure

**Main functions:**

- `call_llm(prompt)`: wrapper function that calls the LLM
  - Takes a prompt and automatically appends it to `chat_history`
  - Calls `generate_content()` (using the global variables `MODEL` and `THINK`)
  - Automatically appends the response to `chat_history`
  - Returns `(response_text, user_message, assistant_message)`

- `summarize_messages(summary_type)`: summary generation function
  - Builds the prompt based on the summary type (`patterns` or `summary`)
  - Uses `call_llm()` internally (appending to `chat_history` is automatic)
  - Returns `(summary_text, user_message, assistant_message)`

**Global variables:**
- `MODEL`: the LLM model name in use
- `THINK`: whether thinking mode is enabled/disabled (controlled by `--no-think`)
- `chat_history`: the full chat history (includes the system message, summary, and translation history)
- `translation_messages`: cumulative translation messages (never deleted)
- `summary_messages`: cumulative summary messages (only the latest 2 messages are used)

## Implementation details

### Implementation approach: improved hierarchical summary with optimized caching strategy

This script implements an improved hierarchical summary approach that maximizes use of the LLM cache.

#### Implementation features

1. **History never reaches zero**: always keeps the most recent 5-15 pairs in full
2. **Cumulative summary**: re-summarizes by merging the existing summary with new history
3. **Two summary methods**:
   - `patterns`: extract translation patterns (favors consistency, risk of fixed expressions)
   - `summary`: summarize content (favors variety, slightly reduced consistency)
4. **Optimized summary-generation timing**:
   - Generated upon reaching 10 pairs (right after translation, for maximum cache hit rate)
   - Applied upon reaching 15 pairs (uses the already-generated summary)
5. **Compression every 10 rounds**: maintains a 90% cache hit rate

#### Operation flow

**With `--summary` specified (threshold=10, keep=5):**

```
Translations 1-9:    chat_history = [S, U1, A1, ..., U9, A9]
            translation_messages = [U1, A1, ..., U9, A9]

After translation 10: i % THRESHOLD == 0  (10 % 10 == 0)
            → sets next_compression = 15
            → generates summary (since compression 15 is reachable next)
            - adds the summary request to chat_history
            - context = [S, U1, A1, ..., U10, A10, U-Sum]
            - an extension of the previous translation-10 context [S, U1, A1, ..., U10, A10]
            - cache hit rate near 100%!
            - adds the summary response to chat_history and summary_messages
            chat_history = [S, U1, A1, ..., U10, A10, U-Sum, A-Sum]

Translations 11-14:  chat_history = [S, U1, ..., U10, A10, U-Sum, A-Sum, U11, A11, ..., U14, A14]
            → everything after the summary is a cache hit

After translation 15: i == next_compression  (15 == 15)
            → compression executed (chat_history rebuilt)
            chat_history = [S, U-Sum, A-Sum, U11, A11, ..., U15, A15]
            → U1-10 removed, summary stays (cache continues!)

            i % THRESHOLD == 0  (15 % 10 == 0)
            → sets next_compression = 20
            → generates summary

Translations 16-19:  chat_history = [S, U-Sum, A-Sum, U11, ..., U15, A15, U16, A16, ..., U19, A19]
            → summary already in context, cache continues

After translation 20: i % THRESHOLD == 0  (20 % 10 == 0)
            → sets next_compression = 25
            → generates summary (since compression 25 is reachable next)
            chat_history = [S, U-Sum1, A-Sum1, U11, ..., U20, A20, U-Sum2, A-Sum2]
            → cumulative summary (can reference the existing summary)

Translations 21-24:  normal translation (cache hit)

After translation 25: i == next_compression  (25 == 25)
            → compression executed
            chat_history = [S, U-Sum2, A-Sum2, U16, A16, ..., U25, A25]
            → only the latest summary is kept

            i % THRESHOLD == 0  (25 % 10 == 0)
            → sets next_compression = 30

From here on:       summary generated at 10, 20, 30, 40...
            compression executed at 15, 30, 45, 60... (same time as summary generation)
```

**With 22 total entries (checking for a wasted summary):**

```
After translation 10: next_compression = 15 → summary generated
After translation 15: compression executed, next_compression = 20 → summary generated
After translation 20: next_compression = None (25 > 22)
            → summary generation skipped (would be wasted)
Translations 21-22:  no compression (since next_compression = None)
```

**Without a summary (default):**

```
Translations 1-9:    history grows from 0 to 9 pairs (maximum cache efficiency)

After translation 10: i % THRESHOLD == 0
            → sets next_compression = 15
            → no summary generated (SUMMARY_TYPE is None)

Translations 11-14:  normal translation (cache hit)

After translation 15: i == next_compression
            → compression executed
            - no summary generated
            - the first 10 pairs (20 messages) are simply deleted
            - the most recent 5 pairs are kept in full
            chat_history = [S, U11, A11, ..., U15, A15]

            sets next_compression = 30

Translations 16-29:  normal translation (cache hit)

After translation 30: compression executed, next_compression = 45

From here on:        compression executed at 15, 30, 45, 60...
```

**Key points:**
- **Index-based management**: timing is managed via the loop variable `i` and `next_compression`
- **Compression timing**: executed after a translation completes (15, 30, 45...), not before the next translation as previously
- **Wasted-summary check**: skips summary generation if the next compression point won't be reached
- **History management**:
  - `translation_messages`: cumulative (never deleted)
  - `summary_messages`: cumulative (only the latest 2 messages are used)
  - `chat_history`: rebuilt at compression time
- **Summary managed as chat history**: treated as an ordinary user/assistant message
- **Ensuring cache continuity**:
  - Immediately appended to chat_history after summary generation
  - The summary is already in context from the next translation onward
  - The summary remains in context even after compression, so the cache is never broken

### Cache efficiency analysis

#### Prefix change pattern (improved version)

```
Translations 1-9:  [S] → [S, U1-A1] → ... → [S, U1-A1, ..., U9-A9]
           ← prefix grows (full cache hit)

Translation 10:    [S, U1-A1, ..., U9-A9, U10-A10, U-Sum, A-Sum]
           ← U-Sum added after translation 10 completes (cache hit)

Translations 11-14: [S, U1-A1, ..., U10-A10, U-Sum, A-Sum, U11-A11, ..., U14-A14]
           ← prefix grows (full cache hit)

Translation 15:    [S, U-Sum, A-Sum, U11-A11, ..., U15-A15]
           ← after translation 15 completes, compression removes U1-10, but U-Sum stays (cache continues!)
           U-Sum2 is added afterward

Translations 16-19: [S, U-Sum, A-Sum, U11-A11, ..., U15-A15, U16-A16, ..., U19-A19]
           ← prefix grows (full cache hit)

Translation 20:    [S, U-Sum1, A-Sum1, U11-A11, ..., U20-A20, U-Sum2, A-Sum2]
           ← U-Sum2 added after translation 20 completes (cache hit)

Translations 21-24: [S, U-Sum1, A-Sum1, U11-A11, ..., U20-A20, U-Sum2, A-Sum2, U21-A21, ..., U24-A24]
           ← prefix grows (full cache hit)

Translation 25:    [S, U-Sum2, A-Sum2, U16-A16, ..., U25-A25]
           ← after translation 25 completes, compression removes U11-20 and U-Sum1, but U-Sum2 stays (cache continues!)
```

**Improvements:**
- Keeping the summary in context lets the cache continue even after compression
- Compression timing right after translation makes timing management clearer
- Old: cache miss at compression → improved: cache hit even after compression

### Performance measurements

> **Measurement environment**: processing time can vary significantly depending on model size and type.

#### Results with 87 entries (gpt-oss:120b)

| Method | Processing time | Ratio to full retention | Ratio to sliding | Cache hit rate |
|------|---------|-----------|----------------|------------------|
| Full retention (LIMIT=0) | 42m59.885s | 100% | 195% | 100% |
| Sliding (LIMIT=20) | 22m0.269s | 51% | 100% | ~30% |
| `--summary patterns` | 25m8.318s | 58% | 114% | ~90% |
| `--summary summary` (old version) | 15m54.388s | 37% | 72% | ~90% |
| **`--summary summary` (improved)** | **13m35.046s** | **32%** | **62%** | **~90%** |
| **No summary (default)** | **12m21.729s** | **29%** | **56%** | **~90%** |

**Improvements in the improved version:**
- Optimization via index-based management
- Wasted-summary check (skips generation if the next compression point won't be reached)
- Optimized compression timing (executed right after translation completes)
- **Result (gpt-oss:120b)**: about 2 minutes 20 seconds (~15%) faster than the old version

#### Results with 87 entries (gemma3:27b)

| Method | Processing time | Ratio to old version | Improvement |
|------|---------|--------|--------|
| `--summary summary` (old version) | 12m22.931s | 100% | - |
| **`--summary summary` (improved)** | **10m0.996s** | **81%** | **-19%** |

**Improvements in the improved version (gemma3:27b):**
- **Result**: about 2 minutes 22 seconds (~19%) faster than the old version
- An even bigger improvement than gpt-oss:120b's 15%
- Smaller models show a more pronounced effect from the optimization

#### Key findings

**Speed:**
- No summary (default): **fastest** - about 10 minutes faster than sliding (-44%)
- `--summary summary` (improved): about 8.5 minutes faster than sliding (-38%)
  - **Unexpected result**: about 11.5 minutes faster than patterns (-46%)
  - Reason: the summary is a simple content summary, so generation is quick
  - Improvements from the improved optimization:
    - **gpt-oss:120b**: about 2 minutes 20 seconds (-15%) faster than the old version
    - **gemma3:27b**: about 2 minutes 22 seconds (-19%) faster than the old version
  - Smaller models show a more pronounced optimization effect
- `--summary patterns`: about 3 minutes slower than sliding (+14%)
  - Detailed translation-pattern extraction takes longer to generate
- Full retention: slowest, but highest quality

**Cache efficiency:**
- About 90% cache hit rate across all methods
  - Prefix changes only once every 10 rounds
  - The other 9 rounds are full cache hits
  - Thanks to optimized summary-generation timing, summary and no-summary modes have comparable cache efficiency
- Sliding: about 30% (nearly 0% after the 21st entry)
  - The prefix changes every time
  - The cache doesn't work

**Quality:**
- `--summary patterns`: cumulative summary preserves context across all history
  - Maintains consistency of proper nouns/terminology
  - Preserves each speaker's tone and style
  - **Downside**: expression patterns also become fixed, making the style uniform (e.g., overuse of "~nano desu.")
- `--summary summary`: content summary preserves context
  - Maintains context of the translated content
  - Preserves expressive variety
  - **Downside**: proper-noun consistency may be slightly reduced
- No summary (default): keeps 5-15 entries of history
  - Maintains short-term consistency
  - Long-term consistency degrades
  - Preserves expressive variety

**Potential issues with patterns mode:**
- The summary extracts and fixes specific translation patterns (endings, phrasing, etc.)
- As a result, expressions can become uniform (e.g., overuse of "~nano desu.")
- Particularly noticeable in documents with a consistent style throughout
- Consistency and expressive variety are a trade-off
- Using `summary` mode or no summary mitigates this issue

#### Recommended use cases

| Method | Recommended scenario |
|------|----------|
| **No summary (default)** | Speed priority. Short documents (<100 entries). Favors expressive variety |
| **--summary summary** | **Recommended for medium-to-long documents**. Balances expressive variety with contextual consistency. Also fast (15% faster with the improved version) |
| **--summary patterns** | When proper-noun/terminology consistency is paramount. Uniform expression is acceptable. Takes longer to process |
| Full retention | Highest quality priority. Only practical for short documents |
| Sliding | Not recommended (slower than default and lower quality) |

### Configuration guidelines

| Document length | threshold | keep | Reason |
|----------|-----------|------|------|
| Short (<50 entries) | 15 | 8 | Lowers summary frequency |
| Medium (50-200 entries) | 10 | 5 | Default settings |
| Long (200-500 entries) | 10 | 5 | Emphasizes cache efficiency |
| Very long (>500 entries) | 8 | 4 | Increases summary frequency |

**Memory usage:**
- No summary: 5-15 pairs (constant)
- With summary: summary + 5-15 pairs (constant)

### Detailed comparison of each mode

| Item | No summary (default) | `--summary summary` | `--summary patterns` |
|------|------------------------|-------------------|---------------------|
| **Speed** | Fastest (12m) | Fast (16m) | Medium (25m) |
| **Proper-noun consistency** | Low | Medium | High |
| **Expressive variety** | High | High | Low |
| **Long-term context retention** | Low | Medium | High |
| **Risk of fixed endings** | None | None | Present |
| **Recommended document length** | <100 entries | 50-500 entries (recommended) | Any (when consistency matters most) |
| **Cache efficiency** | 90% | 90% | 90% |
| **Overall assessment** | Good for short documents | **Balanced** | Consistency-focused |

## Showing help

```bash
python translate-json.py -h
```
