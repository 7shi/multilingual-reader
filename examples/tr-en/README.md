# examples/tr-en/

英語原文からドイツ語・日本語・中国語への翻訳を行い、`examples/` の参照訳を更新するためのディレクトリ。

## 前提

- `examples/` の英語ファイル（`*-en.txt`）が `examples/tr-fr/` の結果で置き換え済みであること
- `examples/terms/*-en.{json,tsv}` が最新の英語ファイルをもとに再生成・校正済みであること（`examples/terms/batch.sh` で生成）

## フロー

1. `make` で翻訳を実行（`tr/` に出力）
2. 翻訳結果を添削
3. `examples/` の該当ファイルを置き換え

評価が必要な場合は `--eval-runs 3` を `Makefile` に追加して `make` を再実行する（`evals/` に JSON、`SCORES.txt` にスコアを出力）。

## 実行

```bash
make
```

- 翻訳モデル: gemma4-26b
- 設定: threshold=20・keep=5・CoT なし・用語ファイル注入（`../terms/*-en.{json,tsv}`）
- 既存ファイルはスキップされるため途中再開可能
- threshold=20 は 26B モデルで問題ないことを確認済み（tr-fr の threshold=10 より広いコンテキストを保持）

ベース言語は ドイツ語 (de), 日本語 (ja) , 中国語 (zh)。onde のみ以下の言語が追加:

- エスペラント (eo), ヒンディー語 (hi), テルグ語 (te), カンナダ語 (kn), トルコ語 (tr), エストニア語 (et), セルビア語 (sr)

個別に実行する場合は `make others` または `make onde`。
