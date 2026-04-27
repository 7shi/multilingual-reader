# examples/terms/

`examples/` の翻訳で使用する用語ファイル（JSON・TSV）を格納するディレクトリ。`trtools term extract/translate` で生成し、校正済みのものを保管する。

## ファイル構成

| ファイル | 内容 |
|---|---|
| `common.tsv` | 全トピック共通の固有名詞（番組名など）。LLM をスキップして訳語を固定する |
| `{topic}-fr.json` | フランス語原文から抽出した用語チャンクマップ（FR→EN・FR→ES 翻訳用） |
| `{topic}-fr.tsv` | フランス語用語の English・Spanish 訳語対応表 |
| `{topic}-en.json` | 英語原文から抽出した用語チャンクマップ（EN→DE・EN→JA・EN→ZH 翻訳用） |
| `{topic}-en.tsv` | 英語用語の German・Japanese・Chinese 訳語対応表（onde のみ Esperanto・Hindi も含む） |

## 生成・更新

```bash
bash batch.sh
```

生成後は TSV を校正すること。LLM はスラッシュ2択・誤訳・余分テキスト混入・誤字などを出力することがある（詳細は [MEMO.md](../../MEMO.md) 参照）。

## 翻訳での使用

```bash
uv run trtools translate input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma4:26b \
  --terms-json {topic}-fr.json \
  --terms-tsv {topic}-fr.tsv
```

`trtools batch` では `--terms-dir` オプションでこのディレクトリを指定する。
