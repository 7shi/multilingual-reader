# Multilingual Reader - 実装ドキュメント

reader.js / reader-multi.js の音声再生システムに関する設計メモと簡易リファレンス。

## ファイル構成

| ファイル | 役割 |
|---|---|
| `templates/static/speech.js` | Web Speech API 共通ユーティリティ（ES Module） |
| `templates/static/reader.js` | 単一言語ページ用ロジック |
| `templates/static/reader-multi.js` | 多言語並列モード用ロジック |

`reader.js` / `reader-multi.js` は `speech.js` を `import` する。テンプレートの `<script type="module">` で読み込まれる。

## 簡易リファレンス

### speech.js エクスポート

```js
getFilteredVoicesForLang(availableVoices, langCode)
// → SpeechSynthesisVoice[]
// 言語コードで音声を絞り込み、優先順にソートして返す。
// multilingual 音声を除外し、完全一致 → オンライン → デフォルト → 名前順。

autoAssignDefaultVoices(speakerVoices, speakers, filteredVoices)
// speakerVoices が全 undefined のときのみ自動割り当てを行う。
// スピーカーが 2 人以上かつ男女音声が揃っていれば交互に割り当て、
// それ以外は filteredVoices の先頭から順に割り当てる。

buildVoiceCandidates(speakerVoices, speakers, speakerIndex, filteredVoices)
// → SpeechSynthesisVoice[]
// speakerIndex の候補リストを構築する。
// 割り当て済み音声（preferred）を先頭に配置し、
// 他スピーカーが使用中の音声は除外する。

async speakWithRetry(text, langCode, rate, candidates, options)
// → "ended" | "cancelled" | "error"
// candidates を順に試し、synthesis-failed なら次の候補へ自動リトライする。
```

### speakWithRetry オプション

| オプション | 型 | 説明 |
|---|---|---|
| `vi` | `number` | 開始インデックス（デフォルト 0） |
| `onstart` | `() => void` | 発話開始時（成功確定時）のコールバック |
| `onboundary` | `(e) => void` | 単語境界イベントのコールバック（ハイライト用） |
| `onUtterance` | `(utt) => void` | utterance 生成直後のコールバック（`currentSynth` 更新用） |
| `onVoiceSuccess` | `(voice) => void` | 発話開始時に成功した音声を渡すコールバック |

`onVoiceSuccess` は `onstart` と同タイミングで呼ばれる。リトライ中の失敗した候補では呼ばれない。

## 音声リトライロジックの実装要点

### 全体の流れ

```
speakLine()
  → buildVoiceCandidates()   # 候補リスト構築
  → speakWithRetry()         # 非同期発話（リトライ込み）
      → speakOne(candidates[0])
          synthesis-failed → speakOne(candidates[1]) → ...
          ended/cancelled/error → resolve
  → onVoiceSuccess()         # speakerVoices 更新 + UI 反映
  → 次の行へ進む or 停止
```

### 候補リスト構築（buildVoiceCandidates）

1. `speakerVoices[speakerIndex]`（ユーザー設定済み or 前回成功音声）を先頭に置く
2. 他スピーカーが使用中の音声は除外する（Speaker が被る場合はスキップ）
3. 残りの filteredVoices を後続候補として追加する

これにより「前回成功した音声を優先して試す」「スピーカー間で音声が重複しない」の両方を満たす。

### 成功音声のキャッシュ（onVoiceSuccess）

`speakWithRetry` の内部では `onstart` イベント（= 発話開始 = その音声が使える確定）のタイミングで `onVoiceSuccess(voice)` を呼ぶ。

呼び出し元の `speakLine` では次の 2 つを行う。

```js
onVoiceSuccess: voice => {
    speakerVoices[speakerIndex] = voice;   // 次回の候補リストで先頭に来る
    updateVoiceSelect(speakerIndex, voice); // プルダウン UI に反映
},
```

これにより、初回だけリトライが発生し 2 回目以降はリトライなしで直接発話できる。

### 非同期キャンセルの競合防止（speechGeneration）

`speakLine` は `async` 関数であり、`await speakWithRetry(...)` 中に `stopText` や `updateRate` が呼ばれうる。

```js
// speakLine の先頭でスナップショットを取る
const gen = speechGeneration;
...
const result = await speakWithRetry(...);

// await から戻った時点で世代が変わっていたら、新しい再生が始まっているので何もしない
if (gen !== speechGeneration) return;
```

`stopText` / `updateRate` / `restartIfPlaying` は `speechGeneration++` してから `speechSynthesis.cancel()` を呼ぶ。キャンセルにより `speakWithRetry` が `"cancelled"` を返して await が解け、`gen !== speechGeneration` の判定で早期 return する。

### ES Module 化の効果

`speech.js` を ES Module（`export` / `import`）にすることで次の利点が得られる。

- `window.Speech` グローバルが不要になり、名前空間汚染がない
- `reader.js` / `reader-multi.js` はモジュールスコープを持つため IIFE が不要
- モジュールはデフォルトで strict mode が有効
- `speech.js` の内部関数（`prioritizeVoicesByRegion`, `speakOne` など）は export せず、自然にカプセル化される
