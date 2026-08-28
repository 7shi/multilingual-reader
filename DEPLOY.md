# Build and deploy architecture

Design details for multilingual-reader's static site generation, runtime behavior, and deployment. For day-to-day operation, see [README.md](README.md).

## Overall flow

```
examples/{topic}-{lang}.txt  ──┐
templates/page.html          ──┤
templates/multi.html         ──┼── templates/build.py (Jinja2) ──▶ dist/
templates/index.html         ──┤                                    │
templates/static/*.{js,css}  ──┘                                    │
                                                                     ▼
                                                templates/deploy.sh (git worktree)
                                                          │
                                                          ▼
                                              push to gh-pages branch
                                                          │
                                                          ▼
                                https://7shi.github.io/multilingual-reader/
```

The stages input data → build → runtime JS → deploy are detailed below.

## 1. Input data

### `examples/{topic}-{lang}.txt`

One file per topic × language (4 topics × 6 languages = 24 files). The format is "one line = one utterance," each line in the form `speaker: text`.

Chinese is the only language that sometimes uses a full-width colon `：` (U+FF1A) as the separator, so `extract_speaker_and_text` in `build.py` handles both the half-width and full-width forms:

```python
for sep in (":", "："):
    if sep in text:
        parts = text.split(sep, 1)
        ...
```

Example (French):
```
Camille: Bonjour et bienvenue dans « Tech Éclair »...
Luc: Et moi, c'est Luc...
```

In the Chinese version, the speaker names themselves are also translated:
```
卡米尔：大家好，欢迎收听《科技快报》...
卢克：我是卢克...
```

### Normalizing speaker indices

In multilingual side-by-side mode, the mapping "speaker N utters line K" must be consistent across all languages. `build.py` determines `speakers_in_order` based on **the order speakers first appear in the French (source) version**, and the `speaker_index` for line i is decided by `speakers_in_order.index(fr_lines[i].speaker)`.

This lets Chinese `卡米尔` and English `Camille` share the same `speaker-0` for CSS color-coding and voice assignment. Within each language's page, the speaker is shown under that language's own name, but the internal ID is unified.

## 2. Templates and build

### Why Jinja2

- HTML auto-escaping is on by default (XSS protection)
- Loops and conditionals are concise (per-line SSR reads naturally)
- Extensibility: templates need no changes even if topics or languages are added later
- The one exception: the embedded JSON inside `<script type="application/json">` uses `|safe` to suppress raw escaping, and `build.py` instead replaces `<`, `>`, `&` with `\uXXXX` escapes itself

### Two kinds of templates

- `templates/page.html` ... single-language page
- `templates/multi.html` ... multilingual side-by-side page
- `templates/index.html` ... landing page

CSS is shared across all pages via `templates/static/reader.css`. JS is split between `reader.js` for single-language pages and `reader-multi.js` for multilingual pages (there's some duplication in the shared parts, but the logic differs enough that keeping them independent was prioritized).

### Build output

| Output | Count | Purpose |
|------|----:|------|
| `dist/{topic}.html` | 4 | Multilingual side-by-side mode (default) |
| `dist/{topic}-{lang}.html` | 24 | Single-language mode |
| `dist/index.html` | 1 | Landing page (4 × 7 matrix: All + 6 languages) |
| `dist/assets/reader.css` | 1 | Shared CSS |
| `dist/assets/reader.js` | 1 | JS for single-language pages |
| `dist/assets/reader-multi.js` | 1 | JS for multilingual pages |

32 files total. A full build takes under a second.

### `LANG_CONFIG` and `TOPIC_LABELS`

Two dictionaries at the top of `build.py` are the single source of truth for topics and languages:

```python
TOPIC_LABELS = {
    "transformer": "🤖 Transformer",
    "finetuning": "🎯 Fine-tuning",
    ...
}

LANG_CONFIG = {
    "fr": {"code": "fr-FR", "name": "Français", "default_rate": 1.0},
    "ja": {"code": "ja-JP", "name": "日本語", "default_rate": 1.4},
    "zh": {"code": "zh-CN", "name": "中文", "default_rate": 1.0,
           "font_family": ["Noto Sans SC", "Microsoft YaHei", ...]},
    ...
}
```

Adding or removing a topic or language is done purely by editing these dictionaries (`make build` regenerates all output).

## 3. Data-embedding strategy

### Hybrid of SSR HTML + page-config JSON

Line text is embedded directly as **pre-rendered (SSR) HTML** (readable even with JS disabled). Meanwhile, metadata that JS needs — the speaker list, language codes, font settings, etc. — is embedded as JSON inside `<script id="page-config" type="application/json">`.

Benefits:
- ✅ Body text renders even with JS disabled (progressive enhancement)
- ✅ Highlighting only needs to walk the DOM (no template logic needed on the JS side)
- ✅ Body text is indexable by search engines

### Escaping the JSON inside `<script type="application/json">`

The HTML parser treats the contents of a `<script>` element as "raw text" and does **not** decode HTML entities (like `&#34;`). Meanwhile, a `</script>` sequence is interpreted as an early tag close.

So `build.py` applies the following replacements to the JSON string before embedding it:

| Original | Replaced with |
|----|--------|
| `<` | `\u003c` |
| `>` | `\u003e` |
| `&` | `\u0026` |

```python
config_json = config_json.replace("<", "\\u003c") \
    .replace(">", "\\u003e") \
    .replace("&", "\\u0026")
```

This makes it safe even if `</script>` happens to occur inside the JSON, and avoids Jinja2's HTML auto-escaping (e.g. `&amp;` for `{{ x }}`, suppressed via `|safe`), so the string the browser reads back via `textContent` can be passed straight to `JSON.parse`.

### Contents of `page-config` (multilingual example)

```json
{
  "topic": "transformer",
  "languages": [
    {"code": "fr", "name": "Français", "lang_code": "fr-FR", "default_rate": 1.0},
    {"code": "zh", "name": "中文", "lang_code": "zh-CN", "default_rate": 1.0,
     "font_family": ["Noto Sans SC", "Microsoft YaHei", ...]},
    ...
  ],
  "speakers": ["Camille", "Luc"]
}
```

The single-language version has a simplified structure with flat fields like `lang` / `lang_code` / `lang_name`.

## 4. Runtime JS

### Bootstrap

On `DOMContentLoaded`:
1. Load the `page-config` JSON via `JSON.parse(document.getElementById("page-config").textContent)`
2. Collect the line elements from the DOM (`.line` or `.translation-line`)
3. Save each `.line-text`'s `textContent` into a `data-original-text` attribute (keeps the original text around for restoring highlights)
4. Check Web Speech API support and call `speechSynthesis.getVoices()`
5. Subscribe to `speechSynthesis.onvoiceschanged` (the voice list is populated asynchronously, so the first call can return an empty array)
6. Build the speaker-voice UI (the `#speakerVoices` section)

### Voice selection logic

`getFilteredVoices(lang)`:
1. From all voices the browser provides, extract those whose language base matches via `voice.lang.split("-")[0]` (e.g. for Japanese, every `ja-*` voice)
2. Stable-sort with `prioritizeVoicesByRegion`:
   - Prefer an exact regional code match (e.g. exactly `fr-FR`)
   - Prefer `localService === false` (online voices) — puts the high-quality Microsoft Azure / Google Cloud voices first
   - Prefer `voice.default === true`
   - The rest, alphabetically
3. Exclude voices whose name contains `multilingual` (mixed-language voices have inconsistent quality)

### Automatic voice assignment

`autoAssignDefaultVoices(lang, filteredVoices)` alternates male and female voices when there are ≥ 2 speakers and voices of both genders are available. Gender is determined via name matching (a whitelist approach):

```js
const maleNames = ["gerard", "thierry", ..., "david", "guy", ..., "ichiro", "yunjian"];
const femaleNames = ["charline", "sylvie", ..., "aria", "jenny", ..., "ayumi", "xiaoxiao"];
```

These are extracted empirically from Microsoft/Google voice names for each language. Keywords like `female`, `male`, `homme`, `femme` are also used.

For languages with no match, voices are assigned in order (the first N of `filteredVoices`).

### Dynamic highlighting

`SpeechSynthesisUtterance.onboundary` fires at word boundaries and provides `event.charIndex` and `event.charLength`. `highlightWord` uses these to rebuild `innerHTML` as 3 segments:

```
[ before ][ TARGET ][ after ]
            ^^^^^^
       <span class="word speaking">
```

At the next `onboundary` or on `onend`, the original text is restored from `data-original-text` (overwriting `textContent`).

Browser implementation differences:
- Chrome / Edge: fires reliably per word, `charLength` is accurate
- Firefox: partial support, fires less often
- Safari: depends on the vendor implementation, has limitations

So highlighting is treated as "best-effort" (read-aloud itself works in every browser).

### Suppressing cancellation errors

Calling `speechSynthesis.cancel()` fires `onerror` on the currently-speaking utterance with `error: 'canceled'` or `'interrupted'`. This happens when:
- The user presses the Stop button
- The rate slider is moved (cancels and restarts at the new rate)
- A language flag is toggled (stops playback if it's currently playing)

These are all "intentional cancellations from user action," and showing an error UI for them would be misleading. Detection:

```js
utterance.onerror = e => {
    if (isStopped || e.error === "canceled" || e.error === "interrupted") {
        clearAllHighlights();
        return;  // no status display, no console.error
    }
    console.error("Speech synthesis error:", e);
    updateStatus("stopped", "Error occurred during playback");
    clearAllHighlights();
};
```

The `isStopped` flag is set to `true` at the top of `stopText()`, preventing a spurious error display even in the state right before cancel.

### Playback loop in multilingual side-by-side mode

State:
- `currentGroupIndex` ... the current line (0-based, an index into `groups[]`)
- `currentStep` ... the current index within the enabled-language list

Once every enabled language has been read for a line, it moves to the next line. Pseudocode for `speakNext()`:

```js
function speakNext() {
    const enabled = languages.filter(L => states[L.code].enabled).map(L => L.code);
    if (enabled.length === 0) { stopText(); return; }
    if (currentStep >= enabled.length) {
        currentStep = 0;
        currentGroupIndex++;
    }
    if (currentGroupIndex >= groups.length) {
        stopText(); updateStatus("stopped", "Finished"); return;
    }
    const lang = enabled[currentStep];
    const group = groups[currentGroupIndex];
    if (!group[lang]) {       // this line doesn't exist for this language
        currentStep++;
        speakNext();           // skip via recursion
        return;
    }
    speak(group[lang], lang);
}
```

`utterance.onend` increments `currentStep`, then queues the next call to `speakNext()` via `setTimeout` with a delay of:
- 400ms → moving to the next language within the same line
- 800ms → moving to the next line

The delay gives a human listener time to distinguish the boundary between languages.

### Playback loop in single-language mode

State is managed with just `currentLineIndex`. `speakLine(index)` reads `lines[index]` aloud, and `onend` increments `currentLineIndex` and moves on. There's no language-step logic like in the multilingual loop, so the code is much simpler.

### Persistence

Each language's read-aloud rate is saved as JSON to `localStorage[multilingualReader.langRates.{topic}]`. It's separated per topic so adjustments like "slow Onde down but keep Transformer at normal speed" are possible.

Speaker voice selection is not persisted (available voices vary widely across browsers/OSes, so saving it wouldn't reproduce reliably).

## 5. Deploy (`deploy.sh`)

### Processing steps

```bash
1. Check that dist/ exists
2. git worktree add .gh-pages-worktree gh-pages
   ├ if gh-pages exists locally:      git worktree add <dir> gh-pages
   ├ if origin/gh-pages exists:       git worktree add -B gh-pages <dir> origin/gh-pages
   └ if neither exists (first run):   git worktree add --orphan -b gh-pages <dir>
3. find <dir> -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
4. cp -r dist/. .gh-pages-worktree/
5. touch .gh-pages-worktree/.nojekyll
6. cd .gh-pages-worktree && git add -A
7. git diff --cached --quiet || git commit -m "Deploy <sha>"
8. git push origin gh-pages
9. cd .. && git worktree remove --force .gh-pages-worktree
```

### Benefits of the git worktree approach

Compared with alternatives:

| Approach | Pros | Cons |
|------|------|------|
| **worktree** | Doesn't switch main's working tree / allows concurrent work / lightweight via shared `.git` | A leftover worktree of the same name causes the next run to fail (handled by removing it beforehand) |
| Branch switching | Simple | `git checkout gh-pages` rewrites the working tree / files being edited would disappear |
| Separate clone | Fully independent | Manages 2 repositories / duplicate push auth |
| GitHub Actions | Automated | Needs YAML / secrets management / tends toward an npm dependency, but this project's policy is to avoid npm |

Since multilingual-reader's policy is to avoid npm, worktree + a shell script is the simplest approach. It's self-contained with just `uv`.

### Why `.nojekyll` is needed

GitHub Pages runs everything through Jekyll by default. Jekyll treats paths starting with `_` as "Jekyll templates" and excludes them from the site (they aren't published). There are no such paths currently, but `.nojekyll` is placed so that adding a directory like `_assets/` in the future won't break, by disabling Jekyll entirely. As a side effect, it also speeds up the build.

### Idempotency

When `git diff --cached --quiet` shows no diff, no commit is made (avoids empty commits). If the content to push hasn't changed, `make deploy` is effectively a no-op, and is safe to run multiple times.

### Commit message

Uses the format `Deploy <main's short sha>`. This lets you look up "which main commit is currently published" from the `gh-pages` commit history.

## 6. Local development

### `make serve`

Serves `dist/` on port 8000 via `uv run python -m http.server 8000`:

```bash
make build && make serve
# http://localhost:8000/
```

### Unified relative paths

Under GitHub Pages, the base path is `/multilingual-reader/`, but since this site references everything with **relative paths only**, it behaves identically locally and after deployment:

- `<link rel="stylesheet" href="assets/reader.css">`
- `<script src="assets/reader.js">`
- `<a href="transformer-fr.html">` (inside index.html)
- `<a href="transformer.html">` (inside lang-nav)

Since no `<base>` tag or absolute path like `/assets/...` is ever used, neither sub-path deployment nor opening the file directly locally breaks.

### Partial builds are not supported

`build.py` always does a full build. With fewer than 30 files completing in under a second, there's no need for incremental builds, and it wouldn't be worth the added complexity.

### `dist/` is gitignored

`dist/` is excluded via `.gitignore`. The main branch never contains build output — only the `gh-pages` branch holds it.

## 7. GitHub Pages setup (one-time)

1. Open **Settings → Pages** on the repository
2. Set **Source** to `Deploy from a branch`
3. Set **Branch** to `gh-pages` / `/ (root)` and click **Save**
4. Published at `https://7shi.github.io/multilingual-reader/` after a few minutes

The `gh-pages` branch is created automatically as an orphan branch the first time `make deploy` runs.

## 8. Design intent behind the two modes

### Multilingual side-by-side mode (`{topic}.html`, default)

- Shows the parallel translation for all 6 languages stacked per line
- Clicking a language flag toggles that language on/off for read-aloud
- Reads all enabled languages in sequence for each line (line N: lang A → lang B → ... → line N+1)
- Read-aloud rate and speaker voice are adjustable independently per language
- **Intended use**: listening to two languages alternately, e.g. "French → Japanese," to learn from parallel translations

### Single-language mode (`{topic}-{lang}.html`)

- Shows and reads only one language
- The lang-nav in the top-right of each page lets you switch instantly to "All" (multilingual) or another language's page
- **Intended use**: focused listening/shadowing practice in a single language, or directly sharing a page for a specific language

### Choosing between the URL forms

| URL pattern | Purpose |
|--------------|------|
| `{topic}.html` | Default (multilingual). The standard form for sharing |
| `{topic}-{lang}.html` | Jumps directly to a specific language. Also treated as an independent page for SEO |
| `index.html` | A listing of all topics × modes |

The "All" column in `index.html` is highlighted (in blue) to indicate that it's the recommended path.
