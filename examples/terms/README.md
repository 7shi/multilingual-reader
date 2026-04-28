# examples/terms/

`examples/` の翻訳で使用する用語ファイル（JSON・TSV）を格納するディレクトリ。`trtools term extract/translate` で生成し、校正済みのものを保管する。

## ファイル構成

| ファイル | 内容 |
|---|---|
| `common.tsv` | 全トピック共通の固有名詞（番組名など）。LLM をスキップして訳語を固定する |
| `{topic}-fr.json` | フランス語原文から抽出した用語チャンクマップ（FR→EN, FR→ES 翻訳用） |
| `{topic}-fr.tsv` | フランス語用語の English・Spanish 訳語対応表 |
| `{topic}-en.json` | 英語原文から抽出した用語チャンクマップ（EN→DE, EN→JA, EN→ZH 翻訳用） |
| `{topic}-en.tsv` | 英語用語の German, Japanese, Chinese 訳語対応表 |

`onde-en.tsv` のみ追加言語の訳語を含む:
Esperanto, Hindi, Telugu, Kannada, Turkish, Estonian, Serbian

## 生成・更新

```bash
bash batch.sh
```

生成後は TSV を校正すること。LLM はスラッシュ2択・誤訳・余分テキスト混入・誤字などを出力することがある（詳細は [MEMO.md](../../MEMO.md) 参照）。

## TSV の校正手順

列数が多いため、言語を1つずつ絞り込んで確認・修正する。

### 1. 言語を絞り込んで表示

```bash
# 特定言語列のみ表示（LLM にペーストして確認する場合にも有用）
uv run trtools term show onde-en.tsv -l Japanese

# 複数言語を並べて比較
uv run trtools term show onde-en.tsv -l Japanese -l German
```

### 2. 問題のあるセルを修正

```bash
uv run trtools term set onde-en.tsv -k "physics" -l Japanese -v "物理学"
```

`-k` はキー（第1列の値）、`-l` は言語列名、`-v` は修正後の値を指定する。

### 3. 修正結果を確認

```bash
uv run trtools term show onde-en.tsv -l Japanese -k physics
```

## 翻訳での使用

```bash
uv run trtools translate input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma4:26b \
  --terms-json {topic}-fr.json \
  --terms-tsv {topic}-fr.tsv
```

`trtools batch` では `--terms-dir` オプションでこのディレクトリを指定する。
