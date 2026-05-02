# 評価者間比較分析ツール

このディレクトリには、3つの翻訳評価者（Gemini-2.5-flash、gpt-oss-20b、gpt-oss-120b）の評価結果を比較分析するツールが含まれています。

## 📁 ファイル一覧

### 実行スクリプト（4つ）

#### 1. `compare_evaluators.py`
**統計分析スクリプト**

**機能**:
- 3つの評価者のSCORES.txtを読み込み
- 基本統計量の算出（平均、中央値、標準偏差）
- 相関分析（ピアソン、スピアマン順位相関）
- 一致度分析（MAE、RMSE、±5/10点範囲内一致率）
- モデルファミリー別・推論レベル別・温度別の系統的バイアス検出
- 問題ケースの抽出（乖離TOP30、0点評価、逆転ケース）
- 移行判定の自動実行

**入力**:
- `../gemini-2.5-flash/SCORES.txt` (716項目)
- `../gpt-oss-20b/SCORES.txt` (716項目)
- `../gpt-oss-120b/SCORES.txt` (716項目)

**出力**:
- `stats.json` - 詳細統計データ（JSON形式）

**実行方法**:
```bash
cd evaluator_comparison
uv run compare_evaluators.py
```

#### 2. `generate_evaluator_report.py`
**レポート生成スクリプト**

**機能**:
- stats.jsonからマークダウンレポートを生成
- エグゼクティブサマリー、詳細統計、移行判定、推奨事項を含む

**出力**:
- `REPORT.md` - 包括的分析レポート（244行、13セクション）

**実行方法**:
```bash
uv run generate_evaluator_report.py
```

#### 3. `compute_euclidean_distances.py`
**距離マトリクス生成スクリプト**

**機能**:
- 3つの評価者のSCORES.txtを読み込み
- 各評価者ペアのユークリッド距離と次元あたりRMSEを計算
- 対角より上を空欄とした下三角マトリクス形式で `DISTANCES.md` を生成

**出力**:
- `DISTANCES.md` - ユークリッド距離＆RMSEマトリクス

**実行方法**:
```bash
uv run compute_euclidean_distances.py
```

#### 4. `analyze_eval_variance.py`
**評価変動分析スクリプト**

**機能**:
- 評価者ごとの3回評価内変動を定量化
- 平均レンジ、σ統計、観点別変動を算出

**実行方法**:
```bash
cd evaluator_comparison
python analyze_eval_variance.py [評価者ID ...]
# 例: python analyze_eval_variance.py gpt-oss-120b gemma-4-31b gemini-2.5-flash
```

### 自動生成データ

#### 3. `stats.json`
**詳細統計データ（JSON形式）**

**内容**:
- メタデータ（716項目、3評価者、生成日時）
- 基本統計量（各評価者の平均、中央値、標準偏差、スコアレンジ分布）
- 相関分析（ピアソンr、スピアマンρ、p値）
- 一致度指標（MAE、RMSE、±5/10点一致率、上位10%一致率）
- 系統的バイアス（モデルファミリー別、推論レベル別、温度別）
- 問題ケース（乖離TOP30、0点評価リスト、逆転ケース）
- 移行判定結果（判定、スコア、理由）

**サイズ**: 約50KB

**利用目的**:
- レポート生成の元データ
- 詳細分析用の生データ

#### 4. `REPORT.md`
**包括的分析レポート（自動生成）**

- `stats.json` を元に `generate_evaluator_report.py` で自動生成
- エグゼクティブサマリー、基本統計、相関分析、一致度分析、系統的バイアス、問題ケース、移行判定を含む

評価者選定の経緯は [memo/evaluators.md](../memo/evaluators.md) を参照。

## 🚀 実行手順

### 1回限りのセットアップ

```bash
# ディレクトリに移動
cd experimental/01/evaluator_comparison

# 依存ライブラリのインストール
uv add numpy scipy
```

### 完全な分析の実行

```bash
# 1. 統計分析
uv run compare_evaluators.py

# 2. レポート生成
uv run generate_evaluator_report.py
```

### 結果の確認

```bash
# メインレポート
cat REPORT.md

# 統計データ
jq '.' stats.json
```

## 📊 確定結果

### 評価者選定の結論

**qwen3.6 を正式評価者として採用（単独運用）**。

| 評価者 | 結論 |
|--------|------|
| **qwen3.6** | **正式評価者に採用。中央値で全716件をランキング** |
| gemma-4-31b | 一次フィルターとしても不要。廃止 |
| gpt-oss-120b | 天井効果あり。廃止 |
| gemini-2.5-flash | 不安定。廃止 |

### 評価者別スコア分布（qwen3.6 採用判定時点）

| 指標 | GPT-OSS 120B | gemma-4-31b | qwen3.6 |
|------|-------------|-------------|---------|
| 平均 | 78.61点 | 76.28点 | 66.92点 |
| 標準偏差 | 16.90点 | 24.30点 | 25.98点 |
| 最高点 | 92点 | 100点 | 98点 |
| 90点以上 | 0% | 37.6% | 23.7% |
| 95点以上 | 0% | 27.2% | 8.1% |
| 100点 | 0件 | 13件 | 0件 |

### 評価者の特性

| 評価者 | 強み | 弱点 |
|--------|------|------|
| gemma-4-31b | 破綻テキストの確実な検出 | 固有名詞誤訳・未翻訳・術語誤りを見逃す |
| gpt-oss-120b | 中程度の内容チェック | CoT を無効化できない（→ [memo/README.md](../memo/README.md)「GPT-OSS 120B の特性と活用方針」） |
| gemini-2.5-flash | 内容エラーの検出力は高い | 同一翻訳への評価が3回で大きくばらつく |
| qwen3.6 | CoT による論理的な欠陥特定 | 平均レンジ14.11点（最大）だが大半は孤立型外れ値で中央値に影響しない |

### 安定性と精度

| 評価者 | 安定性 | 精度 |
|--------|:------:|:----:|
| gemma-4-31b | ◎ | △（内容エラー見逃し） |
| GPT-OSS 120B | ○ | △（天井効果・MoE判断力） |
| gemini-2.5-flash | ✕ | ○（内容エラー検出力高） |

### モデル別最高スコアランキング（qwen3.6・中〜大型）

| ランク | モデル | 最高点 | 最良設定 | 備考 |
|--------|--------|------:|---------|------|
| 1 | gemma3-27b | 98 | 設定0 | tr4/tr5 でも97点・非常に安定 |
| 1 | gpt-oss-120b | 98 | 設定0 | 複数設定で96点・最も安定 |
| 3 | aya-expanse-32b | 97 | tr4 | 設定0で95点 |
| 4 | command-r-35b | 96 | tr4 | 設定0で93点 |
| 4 | ministral-3-8b | 96 | 設定0 | 設定2で95点 |
| 4 | mistral-small3.2 | 96 | tr4 | 複数設定で94-95点・安定 |
| 4 | qwen3-30b | 96 | 設定1, 1-nt | tr系（非構造化）は全0点 |
| 4 | qwen3-32b | 96 | tr4 | 設定3-nt/4 で95点 |
| 9 | gpt-oss-20b | 95 | 設定1,4 | 複数設定で安定 |
| 9 | gemma3-12b | 95 | 設定0 | 設定1で壊滅（11点）|
| 9 | llama3.3 | 95 | 設定0, tr4 | tr6で94点 |
| 9 | llama4-scout | 95 | 設定0 | tr5で94点、設定2以降は低い |
| 9 | ministral-3-14b | 95 | 設定0, tr5 | 設定1以降は不安定 |
| 9 | qwen3-14b | 95 | 設定4, 3 | 設定別のばらつきが大きい |

### 設定タイプ別スコア統計

| 設定 | 件数 | 中央値 | 最高 | 評価 |
|------|-----:|------:|-----:|------|
| 設定0（tr0） | 123 | 83.0 | 98 | ◎ 基本設定として最安定 |
| 設定2-nt | 18 | 83.5 | 95 | ◎ |
| 設定0-nt | 23 | 78.0 | 95 | ○ |
| tr4 | 96 | 78.5 | 97 | ○ 上位モデルで高スコア |
| 設定2 | 98 | 77.0 | 96 | ○ |
| tr5 | 72 | 75.0 | 97 | △ ばらつき大 |
| tr6 | 72 | 71.5 | 96 | △ ばらつき大 |
| 設定1（推論付き構造化） | 98 | 59.0 | 96 | ✗ 大部分のモデルで逆効果 |

分析の経緯は [memo/evaluators.md](../memo/evaluators.md) を参照。

## 🔧 技術仕様

### 依存ライブラリ
- `numpy`: 数値計算、統計処理
- `scipy`: 相関係数計算（stats.pearsonr, stats.spearmanr）

### データフォーマット

#### SCORES.txt形式
```
1→aya-expanse-8b-0-05: 88/100点
2→aya-expanse-8b-0-10: 70/100点
...
```

#### stats.json形式
```json
{
  "metadata": {
    "num_entries": 716,
    "evaluators": ["gemini-2.5-flash", "gpt-oss-20b", "gpt-oss-120b"],
    "generated_at": "2026-01-07 15:21:16"
  },
  "basic_stats": { ... },
  "correlations": { ... },
  "agreement": { ... },
  "systematic_bias": { ... },
  "problem_cases": { ... },
  "migration_decision": { ... }
}
```

## 📚 関連ドキュメント

- [../README.md](../README.md) - 実験全体の概要
- [REPORT.md](REPORT.md) - 包括的分析レポート
- [stats.json](stats.json) - 詳細統計データ

## トラブルシューティング

### エラー: ModuleNotFoundError
```bash
# 解決策: 依存ライブラリをインストール
uv add numpy scipy
```

### エラー: FileNotFoundError (SCORES.txt)
```bash
# 解決策: 正しいディレクトリで実行
cd experimental/01/evaluator_comparison
uv run compare_evaluators.py
```
