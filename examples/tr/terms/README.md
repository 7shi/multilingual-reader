# examples/tr/terms/

`examples/` の翻訳で使用する用語ファイル（JSON・TSV）を格納するディレクトリ。`trtools term extract/translate` で生成し、校正済みのものを保管する。

## ファイル構成

| ファイル | 内容 |
|---|---|
| `common.mk` | `onde-en.tsv` の追加言語 `EXTRA_LANGS` を定義 |
| `common.tsv` | 全トピック共通の固有名詞（番組名など）。LLM をスキップして訳語を固定する |
| `{topic}-fr.json` | フランス語原文から抽出した用語チャンクマップ（FR→EN, FR→ES 翻訳用） |
| `{topic}-fr.tsv` | フランス語用語の English・Spanish 訳語対応表 |
| `{topic}-en.json` | 英語原文から抽出した用語チャンクマップ（EN→DE, EN→JA, EN→ZH 翻訳用） |
| `{topic}-en.tsv` | 英語用語の German, Japanese, Chinese 訳語対応表 |

## 生成・更新

```bash
make
```

生成後は TSV を校正すること。LLM はスラッシュ2択・誤訳・余分テキスト混入・誤字などを出力することがある（詳細は [MEMO.md](../../MEMO.md) 参照）。

## 実行上の注意

- `trtools term set` は TSV を直接更新するため、**同じファイルに対して並列実行しないこと**。`show` / `set` / 再確認は必ず逐次実行する。
- `trtools term show common.tsv -l xx` で列が存在しない場合は、警告付きで `English` 列だけが表示される。これは「その言語列が未作成」であることを意味する。

## TSV の校正手順

列数が多いため、**必ず言語を1つずつ独立したタスクとして分けて**確認・修正すること。

`common.tsv` を校正する場合の追加事項：
- タイトル "Tech Flash", "Bridges in Physics" は翻訳対象とする。
- 人名 "Camille", "Luc" は固有文字を使用する言語では転写する。

### 1. 言語を絞り込んで表示

```bash
# 特定言語列のみ表示（LLM にペーストして確認する場合にも有用）
uv run trtools term show onde-en.tsv -l ja
```

### 2. 問題のあるセルを修正

```bash
uv run trtools term set onde-en.tsv -k "physics" -l ja -v "物理学"
```

`-k` はキー（第1列の値）、`-l` は言語コード（例: `ja`）、`-v` は修正後の値を指定する。

### 3. 修正結果を確認

```bash
uv run trtools term show onde-en.tsv -l ja -k physics
```

## 翻訳での使用

```bash
uv run trtools translate input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma4:26b \
  --terms-json {topic}-fr.json \
  --terms-tsv {topic}-fr.tsv
```

`trtools batch` では `--terms-dir` オプションでこのディレクトリを指定する。
