# Multilingual Podcast Reader - 多言語ポッドキャストリーダー

ポッドキャスト対話を Web Speech API で読み上げる学習ツール。トピック × 言語ごとに独立した静的 HTML を生成し、GitHub Pages で配信。

## 🎯 特徴

- **トピック × 言語の独立ページ**: 4トピック × 6言語（fr/en/es/de/ja/zh）= 24 ページ + ランディング
- **Web Speech API による読み上げ**: 話者別音声選択、グローバル速度調整、再生・停止・一時停止
- **動的ハイライト**: ブラウザ対応時は再生中の単語を boundary イベントで強調
- **話者識別**: 登場順（speaker-0 / speaker-1 ...）で色分け表示
- **言語別フォント**: 中国語は Noto Sans SC、日本語は Hiragino Kaku Gothic ProN を優先

## 🎓 コンテンツ内容

[Multilingual Podcast Reader](https://7shi.github.io/multilingual-reader/) — トピック × 言語のマトリクスから各ページへ遷移できるランディングページ。

- 🤖 **Transformer** — Transformerアーキテクチャの革新（Attention機構・並列処理・転移学習）  
  [全言語](https://7shi.github.io/multilingual-reader/transformer.html) · [フランス語](https://7shi.github.io/multilingual-reader/transformer-fr.html) · [英語](https://7shi.github.io/multilingual-reader/transformer-en.html) · [スペイン語](https://7shi.github.io/multilingual-reader/transformer-es.html) · [ドイツ語](https://7shi.github.io/multilingual-reader/transformer-de.html) · [日本語](https://7shi.github.io/multilingual-reader/transformer-ja.html) · [中国語](https://7shi.github.io/multilingual-reader/transformer-zh.html)
- 🎯 **Fine-tuning** — 機械学習の学習方法と記憶メカニズム（事前学習・転移学習・ファインチューニング）  
  [全言語](https://7shi.github.io/multilingual-reader/finetuning.html) · [フランス語](https://7shi.github.io/multilingual-reader/finetuning-fr.html) · [英語](https://7shi.github.io/multilingual-reader/finetuning-en.html) · [スペイン語](https://7shi.github.io/multilingual-reader/finetuning-es.html) · [ドイツ語](https://7shi.github.io/multilingual-reader/finetuning-de.html) · [日本語](https://7shi.github.io/multilingual-reader/finetuning-ja.html) · [中国語](https://7shi.github.io/multilingual-reader/finetuning-zh.html)
- 🌊 **Onde（波動・量子力学）** — 量子力学の基礎概念（波動関数・不確定性原理・光の回折）  
  [全言語](https://7shi.github.io/multilingual-reader/onde.html) · [フランス語](https://7shi.github.io/multilingual-reader/onde-fr.html) · [英語](https://7shi.github.io/multilingual-reader/onde-en.html) · [スペイン語](https://7shi.github.io/multilingual-reader/onde-es.html) · [ドイツ語](https://7shi.github.io/multilingual-reader/onde-de.html) · [日本語](https://7shi.github.io/multilingual-reader/onde-ja.html) · [中国語](https://7shi.github.io/multilingual-reader/onde-zh.html)
- ⚡ **Momentum（運動量・測定理論）** — 量子測定理論（量子運動量・波動-粒子二重性・測定の哲学）  
  [全言語](https://7shi.github.io/multilingual-reader/momentum.html) · [フランス語](https://7shi.github.io/multilingual-reader/momentum-fr.html) · [英語](https://7shi.github.io/multilingual-reader/momentum-en.html) · [スペイン語](https://7shi.github.io/multilingual-reader/momentum-es.html) · [ドイツ語](https://7shi.github.io/multilingual-reader/momentum-de.html) · [日本語](https://7shi.github.io/multilingual-reader/momentum-ja.html) · [中国語](https://7shi.github.io/multilingual-reader/momentum-zh.html)

## 📁 ファイル構成

```
multilingual-reader/
├── build.py                       # 静的サイトビルダー（uv run build.py）
├── deploy.sh                      # gh-pages ブランチへの push スクリプト
├── Makefile                       # build / clean / serve / deploy ターゲット
├── DEPLOY.md                      # ビルド・実行時・デプロイのアーキテクチャ詳細
├── templates/
│   ├── page.html                  # 単一言語ページのテンプレート
│   ├── multi.html                 # 多言語並列ページのテンプレート
│   ├── index.html                 # ランディングのテンプレート
│   └── static/
│       ├── reader.js              # 単一言語ページ用 JS
│       ├── reader-multi.js        # 多言語並列ページ用 JS
│       └── reader.css             # 共通 CSS
├── examples/                      # 真実の源となる多言語テキスト・参照訳評価
│   ├── {topic}-{lang}.txt         # 4トピック × 6言語 = 24 ファイル
│   ├── evals/                     # trtools eval による参照訳評価
│   └── tr/                        # trtools translate によるローカルLLM翻訳・評価
├── experimental/                  # 翻訳実験系列（01〜10）
├── trtools/                       # 翻訳・評価ツールパッケージ
├── obsolete/                      # 廃止スクリプト・元データ
└── dist/                          # ビルド成果物（.gitignore 対象）
```

## 🚀 ビルドとデプロイ

ビルドパイプライン・実行時 JS・デプロイの設計詳細は [DEPLOY.md](DEPLOY.md) を参照。

### 前提
- `uv`（Python パッケージマネージャー）
- `git`（gh-pages ブランチへの push に worktree を利用）

### ローカルビルド

```bash
# 24 HTML + index.html + assets を dist/ に生成
make build

# ローカルサーバーで動作確認（localhost:8000）
make serve

# ビルド成果物を削除
make clean
```

### GitHub Pages へのデプロイ

```bash
# ビルドして gh-pages ブランチへ push
make deploy
```

`deploy.sh` は `git worktree` で `gh-pages` ブランチを `.gh-pages-worktree/` に展開し、`dist/` の内容で置き換えてコミット・プッシュする。差分がないときは何もしない。

#### 初回セットアップ（GitHub UI 側）

1. GitHub リポジトリの **Settings → Pages** を開く
2. **Source** を `Deploy from a branch` に設定
3. **Branch** を `gh-pages` / `/ (root)` に設定して **Save**
4. 数分後に `https://7shi.github.io/multilingual-reader/` で公開される

`gh-pages` ブランチは初回 `make deploy` 実行時に自動で作成される。

## 🌐 ブラウザ対応

### 必要な機能
- **Web Speech API**: 音声合成
- **ES6 対応**: モダン JavaScript

### 推奨ブラウザ
- **Chrome/Edge**: 最適な音声品質、動的ハイライト完全対応
- **Firefox**: 基本機能対応、動的ハイライト部分対応
- **Safari**: iOS/macOS での音声合成対応、動的ハイライト限定対応

### 音声エンジン
- **Microsoft Azure**: 高品質オンライン音声（優先）
- **Google Cloud**: 多言語対応音声
- **システム音声**: ローカル音声（フォールバック）

## 📝 データ追加

`examples/{topic}-{lang}.txt` を真実の源とする。フォーマットは 1 行 1 発話の `話者名: 発言内容`（中国語は全角コロン `：` も可）。

新トピックを追加する手順：

1. `trtools` で多言語翻訳を生成（[trtools/README.md](trtools/README.md)）
2. `examples/{topic}-{lang}.txt` を 6 言語分配置
3. `build.py` の `TOPIC_LABELS` に新トピックを追加
4. `make build` で全 24 + N ページが再生成される

### 多言語翻訳（trtools）

`trtools translate` で行単位翻訳（空行保持、用語注入・サマリー圧縮方式）。詳細は [trtools/README.md](trtools/README.md) を参照。

```bash
# 用語事前抽出 + 翻訳
uv run trtools term extract base.txt -f French -m ollama:gemma4:12b -o terms.json
uv run trtools term translate terms.json -t Spanish -m ollama:gemma4:12b -o terms.tsv
uv run trtools translate base.txt -f French -t Spanish -o output-es.txt \
  -m ollama:gemma4:26b --terms-json terms.json --terms-tsv terms.tsv
```

## 🛠️ 翻訳評価ツール（trtools/）

全実験で共通して使用するツールをパッケージ化したもの。詳細は [trtools/README.md](trtools/README.md) を参照。

| コマンド | 用途 |
|---------|------|
| `uv run trtools translate` | テキストを行単位で翻訳（用語注入・サマリー圧縮方式） |
| `uv run trtools eval` | LLMによる翻訳品質評価（5項目×20点、100点満点） |
| `uv run trtools agg` | 3回評価の中央値集計 |
| `uv run trtools term` | テキストから用語・固有名詞を抽出し訳語をTSVに保存 |
| `uv run trtools batch` | 翻訳→評価→集約を一括実行 |
| `uv run trtools review` | 高品質ベースラインを別モデルで推敲 |

`trtools` は実験01〜09で得られた成果を統合したもの。実験10で `trtools review` への統合を完了している。詳細は [experimental/README.md](experimental/README.md) を参照。

## 📚 参照訳と評価結果（examples/）

[examples/](examples/) には各トピック × 各言語の参照訳テキストファイルが格納されている。原文はフランス語で、英語・スペイン語はフランス語から直接翻訳しているが、ドイツ語・日本語・中国語は英語を経由した重訳。

全トピック共通の固有名詞や番組名は [examples/tr/terms/common.tsv](examples/tr/terms/common.tsv) で固定している。run ごとの訳語ブレを避けるため。

[examples/evals/](examples/evals/) には `trtools eval`（評価者: `ollama:qwen3.6`）による3回評価の JSON と集計結果（[SCORES.txt](examples/evals/SCORES.txt)）が格納されている。再評価・追加評価は [examples/evals/batch.sh](examples/evals/batch.sh) で実行できる。

**全トピックの評価結果（各トピック3回評価の中央値を言語別に平均）:**

| 言語 | 平均値 | トピック数 | 翻訳元 | 翻訳 | 校正 |
|-----------|------:|---:|---|---|---|
| 英語   | 98.25 |  4 | フランス語 | Gemini 2.5 Pro | Claude Sonnet 4.5 |
| 日本語  | 97.00 |  4 | 英語 | Gemini 2.5 Pro | Claude Sonnet 4.5 |
| スペイン語   | 96.75 |  4 | フランス語 | Gemma 4 26B | Gemini 3.1 Pro Preview |
| 中国語   | 96.50 |  4 | 英語 | Gemma 4 26B | Gemini 3.1 Pro Preview |
| ドイツ語    | 96.25 |  4 | 英語 | Gemma 4 26B | Gemini 3.1 Pro Preview |

全言語とも校正を施しており、参照訳として実験のベースラインに使用できる水準。
