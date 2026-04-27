# 用語事前抽出方式の翻訳実験

[../experimental3/](../experimental3/) のハイブリッドモードを発展させ、**翻訳開始前に全文から用語と固有名詞を抽出して訳語を確定する**方式を検証する実験ディレクトリです。

## 背景と動機

experimental3 までは、翻訳ループの中でサマリー（glossary）が逐次蓄積される方式でした。この方式では序盤の数行で誤訳が発生すると、それが glossary に固定されて後続全体に伝播する「初期蓄積のブレ」問題があります（experimental3 の急落 run はこれが主因）。

experimental4 では:

- **翻訳開始前に全文をスキャンして用語を抽出**（チャンク単位）
- **抽出した用語を一括翻訳**して glossary を確定
- **再編成のたびに対象範囲に絞った用語リストを注入**

これにより、初期蓄積のブレを排除しつつ、用語の一貫性を翻訳全体で確保することを目指します。固有名詞（人名・地名）を抽出対象に含めることで、**音写の統一**（一度決めた表記を全体で揃える）も同時に解決します。

## 翻訳システム

スクリプト実行は必ず `uv run` を使うこと。

### translate.py

```bash
uv run translate.py <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**オプション:**

| オプション | デフォルト | 説明 |
|---|---|---|
| `--threshold` | 10 | 要約生成の間隔（翻訳ペア数） |
| `--keep` | 5 | 要約後〜再編成までの翻訳ペア数 |
| `--terms` | `<output_base>-terms.json` | 用語ファイルのパス。既存ファイルがあれば抽出をスキップして読み込む |
| `--terms-only` | なし | 用語抽出と訳生成のみ実行して終了（翻訳は行わない） |

experimental3 にあった `--no-think` は廃止し、CoT 不使用に固定しています（翻訳・要約・抽出・訳生成すべて think=False）。

### 動作仕様（threshold=10, keep=5）

#### Phase 0: 用語抽出と訳生成（前処理）

1. 入力を `keep` 行ごとのチャンクに分割（43行なら9チャンク）
2. 各チャンクから元言語の用語・固有名詞を構造化出力で抽出（CoT なし）
3. 全チャンクの用語を統合・重複除去
4. 一括の構造化出力で全用語の訳語を生成
5. 用語ファイル（デフォルト `<output_base>-terms.json`）に保存

用語ファイルが既に存在する場合は読み込みのみで済ませます（再実験時の時間節約用）。用語や訳語に問題があれば JSON を直接編集してから再実行することで、抽出をやり直さずに翻訳だけ再実行できます。

#### Phase 1: 翻訳ループ

experimental3 と同じ threshold+keep サイクルで翻訳します。違いは再編成時のコンテキスト構造です:

| タイミング | chat_history |
|---|---|
| 初期 | `[system, terms(1〜threshold+keep)]` |
| 翻訳1〜10 | 逐次拡張 |
| 翻訳10直後 | サマリー生成 → 履歴から削除 |
| 翻訳11〜15 | 拡張継続 |
| 翻訳15直後（再編成） | `[system, terms(16〜30), latest_summary, last 5 pairs]` |
| 翻訳16〜25 | 拡張継続 |
| 翻訳25直後 | サマリー生成 → 履歴から削除 |
| ... | ... |

- 用語注入の対象範囲は「次のサイクルで翻訳する threshold+keep 行」
- 用語抽出はチャンク（keep 行）単位で行うため、範囲フィルタリングが可能

### 用語ファイルのフォーマット（JSON）

```json
{
  "from": "French",
  "to": "Spanish",
  "chunks": [
    {"index": 1, "start": 1, "end": 5, "terms": ["Aurélien Géron", "TensorFlow"]},
    {"index": 2, "start": 6, "end": 10, "terms": ["fine-tuning", "LoRA", "TensorFlow"]}
  ],
  "glossary": {
    "Aurélien Géron": "Aurélien Géron",
    "TensorFlow": "TensorFlow",
    "fine-tuning": "ajuste fino",
    "LoRA": "LoRA"
  }
}
```

- `chunks`: チャンクごとの抽出用語。`start`/`end` は入力ファイルの 1-indexed 行番号
- `glossary`: 元言語 → 翻訳先言語の対応辞書（再編成時の範囲フィルタに使用）

### batch.sh

```bash
bash batch.sh
```

[MODELS.txt](MODELS.txt) の2モデル（gemma4-26b、gemma4-e4b）について、**翻訳3回 × 評価3回** を実行します。experimental3/10-nt と同じ条件で、用語事前抽出の有無のみが差分です。

**ファイル命名:**

```
tr/<model>-<trrun>.txt              例: tr/gemma4-26b-1.txt
tr/<model>-<trrun>-terms.json       例: tr/gemma4-26b-1-terms.json
evals/<model>-<trrun>-eval-<evrun>.json
```

## 対象モデル

experimental3 で安定動作が確認された gemma4-26b と、省リソースの代替モデルとして gemma4-e4b の2モデルに絞りました。qwen3.6-27b は experimental3 で急落リスクと KV キャッシュ非効率が課題として確認されているため除外しています。

| モデル | experimental3/10-nt 中央値 | 選定理由 |
|---|:---:|---|
| gemma4-26b | 96 / 100 / 96 | 全 run で急落なし、最安定 |
| gemma4-e4b | 95 / 96 / 85 | リソース制約がある場合の代替 |

## 評価システム

[../experimental3/](../experimental3/) と同じパイプラインを使用します。

- 評価者: `ollama:qwen3.6`
- 5項目 × 20点 = 100点満点
- 集計: 3回評価の中央値

## 試行

| 試行 | threshold | 結果 |
|---|:---:|---|
| [tr/](tr/) | 10 | gemma4-26b: 96/96/99、gemma4-e4b: 95/96/92 |

## 比較結果

experimental3/10-nt（用語抽出なし）との比較（差分: 用語事前抽出の有無のみ）:

| モデル | experimental3/10-nt | experimental4 |
|---|:---:|:---:|
| gemma4-26b run 1 | 96 | 96 |
| gemma4-26b run 2 | 100 | 96 |
| gemma4-26b run 3 | 96 | 99 |
| gemma4-e4b run 1 | 95 | 95 |
| gemma4-e4b run 2 | 96 | 96 |
| gemma4-e4b run 3 | **85**（急落） | **92**（急落軽減） |

**観察:**

- **gemma4-e4b の急落が軽減**: 85点 → 92点。急落自体は残るが、ダメージが大幅に縮小。用語事前抽出の効果が確認できた
- **gemma4-26b は安定維持**: 急落なし。run 3 が 96→99 と微改善
- **用語集の run 間ブレが残存**: `affinage` の訳語が run によって `refinamiento` と `ajuste fino` に分かれるなど、用語抽出フェーズ自体に確率的なブレがある。glossary 初期蓄積のブレを翻訳ループから用語抽出フェーズに移しただけとも言える
- **一般語の混入**: `mathématiques`・`physicien`・`anglais` など専門用語ではない語が抽出される。抽出プロンプトの改善余地あり
