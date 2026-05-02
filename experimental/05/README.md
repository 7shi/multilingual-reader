# trtools translate を用いた翻訳実験

[experimental/04](../04/) の用語事前抽出方式を踏襲しつつ、翻訳スクリプトを `trtools translate` に移行した実験ディレクトリです。

## 背景と動機

experimental/04 では用語抽出・訳語確定・翻訳が一体化したスクリプトでしたが、用語 TSV の校正ワークフロー（抽出 → 人手確認・編集 → 翻訳）を確立するため `trtools term extract/translate` として分離しました。

experimental/05 では:

- **用語は事前に `trtools term` で抽出・校正済み**（`examples/terms/finetuning-fr.tsv`）
- **翻訳は `trtools translate` で実行**（共有用語ファイルを参照）
- experimental/04 と同一の threshold=10・keep=5・CoT なし設定

これにより、複数の翻訳 run が同じ校正済み用語辞書を共有するため、run 間の用語ブレ（`affinage` → `refinamiento` / `ajuste fino` のような揺れ）を原理的に排除できます。

## 翻訳システム

### trtools translate

```bash
uv run trtools translate <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**主要オプション:**

| オプション | 値 | 説明 |
|---|---|---|
| `--threshold` | 10 | 要約生成の間隔（行数） |
| `--keep` | 5 | 圧縮後に保持する翻訳ペア数 |
| `--no-think` | （フラグ） | CoT 無効化（翻訳品質への影響なし、速度向上） |
| `--terms-json` | `examples/terms/finetuning-fr.json` | 用語チャンクマップ |
| `--terms-tsv` | `examples/terms/finetuning-fr.tsv` | 用語訳語対応表 |

### 用語ファイル

`examples/terms/finetuning-fr.tsv` は `trtools term extract/translate` で生成・校正済みの TSV。
全 run が同じ用語辞書を共有するため、run 間の用語ブレが発生しない。

| 言語 | 列 |
|---|---|
| French（原語） | 列1 |
| English | 列2 |
| Spanish（翻訳先） | 列3 |

### batch.sh

```bash
bash batch.sh
```

MODELS.txt の2モデル（gemma4-26b、gemma4-e4b）について **翻訳3回 × 評価3回** を実行します。

**ファイル命名:**

```
tr/<model>-<trrun>.txt              例: tr/gemma4-26b-1.txt
evals/<model>-<trrun>-eval-<evrun>.json
```

experimental/04 と異なり、tr/ に `-terms.json` ファイルは生成されません（用語は共有ファイルを使用）。

## 対象モデル

experimental/03 や experimental/04 と同じ2モデル。

| モデル | experimental/04 スコア | 選定理由 |
|---|:---:|---|
| gemma4-26b | 96 / 96 / 99 | 全 run で急落なし、最安定 |
| gemma4-e4b | 95 / 96 / 92 | リソース制約がある場合の代替 |

## 評価システム

experimental/04 と同じパイプライン。

- 評価者: `ollama:qwen3.6`
- 5項目 × 20点 = 100点満点
- 集計: 3回評価の中央値

## 試行

| 試行 | threshold | 結果 |
|---|:---:|---|
| [tr/](tr/) | 10 | gemma4-26b: 95/96/97、gemma4-e4b: 95/95/94 |

## 比較結果

experimental/04（run ごとに用語抽出）との比較（差分: 用語辞書の共有有無のみ）:

| モデル | experimental/04 | experimental/05 |
|---|:---:|:---:|
| gemma4-26b run 1 | 96 | 95 |
| gemma4-26b run 2 | 96 | 96 |
| gemma4-26b run 3 | 99 | 97 |
| gemma4-e4b run 1 | 95 | 95 |
| gemma4-e4b run 2 | 96 | 95 |
| gemma4-e4b run 3 | **92**（急落） | 94 |

**観察:**

- **gemma4-e4b の急落が解消**: 92点 → 94点。急落なし。共有用語辞書により run 間の用語ブレが排除された効果が確認できた
- **gemma4-26b**: 上限が 99→97 に微減したが、95〜97 の範囲で安定維持
- **全体**: 両モデルとも 94〜97 の範囲に収束。qwen3.6 評価者の実質上限（97点）を踏まえると、校正済み共有用語辞書は安定性向上に寄与している

## 減点分析

評価ログ全18件（各モデル9件）を分析した結果。

### gemma4-26b（9件）

| 項目 | 平均 | 最低 |
|---|:---:|:---:|
| information_completeness | 19.89 | 19 |
| contextual_adaptation | 19.22 | 19 |
| terminology | 19.44 | 18 |
| readability | 18.89 | 18 |
| fluency | 18.67 | 17 |

**減点パターン:**
- `antisèche`（カンニングペーパー）の訳が `acordeón` — 地域によっては通じるが普遍的でない（`chuleta` が推奨）。用語辞書に含めていないため run によって揺れる
- fluency の -3 点（run 1 eval-2）は `acordeón` およびわずかな不自然な表現の組み合わせ
- 構造的欠陥はなし

### gemma4-e4b（9件）

| 項目 | 平均 | 最低 |
|---|:---:|:---:|
| terminology | 19.11 | 18 |
| readability | 18.78 | 18 |
| fluency | 18.33 | 17 |
| contextual_adaptation | 18.78 | 17 |
| information_completeness | 19.44 | 18 |

**減点パターン:**
- **run 2**: 二人称の不統一（`Vean más bien: usted no le enseñaría...` — 同一文内で ustedes 命令形と usted 単数形が混在）。地域変種（ラテンアメリカ vs. スペイン）を明示しないとモデルが揺れる
- **run 3**: 発言者ラベルの消失（`Camille: Elle oublie tout.` → `Olvida todo.`）および `antisèche → sinopsis`（「あらすじ」への誤訳）が重なり、評価者 1回が readability・contextual_adaptation・information_completeness の複数項目で計 7点減点。ただし 3回中 2回（eval-1・eval-3）は見落とし（93〜94点）

### まとめ

gemma4-26b の減点はほぼ `antisèche` の訳語選択という単一の様式的問題に収束しており、構造的欠陥はない。gemma4-e4b はリソース制約がある環境向けの代替として割り切って使う位置付けであり、run によっては発言者消失や人称不統一といった軽微な構造的問題が出る点を許容する。gemma4-26b が利用できる場合は引き続き第一推奨。
