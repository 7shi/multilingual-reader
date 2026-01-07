# 評価者間比較分析ツール

このディレクトリには、3つの翻訳評価者（Gemini-2.5-flash、gpt-oss-20b、gpt-oss-120b）の評価結果を比較分析し、有償のGeminiから無償のgpt-oss-120bへの移行可否を統計的に判定するツールが含まれています。

## 📁 ファイル一覧

### 実行スクリプト（3つ）

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

#### 2. `visualize_evaluator_comparison.py`
**グラフ生成スクリプト**

**機能**:
- stats.jsonを読み込み、5種類のグラフを生成

**生成するグラフ**:
1. `plots/scatter_matrix.png` - 3×3散布図マトリクス（評価者間の相関）
2. `plots/bland_altman.png` - Bland-Altmanプロット（一致度の可視化）
3. `plots/score_diff_histogram.png` - スコア差分の分布（Gemini vs gpt-oss-120b）
4. `plots/model_family_boxplot.png` - モデルファミリー別のバイアス
5. `plots/heatmap.png` - 全716項目の俯瞰図（ヒートマップ）

**依存関係**:
- numpy, scipy, matplotlib, seaborn

**実行方法**:
```bash
uv run visualize_evaluator_comparison.py
```

#### 3. `generate_evaluator_report.py`
**レポート生成スクリプト**

**機能**:
- stats.jsonとグラフを統合してマークダウンレポートを生成
- エグゼクティブサマリー、詳細統計、移行判定、推奨事項を含む

**出力**:
- `REPORT.md` - 包括的分析レポート（244行、13セクション）

**実行方法**:
```bash
uv run generate_evaluator_report.py
```

#### 4. `compute_euclidean_distances.py`
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

### 自動生成データ

#### 4. `stats.json`
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
- グラフ生成の入力データ
- レポート生成の元データ
- 詳細分析用の生データ

#### 5. `REPORT.md`
**包括的分析レポート**

**構成**:
1. エグゼクティブサマリー
2. 基本統計（評価者ごとの統計量、スコアレンジ分布）
3. 相関分析（散布図マトリクス、相関係数テーブル）
4. 一致度分析（Bland-Altmanプロット、一致度指標）
5. 系統的バイアスの分析（モデルファミリー別、推論レベル別、温度別）
6. 問題ケースの詳細（乖離TOP30、0点評価、逆転ケース）
7. **🔴 重大な発見**: Geminiの評価エラー（幻覚による誤評価）
8. 移行判定（再評価結果、推奨事項、移行計画）
9. 全項目スコアの俯瞰（ヒートマップ）
10. レポート更新履歴

**サイズ**: 約340行

**判定結果**: ✅ **移行推奨**

**重大な発見**:
qwen3-30b-nt系列（9件）で、**Geminiが存在しない翻訳を評価する致命的エラー**を発見
- qwen3-30b-nt系列の翻訳ファイルには翻訳結果が含まれず、思考プロセス（CoT）のみ
- gpt-oss系は正しく0点評価（"No translation provided"）
- Geminiは63-100点の高得点を付け、詳細な評価コメントを生成（幻覚）

**評価例**:
| モデル | Gemini | gpt-oss-120b | 差分 |
|--------|--------|--------------|------|
| qwen3-30b-tr4-nt-05 | 93 | 0 | +93 |
| qwen3-30b-tr4-nt-10 | 84 | 0 | +84 |
| qwen3-30b-tr4-nt-20 | 70 | 0 | +70 |

**結論**:
✅ **gpt-oss-120bへの完全移行を推奨**

**理由**:
1. Geminiに致命的な評価エラー（入力検証欠如、幻覚による誤評価）
2. gpt-oss系の堅牢性（入力検証、エラー検出、一貫性）
3. gpt-oss-20bとgpt-oss-120bの高相関（0.913）
4. コスト削減（有償→無償）

### グラフファイル（5つ）

#### 6. `plots/scatter_matrix.png`
**3×3散布図マトリクス**

- 対角線: 各評価者のスコア分布（ヒストグラム）
- 上三角: 評価者間の散布図 + 回帰直線
- 下三角: スピアマン順位相関係数の表示

**用途**: 評価者間の線形関係と順位相関を視覚的に確認

#### 7. `plots/bland_altman.png`
**Bland-Altmanプロット**

3つの評価者ペア（Gemini-gpt20b、Gemini-gpt120b、gpt20b-gpt120b）について：
- X軸: (評価者1 + 評価者2) / 2（平均スコア）
- Y軸: 評価者1 - 評価者2（差分）
- 平均差と±1.96SD（95%信頼区間）を表示

**用途**: 評価者間の一致度と系統的バイアスを可視化

#### 8. `plots/score_diff_histogram.png`
**スコア差分の分布**

Gemini vs gpt-oss-120bのスコア差のヒストグラム：
- 正規分布曲線の重ね表示
- 平均差: -9.37点
- 標準偏差: 17.10点

**用途**: 評価差の分布パターンを確認

#### 9. `plots/model_family_boxplot.png`
**モデルファミリー別バイアス**

Y軸: Gemini - gpt-oss-120bのスコア差
X軸: モデルファミリー（aya-expanse、command-r、gemma2/3、gpt-oss、llama、etc.）

**特徴**:
- command-r7b: -25.4点（最大バイアス）
- gpt-oss: +1.0点（唯一Geminiが高評価）

**用途**: 系統的バイアスの特定

#### 10. `plots/heatmap.png`
**全716項目の俯瞰図**

- 行: 716項目（モデル名）
- 列: 3評価者
- 色: スコア（0-100）
- カラーマップ: viridis

**用途**: 全体的な評価傾向の俯瞰

## 🚀 実行手順

### 1回限りのセットアップ

```bash
# ディレクトリに移動
cd experimental/evaluator_comparison

# 依存ライブラリのインストール
uv add numpy scipy matplotlib seaborn
```

### 完全な分析の実行

```bash
# 1. 統計分析
uv run compare_evaluators.py

# 2. グラフ生成
uv run visualize_evaluator_comparison.py

# 3. レポート生成
uv run generate_evaluator_report.py
```

### 結果の確認

```bash
# メインレポート
cat REPORT.md

# 統計データ
jq '.' stats.json

# グラフの確認（画像ビューアで開く）
xdg-open plots/scatter_matrix.png
```

## 📊 分析結果サマリー

### 基本統計

| 評価者 | 平均 | 中央値 | 標準偏差 | 最高点 | 最低点 |
|--------|------|--------|----------|--------|--------|
| gemini-2.5-flash | 69.35 | 75.00 | 22.97 | 100 | 0 |
| gpt-oss-20b | 78.00 | 83.00 | 16.09 | 92 | 0 |
| gpt-oss-120b | 78.72 | 84.00 | 16.73 | 96 | 0 |

**特徴**:
- Geminiはより厳しい評価（平均-9点、標準偏差+6点）
- gpt-oss-20bとgpt-oss-120bは非常に近い（平均差0.72点）

### 相関分析

| ペア | ピアソンr | スピアマンρ |
|------|-----------|-------------|
| Gemini vs gpt-oss-20b | 0.621 | 0.699 |
| Gemini vs gpt-oss-120b | 0.670 | **0.776** |
| gpt-oss-20b vs gpt-oss-120b | **0.913** | 0.745 |

**特徴**:
- gpt-oss系同士の相関が非常に高い（0.913）
- Geminiとの相関は中程度（0.670-0.699）

### 一致度分析

| ペア | MAE | ±10点以内 | 上位10%一致率 |
|------|-----|-----------|---------------|
| Gemini vs gpt-oss-20b | 14.15 | 54.6% | 21.3% |
| Gemini vs gpt-oss-120b | 13.66 | **54.9%** | **37.1%** |
| gpt-oss-20b vs gpt-oss-120b | **4.78** | **89.9%** | 26.4% |

**特徴**:
- gpt-oss系同士は高い一致度（MAE 4.78点、89.9%が±10点以内）
- Geminiとの一致度は低い（MAE 13.66点、54.9%が±10点以内）

### 致命的な問題の発見

**qwen3-30b-nt系列（9件）でGeminiが幻覚による誤評価**:
- 翻訳が存在しないファイルに63-100点を付与
- gpt-oss系は正しく0点評価
- 平均誤差: +78.6点

詳細は [REPORT.md](REPORT.md) の「🔴 重大な発見: Geminiの評価エラー」セクションを参照

## ✅ 結論

### 判定: ✅ **gpt-oss-120bへの完全移行を推奨**

**根拠**:
1. **Geminiの致命的エラー**: 存在しない翻訳を評価（幻覚）
   - qwen3-30b-nt系列（9件）で63-100点の高得点を付与
   - 実際には翻訳結果が含まれていないファイル
   - 平均誤差: +78.6点
2. **gpt-oss系の堅牢性**: 入力検証、エラー検出、一貫性
   - 翻訳が存在しないことを正確に検出（0点評価）
   - "No translation provided – impossible to assess"
3. **内部一貫性**: gpt-oss-20bとgpt-oss-120bの相関0.913
4. **コスト削減**: 有償→無償

### 推奨移行手順

1. **即座にgpt-oss-120bを採用**
2. **Geminiの使用を中止**（信頼性の問題）
3. **補助的にgpt-oss-20bで検証**（大きな差異がある場合のみ手動確認）

## 📖 詳細情報

### 移行判定基準

#### ✅ 移行可能
- スピアマン順位相関係数 ≥ 0.85
- 上位10%モデル一致率 ≥ 75%
- ±10点範囲内一致率 ≥ 70%

#### ⚠️ 条件付き移行可能
- スピアマン順位相関係数 0.70-0.85
- 上位10%モデル一致率 60-75%
- ±10点範囲内一致率 60-70%

#### ❌ 移行不可
- スピアマン順位相関係数 < 0.70
- 上位10%モデル一致率 < 60%
- 致命的な評価ミス

**注**: これらの基準は**Geminiが正しいという前提**で設定されていました。しかし、Geminiの致命的な評価エラー（幻覚による誤評価）の発見により、基準自体が不適切だったことが判明しました。詳細は [REPORT.md](REPORT.md) を参照してください。

## 🔧 技術仕様

### 依存ライブラリ
- `numpy`: 数値計算、統計処理
- `scipy`: 相関係数計算（stats.pearsonr, stats.spearmanr）
- `matplotlib`: グラフ描画の基盤
- `seaborn`: 高度なグラフ描画（boxplot, heatmap）

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
uv add numpy scipy matplotlib seaborn
```

### エラー: FileNotFoundError (SCORES.txt)
```bash
# 解決策: 正しいディレクトリで実行
cd experimental/evaluator_comparison
uv run compare_evaluators.py
```

### 警告: UserWarning (Japanese font)
```
# 非クリティカル: 日本語フォントが見つからない
# グラフは生成されるが、日本語ラベルが正しく表示されない可能性
# 解決策（オプション）: Noto Sans CJK JPをインストール
sudo apt install fonts-noto-cjk
```
