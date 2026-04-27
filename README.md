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
├── trtools/                      # 共通の翻訳・評価ツール
├── split_podcast_data.py         # テキスト分割スクリプト（データセット配列対応）
├── merge_podcast_data.py         # テキスト統合スクリプト（nameフィールドなし配列形式）
├── convert_genspark.py           # GenSpark HTML対話データ抽出
├── translate.py                  # 多言語翻訳スクリプト（英語→フランス語・日本語）
├── pyproject.toml                # Pythonプロジェクト設定
├── README.md                     # このファイル
└── MEMO.md                       # プロジェクト全体のメモ（将来の検討事項等）
```

### 翻訳評価ツール（trtools/）

全実験で共通して使用するツールをパッケージ化したもの。

| コマンド | 用途 |
|---------|------|
| `uv run trtools eval` | LLMによる翻訳品質評価（5項目×20点、100点満点） |
| `uv run trtools agg` | 3回評価の中央値集計 |
| `uv run trtools term` | テキストから用語・固有名詞を抽出し訳語をJSONに保存 |

### 参照訳と評価結果（examples/）

`examples/` には各トピック × 各言語の参照訳テキストファイルが格納されています。原文はすべてフランス語です。

`examples/evals/` には `trtools eval`（評価者: `ollama:qwen3.6`）による3回評価の JSON と集計結果（`SCORES.txt`）が格納されています。再評価・追加評価は `examples/evals/batch.sh` で実行できます。

**全トピックの評価結果（各トピック3回評価の中央値を言語別に平均）:**

| 言語 | 平均値 | トピック数 | 評価原文 |
|-----------|------:|---:|---|
| English   | 98.25 |  4 | French |
| Japanese  | 97.00 |  4 | English |
| Spanish   | 95.00 |  4 | French |
| German    | 94.50 |  4 | English |
| Chinese   | 91.00 |  4 | English |
| Hindi     | 29.00 |  1 | English |
| Esperanto | 11.00 |  1 | English |

英語・日本語・スペイン語・ドイツ語は高品質な参照訳として実験のベースラインに使用できる水準。中国語は課題が残る。エスペラント・ヒンディー語（`onde` トピックのみ）は構造的欠陥レベルのため再翻訳予定。

### 実験ディレクトリの流れ

4つのディレクトリは連続した実験系列です。詳細は [MEMO.md](MEMO.md) を参照してください。

- **[experimental/](experimental/)**: 推論レベル別性能分析。スライディング方式の用語ブレ・KV キャッシュ問題を発見。レベル0（直接翻訳）が最高効率、CoT は翻訳に有害と結論。
- **[experimental2/](experimental2/)**: サマリー圧縮方式に移行。`--summary glossary` + `--no-think` + 構造化出力廃止を基本設定とし、用語ブレ・KV キャッシュ問題を解決。32モデルの本番実験で上位モデルが 95〜97点を達成。
- **[experimental3/](experimental3/)**: ハイブリッドモードを実装。翻訳本体は CoT なし、要約生成のみ CoT ありとし、要約を履歴から除外して KV キャッシュ効率を維持。gemma4-26b が全設定・全 run で安定して最優秀。
- **[experimental4/](experimental4/)**: 用語事前抽出方式を実装。翻訳開始前に全文から用語・固有名詞を抽出して訳語を確定し、再編成ごとに対象範囲に絞った用語リストを注入する。experimental3 の glossary 初期蓄積のブレ問題の解消を狙う。

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
まず、対話形式のテキストデータを生成する必要があります。

**GenSparkで生成した場合**：
1. GenSparkの出力からDOMの該当箇所をコピーしてHTMLファイルとして保存
2. `convert_genspark.py`を使用して対話データを抽出：

```bash
# GenSpark HTMLから対話データを抽出
uv run convert_genspark.py genspark_output.html -o base_dialogue.txt --speaker Camille,Luc
```

#### 2. 多言語翻訳
生成された対話データを必要な言語に翻訳：

```bash
# 英語から他言語への翻訳
uv run translate.py base_dialogue.txt -f English -t French -o new_dataset-fr.txt
uv run translate.py base_dialogue.txt -f English -t Japanese -o new_dataset-ja.txt
# 元データが英語の場合は、そのまま使用
cp base_dialogue.txt new_dataset-en.txt
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


### GenSpark HTML対話データの抽出
`convert_genspark.py`スクリプトを使用して、GenSpark HTMLファイルから対話データを抽出：

```bash
# 基本使用（デフォルトの話者名 A,B）
uv run convert_genspark.py input.html -o output.txt

# 話者名を指定
uv run convert_genspark.py input.html -o output.txt --speaker Camille,Luc
```

**スクリプト機能**：
- GenSpark HTMLファイルから話者別対話データを抽出
- `--speaker`オプションで話者名をカンマ区切りで指定可能
- デフォルトでは話者名A,Bを使用
- プル型XMLパーサーによる効率的なHTML解析
- UTF-8エンコーディングで多言語対応

### 多言語翻訳
`translate.py`スクリプトを使用して、指定した言語間で1:1翻訳：

```bash
# 基本使用（デフォルトモデル: ollama:gemma3n:e4b）
uv run translate.py input.txt -f English -t Japanese -o output.txt

# カスタムモデル指定
uv run translate.py input.txt -f French -t English -o translated.txt -m ollama:llama3.1:8b

# テストモード（実際の翻訳は行わない）
uv run translate.py input.txt -f English -t Japanese -o test.txt --test
```

**必須オプション**：
- `-f/--from`: 原語（完全な言語名: English, French, Japanese, German等）
- `-t/--to`: 翻訳先言語（完全な言語名: English, French, Japanese, German等）
- `-o/--output`: 出力ファイル名

**オプション**：
- `-m/--model`: 翻訳モデル（デフォルト: ollama:gemma3n:e4b）
- `--test`: dry-runモード

**スクリプト機能**：
- 任意の言語間での1:1翻訳
- ローカルLLMによる文脈付き翻訳（ollama対応）
- 話者別対話形式の保持
- 翻訳前の推論過程を含む構造化出力
- 完全な言語名による直感的な操作

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

## GPT-OSS 120B の評価外活用

翻訳・評価タスクでは天井効果（最高92点）により評価者として不採用だが、高速推論を活かした補助的な用途が考えられる。具体的には用語確認（訳語候補の列挙・妥当性チェック）や背景知識補完（固有名詞・文化的文脈の説明）など、判断力より知識量と速度が求められる場面での活用。
