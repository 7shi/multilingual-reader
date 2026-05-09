# 実験10: trtools review の動作検証

実験07・09で確立した他者評価アプローチ（`review.py`）を `trtools` のサブコマンドとして統合した後、ブルガリア語1言語で translate → eval → review → eval のフルパイプラインを動作検証する。

## 目的

- `trtools review` サブコマンドの実装検証
- `translate`・`eval`・`review` を通じた `StatusLine`（Rich プログレスバー）の統合表示確認
- ブルガリア語を対象に推敲前後のスコアを比較

## フロー

1. **翻訳**: `trtools translate`（gemma4:26b、`--threshold 20`、用語注入あり）→ `tr/onde-bg.txt`
2. **翻訳評価 × 3**: `trtools eval`（qwen3.6）→ `evals/onde-bg-{1,2,3}.json`
3. **推敲**: `trtools review`（qwen3.6、`--no-think`）→ `tr/onde-bg-rev.txt`
4. **推敲後評価 × 3**: `trtools eval`（qwen3.6）→ `evals/onde-bg-rev-{1,2,3}.json`

## 結果

| フェーズ | スコア |
|---|---|
| ベース翻訳 | 88/100点 |
| 推敲後 | 87/100点 |

実行時間: 約38分（37m57.938s）

## 考察

ベーススコア88点と既に高水準であったため、推敲で1点の微減となった。実験09のブルガリア語はベース80点→推敲後97点（+17点）と大幅改善しているが、これはベーススコアが中程度（80点台）だったことが推敲効果の前提になっていたと考えられる。実験09の知見（推敲前スコアが高い言語では余計な変更で品質が低下する傾向）と整合する結果である。

`trtools review` サブコマンドおよびプログレスバー統合は正常に動作することを確認した。
