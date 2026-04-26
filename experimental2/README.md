# サマリー圧縮方式 翻訳実験

[../experimental/](../experimental/) の翻訳アーキテクチャを「サマリー圧縮方式」に移行する実験ディレクトリです。

## 背景と動機

旧アーキテクチャ（[../experimental/translate.py](../experimental/translate.py)）はスライディング方式で、毎リクエストに過去の翻訳を文字列として埋め込むため：

- **KV キャッシュが無効**：プロンプトの先頭が毎回変化するため、モデルのキャッシュが再利用されない
- **用語ブレ**：古い履歴がウィンドウ外に押し出されると、固有名詞や術語の訳が変化する

新アーキテクチャは[参照実装](ref/) をベースに、`system + summary + 直近 N 件` の固定構造を維持し、この2つの問題を解決します。

## 翻訳システム

スクリプト実行は必ず `uv run` を使うこと（`python` 直接呼び出しは依存関係が解決されない）。

### translate.py

```bash
uv run translate.py <input_file> -f <from_lang> -t <to_lang> -o <output> -m <model> [options]
```

**オプション:**

| オプション | デフォルト | 説明 |
|---|---|---|
| `--threshold` | 15 | 圧縮発動までの翻訳ペア数 |
| `--keep` | 5 | 圧縮後に保持する直近ペア数 |
| `--summary glossary` | なし | サマリー方式（未指定で単純削除） |
| `--schema` | なし | 構造化出力（JSON スキーマ）を有効化（翻訳直接出力タスクでは不使用） |
| `--no-think` | なし | reasoning を無効化（Qwen3/Gemma4 用、翻訳時は原則指定） |

**CoT（think）について:**

翻訳時は `--no-think` を原則指定する理由：

- **品質面**: 1行ずつのシンプルな翻訳タスクに CoT での推敲は過剰。以前の実験（[../experimental/README.md](../experimental/README.md)）でも CoT は翻訳に有害との結論。
- **速度面**: CoT により処理時間が数十倍に膨らむ。
- **KV キャッシュ面**: CoT トークンはモデルの生成履歴に含まれるため、履歴から CoT を除いて渡すとシーケンスが変わりキャッシュミスが発生する。かといって CoT を履歴に含めると翻訳本文の何十倍もの量が蓄積してしまう。`--no-think` ならこの問題自体が発生しない。

CoT が活きるのは「複数の情報を統合して判断する」場面であり、1行翻訳にはその余地がほとんどない。セクション単位で渡せば文脈・文体の一貫性を推敲できるが、30B クラスのモデルでは長い出力の途中で行の欠落やハルシネーションが入り込むリスクがある。「1行ずつ・no-think」は 30B モデルでの信頼性と品質のバランスをとった現実的な最適解。

**CoT 有害性の具体例（debug1）:** gemma4:31b（think）× `--schema`（glossary-schema）で 43行中 23行目の出力が崩壊した。`bachoter pour un examen`（フランス語の慣用句）を訳す際、CoT の推論過程で複数言語が混在し、スキーマ制約下でスペイン語に戻りきれず以下の出力が生成された：

```
Camille: ¿La diferencia entre estudiar hurriedlyдля an exam and truly mastering a subject?
```

英語（`hurriedly`）とキリル文字（`для`、ロシア語）がスペイン語の文中に混入。この1箇所でスコアが 62点に急落した。同モデルで `--no-think` にすると 96点に回復しており、`think × schema` の組み合わせ固有の問題と見られる。

**glossary 方式の設計:**

事前にテキスト全体から用語を一括抽出する方式も検討したが、漏れが生じる可能性があるため、翻訳しながら逐次ピックアップする局所的な方式（`--summary glossary`）を採用した。翻訳の進行とともに用語集が積み上がるため、後半ほど一貫性が高まる。

**サマリー方式の動作（threshold=15, keep=5 の場合）:**

- 10行ごとにサマリーを生成し、サマリー生成後 5行で `system + 最新サマリー + 直近5件` に圧縮する（圧縮は 15, 25, 35, ... 行目）
- 10行目にサマリーを生成し、5件の翻訳を挟んで 15行目で圧縮する（圧縮は 15, 25, 35, ... 行目）。サマリー生成後〜圧縮前の 5件は KV キャッシュが有効。圧縮直後のリクエストは prefix が変わるため cold start になり、以降は新しい prefix でキャッシュが再開される（詳細 → [debug2/README.md](debug2/README.md)）
- 直近 N 件は翻訳スタイルの few-shot として機能する。要約だけでセッションを作り変えると、モデルが要約の文体に引っ張られて翻訳が崩れる可能性があるため、実際の翻訳例を数件残すことでスタイルを安定させる

**実装上の特記事項:**

- 1行ずつ翻訳することで、行の欠落やハルシネーション（翻訳中に作文に転落する現象）を防ぐ
- `--schema` 指定時のみ構造化出力（`pydantic.BaseModel`）を使用。未指定時は生テキストで受け取る
- `llm7shi.compat.generate_with_schema` 経由でモデルを呼び出すため、`ollama:`, `openai:`, `google:` プレフィックスによるプロバイダー切り替えが可能
- `chat_history`（role 付き）をそのまま渡すことで KV キャッシュを有効化（詳細 → [debug2/README.md](debug2/README.md)）

**KV キャッシュの懸念点（ハイブリッドモード）:** 要約生成後に要約を履歴から削除して翻訳を継続する設計は、Ollama が前方一致による prefix キャッシュに対応していることを前提とする。要約生成リクエストの後、履歴を巻き戻した状態（`[system, u1..u10, u11]`）を送った場合、Ollama が `[system, u1..u10]` までのキャッシュを再利用できるかは未確認。対応していない場合、要約後の翻訳は毎回キャッシュミスになる。

### batch.sh

指定モデル × バリアントの翻訳・評価・集約を一括実行するスクリプトです。

```bash
bash batch.sh
```

翻訳・評価・集約の3フェーズに分離しており、既存ファイルはスキップされるため途中から再開可能です。翻訳結果は [tr/](tr/)、評価結果は [evals/](evals/) に出力し、最終的に [SCORES.txt](SCORES.txt) を生成します。

---

## 評価システム

[../experimental/](../experimental/) の評価パイプラインをそのまま使用します。

### 評価基準（5項目 × 20点 = 100点満点）

| 項目 | 説明 |
|---|---|
| **読みやすさと理解しやすさ** | ターゲット言語の読者が内容を容易に理解できるか。文章構造が論理的か。 |
| **流暢さと自然さ** | ネイティブスピーカーにとって自然か。不自然な直訳・語彙選択がないか。 |
| **専門用語の適切性** | 専門用語（`fine-tuning`, `in-context learning` 等）が適切かつ一貫して処理されているか。 |
| **文脈適応性** | 原文の意図が伝わるか。ターゲット文化への配慮があるか。 |
| **情報の完全性** | 重要な情報の欠落・過剰追加がないか。 |

詳細な採点基準 → [../experimental/EVAL.md](../experimental/EVAL.md)

### 採点の目安

| 点数帯 | 評価 |
|---|---|
| 18〜20点 | 高品質、特筆すべき欠陥なし |
| 13〜17点 | 軽微な問題あり |
| 6〜12点 | 主要な欠陥（文法エラー、未翻訳箇所等） |
| 0〜5点 | 構造的欠陥（言語混在、JSON フラグメント等） |

### 評価パイプライン

```bash
# 1. 個別評価（1回）
uv run ../experimental/evaluate_translation.py \
  --original ../examples/finetuning-fr.txt \
  --translation <translation.txt> \
  -f French -t Spanish -m ollama:qwen3.6 -w 3 -o <output.json>

# 2. 3回評価 → 中央値集計
uv run ../experimental/aggregate_evaluations.py evals/*.json

# 3. SCORES.md 生成
uv run ../experimental/generate_scores_md.py -1 91 -2 92 SCORES.txt
```

**評価者:** `qwen3.6`（CoT による論理的検証で技術的欠陥を正確に特定）  
**集計:** 3回評価の中央値（評価ブレを排除）  
**統計:** 中央値・平均値・標準偏差を項目別・総合別に算出

評価者選定の経緯 → [../experimental/MEMO.md](../experimental/MEMO.md)

### 参照訳の評価（Gemini 3.0 Pro）

[../examples/finetuning-es.txt](../examples/finetuning-es.txt)（Gemini 3.0 Pro による参照訳）を同じパイプライン（3回評価・中央値）で採点した。

| 項目 | eval-1 | eval-2 | eval-3 | 中央値 |
|---|:---:|:---:|:---:|:---:|
| readability | 19 | 19 | 19 | **19** |
| fluency | 19 | 19 | 19 | **19** |
| terminology | 19 | 20 | 20 | **20** |
| contextual_adaptation | 20 | 19 | 19 | **19** |
| information_completeness | 20 | 20 | 20 | **20** |
| **合計** | **97** | **97** | **97** | **97** |

3回とも97点で評価ブレがゼロ。

**減点の内容:**

- **readability -1（全3回）**: 具体的な問題指摘なし。天井効果と思われる
- **fluency -1（全3回）**: `Lo has entendido todo`（直訳調、eval-3 指摘）、`guía rápida`（`antisèche` の訳として比喩が弱い、eval-2 指摘）
- **terminology -1（eval-1 のみ）**: 減点理由が明確でなく、reasoning は「標準的・一貫している」と肯定的。天井効果の可能性
- **contextual_adaptation -1（eval-2, eval-3）**: `Tech Relámpago`（`Tech Éclair` の直訳）が原文の洒落を完全に再現できていないとの指摘

**備考:**

- `Tech Relámpago` はポッドキャストをスペイン語原文と仮定して翻訳したものであり、今回の実験ではその前提を評価者に伝えていない。評価者はフランス語からの翻訳として採点しているため、この指摘は前提条件の違いによるものである。
- `antisèche` を `guía rápida`（簡単なガイド）と訳しているが、`chuleta`（カンニングペーパー）の方が原義に近いとの指摘は今回の評価では出なかった。

---

## 実験結果

### Phase A: 動作確認（gemma3:27b）

翻訳入力: [../examples/finetuning-fr.txt](../examples/finetuning-fr.txt)（43行、フランス語ポッドキャスト）
翻訳先: スペイン語（3回評価の中央値）

| バリアント | 処理時間 | 評価（3回中央値） |
|---|---|---|
| `none` | 4.0分 | 95点 |
| `glossary` | 6.8分 | 98点 |

`--schema` なし（生テキスト受け取り）で実施。`llm7shi` v0.10.1 アップデート（ロール変換問題の修正）後に再評価し、`glossary` が `none` を上回ることを確認。

**用語翻訳の例（glossary モード）:**
- `pré-entraînement` → `pre-entrenamiento`
- `ajuste fino (fine-tuning)` （英語を括弧内に併記）
- `aprendizaje por transferencia`
- `aprendizaje en contexto (ICL)`
- `anclaje (grounding)`
- `bachoter` → `memorizar para un examen`（文化的ローカライズ）

### debug1: 方式選定

| モデル | none | glossary | none-schema | glossary-schema |
|---|---|---|---|---|
| gemma3:27b | 95 | **98** | 99 | 96 |
| gemma4:31b（think） | 98 | **98** | 97 | 62 |
| gemma4:31b（no-think） | 98 | **97** | 96 | 96 |
| gpt-oss:120b | **97** | 87 | 88 | 90 |
| qwen3.6（think） | 96 | **97** | 96 | 96 |
| qwen3.6（no-think） | 93 | **94** | — | — |

- `--schema` 廃止: gemma4:31b の glossary-schema=62点が象徴的。複数モデルで品質低下
- `--summary glossary` 採用: gpt-oss:120b は `bachotaje`（フランス語直写）問題で逆効果、gemma4:31b（no-think）は 1点差（97 vs 98）だが、それ以外のモデルは同等以上
- `--no-think` 採用: qwen3.6 は think あり(97) > no-think(94) と差があるが、処理時間が数十倍になるため no-think で十分

### Phase B: 本番実験

[MODELS.txt](MODELS.txt) 全モデル（34モデル）× `glossary` モード × 3回評価（[SCORES.txt](SCORES.txt) に集約）

**方針:**
- 構造化出力（`--schema`）は翻訳直接出力タスクには不要と判断し不使用
- `--summary glossary` を採用（用語の揺れを防ぐため）
- `--no-think` は Qwen3/Gemma4 系モデルに適用

**結果（32モデル、スコア降順）:**

| モデル | スコア | 備考 |
|---|---|---|
| qwen3.6-27b | 97 | `Exactamente` 繰り返し（語彙多様性低下） |
| gemma4-31b | 97 | タイポ（アクセント・引用符）、敬語不一致（`usted`/`hablarte`） |
| gemma4-26b | 97 | `en coulisses` → `de forma interna`（`entre bastidores` 推奨） |
| llama4-scout | 96 | `bachoter` 誤訳（意味反転）、eval-2 が89点に急落 |
| gemma3-27b | 96 | `antisèche` → `memoria auxiliar`（`chuleta` 推奨） |
| aya-expanse-32b | 96 | 全角感嘆符タイポ、ポッドキャスト名 `Tech Relámpago` 直訳 |
| qwen3.6-35b | 95 | `fine-tuning` → `afinamiento`/`ajuste fino` 揺れ（3回全て指摘） |
| qwen3-32b | 95 | eval-3 が92点（fluency=17、`¿Es decir?` など直訳調会話表現） |
| mistral-small3.2 | 95 | eval-3 が93点（fluency=17、`informaciones` フランス語干渉） |
| gemma4-e4b | 95 | `*prompt*` マークアップ残り（eval-3）、`anclaje` 術語選択の好み |
| gemma3-12b | 95 | `sus inmensas conocimientos` 性数一致エラー（eval-1 が93点） |
| ministral-3-14b | 94 | eval-2 が88点急落（fluency=16、文法エラー・フランス語干渉） |
| gpt-oss-120b | 94 | eval-3 が76点急落（`¿Eso qué?` スラング・false friend 問題） |
| gpt-oss-20b | 91 | 評価ブレ大（88〜97点）、fluency・術語の一貫性問題 |
| qwen3.5-27b | 90 | `informações`（ポルトガル語）混入、`muletilla`（`antisèche` 誤訳） |
| ministral-3-8b | 89 | eval-2 が74点急落（翻訳者メタノート挿入、性数エラー、術語問題） |
| gemma4-e2b | 88 | フランス語干渉（`levantar el velo`等）、`tras bambalée`（存在しない表現） |
| llama3.3 | 84 | `haber nos escuchado` 文法エラー（3回全て指摘）、`afinizar`（造語） |
| gemma3-4b | 84 | `bachoter` → `aprobar por nota`（意味ずれ）、フランス語慣用句直訳 |
| qwen3.5-35b | 82 | `informaciones`/`informaciónes`（フランス語干渉）、eval-2 が76点 |
| aya-expanse-8b | 79 | `ICL` → `LCL` 誤字、`grounding` → `referenciación`/`ancraje`（非標準） |
| gemma3n-e4b | 78 | 敬語混在（`tú`/`usted`/`vosotros`）、タイポ（`pre-entrerenamiento`等） |
| phi4 | 76 | `informaciones` フランス語干渉、`ancoraje`（非標準）、評価ブレ大（73〜84点） |
| command-r7b | 76 | `grounding` → `amarre`（係留の意）誤訳、敬語不一致（`tú`/`usted`混在） |
| qwen3.5-4b | 74 | `Solucionamos estas IAs`（`percibimos` の誤訳）、フランス語直訳多数 |
| qwen3-14b | 74 | 性数一致エラー多数（`Las conocimientos`等）、eval-3 が64点急落 |
| command-r-35b | 72 | `cuando begins`（英語混入）、eval-3 が63点急落（fluency=7） |
| qwen3.5-9b | 70 | 系統的な性数一致エラー（`las conocimientos`等）、`ajustamiento fino`（非標準） |
| ministral-3-3b | 63 | eval-3 が52点急落（fluency=8、`bachotaje` フランス語残り・性数エラー多数） |
| qwen3-4b | 40 | 能力限界（旧実験最高74点）。多言語混入・訳語不安定 |
| gemma2-9b | 27 | 翻訳後に `Let me know if you need anything else translated!` を毎行付加。翻訳内容自体は正確 |
| qwen3-30b | 0 | 構造化出力必須モデル。`--no-think` + 自由記述で CoT 推論テキストを翻訳として出力。旧実験で既知の挙動 |
| mixtral-8x7b | - | 対話的コメントが累積・増幅してエラー |
| mixtral-8x22b | - | 読み込み不可（メモリ構成の影響） |

上位 LLM モデルは参照訳と同水準。readability と fluency で一律 -1 が入るパターンは上位モデル全般に共通しており、この評価者では **97点が実質的な上限（天井）** と考えられる。97点モデルはほぼ満点と見なしてよい。

**主なパターン:**

- **フランス語干渉**: `informaciones`（スペイン語で不可算名詞）が複数モデルで出現（qwen3.5-27b・qwen3.5-35b・phi4・ministral-3-3b 等）。`haber nos`（llama3.3）、`tras bambalée`（gemma4-e2b）など
- **性数一致エラー**: `Las/sus conocimientos`（女性扱い→男性が正しい）が中〜低スコアモデルで繰り返し発生（qwen3-14b・qwen3.5-9b・ministral-3-3b 等）
- **術語誤訳**: `grounding` → `amarre`（係留の意、command-r7b）、`ICL` → `LCL`（aya-expanse-8b）など構造的な誤り
- **敬語・人称混在**: `tú`/`usted`/`vosotros` を同一テキスト内で混用（gemma3n-e4b・command-r7b・qwen3-14b 等）
- **翻訳者メタノート挿入**: 翻訳結果に注釈やコメントを付加するモデルが散発（ministral-3-8b の eval-2 で急落の主因）

**総評:**

- **gemma4-26b** が最も優れた選択。スコア安定性が最高（範囲1）で、減点がイディオム選択の好みの問題だけ。誤訳・タイポ・文法的欠陥はゼロ。gemma4-31b と同等スコアながらパラメータ数が少ない。
- **qwen3.6-27b** は次点だが、評価者が同系モデル（`ollama:qwen3.6`）のため自己評価バイアスに注意。
- **llama4-scout** は中央値96点でも `bachoter` 誤訳（89点急落）が再現した場合の信頼性に懸念が残る。

---

### Phase C: 旧アーキテクチャとの比較

旧アーキテクチャ（[../experimental/qwen3.6/SCORES.md](../experimental/qwen3.6/SCORES.md)）の「モデル別実用設定一覧」から各モデルの上位1スコアと比較（nt の区別なし）。

| モデル | 旧ベスト | 新 glossary | 差分 |
|---|:---:|:---:|:---:|
| gemma3-27b | 98 | 96 | -2 |
| gpt-oss-120b | 98 | 94 | -4 |
| aya-expanse-32b | 97 | 96 | -1 |
| command-r-35b | 96 | 72 | **-24** |
| ministral-3-8b | 96 | 89 | -7 |
| mistral-small3.2 | 96 | 95 | -1 |
| qwen3-30b | 96 | 0 | **-96** |
| qwen3-32b | 96 | 95 | -1 |
| gemma3-12b | 95 | 95 | 0 |
| gpt-oss-20b | 95 | 91 | -4 |
| llama3.3 | 95 | 84 | -11 |
| llama4-scout | 95 | 96 | **+1** |
| ministral-3-14b | 95 | 94 | -1 |
| qwen3-14b | 95 | 74 | **-21** |
| gemma2-9b | 94 | 27 | **-67** |
| aya-expanse-8b | 93 | 79 | -14 |
| mixtral-8x22b | 93 | 未実行 | — |
| gemma3n-e4b | 91 | 78 | -13 |
| phi4 | 91 | 76 | -15 |
| mixtral-8x7b | 85 | 未実行 | — |
| gemma3-4b | 81 | 84 | **+3** |
| ministral-3-3b | 74 | 63 | -11 |
| qwen3-4b (nt) | 74 | 40 | **-34** |
| command-r7b | 71 | 76 | **+5** |

**傾向:**

- **改善・同等（±2点以内）:** gemma3-12b(0)、aya-expanse-32b(-1)、mistral-small3.2(-1)、qwen3-32b(-1)、ministral-3-14b(-1)、llama4-scout(+1)、gemma3-4b(+3)、command-r7b(+5)
- **軽微な低下（-3〜-15点）:** gpt-oss-120b(-4)、gpt-oss-20b(-4)、ministral-3-8b(-7)、llama3.3(-11)、ministral-3-3b(-11)、gemma3n-e4b(-13)、aya-expanse-8b(-14)、phi4(-15)
- **大幅低下（既知の問題）:** command-r-35b(-24)、qwen3-14b(-21)、qwen3-4b(-34)、gemma2-9b(-67)、qwen3-30b(-96)

旧のベストは「設定を最適化した最高点」であるのに対し、新アーキテクチャは一律の設定（`--summary glossary`）で近い水準に達している。大幅低下の多くは既知の問題（qwen3-30b は構造化出力必須モデル、gemma2-9b は毎行「Let me know if you need anything else translated!」付加）によるもの。

**用語ブレの定性チェック（gemma3-27b）:**

旧 [tr-0/gemma3-27b-0-20-a.txt](tr-0/gemma3-27b-0-20-a.txt) と新 [tr/gemma3-27b.txt](tr/gemma3-27b.txt) を比較。

| 術語（原文） | 旧 | 新 | 一致 |
|---|---|---|:---:|
| pré-entraînement | pre-entrenamiento | pre-entrenamiento | ✓ |
| fine-tuning | ajuste fino (fine-tuning) | ajuste fino (fine-tuning) | ✓ |
| aprendizaje por transferencia | aprendizaje por transferencia | aprendizaje por transferencia | ✓ |
| ICL | aprendizaje en contexto, o ICL (In-Context Learning) | aprendizaje en contexto, o ICL (In-Context Learning) | ✓ |
| grounding | anclaje (grounding) | anclaje (grounding) | ✓ |
| bachoter | memorizar para un examen | memorizar para un examen | ✓ |
| Transformers | los Transformers | los Transformers | ✓ |
| ventana de contexto | ventana de contexto | ventana de contexto | ✓ |

術語ブレなし。文体面では新の方がスペイン語として自然な表現（親称統一、主語省略）を採用している箇所が複数あった。`--summary glossary` による用語一貫性は旧アーキテクチャと同等以上。

**用語ブレ確認 (qwen3-32b):**

`--summary glossary` により文書内一貫性は保たれているが、標準的な術語から逸脱する選択が発生：

- `fine-tuning` → 「ajuste fino」ではなく「**afinamiento**」で統一
- `ICL` → 標準略語ではなく独自略語「**AEC**」で統一

旧アーキテクチャでの用語ブレ（行ごとに訳語が揺れる現象）は解消されたが、モデル固有の術語選択の問題は残る。用語集の初期投入や強制的な用語指定が必要な場合はプロンプトレベルでの対策が必要。

---

## 軽量モデル分析：gemma4-e4b

軽量モデルの中で gemma4-e4b（95点）が突出しており、詳細を分析した。

### 項目別スコア

| 項目 | eval-1 | eval-2 | eval-3 |
|---|:---:|:---:|:---:|
| readability | 19 | 19 | 19 |
| fluency | 19 | 19 | 18 |
| terminology | **20** | 18 | 18 |
| contextual_adaptation | 19 | 19 | 19 |
| **information_completeness** | **20** | **20** | **20** |
| **合計** | **97** | **95** | **94** |

### 注目点：情報完全性が3回全て満点

`information_completeness` が3評価すべて20/20。上位大型モデルでも評価によって19点になるケースがある中で、情報の欠落・付加・歪曲が一切ないという評価を全回維持している。

### 減点の内容

減点はほぼ術語選択の問題に集中しており、構造的欠陥は皆無：

- **`anclaje`（grounding の訳）**: eval-2,3 で「NLP 専門文献では `fundamentación contextual` か英語維持が多い」と指摘。ただし上位大型モデルでも同じ選択をしているものが多く、評価者の好みの域を出ない
- **`ajuste fino`（fine-tuning の訳）**: eval-3 で「技術文脈では英語 `fine-tuning` を維持することも多い」と指摘。これも上位モデル全般に共通の選択
- **fluency -2（eval-3 のみ）**: `*prompt*` のマークアップ残りと上記の件が重なって2点減

### 軽量モデルとしての位置づけ

| モデル | スコア |
|---|:---:|
| gemma4-e4b | **95** |
| gemma3-12b | 95 |
| gemma4-e2b | 88 |
| gemma3-4b | 84 |
| gemma3n-e4b | 78 |

gemma4-e4b は gemma3-12b（数倍のパラメータ）と同点。減点理由の質も大型モデルと変わらず、「軽量モデルの限界」による問題（多言語混入・構造崩壊・情報欠落）が一切出ていない。リソース制約がある環境での第一候補として明確に評価できる。
