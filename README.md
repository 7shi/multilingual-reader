# Multilingual Podcast Reader - 多言語ポッドキャストリーダー

多言語対応のポッドキャスト音声読み上げアプリケーション。対訳形式で複数言語（フランス語・ドイツ語・英語・中国語・日本語）を同時表示し、各文を選択した言語で連続読み上げする学習ツールです。


デモページ: [Multilingual Podcast Reader](https://codepen.io/7shi/embed/QwjKWmv?default-tab=result)

## 🎯 特徴

### 📖 対訳表示
- **多言語同時表示**: 設定された言語を行ごとに対訳表示（対応言語：フランス語・ドイツ語・英語・中国語・日本語）
- **視覚的識別**: 各言語に言語コード表示（FR/DE/EN/ZH/JA等）
- **話者識別**: 話者を登場順（Speaker 1, Speaker 2）で識別・色分け表示
- **言語フラグ制御**: 言語フラグをクリックして読み上げ対象言語を選択

### 🎛️ 再生機能
- **選択的多言語読み上げ**: 有効化された言語のみを順次読み上げ
- **言語別音声選択**: 各言語で最適化された音声を自動選択
- **話者別音声設定**: Speaker 1、Speaker 2に異なる音声を割り当て可能（データセット間で共通）
- **動的ハイライト**: 再生中の文字・単語を動的にリアルタイム強調表示（ブラウザ対応時）
- **速度調整**: グローバル速度（0.5-2.0倍速）と言語別速度調整

## 📁 ファイル構成

```
multilingual-reader/
├── podcast-reader.html           # メインHTML（UI構造）
├── podcast-reader.css            # スタイルシート
├── podcast-reader.js             # JavaScriptロジック
├── transformer.js                # 多言語テキストデータ（Transformerテクノロジー）
├── finetuning.js                 # 多言語テキストデータ（ファインチューニング・転移学習）
├── onde.js                       # 多言語テキストデータ（波動・量子力学）
├── momentum.js                   # 多言語テキストデータ（運動量・測定理論）
├── examples/                     # 参照訳テキストファイルと評価結果
│   └── evals/                    # trtools eval による参照訳評価（SCORES.txt・各言語 JSON）
├── experimental/                 # ローカルLLM翻訳実験とパフォーマンス分析
├── experimental2/                # サマリー圧縮方式翻訳実験
├── experimental3/                # ハイブリッドモード翻訳実験（翻訳=CoTなし、要約=CoTあり）
├── experimental4/                # 用語事前抽出方式翻訳実験（翻訳前に全文から用語を抽出・確定）
├── experimental5/                # trtools translate 移行後の翻訳実験（校正済み共有用語辞書を使用）
├── trtools/                      # 共通の翻訳・評価ツール
├── split_podcast_data.py         # テキスト分割スクリプト（データセット配列対応）
├── merge_podcast_data.py         # テキスト統合スクリプト（nameフィールドなし配列形式）
├── pyproject.toml                # Pythonプロジェクト設定
├── README.md                     # このファイル
└── MEMO.md                       # プロジェクト全体のメモ（将来の検討事項等）
```

### 翻訳評価ツール（trtools/）

全実験で共通して使用するツールをパッケージ化したもの。詳細は [trtools/README.md](trtools/README.md) を参照。

| コマンド | 用途 |
|---------|------|
| `uv run trtools translate` | テキストを行単位で翻訳（用語注入・サマリー圧縮方式） |
| `uv run trtools eval` | LLMによる翻訳品質評価（5項目×20点、100点満点） |
| `uv run trtools agg` | 3回評価の中央値集計 |
| `uv run trtools term` | テキストから用語・固有名詞を抽出し訳語をTSVに保存 |
| `uv run trtools batch` | 翻訳→評価→集約を一括実行 |

### 参照訳と評価結果（examples/）

`examples/` には各トピック × 各言語の参照訳テキストファイルが格納されています。原文はすべてフランス語です。

`examples/evals/` には `trtools eval`（評価者: `ollama:qwen3.6`）による3回評価の JSON と集計結果（`SCORES.txt`）が格納されています。再評価・追加評価は `examples/evals/batch.sh` で実行できます。

**全トピックの評価結果（各トピック3回評価の中央値を言語別に平均）:**

| 言語 | 平均値 | トピック数 | 評価原文 |
|-----------|------:|---:|---|
| English   | 98.25 |  4 | French |
| Japanese  | 97.00 |  4 | English |
| Spanish   | 96.75 |  4 | French |
| Chinese   | 96.50 |  4 | English |
| German    | 96.25 |  4 | English |

全言語とも高品質な参照訳として実験のベースラインに使用できる水準。

### 実験ディレクトリの流れ

4つのディレクトリは連続した実験系列です。詳細は [MEMO.md](MEMO.md) を参照してください。

- **[experimental/](experimental/)**: 推論レベル別性能分析。スライディング方式の用語ブレ・KV キャッシュ問題を発見。レベル0（直接翻訳）が最高効率、CoT は翻訳に有害と結論。
- **[experimental2/](experimental2/)**: サマリー圧縮方式に移行。`--summary glossary` + `--no-think` + 構造化出力廃止を基本設定とし、用語ブレ・KV キャッシュ問題を解決。32モデルの本番実験で上位モデルが 95〜97点を達成。
- **[experimental3/](experimental3/)**: ハイブリッドモードを実装。翻訳本体は CoT なし、要約生成のみ CoT ありとし、要約を履歴から除外して KV キャッシュ効率を維持。gemma4-26b が全設定・全 run で安定して最優秀。
- **[experimental4/](experimental4/)**: 用語事前抽出方式を実装。翻訳開始前に全文から用語・固有名詞を抽出して訳語を確定し、再編成ごとに対象範囲に絞った用語リストを注入する。experimental3 の glossary 初期蓄積のブレ問題の解消を狙う。
- **[experimental5/](experimental5/)**: `trtools translate` へ移行。用語抽出を `trtools term` で分離・校正し、全 run が共有用語辞書を参照することで run 間の用語ブレを排除する。

## 🎓 コンテンツ内容

### シリーズ: AI・機械学習技術

#### 🤖 Transformer (Transformerテクノロジー)
AI研究者CamilleとLucの対話形式でTransformerアーキテクチャの革新を解説：
1. **Attention機構の革命**
2. **Self-Attentionの技術革新**
3. **マルチヘッドアテンション**
4. **Position Encodingの独創性**
5. **現代AIへの影響**

#### 🎯 Fine-tuning (ファインチューニング・転移学習)
AI研究者CamilleとLucの対話形式で機械学習の学習方法と記憶メカニズムを解説：
1. **事前学習（Pre-training）**
2. **転移学習（Transfer Learning）**
3. **ファインチューニング vs インコンテキスト学習**
4. **記憶メカニズムの実際**
5. **実用的な選択指針**

### シリーズ: 物理学基礎

#### 🌊 Onde (波動・量子力学)
物理学者CamilleとLucの対話形式で量子力学の基礎概念を解説：
1. **波動関数（ψ）の本質**
2. **量子力学と古典物理の統一性**
3. **ハイゼンベルクの不確定性原理**
4. **光の回折と解像度限界**
5. **哲学的考察**

#### ⚡ Momentum (運動量・測定理論)
物理学者CamilleとLucの対話形式で量子測定理論を解説：
1. **量子運動量の概念転換**
2. **波動-粒子二重性**
3. **不確定性原理の実践的理解**
4. **一般化された測定**
5. **測定の哲学**

## 🌐 ブラウザ対応

### 必要な機能
- **Web Speech API**: 音声合成機能
- **ES6対応**: モダンJavaScript構文
- **CSS Grid/Flexbox**: レスポンシブレイアウト

### 推奨ブラウザ
- **Chrome/Edge**: 最適な音声品質とMultilingual音声除外、動的ハイライト完全対応
- **Firefox**: 基本機能対応、動的ハイライト部分対応
- **Safari**: iOS/macOS での音声合成対応、動的ハイライト限定対応

### 音声エンジン
- **Microsoft Azure**: 高品質オンライン音声（優先）
- **Google Cloud**: 多言語対応音声
- **システム音声**: ローカル音声（フォールバック）

## 🎨 カスタマイズ

### 新しいデータセットの追加

アプリケーションに新しいデータセットを追加するには、以下の手順に従ってください：

#### 1. 対話データの生成

`話者名: 発言内容` 形式のテキストファイルを用意します。

#### 2. 多言語翻訳
生成された対話データを必要な言語に翻訳：

```bash
# 用語を事前抽出して翻訳（推奨）
uv run trtools term extract base_dialogue.txt -f French -m ollama:gemma4:12b -o terms.json
uv run trtools term translate terms.json -t Spanish -m ollama:gemma4:12b -o terms.tsv
uv run trtools translate base_dialogue.txt -f French -t Spanish -o new_dataset-es.txt \
  -m ollama:gemma4:12b --terms-json terms.json --terms-tsv terms.tsv

# 用語なし（シンプルモード）
uv run trtools translate base_dialogue.txt -f French -t Spanish -o new_dataset-es.txt \
  -m ollama:gemma4:12b
```

#### 3. データセットファイルの作成
翻訳された複数ファイルを統合してJavaScriptファイルを作成：

```bash
# 翻訳済みファイルから多言語データセットを生成
uv run merge_podcast_data.py -o new_dataset.js new_dataset-fr.txt new_dataset-en.txt new_dataset-ja.txt
```

#### 4. HTMLファイルでのスクリプト読み込み
`podcast-reader.html`に新しいデータセットファイルを追加：

```html
<script src="transformer.js"></script>
<script src="finetuning.js"></script>
<script src="onde.js"></script>
<script src="momentum.js"></script>
<script src="new_dataset.js"></script> <!-- 新しいデータセット -->
```

#### 5. 初期化設定の更新
`podcast-reader.html`の初期化部分でデータセット情報を追加：

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // データセット設定
    const datasetLabels = {
        'transformer': '🤖 Transformer',
        'finetuning': '🎯 Fine-tuning',
        'onde': '🌊 Onde (Waves)',
        'momentum': '⚡ Momentum',
        'new_dataset': '🆕 New Dataset'  // 新しいデータセット
    };
    
    // 言語設定（必要に応じて言語を追加・変更）
    const languageConfig = {
        fr: { code: 'fr-FR', name: 'Français', defaultRate: 1.0 },
        de: { code: 'de-DE', name: 'Deutsch', defaultRate: 1.0 },
        en: { code: 'en-US', name: 'English', defaultRate: 1.0 },
        zh: { code: 'zh-CN', name: '中文', defaultRate: 1.0,
              fontFamily: ['Noto Sans SC', 'Microsoft YaHei', 'PingFang SC',
                           'Hiragino Sans GB', 'sans-serif'] },
        ja: { code: 'ja-JP', name: '日本語', defaultRate: 1.4 }
    };
    
    init(datasetLabels, languageConfig);
});
```

**注意事項**：
- 記述順がインデックス順となります（最初に記述したものがインデックス0）
- 最初に記述されたデータセットが自動的に選択されます
- HTMLのselectオプションは自動生成されるため、手動で追加する必要はありません
- データセットのインデックスは、JavaScriptファイルが読み込まれる順序に対応します


### 多言語翻訳

`trtools translate` で行単位翻訳（空行保持、用語注入・サマリー圧縮方式）。オプション詳細は [trtools/README.md](trtools/README.md) を参照。

```bash
# 基本使用
uv run trtools translate input.txt -f French -t Spanish -o output.txt -m ollama:gemma4:26b --no-think

# 用語ファイルを指定（用語の一貫性を確保）
uv run trtools translate input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma4:26b --no-think \
  --terms-json terms.json --terms-tsv terms.tsv
```

### テキスト統合・分割

#### テキスト統合（merge_podcast_data.py）
複数言語のテキストファイルを行ごとの対訳形式でJavaScript配列形式に統合：

```bash
# ファイルを指定順序で統合（拡張子を除いた最後の-xx部分を言語コードとして認識）
uv run merge_podcast_data.py -o onde.js onde_physics-fr.txt onde_physics-en.txt onde_physics-ja.txt
uv run merge_podcast_data.py -o momentum.js momentum_data-fr.txt momentum_data-en.txt momentum_data-ja.txt

# 指定順序でマージされ、データ構造に反映される
```

**出力形式**（nameフィールドなし）：
```javascript
// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {
    var datasets = [];
}

// Add dataset to datasets array
datasets.push([
  {"fr": "...", "en": "...", "ja": "..."},
  {"fr": "...", "en": "...", "ja": "..."},
  ...
]);
```

**スクリプト機能**：
- ファイル名から言語コードを自動検出（拡張子除去後の-xx部分）
- 指定順序での行ごと対訳形式JSON配列生成
- datasets配列形式（nameフィールドなし）で出力
- 任意の言語コード・言語順序に対応

#### テキスト分割（split_podcast_data.py）
datasets配列形式の多言語データを個別ファイルに分割：

```bash
# 新しいdatasets配列形式
uv run split_podcast_data.py onde.js -o onde_physics
uv run split_podcast_data.py momentum.js -o momentum_physics

# 出力ファイル
# onde_physics-fr.txt     (フランス語)
# onde_physics-en.txt     (英語) 
# onde_physics-ja.txt     (日本語)
```

**スクリプト機能**：
- datasets配列形式の自動検出・解析（最初のdatasets.push()を抽出）
- 動的な言語検出（決め打ちなし）
- 言語構成の一貫性チェック
- 各言語のテキストを個別のテキストファイルに抽出
- UTF-8エンコーディングで多言語対応

