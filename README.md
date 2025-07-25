# Multilingual Podcast Reader - 多言語ポッドキャストリーダー

多言語対応のポッドキャスト音声読み上げアプリケーション。対訳形式で3言語（フランス語・英語・日本語）を同時表示し、各文を3言語で連続読み上げする学習ツールです。

## 🎯 特徴

### 📖 対訳表示
- **3言語同時表示**: フランス語（原文）、英語、日本語を行ごとに対訳表示
- **視覚的識別**: 各言語に色分けされた国旗表示（FR/EN/JA）
- **話者識別**: 話者を登場順（Speaker 1, Speaker 2）で識別・色分け表示

### 🔊 高品質音声合成
- **言語別音声選択**: 各言語で最適化された音声を自動選択
- **話者別音声設定**: Speaker 1、Speaker 2に異なる音声を割り当て可能（データセット間で共通）
- **音声品質優先**: オンライン音声（localService=false）を優先選択
- **Multilingual音声除外**: 品質の劣るMultilingual音声を自動除外

### 🎛️ 再生機能
- **多言語連続読み上げ**: 各文をフランス語→英語→日本語の順で自動読み上げ
- **言語切り替え再生**: 任意の言語行をクリックしてその言語で再生開始
- **動的ハイライト**: 再生中の文字・単語を動的にリアルタイム強調表示（ブラウザ対応時）
- **多言語対応ハイライト**: 日本語の分かち書きなしテキストにも対応
- **速度調整**: 0.5倍速から2倍速まで調整可能
- **統合音声制御**: Play/Pauseボタンが状態に応じて切り替わる直感的操作

### 📚 データセット機能
- **複数データセット対応**: 異なる物理学トピックを切り替え可能
- **データセット切り替え**: ドロップダウンで簡単にコンテンツ変更
- **音声設定保持**: データセット変更時も話者別音声設定を維持

### 🧮 数式読み上げ対応
物理学の数式記号を各言語で読み上げ可能な単語に変換：
- **|ψ|²**: フランス語「psi au carré」、英語「psi squared」、日本語「プサイの二乗」
- **λ/2**: フランス語「lambda sur deux」、英語「lambda over two」、日本語「ラムダを2で割った値」
- **Δx, Δk**: フランス語・英語「delta x/k」、日本語「デルタx/k」

## 🚀 使用方法

### 基本操作
1. **コンテンツ選択**: 
   - **Dataset**: どの物理学トピック（Onde/Momentum）を学習するか選択
   - **Language**: 再生モード選択（Multi-Language/単言語）
2. **再生制御**:
   - **▶️/⏸️ ボタン**: 再生状態に応じてPlay/Pauseが切り替わる統合ボタン
   - **⏹️ Stop**: 再生停止
   - 行クリック: 特定の行・言語から再生開始
3. **音声設定**: 「Speaker Voice Assignment & Language Speeds」セクションをクリックして展開
   - 折りたたみ可能なUIでスペースを節約
   - 言語ごとに横並びで表示される設定パネル
   - Speaker 1/Speaker 2の音声を個別選択

### 音声設定
1. **横並び表示**: 3言語（Français/English/日本語）が横に並んで表示
2. **言語別速度調整**: 各言語ごとに個別の再生速度を設定可能
3. **話者別設定**: Speaker 1/Speaker 2に個別の音声を割り当て
4. **自動選択**: 初回時は性別に基づいて最適な音声を自動割り当て
5. **折りたたみUI**: デフォルトで折りたたまれ、必要時のみ展開
6. **データセット間共通**: 音声設定はデータセット切り替え時にリセット

### 学習機能
- **多言語比較学習**: Multi-Langモードで同じ文を3言語で連続比較
- **対訳学習**: 同じ内容を3言語で比較しながら学習
- **専門用語習得**: 物理学の専門用語を多言語で理解
- **発音練習**: ネイティブ音声での正確な発音を確認
- **集中学習**: 特定の文を繰り返し3言語で聞いて理解を深化

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

### CSS変数
主要な色やサイズはCSS変数で定義されており、容易にカスタマイズ可能：
- 話者別色設定（Camille: 紫、Luc: 緑）
- 言語別色設定（FR: 青、EN: 赤、JA: 深紅）

### 音声優先順位
`prioritizeVoices()`関数で音声選択の優先順位を変更可能：
1. オンライン音声（localService=false）
2. 非Multilingual音声
3. デフォルト音声
4. アルファベット順

## 🔧 開発・拡張

### 技術的特徴
- **動的ハイライト**: `onboundary`イベントの`charLength`情報を使用した正確な文字範囲ハイライト
- **UI改善**: 折りたたみ可能な音声設定、横並び言語パネル、統合されたMulti-Language選択
- **コード統合**: 重複コードを統合し、メンテナンス性を向上（約300行削減）
- **共通関数**: `parseAllLanguageTexts()`と`speakLineWithUtterance()`による処理の統一化
- **フォールバック対応**: `charLength`未対応ブラウザでは音声のみ再生
- **レスポンシブ対応**: デスクトップでは横並び、モバイルでは縦並びレイアウト

### 新しい言語の追加
1. `langCodes`オブジェクトに言語コード追加
2. `podcastTexts`にテキストデータ追加
3. HTMLの言語選択オプションと列要素追加
4. CSS色設定追加

### 新しいコンテンツの追加
1. **新しいデータセット作成**:
   - `datasets.push([...]);`形式でJavaScriptファイル作成
   - HTMLで読み込み（`<script src="new_dataset.js"></script>`）
2. **UIの更新**:
   - HTMLのdatasetセレクターに新しいオプション追加
   - JavaScriptの配列インデックス対応追加
3. **音声設定の確認**:
   - 話者数と音声自動割り当ての確認
   - 数式記号の読み上げ対応確認

### GenSpark HTML対話データの抽出
`convert_genspark.py`スクリプトを使用して、GenSpark HTMLファイルから対話データを抽出：

```bash
# 基本使用（デフォルトの話者名 A,B）
python convert_genspark.py input.html -o output.txt

# 話者名を指定
python convert_genspark.py input.html -o output.txt --speaker Camille,Luc
```

**スクリプト機能**：
- GenSpark HTMLファイルから話者別対話データを抽出
- `--speaker`オプションで話者名をカンマ区切りで指定可能
- デフォルトでは話者名A,Bを使用
- プル型XMLパーサーによる効率的なHTML解析
- UTF-8エンコーディングで多言語対応

### 多言語翻訳
`translate.py`スクリプトを使用して、英語テキストをフランス語と日本語に翻訳：

```bash
# 基本使用（デフォルトモデル: ollama:gemma3n:e4b）
python translate.py input-en.txt

# カスタムモデル指定
python translate.py input-en.txt -m ollama:llama3.1:8b

# テストモード（実際の翻訳は行わない）
python translate.py input-en.txt --test

# 出力ファイル
# input-fr.txt  (フランス語翻訳)
# input-ja.txt  (日本語翻訳)
```

**スクリプト機能**：
- 英語対話テキストをフランス語・日本語に翻訳
- ローカルLLMによる文脈付き翻訳（ollama対応）
- 話者別対話形式の保持
- 翻訳前の推論過程を含む構造化出力
- 動的な出力ファイル名生成

### テキスト統合・分割

#### テキスト統合（merge_podcast_data.py）
複数言語のテキストファイルを行ごとの対訳形式でJavaScript配列形式に統合：

```bash
# プレフィックスを使用した自動検索
python merge_podcast_data.py -o onde.js --prefix onde_physics
# → onde_physics-fr.txt, onde_physics-en.txt, onde_physics-ja.txt を自動検索

# ファイルを直接指定
python merge_podcast_data.py -o momentum.js file1-fr.txt file2-en.txt file3-ja.txt
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
- 複数言語ファイルの自動検出・読み込み
- 行ごとの対訳形式でJSON配列生成
- datasets配列形式（nameフィールドなし）で出力
- プレフィックス指定とファイル直接指定の両方に対応

#### テキスト分割（split_podcast_data.py）
datasets配列形式の多言語データを個別ファイルに分割：

```bash
# 新しいdatasets配列形式
python split_podcast_data.py onde.js -o onde_physics
python split_podcast_data.py momentum.js -o momentum_physics

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

### ハイライト機能の仕組み
- **Web Speech API**: `SpeechSynthesisUtterance.onboundary`イベントを使用
- **文字範囲特定**: `event.charIndex`と`event.charLength`で正確な範囲を特定
- **動的DOM更新**: 再生中にテキストを動的に分割してハイライト表示
- **多言語対応**: 事前の単語分割に依存せず、どの言語でも対応可能

## 📚 教育利用

### 対象者
- **物理学学習者**: 量子力学の基礎概念理解
- **多言語学習者**: 科学的内容での語学練習
- **教育者**: インタラクティブな教材として

### 学習効果
- **概念理解**: 抽象的な量子概念の直感的理解
- **多言語思考**: 同一概念を3言語で瞬時に理解する能力向上
- **専門用語**: 物理学用語の多言語習得と記憶定着
- **発音練習**: 科学プレゼンテーションスキル向上
- **言語間比較**: 各言語の表現の違いと共通点の発見
- **視聴覚学習**: 動的ハイライトによる読み上げ箇所の視覚的確認
- **集中力向上**: リアルタイム文字追跡による集中的な学習体験

## 📄 ライセンス

このプロジェクトは教育目的で作成されました。コンテンツの再利用や改変は自由に行えます。

---

*「量子世界の神秘と日常の物理学を結ぶ架け橋」- Multilingual Podcast Reader*
