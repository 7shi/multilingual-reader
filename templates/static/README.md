# Multilingual Reader - Implementation Notes

Design notes and a quick reference for the speech playback system in reader.js / reader-multi.js.

## File Layout

| File | Role |
|---|---|
| `templates/static/speech.js` | Web Speech API shared utilities (ES Module) |
| `templates/static/reader.js` | Logic for the single-language page |
| `templates/static/reader-multi.js` | Logic for the multilingual parallel mode |

`reader.js` / `reader-multi.js` `import` `speech.js`. They are loaded via `<script type="module">` in the templates.

## Quick Reference

### speech.js exports

```js
getFilteredVoicesForLang(availableVoices, langCode)
// → SpeechSynthesisVoice[]
// Filters voices by language code, sorted by priority.
// Excludes multilingual voices, then orders by exact match → online → default → name.

autoAssignDefaultVoices(speakerVoices, speakers, filteredVoices)
// Auto-assigns voices only when speakerVoices has no assignments at all.
// If there are 2+ speakers and both male and female voices are available,
// assigns them alternately; otherwise assigns from the front of filteredVoices in order.

buildVoiceCandidates(speakerVoices, speakers, speakerIndex, filteredVoices)
// → SpeechSynthesisVoice[]
// Builds the candidate list for speakerIndex.
// Puts the already-assigned voice (preferred) first,
// and excludes voices currently used by other speakers.

async speakWithRetry(text, langCode, rate, candidates, options)
// → "ended" | "cancelled" | "error"
// Tries candidates in order, automatically retrying the next one on synthesis-failed.
```

### speakWithRetry options

| Option | Type | Description |
|---|---|---|
| `vi` | `number` | Starting index (default 0) |
| `onstart` | `() => void` | Callback when speech starts (success confirmed) |
| `onboundary` | `(e) => void` | Callback for word-boundary events (for highlighting) |
| `onUtterance` | `(utt) => void` | Callback right after the utterance is created (used to update `currentSynth`) |
| `onVoiceSuccess` | `(voice) => void` | Callback passed the voice that succeeded when speech starts |

`onVoiceSuccess` is called at the same time as `onstart`. It is not called for candidates that failed during retry.

## Implementation Notes for the Voice Retry Logic

### Overall flow

```
speakLine()
  → buildVoiceCandidates()   # build candidate list
  → speakWithRetry()         # asynchronous speech (with retry)
      → speakOne(candidates[0])
          synthesis-failed → speakOne(candidates[1]) → ...
          ended/cancelled/error → resolve
  → onVoiceSuccess()         # update speakerVoices + reflect in UI
  → advance to next line or stop
```

### Building the candidate list (buildVoiceCandidates)

1. Put `speakerVoices[speakerIndex]` (a user setting or the voice that succeeded last time) first
2. Exclude voices currently used by other speakers (skip if a speaker's voice would collide)
3. Append the remaining filteredVoices as subsequent candidates

This satisfies both "prefer trying the voice that succeeded last time" and "no voice overlap between speakers."

### Caching the successful voice (onVoiceSuccess)

Inside `speakWithRetry`, `onVoiceSuccess(voice)` is called at the timing of the `onstart` event (i.e. speech has started = that voice is confirmed usable).

The caller, `speakLine`, does the following two things:

```js
onVoiceSuccess: voice => {
    speakerVoices[speakerIndex] = voice;   // will be first in the next candidate list
    updateVoiceSelect(speakerIndex, voice); // reflect in the dropdown UI
},
```

This means retries only happen the first time; from the second call onward, speech happens directly with no retry.

### Preventing races on asynchronous cancellation (speechGeneration)

`speakLine` is an `async` function, and `stopText` or `updateRate` can be called while `await speakWithRetry(...)` is pending.

```js
// Take a snapshot of the generation at the top of speakLine
const gen = speechGeneration;
...
const result = await speakWithRetry(...);

// If the generation has changed by the time await returns, a new playback has already started, so do nothing
if (gen !== speechGeneration) return;
```

`stopText` / `updateRate` / `restartIfPlaying` call `speechGeneration++` before calling `speechSynthesis.cancel()`. The cancellation causes `speakWithRetry` to return `"cancelled"`, resolving the await, and the `gen !== speechGeneration` check causes an early return.

### Benefits of using an ES Module

Making `speech.js` an ES Module (`export` / `import`) provides the following benefits:

- No `window.Speech` global is needed, so there's no namespace pollution
- `reader.js` / `reader-multi.js` have module scope, so no IIFE is needed
- Modules have strict mode enabled by default
- `speech.js`'s internal functions (`prioritizeVoicesByRegion`, `speakOne`, etc.) are naturally encapsulated by not being exported
