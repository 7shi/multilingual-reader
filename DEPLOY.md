# ビルドとデプロイのアーキテクチャ

multilingual-reader の静的サイト生成・実行時挙動・デプロイの設計詳細。日常運用は [README.md](README.md) を参照。

## 全体フロー

```
examples/{topic}-{lang}.txt  ──┐
templates/page.html          ──┤
templates/multi.html         ──┼── build.py (Jinja2) ──▶ dist/
templates/index.html         ──┤                          │
templates/static/*.{js,css}  ──┘                          │
                                                          ▼
                                          deploy.sh (git worktree)
                                                          │
                                                          ▼
                                            gh-pages ブランチへ push
                                                          │
                                                          ▼
                                https://7shi.github.io/multilingual-reader/
```

入力データ → ビルド → 実行時 JS → デプロイ の各段階を以下で詳述する。

## 1. 入力データ

### `examples/{topic}-{lang}.txt`

トピック × 言語ごとに 1 ファイル（4 トピック × 6 言語 = 24 ファイル）。フォーマットは「1 行 = 1 発話」、各行は `話者名: 発言内容` 形式。

中国語のみ全角コロン `：` (U+FF1A) を区切りに使うことがあり、`build.py` の `extract_speaker_and_text` は半角・全角の両方に対応する:

```python
for sep in (":", "："):
    if sep in text:
        parts = text.split(sep, 1)
        ...
```

例 (フランス語):
```
Camille: Bonjour et bienvenue dans « Tech Éclair »...
Luc: Et moi, c'est Luc...
```

中国語版では話者名そのものも訳されている:
```
卡米尔：大家好，欢迎收听《科技快报》...
卢克：我是卢克...
```

### 話者インデックスの正規化

多言語並列モードでは「話者 N が行 K を発する」という対応関係を全言語で統一する必要がある。`build.py` は **フランス語版（原文）の登場順** を基準として `speakers_in_order` を確定し、行 i の `speaker_index` は `speakers_in_order.index(fr_lines[i].speaker)` で決定する。

これにより中国語の `卡米尔` も英語の `Camille` も同じ `speaker-0` として CSS 色分けと音声割り当てを共有できる。各言語ページ内では各言語の名前で表示されるが、内部 ID は統一されている。

## 2. テンプレートとビルド

### Jinja2 を選定した理由

- HTML 自動エスケープが既定で有効（XSS 対策）
- ループ・条件分岐が簡潔（行ごとの SSR が自然に書ける）
- 拡張性: 将来トピックや言語を増やしてもテンプレートは変更不要
- 唯一の例外として、`<script type="application/json">` 内の埋め込み JSON のみ `|safe` で生エスケープ抑制し、代わりに `build.py` 側で `<` `>` `&` を `\uXXXX` に置換する

### テンプレート 2 種類

- `templates/page.html` ... 単一言語ページ
- `templates/multi.html` ... 多言語並列ページ
- `templates/index.html` ... ランディング

CSS は `templates/static/reader.css` で全ページ共通。JS は単一言語が `reader.js`、多言語が `reader-multi.js` で分離（共有部分の重複はあるが、ロジックの差が大きいため独立性を優先）。

### 生成物

| 出力 | 件数 | 用途 |
|------|----:|------|
| `dist/{topic}.html` | 4 | 多言語並列モード（デフォルト） |
| `dist/{topic}-{lang}.html` | 24 | 単一言語モード |
| `dist/index.html` | 1 | ランディング（4 × 7 マトリクス: All + 6 言語） |
| `dist/assets/reader.css` | 1 | 共通 CSS |
| `dist/assets/reader.js` | 1 | 単一言語用 JS |
| `dist/assets/reader-multi.js` | 1 | 多言語用 JS |

合計 32 ファイル。フルビルドで 1 秒未満。

### `LANG_CONFIG` と `TOPIC_LABELS`

`build.py` 冒頭の 2 つの辞書がトピック・言語の単一情報源:

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

トピック・言語の追加・削除はこれらの編集だけで完結する（`make build` で全成果物が再生成される）。

## 3. データ埋め込み戦略

### SSR HTML + page-config JSON のハイブリッド

行のテキストは **SSR 済み HTML** として直接埋め込む（JS 無効でも読める）。一方、話者リスト・言語コード・フォント設定など JS が必要とするメタ情報は `<script id="page-config" type="application/json">` 内に JSON で埋め込む。

利点:
- ✅ JS 無効でも本文が表示される（プログレッシブエンハンスメント）
- ✅ ハイライト処理は DOM 走査のみで完結（JS 側のテンプレートロジック不要）
- ✅ 検索エンジンから本文がインデックス可能

### `<script type="application/json">` 内 JSON のエスケープ

HTML パーサは `<script>` 要素の中身を「raw text」として処理し、HTML エンティティ（`&#34;` など）を **デコードしない**。一方、`</script>` シーケンスはタグの早期終了として解釈される。

そのため `build.py` は JSON 文字列に対して以下の置換を行ってから埋め込む:

| 元 | 置換後 |
|----|--------|
| `<` | `\u003c` |
| `>` | `\u003e` |
| `&` | `\u0026` |

```python
config_json = config_json.replace("<", "\\u003c") \
    .replace(">", "\\u003e") \
    .replace("&", "\\u0026")
```

これで `</script>` が JSON 内に偶発的に出現しても安全で、Jinja2 の HTML 自動エスケープ（`{{ x }}` での `&amp;` など）も発生せず（`|safe` で抑制）、ブラウザ側 `textContent` で取り出した文字列がそのまま `JSON.parse` 可能になる。

### `page-config` の中身（多言語版の例）

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

単一言語版は構造が簡略化され `lang` / `lang_code` / `lang_name` などの単一フィールド。

## 4. 実行時 JS

### ブートストラップ

`DOMContentLoaded` で:
1. `page-config` JSON を `JSON.parse(document.getElementById("page-config").textContent)` で読み込み
2. DOM から行要素（`.line` または `.translation-line`）を収集
3. 各 `.line-text` の `textContent` を `data-original-text` 属性に保存（ハイライト復元用に元テキストを保持）
4. Web Speech API のサポート確認、`speechSynthesis.getVoices()` を呼び出し
5. `speechSynthesis.onvoiceschanged` を購読（音声リストは非同期で揃うため、初回読み込み時は空配列が返る場合がある）
6. 話者音声 UI（`#speakerVoices` セクション）を構築

### 音声選択ロジック

`getFilteredVoices(lang)`:
1. ブラウザが提供する全音声から `voice.lang.split("-")[0]` で言語ベースが一致するものを抽出（例: 日本語なら `ja-*` がすべて）
2. `prioritizeVoicesByRegion` で安定ソート:
   - 同一地域コード（例: `fr-FR` 完全一致）を優先
   - `localService === false`（オンライン音声）を優先 — Microsoft Azure / Google Cloud 由来の高品質音声が先頭に来る
   - `voice.default === true` を優先
   - 残りはアルファベット順
3. `multilingual` を名前に含む音声は除外（複数言語混合音声は品質が不均一なため）

### 自動音声割り当て

`autoAssignDefaultVoices(lang, filteredVoices)` は話者数 ≥ 2 かつ男女両方の音声が利用可能な場合、男女を交互に割り当てる。性別判定は名前マッチング（ホワイトリスト方式）:

```js
const maleNames = ["gerard", "thierry", ..., "david", "guy", ..., "ichiro", "yunjian"];
const femaleNames = ["charline", "sylvie", ..., "aria", "jenny", ..., "ayumi", "xiaoxiao"];
```

各言語の Microsoft / Google 音声の名前から経験的に抽出している。`female` `male` `homme` `femme` などのキーワードも併用。

該当が無い言語では順番割り当て（filteredVoices の頭から N 個）。

### 動的ハイライト

`SpeechSynthesisUtterance.onboundary` は単語境界で発火し、`event.charIndex` と `event.charLength` を提供する。`highlightWord` はこれを使い:

```
[ before ][ TARGET ][ after ]
            ^^^^^^
       <span class="word speaking">
```

の 3 セグメントに `innerHTML` を再構成する。次の `onboundary` または `onend` のタイミングで `data-original-text` から元のテキストを復元（`textContent` への上書き）。

ブラウザ実装の差:
- Chrome / Edge: word 単位で安定発火、`charLength` も正確
- Firefox: 部分的な対応、発火頻度が低い
- Safari: ベンダー実装に依存、機能制限あり

そのためハイライトは "best-effort" として扱う（読み上げ自体は全ブラウザで動作）。

### キャンセル系エラーの抑制

`speechSynthesis.cancel()` を呼ぶと、現在発話中の utterance に対して `onerror` が `error: 'canceled'` または `'interrupted'` で発火する。これは:
- ユーザーが Stop ボタンを押したとき
- 速度スライダーを動かしたとき（cancel して新しい rate で再開）
- 言語フラグをトグルしたとき（再生中なら停止）

これらは「ユーザー操作による意図的なキャンセル」であり、エラー UI を表示すると誤解を招く。判別:

```js
utterance.onerror = e => {
    if (isStopped || e.error === "canceled" || e.error === "interrupted") {
        clearAllHighlights();
        return;  // status 表示・console.error なし
    }
    console.error("Speech synthesis error:", e);
    updateStatus("stopped", "Error occurred during playback");
    clearAllHighlights();
};
```

`isStopped` フラグは `stopText()` の冒頭で `true` にセットされ、cancel 直前の状態でも誤エラー表示を防ぐ。

### 多言語並列モードの再生ループ

状態:
- `currentGroupIndex` ... 現在の行（0 始まり、`groups[]` の添字）
- `currentStep` ... 有効言語リスト内の現在のインデックス

各行で有効言語をすべて読み終えたら次の行へ。`speakNext()` の擬似コード:

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
    if (!group[lang]) {       // その行が当該言語に存在しない場合
        currentStep++;
        speakNext();           // 再帰でスキップ
        return;
    }
    speak(group[lang], lang);
}
```

`utterance.onend` で `currentStep++` してから次のキューを `setTimeout` で:
- 同一行内の次言語へ → 400ms
- 次の行へ移る → 800ms

の delay で `speakNext()` 再呼び出し。delay は人間が言語の境目を聞き分けやすくする間。

### 単一言語モードの再生ループ

`currentLineIndex` のみで状態管理。`speakLine(index)` が `lines[index]` を読み上げ、`onend` で `currentLineIndex++` して次へ。多言語ループのような言語ステップは無いためコードは大幅に簡略。

### 永続化

各言語の読み上げ速度は `localStorage[multilingualReader.langRates.{topic}]` に JSON で保存。トピックごとに分離しているのは「Onde は速度落としたいが Transformer は等速」のような調整を許容するため。

話者音声の選択は永続化しない（ブラウザ・OS 間で利用可能な音声が大きく異なり、保存しても再現性が無いため）。

## 5. デプロイ (`deploy.sh`)

### 処理ステップ

```bash
1. dist/ の存在チェック
2. git worktree add .gh-pages-worktree gh-pages
   ├ ローカルに gh-pages がある:    git worktree add <dir> gh-pages
   ├ origin/gh-pages がある:        git worktree add -B gh-pages <dir> origin/gh-pages
   └ どちらも無い（初回）:          git worktree add --orphan -b gh-pages <dir>
3. find <dir> -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
4. cp -r dist/. .gh-pages-worktree/
5. touch .gh-pages-worktree/.nojekyll
6. cd .gh-pages-worktree && git add -A
7. git diff --cached --quiet || git commit -m "Deploy <sha>"
8. git push origin gh-pages
9. cd .. && git worktree remove --force .gh-pages-worktree
```

### git worktree 方式の利点

代替案との比較:

| 方式 | 利点 | 欠点 |
|------|------|------|
| **worktree** | main の作業ツリーを切り替えない / 並行作業可 / `.git` 共有で軽量 | 同名 worktree が残ると次回失敗（事前削除で対応済） |
| ブランチ切替 | シンプル | `git checkout gh-pages` で作業ツリーが書き換わる / 編集中ファイルが消える |
| 別クローン | 完全に独立 | リポジトリを 2 つ管理 / push 認証が二重 |
| GitHub Actions | 自動化 | YAML / シークレット管理が必要 / npm 依存しがちだが本プロジェクトは npm 不使用方針 |

multilingual-reader は npm を使わない方針のため、worktree + シェルスクリプトが最もシンプル。`uv` だけで完結する。

### `.nojekyll` の必要性

GitHub Pages はデフォルトで Jekyll を経由する。Jekyll は `_` で始まるパスを「Jekyll 用テンプレート」として扱い、サイトに含めない（公開されない）。今回はそうしたパスは無いが、将来 `_assets/` のようなディレクトリを置いても破綻しないように `.nojekyll` を置いて Jekyll 自体を無効化している。副次的にビルド時間も短縮される。

### 冪等性

`git diff --cached --quiet` で差分が無いときは commit しない（空コミットを避ける）。push する内容が変わらない場合 `make deploy` は実質 no-op で、複数回実行しても安全。

### コミットメッセージ

`Deploy <main の short sha>` 形式。これにより `gh-pages` のコミット履歴から「どの main コミットが現在公開されているか」を逆引きできる。

## 6. ローカル開発

### `make serve`

`uv run python -m http.server 8000` で `dist/` を 8000 番ポートで配信:

```bash
make build && make serve
# http://localhost:8000/
```

### 相対パスでの統一

GitHub Pages 配下では `/multilingual-reader/` が base path だが、本サイトは **すべて相対パス**で参照しているため、ローカルとデプロイ後で同一に動作する:

- `<link rel="stylesheet" href="assets/reader.css">`
- `<script src="assets/reader.js">`
- `<a href="transformer-fr.html">`（index.html 内）
- `<a href="transformer.html">`（lang-nav 内）

`<base>` タグや絶対パス `/assets/...` を一切使わないため、サブパス配信・ローカル直開きいずれでも壊れない。

### 部分ビルドはサポートしない

`build.py` は常にフルビルド。30 ファイル弱で 1 秒未満で完了するため差分ビルドの必要が無く、複雑度を上げる価値が無い。

### dist/ は gitignore 対象

`dist/` は `.gitignore` で除外。main ブランチには成果物は含まれず、`gh-pages` ブランチのみが成果物を保持する。

## 7. GitHub Pages 設定（初回のみ）

1. リポジトリの **Settings → Pages** を開く
2. **Source** を `Deploy from a branch` に設定
3. **Branch** を `gh-pages` / `/ (root)` に設定して **Save**
4. 数分後に `https://7shi.github.io/multilingual-reader/` で公開

`gh-pages` ブランチは初回 `make deploy` 実行時に自動で orphan として作成される。

## 8. 二つのモードの設計意図

### 多言語並列モード (`{topic}.html`, デフォルト)

- 全 6 言語の対訳を行ごとに重ねて表示
- language-flag のクリックで読み上げ対象言語をオン / オフ
- 有効な言語を行ごとに順次読み上げ（行 N の lang A → lang B → ... → 行 N+1）
- 言語別の読み上げ速度・話者音声を個別調整
- **想定ユース**: 「フランス語 → 日本語」のように 2 言語を交互に聞いて対訳学習する

### 単一言語モード (`{topic}-{lang}.html`)

- 1 言語のみ表示・読み上げ
- 各ページ右上の lang-nav から「All」（多言語版）と他言語版へ即座に切替可能
- **想定ユース**: 単一言語に集中してリスニング・シャドーイング、または特定言語のページを直接共有する

### URL の使い分け

| URL パターン | 用途 |
|--------------|------|
| `{topic}.html` | デフォルト（多言語）。共有時の標準形 |
| `{topic}-{lang}.html` | 特定言語に直接ジャンプ。SEO 上も独立ページとして扱われる |
| `index.html` | 全トピック × モードの一覧 |

`index.html` の「All」列が強調表示（青塗り）されているのは、こちらが推奨経路であることを示すため。
