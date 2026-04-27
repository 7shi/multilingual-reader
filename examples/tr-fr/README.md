# examples/tr-fr/

フランス語原文から英語・スペイン語への翻訳を行い、`examples/` の参照訳を更新するためのディレクトリ。

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
- 対象: finetuning・transformer・onde・momentum × FR→EN・FR→ES
- 設定: threshold=10・keep=5・CoT なし・用語ファイル注入（`../terms/*-fr.{json,tsv}`）
- 既存ファイルはスキップされるため途中再開可能
