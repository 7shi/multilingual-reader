# Multilingual Podcast Reader - 多言語ポッドキャストリーダー

多言語対応のポッドキャスト音声読み上げアプリケーション。対訳形式で3言語（フランス語・英語・日本語）を同時表示し、各文を3言語で連続読み上げする学習ツールです。

## 🎯 特徴

### 📖 対訳表示
- **3言語同時表示**: フランス語（原文）、英語、日本語を行ごとに対訳表示
- **視覚的識別**: 各言語に色分けされた国旗表示（FR/EN/JA）
- **話者識別**: 話者を登場順（Speaker 1, Speaker 2）で識別・色分け表示

### 🎛️ 再生機能
- **多言語連続読み上げ**: 各文をフランス語→英語→日本語の順で自動読み上げ
- **言語別音声選択**: 各言語で最適化された音声を自動選択
- **話者別音声設定**: Speaker 1、Speaker 2に異なる音声を割り当て可能（データセット間で共通）
- **動的ハイライト**: 再生中の文字・単語を動的にリアルタイム強調表示（ブラウザ対応時）
- **速度調整**: 0.5倍速から2倍速まで調整可能

## 📁 ファイル構成

```
multilingual-reader/
├── podcast-reader.html           # メインHTML（UI構造）
├── podcast-reader.css            # スタイルシート
├── podcast-reader.js             # JavaScriptロジック
├── onde.js                       # 多言語テキストデータ（波動・量子力学）
├── momentum.js                   # 多言語テキストデータ（運動量・測定理論）
├── split_podcast_data.py         # テキスト分割スクリプト（データセット配列対応）
├── merge_podcast_data.py         # テキスト統合スクリプト（nameフィールドなし配列形式）
├── convert_genspark.py           # GenSpark HTML対話データ抽出
├── translate.py                  # 多言語翻訳スクリプト（英語→フランス語・日本語）
├── pyproject.toml                # Pythonプロジェクト設定
└── README.md                      # このファイル
```

## 🎓 コンテンツ内容

### 🌊 Dataset 1: Onde (波動・量子力学)
物理学者CamilleとLucの対話形式で量子力学の基礎概念を解説：

1. **波動関数（ψ）の本質**
   - 物質波と確率波の違い
   - Born規則（|ψ|²）の意味

2. **量子力学と古典物理の統一性**
   - 確率密度とエネルギー密度の類似性
   - 物理法則の普遍的な美しさ

3. **ハイゼンベルクの不確定性原理**
   - 位置と運動量の関係（Δx・Δk）
   - マクロ世界での現れ方

4. **光の回折と解像度限界**
   - アッベ限界（λ/2）
   - 超解像技術（NSOM）

5. **哲学的考察**
   - 確率の物理的実在性
   - 量子世界と日常世界の架け橋

### ⚡ Dataset 2: Momentum (運動量・測定理論)
物理学者MaryとJohnの対話形式で量子測定理論を解説：

1. **量子運動量の概念転換**
   - 古典的直感から量子現実への跳躍
   - 運動量演算子の物理的意味

2. **波動-粒子二重性**
   - 電子の波的性質
   - 波の「波打ち具合」としての運動量

3. **不確定性原理の実践的理解**
   - 完全な運動量 vs 完全な位置
   - 測定の根本的トレードオフ

4. **一般化された測定**
   - 間接測定の巧妙な戦略
   - 磁場を利用した運動量測定

5. **測定の哲学**
   - 受動的観察から能動的操作へ
   - 量子世界における物理量の本質

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

#### 1. データセットファイルの作成
新しいデータセット用のJavaScriptファイルを作成します：

```bash
# 指定されたファイルから多言語データセットを生成
uv run merge_podcast_data.py -o new_dataset.js new_dataset-fr.txt new_dataset-en.txt new_dataset-ja.txt
```

#### 2. HTMLファイルでのスクリプト読み込み
`podcast-reader.html`に新しいデータセットファイルを追加：

```html
<script src="onde.js"></script>
<script src="momentum.js"></script>
<script src="new_dataset.js"></script> <!-- 新しいデータセット -->
```

#### 3. HTMLのselectオプション追加
dataset選択プルダウンに新しいオプションを追加：

```html
<select id="dataset">
    <option value="onde" selected>🌊 Onde (Waves)</option>
    <option value="momentum">⚡ Momentum</option>
    <option value="new_dataset">🆕 New Dataset</option> <!-- 新しいオプション -->
</select>
```

#### 4. 初期化設定の更新
`podcast-reader.html`の初期化部分でデータセットマッピングを更新：

```javascript
document.addEventListener('DOMContentLoaded', () => {
    init({
        'onde': 0,
        'momentum': 1,
        'new_dataset': 2  // 新しいデータセットのインデックス
    });
});
```

**注意事項**：
- データセットのインデックスは、JavaScriptファイルが読み込まれる順序に対応します
- 各データセットファイルは`datasets.push([...])`形式で配列に追加されます
- ファイル読み込み順序とマッピングのインデックスを一致させる必要があります

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
