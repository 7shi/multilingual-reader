# trtools リファレンス

翻訳・評価・用語管理を一括で行うコマンドラインツール集。

```
uv run trtools [--label LABEL] [--start START] <command> [options]
```

---

## メインオプション

どのサブコマンドでも共通して使用できるオプション。プログレスバーの表示制御に使う。

| オプション | 説明 |
|---|---|
| `--label LABEL` | プログレスバーに表示するラベル文字列（例: `bg: Bulgarian (2/10)`）。指定しなければ非表示 |
| `--start START` | バッチ開始時刻（Unixタイムスタンプ）。指定するとバッチ全体の経過時間を表示 |

`--label` と `--start` がどちらも未指定の場合、プログレスバーのセパレータ `|` も非表示になる。

---

## 設計思想

### translate: サマリー圧縮方式

スライディング方式（直近N件のみ保持）では古い履歴が押し出されると**用語ブレ**が発生し、プロンプト先頭が毎回変化するため**KVキャッシュが無効**になるという課題があった。これを解決するため、チャットの構造を `system + summary（最新1件） + 直近keep件` に固定する**サマリー圧縮方式**を採用している。

`--threshold` 行ごとに翻訳履歴を英語サマリーに圧縮し、`--keep` 件の直近ペアと組み合わせてコンテキストを再構築する。これにより長文でも一貫性を保ちながら KV キャッシュが安定して効く。

サマリーは英語で出力され、翻訳先言語 (`to_lang`) に依存しない内容のため、`summary` サブコマンドで原文（トピック）ごとに事前生成しておく。原文と同じディレクトリに `{topic}-summary.jsonl` として保存され、同じトピックの全ての `to_lang`・複数回の `translate` 実行で使い回せる。`translate`・`batch` はいずれも生成済みのキャッシュを読むだけで自動生成はせず、未生成の場合はエラーになるため、事前に `summary` を実行しておく必要がある。

`translate` は1行訳すごとに出力ファイルへ逐次書き込む。途中で失敗・中断しても、同じコマンドで再実行すれば既存の翻訳行を飛ばして続きから再開する（chat_history は事前生成済みサマリーと出力ファイルの既存行から同じ手順で再構築される）。1行の翻訳結果が空、または内部に改行を含む場合は不正とみなし最大3回まで再試行、失敗時は例外を送出する。

### term extract/translate: 翻訳ループからの分離

用語抽出を翻訳ループ内で行うと、run ごとに抽出結果がブレて**訳語の不一致**が生じる（例: `affinage` → `refinamiento` / `ajuste fino`）。`term extract/translate` で用語を事前に確定・校正してから全 run で共有することで、このブレを原理的に排除する。

用語 TSV は LLM 生成後に校正が必要。ローカル LLM はスラッシュ2択・誤訳・他言語混入・語尾ミスなどの誤りを含みやすい。校正済み TSV を `trtools translate --terms-json/--terms-tsv` で注入することで、一貫した訳語が全翻訳 run に適用される。

### eval/agg: 3回評価の中央値

評価モデルの出力は run ごとに揺れるため、1回のスコアは信頼性が低い。同一翻訳に対して評価を3回実行し、`agg` で中央値をとることで評価者のランダム性を抑制する。

推奨評価モデルは **qwen3.6**。CoT による論理的検証で技術的欠陥を正しく特定できる。GPT-OSS 120B は92点が上限で上位モデルの差別化が困難なため非推奨。評価の CoT は無効化しないほうが信頼性が高い。

### モデル選定の指針

推奨翻訳モデルは **gemma4-26b**（`ollama:gemma4:26b`）。MoE のため高速で、スコア安定性が高く、評価者（qwen3.6）と異なるアーキテクチャのため自己評価バイアスも排除できる。

リソース制約がある環境では **gemma4-e4b**（`ollama:gemma4:e4b`）が代替候補。校正済み共有用語辞書（`--terms-json`/`--terms-tsv`）を使用することで安定性が向上する。ただし人称不統一といった文法的問題が出やすい点は許容が必要。

両モデル共に短い相槌行や話者交代を挟む継続行でスピーカータグが脱落することがあり、翻訳後の確認が必要。

---

## サブコマンド一覧

| コマンド | 概要 |
|---|---|
| [`summary`](#summary) | 原文の要約を事前生成（`translate` 用キャッシュ） |
| [`translate`](#translate) | テキストを行単位で翻訳 |
| [`review`](#review) | 他者評価による翻訳推敲 |
| [`eval`](#eval) | 翻訳品質を5項目で評価 |
| [`agg`](#agg) | 評価結果JSONを集約（中央値） |
| [`trend`](#trend) | 評価ログから言語ごとの傾向を要約 |
| [`term extract`](#term-extract) | テキストから専門用語を抽出 |
| [`term translate`](#term-translate) | 抽出用語をTSVに翻訳 |
| [`term show`](#term-show) | 用語TSVを言語・キーで絞り込んで表示 |
| [`term set`](#term-set) | 用語TSVの特定セルを更新 |
| [`term reorder`](#term-reorder) | 用語TSVの列を指定順に並べ替えて出力 |
| [`term merge`](#term-merge) | 複数の用語TSVを列結合して出力 |
| [`batch`](#batch) | 翻訳→評価→集約を一括実行 |

---

## summary

`translate` のサマリー圧縮方式で使う要約を原文だけから事前生成する。要約は英語で出力され `to_lang` に依存しないため、原文（トピック）ごとに1回生成すれば、そのトピックの全ての `to_lang`・複数回の `translate` 実行で使い回せる。

保存先は原文と同じディレクトリの `{topic}-summary.jsonl`（トピック名は入力ファイル名の `-<言語コード>` を除いた部分。例: `finetuning-fr.txt` → `finetuning-summary.jsonl`）。既に必要なチェックポイント分が揃っていれば何もしない。

```
uv run trtools summary <input_file...> -f <from_lang> -m <model> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `input_files` | 要約対象のテキストファイル（複数指定可）。ファイルごとに `[i/n]` を表示しながら順に処理する |
| `-f`, `--from` | 原語。言語名（`French`）または言語コード（`fr`） |
| `-m`, `--model` | 要約生成モデル |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--threshold` | `10` | 要約生成の間隔（行数）。`translate` と揃える |
| `--keep` | `5` | チェックポイント算出用の保持行数。`translate` と揃える |
| `--no-think` | false | thinking処理を無効化（Qwen3モデル用） |
| `-w`, `--retry-wait` | 3 | リトライ待機秒数 |

### 使用例

```bash
# 単一ファイル
uv run trtools summary finetuning-fr.txt -f fr -m ollama:gemma4:26b

# 複数ファイルをまとめて処理（[1/2], [2/2] と進捗表示）
uv run trtools summary finetuning-en.txt transformer-en.txt -f en -m ollama:gemma4:26b
```

---

## translate

テキストファイルを行単位で翻訳する。空行を保持しながら1行ずつ翻訳し、コンテキスト圧縮で長文に対応する。事前に `summary` サブコマンドで要約キャッシュを生成しておく必要がある（未生成の場合はエラーになる）。

```
uv run trtools translate <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `input_file` | 翻訳対象のテキストファイル |
| `-f`, `--from` | 原語。言語名（`French`）または言語コード（`fr`） |
| `-t`, `--to` | 翻訳先言語。言語名（`Spanish`）または言語コード（`es`） |
| `-o`, `--output` | 出力ファイル名 |
| `-m`, `--model` | 翻訳モデル（例: `ollama:gemma4:26b`） |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--threshold` | `10` | 要約生成の間隔（行数） |
| `--keep` | `5` | 圧縮後に保持する翻訳ペア数 |
| `--terms-json` | なし | `term extract` の出力JSONファイル |
| `--terms-tsv` | なし | `term translate` の出力TSVファイル |
| `--no-think` | false | thinking処理を無効化（Qwen3モデル用） |
| `-w`, `--retry-wait` | 3 | リトライ待機秒数 |
| `--fix` | false | 既存出力の空行のみ再翻訳。通常モードは行数のみで再開判定するため空行を検出せず継続してしまうが、`--fix` では出力ファイル全体を書き直して空行の箇所だけ再翻訳する |

### 使用例

```bash
# 基本的な翻訳
uv run trtools translate finetuning-fr.txt -f fr -t es \
  -o finetuning-es.txt -m ollama:gemma4:26b --no-think

# 用語注入あり
uv run trtools translate finetuning-fr.txt -f fr -t es \
  -o finetuning-es.txt -m ollama:gemma4:26b \
  --threshold 10 --keep 5 --no-think \
  --terms-json terms/finetuning-fr.json \
  --terms-tsv terms/finetuning-fr.tsv
```

---

## review

翻訳ファイルをLLMによる他者評価で推敲する。話者名付き行（`話者: テキスト` 形式）を対象に、分析→改善の2段階プロンプトで翻訳品質を向上させる。

```
uv run trtools review --original <orig> --translation <tr> -f <from> -t <to> -o <output> -m <model> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `--original` | 原文ファイル |
| `--translation` | 推敲対象の翻訳ファイル |
| `-f`, `--from` | 原語コード（例: `en`） |
| `-t`, `--to` | 翻訳先言語コード（例: `nl`） |
| `-o`, `--output` | 推敲後の出力ファイル名 |
| `-m`, `--model` | 推敲に使用するモデル |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--history` | `10` | コンテキストとして参照する直前の推敲済み行数 |
| `--no-think` | false | thinking処理を無効化 |
| `--terms` | なし | 用語対訳TSVファイル（話者名の変換に使用） |

### 動作

- 話者名付き行（`話者: テキスト`）のみ推敲対象とし、空行・話者名なし行はそのまま出力する
- 推敲は2段階：① 翻訳の問題点を分析（`No issues` なら改善スキップ）→ ② 改善訳を生成
- `--terms` で渡したTSVの話者名列を参照し、出力の話者名を対象言語に変換する

### 使用例

```bash
uv run trtools review \
  --original finetuning-en.txt \
  --translation tr/finetuning-nl.txt \
  -f en -t nl \
  -o reviewed/finetuning-nl.txt \
  -m ollama:gemma4:26b \
  --terms terms/finetuning-en.tsv
```

---

## eval

翻訳品質を5項目（各20点、合計100点）で評価する。評価結果をJSONファイルに保存できる。

```
uv run trtools eval --original <orig> --translation <tr> -f <from> -t <to> -m <model> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `--original` | 原文ファイル |
| `--translation` | 翻訳文ファイル |
| `-f`, `--from` | 原語。言語名または言語コード |
| `-t`, `--to` | 翻訳先言語。言語名または言語コード |
| `-m`, `--model` | 評価モデル（例: `ollama:qwen3.6`） |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `-o`, `--output` | なし | 評価結果JSONの保存先 |
| `-w`, `--retry-wait` | 3 | リトライ待機秒数 |
| `--no-think` | false | thinking処理を無効化 |
| `--run` | `1` | 現在の評価回数（プログレスバーの表示に使用） |
| `--runs` | `1` | 評価の総回数（プログレスバーの表示に使用） |

### 評価項目

1. **読みやすさと理解しやすさ**（20点）
2. **流暢さと自然さ**（20点）
3. **専門用語の適切性**（20点）
4. **文脈適応性**（20点）
5. **情報の完全性**（20点）

### 使用例

```bash
# 1回評価
uv run trtools eval \
  --original finetuning-fr.txt \
  --translation finetuning-es.txt \
  -f fr -t es \
  -m ollama:qwen3.6 -w 3 \
  -o evals/finetuning-es-1.json

# 3回評価（プログレスバーに x/3 を表示）
for run in 1 2 3; do
  uv run trtools eval \
    --original finetuning-fr.txt \
    --translation finetuning-es.txt \
    -f fr -t es \
    -m ollama:qwen3.6 -w 3 \
    --run $run --runs 3 \
    -o evals/finetuning-es-$run.json
done
```

---

## agg

`eval` で生成した評価JSONファイル（3回分）を集約し、各項目の中央値を計算する。ファイル名は `<base>-1.json`, `<base>-2.json`, `<base>-3.json` の形式を想定。

```
uv run trtools agg <json_files...> [options]
```

### 引数

| 引数 | 説明 |
|---|---|
| `files` | 評価JSONファイル（複数指定可、ワイルドカード可） |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `-o`, `--output` | なし | 集約結果JSONの保存先 |
| `--verbose` | false | 項目別の中央値・平均・標準偏差を表示 |

### 使用例

```bash
# 全evalファイルを集約してSCORES.txtに保存
uv run trtools agg evals/*.json | tee SCORES.txt

# 詳細表示
uv run trtools agg evals/*.json --verbose
```

---

## trend

`eval` で生成した評価JSON（3回分）を言語ごとにマージし、LLM に要約させて `README.md` の「傾向の分析」列に入れる一文を生成する。中間結果を JSONL に追記し、そこから Markdown の表を組み立てて `README.md` に書き戻す。

```
uv run trtools trend <json_files...> -m <model> [options]
```

### 引数

| 引数 | 説明 |
|---|---|
| `files` | 評価JSONファイル（複数指定可、ワイルドカード可）。`--render-only` 時は不要 |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `-m`, `--model` | なし | 要約に使用するモデル（`--render-only` 時は不要） |
| `-o`, `--output` | `TRENDS.jsonl` | 中間結果のJSONL |
| `--sync` | なし | 生成後に表を書き戻す `README.md` のパス |
| `--render-only` | false | 生成せずJSONLから表の出力・同期のみ行う |
| `--no-think` | false | thinking処理を無効化 |
| `-w`, `--retry-wait` | 3 | リトライ時の待機時間（秒） |
| `-l`, `--lang` | `en` | 要約の出力言語（`en`/`ja`） |

### 動作

LLM に渡すのは評価ログのみで、訳文は渡さない。訳文を渡すと4回目の評価をやり直すことになり、3回評価の中央値による安定化が活きないため。ファイルパスやモデル名、criterion 別のスコア・reasoning など要約を混乱させる情報は渡さず、評価ごとの総合スコア `total_score` と総合評価 `overall_comment` のみを渡す。3回とも指摘された欠陥は1回だけのものより信頼できる、という判断材料になる。

プロンプトでは評価結果を所与として信頼させ、ログにない具体性を補わないよう制約している（例：混入言語が特定されていなければどの言語かを断定せず一般的な表現にとどめさせる）。出力言語（`-l`/`--lang` で指定、デフォルト `en`）と評価対象言語の混同も明示的に禁止している。

出力は1項目のみのため構造化出力は使わず、プレーンテキストで受け取る。ラベルや引用符、句点、前後の説明を付けないようプロンプトで指示し、受け取った側でも全体を囲む引用符・末尾の句点・改行を除去し、表のセルと衝突する `|` をエスケープする。指定した言語で返ってこなかった場合は最大3回まで再指示して引き直す。

**中断からの再開**: 1言語ぶん生成するたびに JSONL へ追記し、起動時に JSONL を読んで既存の言語をスキップする。中断しても失うのは最大1言語ぶん。特定言語だけ引き直したい場合は該当行を削除して再実行する。

**表の同期**: `--sync` を指定すると、対象ファイル内の `| 言語 | スコア | 傾向の分析 |`（`ja`）または `| Language | Score | Trend Analysis |`（`en`）というヘッダを持つ表を丸ごと差し替える。ヘッダが一致する表のみを対象とするため、同一ファイル内の他の表は影響を受けない。ヘッダ自体も `-l`/`--lang` に応じて生成されるため、既存の表がどちらの言語で書かれていても検出・置換できる。行はスコア降順・言語コード昇順に並べ、言語名は `LANGUAGES`（[language.py](language.py)）の `-l`/`--lang` に対応する表記（`en`/`ja`）を使う。

### 使用例

```bash
# 全言語の傾向を生成して README.md の表を更新
uv run trtools trend evals/*.json -m ollama:qwen3.6 --no-think --sync README.md

# 中断後の再開（未生成の言語だけ処理される）
uv run trtools trend evals/*.json -m ollama:qwen3.6 --no-think --sync README.md

# 生成済みJSONLから表の再出力・同期のみ
uv run trtools trend --render-only --sync README.md
```

---

## term extract

テキストファイルから固有名詞・専門用語を抽出し、チャンク単位でJSONに保存する。`translate` サブコマンドの `--terms-json` に渡す用途。

```
uv run trtools term extract <input_file> -f <from_lang> -m <model> -o <output.json> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `input_file` | 用語を抽出するテキストファイル |
| `-f`, `--from` | 原語。言語名または言語コード |
| `-m`, `--model` | 使用モデル |
| `-o`, `--output` | 出力JSONファイル名 |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--keep` | `5` | チャンクサイズ（行数） |
| `-w`, `--retry-wait` | 3 | リトライ待機秒数 |
| `--no-think` | false | thinking処理を無効化 |

### 使用例

```bash
uv run trtools term extract finetuning-fr.txt \
  -f fr -m ollama:gemma4:31b \
  --keep 5 --no-think \
  -o terms/finetuning-fr.json
```

---

## term translate

`term extract` で生成したJSONを読み込み、各言語の用語翻訳をTSVファイルに書き出す。共通語彙TSV（`-c`）があれば一致する用語はLLMをスキップして流用する。

```
uv run trtools term translate <extract.json> -t <lang> [-t <lang> ...] -m <model> -o <output.tsv> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `extract_file` | `term extract` の出力JSON |
| `-t`, `--to` | 翻訳先言語。言語名または言語コード（複数指定可） |
| `-m`, `--model` | 使用モデル |
| `-o`, `--output` | 出力TSVファイル名 |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `-c`, `--common` | なし | 共通語彙TSVファイル（既存翻訳の流用） |
| `-w`, `--retry-wait` | 3 | リトライ待機秒数 |
| `--no-think` | false | thinking処理を無効化 |

### 使用例

```bash
# フランス語 → 英語・スペイン語
uv run trtools term translate terms/finetuning-fr.json \
  -t en -t es \
  -m ollama:gemma4:31b --no-think \
  -c terms/common.tsv \
  -o terms/finetuning-fr.tsv

# 英語 → ドイツ語・日本語・中国語
uv run trtools term translate terms/finetuning-en.json \
  -t de -t ja -t zh \
  -m ollama:gemma4:31b --no-think \
  -c terms/common.tsv \
  -o terms/finetuning-en.tsv
```

---

## term show

用語TSVを言語列・キーで絞り込んで標準出力に表示する。列数が多いTSVをLLMに渡す際の前処理や、校正対象の確認に使用する。

```
uv run trtools term show <tsv_file> [-l <lang> ...] [-k <key> ...]
```

### 引数

| 引数 | 説明 |
|---|---|
| `tsv_file` | 対象TSVファイル |
| `-l`, `--lang` | 表示する言語列。言語名または言語コード（複数指定可、省略時は全列） |
| `-k`, `--key` | 表示するキー・第1列の値（複数指定可、省略時は全行） |

キー列（第1列）は `-l` の指定に関わらず常に先頭に出力される。

### 使用例

```bash
# 日本語列のみ全行表示
uv run trtools term show terms/onde-en.tsv -l ja

# 日本語・ドイツ語を2列表示
uv run trtools term show terms/onde-en.tsv -l ja -l de

# キーで絞り込み
uv run trtools term show terms/onde-en.tsv -l ja -k physics -k waves
```

---

## term set

用語TSVの特定セルを上書きして保存する。LLMによる自動翻訳後の個別校正に使用する。

```
uv run trtools term set <tsv_file> -k <key> -l <lang> -v <value>
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `tsv_file` | 対象TSVファイル |
| `-k`, `--key` | 変更するキー（第1列の値） |
| `-l`, `--lang` | 変更する言語列名。言語名または言語コード |
| `-v`, `--value` | 新しい値 |

### 使用例

```bash
uv run trtools term set terms/onde-en.tsv -k "physics" -l ja -v "物理学"
```

---

## term reorder

用語TSVの列を指定した順序に並べ替えて出力する。存在しない列は空列として追加される。

```
uv run trtools term reorder <tsv_file> -c <lang> [...] -o <output.tsv>
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `tsv_file` | 対象TSVファイル |
| `-c`, `--col` | 出力する列名。言語名または言語コード（複数指定） |
| `-o`, `--output` | 出力TSVファイル |

### 使用例

```bash
uv run trtools term reorder terms/finetuning-en.tsv \
  -c en -c fr -c es -c de -c ja -c zh \
  -o terms/finetuning-en-reordered.tsv
```

---

## term merge

複数の用語TSVを列結合して出力する。キー列（第1列）が共通の場合はキー値でマッチし、キー列がない場合は行位置でマッチする。同じ列名が複数ファイルに存在する場合、後のファイルの非空値がセル単位で上書きする。

```
uv run trtools term merge <file1> <file2> [...] -o <output.tsv>
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `FILE...` | 入力TSVファイル（複数） |
| `-o`, `--output` | 出力TSVファイル |

### 使用例

```bash
# 既存TSVに別ファイルの言語列を追加
uv run trtools term merge terms/finetuning-en.tsv extra-langs.tsv \
  -o terms/finetuning-en-full.tsv
```

---

## batch

翻訳→評価→集約を一括実行する。ファイル名の言語コード（例: `finetuning-fr.txt` → `fr`）から原語を自動導出し、`--tr-dir` と `--eval-dir` で指定したディレクトリに出力を整理する。既存ファイルはスキップする。

`summary` は自動生成しないため、翻訳フェーズの前に対象ファイルの `{topic}-summary.jsonl` を `trtools summary` で生成しておくこと。未生成の場合はその翻訳対象がエラーになりスキップされる。

```
uv run trtools batch <files...> --langs <lang...> -m <model> [options]
```

### 必須引数

| 引数 | 説明 |
|---|---|
| `files` | 入力テキストファイル（例: `../finetuning-fr.txt`）。ファイル名末尾の `-XX` が原語コードとして使われる |
| `--langs` | 翻訳先言語コードリスト（例: `en es de`） |
| `-m`, `--model` | 翻訳モデル（`--eval-only` 時は不要） |

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--evaluator` | なし | 評価モデル（`--tr-only` 時は不要） |
| `--tr-only` | false | 翻訳のみ実行（評価・集約をスキップ） |
| `--eval-only` | false | 評価のみ実行（翻訳・集約をスキップ） |
| `--no-agg` | false | 集約のみスキップ（`SCORES.txt` を生成しない） |
| `-f`, `--from` | ファイル名から自動導出 | 原語（手動指定する場合） |
| `--terms-dir` | なし | 用語ファイルのディレクトリ（`<topic>-<from>.json/tsv` を自動検索） |
| `--tr-runs` | `1` | 翻訳の実行回数 |
| `--eval-runs` | `3` | 評価の実行回数 |
| `--threshold` | `10` | 要約生成の間隔（行数） |
| `--keep` | `5` | 圧縮後に保持する翻訳ペア数 |
| `--no-think` | false | CoT無効化 |
| `--tr-dir` | `tr` | 翻訳出力ディレクトリ |
| `--eval-dir` | `evals` | 評価出力ディレクトリ |
| `-w`, `--retry-wait` | `3` | リトライ待機秒数 |

### 出力ファイル構成

`--tr-runs 1`（デフォルト）の場合:

```
<tr-dir>/
  <topic>-<lang>.txt          # 翻訳結果
<eval-dir>/
  <topic>-<lang>-1.json  # 評価結果（eval-runごと）
  <topic>-<lang>-2.json
  <topic>-<lang>-3.json
SCORES.txt                    # 集約スコア
```

`--tr-runs 3` の場合はサフィックス付き（例: `<tr-dir>/finetuning-de-1.txt`, `<eval-dir>/finetuning-de-1-1.json`）。

### 対応言語コード

[trtools/language.py](language.py) を参照。登録されていない言語コードは言語名として大文字化して渡される（例: `xx` → `Xx`）。

一定の品質が確認されている言語（全4トピック・gemma4-26b、[examples/](../examples/) 参照訳として採用済み）: `en` English, `ja` Japanese, `es` Spanish, `zh` Chinese, `de` German

上記以外の言語の品質は未確認。生成結果は必ず確認・校正すること。

### 使用例

```bash
# 事前に要約を生成（trtools batch は自動生成しない）
uv run trtools summary ../finetuning-en.txt ../transformer-en.txt \
  -f en -m ollama:gemma4:26b --threshold 20

# 翻訳のみ（複数ファイル・複数言語）
uv run trtools batch \
  ../finetuning-en.txt ../transformer-en.txt \
  --langs de ja zh \
  -m ollama:gemma4:26b \
  --terms-dir ../terms \
  --threshold 20 --no-think \
  --tr-only

# 翻訳 + 評価 + 集約
uv run trtools batch \
  ../finetuning-fr.txt ../transformer-fr.txt \
  --langs en es \
  -m ollama:gemma4:26b \
  --evaluator ollama:qwen3.6 \
  --terms-dir ../terms \
  --no-think

# 評価のみ（翻訳済みファイルを前提に、評価だけ再実行）
uv run trtools batch \
  ../finetuning-en.txt \
  --langs de ja zh \
  --evaluator ollama:qwen3.6 \
  --eval-only

# 集約は別途実行
uv run trtools agg evals/*.json | tee SCORES.txt
```

---

## 典型的なワークフロー

### 1. 用語ファイルを準備する

```bash
# 用語抽出
uv run trtools term extract topic-fr.txt \
  -f fr -m ollama:gemma4:31b --keep 5 --no-think \
  -o terms/topic-fr.json

# 用語翻訳
uv run trtools term translate terms/topic-fr.json \
  -t en -t es \
  -m ollama:gemma4:31b --no-think \
  -c terms/common.tsv -o terms/topic-fr.tsv
```

### 2. 要約を事前生成する

```bash
uv run trtools summary topic-fr.txt -f fr -m ollama:gemma4:26b
```

### 3. 翻訳と評価を一括実行する

```bash
uv run trtools batch topic-fr.txt \
  --langs en es \
  -m ollama:gemma4:26b \
  --evaluator ollama:qwen3.6 \
  --terms-dir terms \
  --no-think
```

### 4. 個別に翻訳・評価・集約を実行する

```bash
# 翻訳（事前に summary topic-fr.txt を実行済みであること）
uv run trtools translate topic-fr.txt -f fr -t en \
  -o tr/topic-en.txt -m ollama:gemma4:26b --no-think \
  --terms-json terms/topic-fr.json --terms-tsv terms/topic-fr.tsv

# 評価（3回）
for run in 1 2 3; do
  uv run trtools eval \
    --original topic-fr.txt --translation tr/topic-en.txt \
    -f fr -t en \
    -m ollama:qwen3.6 -w 3 \
    --run $run --runs 3 \
    -o evals/topic-en-$run.json
done

# 集約
uv run trtools agg evals/topic-en-*.json | tee SCORES.txt
```
