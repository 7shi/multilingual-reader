# 実験10: trtools review の動作検証

実験07・09で確立した他者評価アプローチ（`review.py`）を `trtools` のサブコマンドとして統合した後、実験09で推敲効果が高かった5言語（bg・eu・et・sl・hu）で translate → eval → review → eval のフルパイプラインを動作検証する。

## 目的

- `trtools review` サブコマンドの実装検証
- `translate`・`eval`・`review` を通じた `StatusLine`（Rich プログレスバー）の統合表示確認
- 推敲前後のスコアを比較

## フロー

1. **翻訳**: `trtools translate`（gemma4:26b、`--threshold 20`、用語注入あり）→ `tr/onde-{lang}.txt`
2. **翻訳評価 × 3**: `trtools eval`（qwen3.6）→ `evals/onde-{lang}-{1,2,3}.json`
3. **推敲**: `trtools review`（qwen3.6、`--no-think`）→ `tr-rev/onde-{lang}.txt`
4. **推敲後評価 × 3**: `trtools eval`（qwen3.6）→ `evals-rev/onde-{lang}-{1,2,3}.json`

## 結果

| 言語 | ベース翻訳 | 推敲後 | 差分 |
|---|---|---|---|
| bg: Bulgarian | 88 | 87 | -1 |
| et: Estonian  | 30 | 51 | +21 |
| eu: Basque    | 17 | 59 | +42 |
| hu: Hungarian | 26 | 89 | +63 |
| sl: Slovene   | 56 | 83 | +27 |

実行時間: 約3時間半（bg: 37m57.938s、eu・et・sl・hu: 172m9.014s）

## 考察

実験10のベーススコアは実験09より全体的に低い。実験09ではモデルを言語ごとに最適選択していたのに対し、実験10は gemma4:26b に統一しているため、中リソース言語では翻訳品質が低下している。

推敲による改善は eu (+42)・hu (+63)・sl (+27)・et (+21) で大きく、ベーススコアが低くても推敲が有効に機能することを確認した。ただし推敲後の最終スコアは実験09（eu: 87、hu: 96、sl: 95、et: 82）に届いていない。

bg はベース88点と高水準だったため推敲で微減（-1）となった。実験09の知見（推敲前スコアが高い言語では余計な変更で品質が低下する傾向）と整合する結果である。

`trtools review` サブコマンドおよびプログレスバー統合は正常に動作することを確認した。
