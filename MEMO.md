# メモ

## examples/ の翻訳言語戦略

`examples/` の多言語参照訳は以下の2段階方式で生成する。LLM の学習データ充実度を考慮し、英語を中継言語として活用することで重訳品質を確保する。

| ルート | 対象言語 | 備考 |
|---|---|---|
| FR → EN | English | 直接翻訳 |
| FR → ES | Spanish | 直接翻訳 |
| EN → DE | German | 英語からの重訳 |
| EN → JA | Japanese | 英語からの重訳 |
| EN → ZH | Chinese | 英語からの重訳 |
| EN → EO | Esperanto | 英語からの重訳（onde のみ） |
| EN → HI | Hindi | 英語からの重訳（onde のみ） |

評価は各ルートの原文を基準とする（EN/ES は FR と比較、DE/JA/ZH/EO/HI は EN と比較）。`examples/evals/` の eval ファイル名は `{topic}-{from}-{to}-{run}.json` 形式で言語ルートを明示する。

**共通語彙（`examples/terms/common.tsv`）**: 番組名など全トピック共通の固有名詞はここに記載し、`trtools term translate -c common.tsv` で LLM をスキップして採用する。LLM に任せると run ごとに訳語がブレるため、番組名は必ずここで固定する。

### examples/terms/ の用語TSVは校正が必要

`trtools term extract/translate` でローカル LLM（gemma4:31b）が生成した用語 TSV は、以下のような誤りが含まれるため**校正が必要**。

- **スラッシュ2択**: `refinement/fine-tuning`・`接地/锚定` のように訳語を絞り切れず複数形式で出力する
- **誤訳**: `balle de baseball` → `baseball`（ball が欠落）など
- **余分テキスト混入**: ` evanescent waves ( evanescent waves / 消逝波)` のように原語が訳語欄に混入する
- **誤字**: `ultrastreine`（→ `ultrafeine`）など

### examples/tr-fr/: FR→EN・FR→ES 参照訳の再生成

現行の `examples/` 参照訳（英語: Gemini 翻訳＋Claude レビュー、スペイン語: Gemini 2.5 Pro）を gemma4-26b で再生成し、手動添削の上で置き換える。

**フロー**: `make translate` → 添削 → `make evaluate` → `examples/` 置き換え。初回評価を無駄にしないため、添削後に評価を実施する。`trtools batch` のデフォルト（`--tr-runs 1`）でサフィックスなしのファイル名（`tr/finetuning-en.txt` 等）を生成する。

- **翻訳**: `make translate`（`trtools batch --translate-only`、評価・集約なし）
- **評価**: `make evaluate`（`trtools batch --evaluator ollama:qwen3.6`、翻訳済みファイルをスキップ）
- **一括**: `make` または `make all`（translate → evaluate の順に実行）
- **対象**: finetuning・transformer・onde・momentum の4トピック × FR→EN・FR→ES
- **設定**: gemma4-26b・threshold=10・keep=5・CoT なし・用語ファイル注入（`examples/terms/*-fr.{json,tsv}`）

#### 結果サマリー（初回実施）

**FR→ES は全面差し替え**、**FR→EN は旧訳を維持**。

| トピック | FR→EN | FR→ES |
|---|:---:|:---:|
| finetuning | 旧訳維持（100→97） | 差し替え（97→97） |
| transformer | 旧訳維持（97→97） | 差し替え（94→96） |
| onde | 旧訳維持（96→97） | 差し替え（97→97） |
| momentum | 旧訳維持（100→96） | 差し替え（92→97） |

FR→EN は旧訳（Gemini 翻訳＋Claude レビュー）が上質なため維持。主な差異：

- **短縮形の一貫性**: 旧訳は "I'm" / "we're" / "it's" / "you've" を全体で統一。新訳は "I am" / "It is" と短縮形が混在し、ポッドキャストとして不統一
- **慣用句**: 旧 "pull back the curtain on"（より口語的）vs 新 "lift the veil on"（フランス語 "lever le voile" の直訳感が残る）
- **相槌**: 旧 "You've got it."（自然な会話調）vs 新 "You have understood it perfectly."（硬い）
- **比喩表現**: 旧 "the physics of balance"（バイクの例として正確）vs 新 "how to balance"（意訳）

FR→ES は旧訳（Gemini 2.5 Pro）より全体的に同等以上で差し替え。

`examples/` への反映: `*-es.txt`（4ファイル）と `examples/evals/*-fr-es-*.json`（12ファイル）を差し替え済み。

#### 添削所感（初回生成時）

gemma4-26b の生成品質は全体的に高く、構造的欠陥はほぼなし。主な指摘パターン：

- **スピーカータグ欠落**: momentum-es（4箇所）・onde-es（1箇所）。モデルが短い相槌行（"¿Oh?"・"De acuerdo." 等）のタグを落とす傾向あり
- **フランス語直訳の残留**: momentum-en "angular momentum"（文脈上は linear momentum）・transformer-en "The discussion is open."（→ "The floor is yours."）・momentum-en "calls the world into question"（→ "calls everything into question"）
- **英語の冗長表現**: momentum-en "baseball ball"（→ "baseball"）・finetuning-en "laws of balance"（→ "how to balance"）
- **視点の混在**: finetuning-en "before it starts talking to **you**"（→ "**us**"、ES版 "nosotros" と不一致）
- **用語の不統一**: momentum-es で "momentum"（英語借用）・"momento"・"cantidad de movimiento" が混在（→ "momento" に統一）
- **専門用語の誤訳**: transformer-es "atención multi-**cabezal**"（→ "multi-**cabeza**"）

EN 訳は概ね高品質だが、フランス語慣用句の直訳が残りやすい。ES 訳はスピーカータグ欠落と用語揺れが課題。いずれも文意は正確で添削コストは低い。

### examples/tr-en/: EN→DE・EN→JA・EN→ZH 参照訳の再生成

英語版（`*-en.txt`）を中継言語としてドイツ語・日本語・中国語、および onde のみエスペラント・ヒンディー語へ翻訳する。

**tr-fr との依存関係**: 英語ファイルが翻訳・添削・確定済みであることが前提。英語版が置き換わると用語の文脈も変わるため、`examples/terms/batch.sh` で `*-en.{json,tsv}` を再生成・校正してから `examples/tr-en/` に入る。

tr-fr と同じフロー（`make translate` → 添削 → `make evaluate`）。`others`（finetuning・transformer・momentum）と `onde` を別 BATCH_BASE 変数で管理し、`translate`・`evaluate` ターゲットがそれぞれ両方を実行する。

- **翻訳**: `make translate`（`--translate-only`、評価・集約なし）
- **評価**: `make evaluate`（`--evaluator ollama:qwen3.6`、翻訳済みファイルをスキップ）
- **一括**: `make` または `make all`（translate → evaluate の順に実行）
- **対象**: finetuning・transformer・momentum × EN→DE・EN→JA・EN→ZH、onde × EN→DE・EN→JA・EN→ZH・EN→EO・EN→HI
- **設定**: gemma4-26b・threshold=20・keep=5・CoT なし・用語ファイル注入（`examples/terms/*-en.{json,tsv}`）

---

## 実験の流れ

### translate.py: 実験系列の起源

ルートの `translate.py` が experimental 系列の出発点。構造化出力（`generate_with_schema` + Pydantic）で推論レベル 0〜2 を実装し、直近5件のスライディング方式で文脈を管理。

### 初期試行（OBSOLETE）: 多モデル協調フェーズ

`translate.py` の成果をベースに `translate-exp.py`・`translate2.py`・`translate3.py` を作成し、多モデル協調（Phase 2a）を試みた段階。詳細は `experimental/OBSOLETE.md`。

**試みた手法**:
- Phase 1: gemma3n:e4b で初回翻訳
- Phase 2a: qwen2.5:7b で品質チェック＋修正を統合実行
- 最終的に `translate3.py`（一気通貫版）が「92点」として最推奨に

**行き詰まりと仕切り直しの理由**:
- 評価が Claude Code による主観的な1回評価で、採点基準・rubric なし
- 評価の根拠が不明確なため、スコアの信頼性に疑惑が生じた
- ad hoc な手法の積み上げで体系的な比較が困難
- → experimental/ として評価方式から設計し直すことになった

### 評価言語ペアの選定方針

実験全体を通じて翻訳タスクは**フランス語→スペイン語**（FR→ES）を基準軸に採用している。

- **英語↔西欧語**は LLM の学習データが最も充実しており最高精度が「当たり前」のため、モデル間差異が出にくく評価軸として不適切
- **ロマンス語間**（FR↔ES）は言語距離が適度に近く、術語・慣用表現・文化的ローカライズで差が出やすい。97〜100点帯での細かい差別化が可能
- 日本語・中国語・ドイツ語等は参照訳の品質確認には使えるが、評価者（qwen3.6）の得意不得意が結果に影響しやすい

`examples/` の参照訳を評価した結果、英語訳（Gemini 翻訳 + Claude レビュー）は中央値100点を達成。FR→ES（Gemini 2.5 Pro）が97点止まりだったことは、評価者の英語優位バイアスを示すとともに、FR→ES を実験軸に選んだ設計判断の妥当性を裏付けている。

### experimental/: 推論レベル別性能分析

**目的**: 構造化出力の推論レベル（0〜4）が翻訳品質に与える影響を体系的に分析。評価方式を5項目・複数回に刷新し、初期試行の主観評価を排除した仕切り直し実験。ただし評価者モデルの選定に手間取り、最終的に Qwen 3.6 35B-A3B を採用した。評価者の変遷は以下の通り：
- **Gemini 2.5 Flash**: 初期評価者
- **GPT-OSS 120B**: 移行を試みたが 92点が上限で上位モデルの差別化が困難なため廃止
- **Qwen 3.6 35B-A3B**: 最終採用。CoT による論理的検証で技術的欠陥を正しく特定

`experimental/translate.py` はルートの `translate.py` の直系発展版（推論レベルを 0〜4 に拡張、`--history`・`--no-think`・`--translated-context` 追加）。コア構造（スライディング履歴・プロンプト埋め込み方式）は共通。

**主な課題の発見**:
- スライディング方式の履歴管理では古い履歴が押し出されると**用語ブレ**が発生
- プロンプト先頭が毎回変化するため **KV キャッシュが無効**

**主な知見**:
- 推論レベルを上げても翻訳品質は改善しない（逆効果）。レベル1（構造化推論）の中央値は59点と全体で最低
- レベル0（直接翻訳）が最も安定・高品質。モデルに合わせて構造化/非構造化を選ぶことが重要
- 評価者として qwen3.6 を採用（CoT による論理的検証が有効。GPT-OSS 120B は天井効果で廃止）
- 次期アーキテクチャへの方針：用語集付きサマリー圧縮へ移行

### experimental2/: サマリー圧縮方式への移行

**目的**: experimental/ の課題（用語ブレ・KV キャッシュ無効）を解決する新アーキテクチャの検証。

**解決策**: `system + summary + 直近N件` の固定構造
- `--summary glossary`: 翻訳しながら逐次用語集を積み上げ、後半ほど一貫性が高まる
- `--no-think`: 翻訳タスクに CoT は過剰。速度・品質・KV キャッシュの三点で有利
- `--schema`（構造化出力）廃止: gemma4:31b の glossary-schema=62点が象徴的。翻訳タスクには不要

**主な知見**:
- 34モデルの本番実験（Phase B）で上位モデルが 95〜97点を達成
- 評価者（qwen3.6）では **97点が実質的な上限**（天井効果）
- **gemma4-26b** が最優秀：スコア安定性最高（範囲1）、構造的欠陥ゼロ
- 旧アーキテクチャのベストと新アーキテクチャの一律設定が同等水準に達することを確認

**残課題**:
- 要約を翻訳履歴に含めると翻訳スタイルへの干渉リスクがある（理論的懸念）

### experimental3/: ハイブリッドモード

**目的**: 要約を翻訳履歴から除外することで、スタイル干渉を回避しつつ KV キャッシュ効率を維持する。

**解決策**: 翻訳本体は CoT なし（速度・安定性・KV キャッシュ）、要約生成のみ CoT あり（複数情報の統合判断）。要約は再編成タイミングまで履歴から除外されるため、翻訳ループの KV キャッシュが汚染されない。

**実験設定**: Phase B 上位3モデル（qwen3.6-27b・gemma4-26b・gemma4-e4b）× 翻訳3回 × 評価3回

**スコア結果**（推奨設定 threshold=10・CoT なし）:

| モデル | run 1 | run 2 | run 3 |
|---|:---:|:---:|:---:|
| qwen3.6-27b | 96 | **86**（急落） | 94 |
| gemma4-26b | 96 | 100 | 96 |
| gemma4-e4b | 95 | 96 | **85**（急落） |

**主な知見**:
- threshold・CoT 有無による翻訳品質の有意差なし
- 急落はどの設定でも **glossary 初期蓄積のブレ**によって確率的に発生（設定依存ではない）
- gemma4-e4b で要約履歴除外による急落ダメージ軽減の兆候あり（サンプル数が少なく断定は保留）
- **推奨設定**: threshold=10・CoT なし（処理時間最短、品質劣化なし）

**モデル別推奨**:
- **gemma4-26b**: 第一推奨。全設定・全 run で急落なし。評価者（qwen3.6）と異なるアーキテクチャのため自己評価バイアスも排除できる
- **gemma4-e4b**: リソース制約がある場合の代替。急落リスクは残るが threshold=10 で一定の品質を確保
- **qwen3.6-27b**: 積極採用の理由に乏しい。急落リスクあり、KV キャッシュが効かず処理時間も長い

### experimental4/: 用語事前抽出方式

**目的**: 翻訳フローの改善。用語集を翻訳前に確定・編集可能にすることで、「用語集を修正してから翻訳」というワークフローを実現する。性能向上が目的ではなく、用語の一貫性制御を人間が介入できる形にすることが主眼。副次的には glossary 初期蓄積のブレを翻訳ループ外に切り出す効果もある。

**解決策**:
- **Phase 0（前処理）**: 入力を `keep` 行ごとのチャンクに分割し、チャンク単位で用語を構造化出力で抽出。全用語を統合・重複除去後、1回の構造化出力で一括翻訳。結果を `<output_base>-terms.json` に保存（既存ファイルがあれば再利用）
- **Phase 1（翻訳ループ）**: experimental3 の threshold+keep 方式を踏襲。再編成のたびに「次の threshold+keep 行に登場する用語のみ」に絞って chat_history に注入する
- CoT は全段で無効（翻訳・要約・抽出・訳生成すべて think=False）

**実験設定**: gemma4-26b・gemma4-e4b × 翻訳3回 × 評価3回（qwen3.6-27b は急落リスクと KV キャッシュ非効率のため除外）

**スコア結果**:

| モデル | run 1 | run 2 | run 3 |
|---|:---:|:---:|:---:|
| gemma4-26b | 96 | 96 | 99 |
| gemma4-e4b | 95 | 96 | **92**（急落） |

**主な知見**:
- **フロー改善が主効果**: 用語集を JSON ファイルとして出力することで、翻訳前に人手で確認・修正→再翻訳というワークフローが可能になった
- **gemma4-e4b の急落が軽減（副次効果）**: 85点 → 92点。ただし「ブレを翻訳ループから用語抽出フェーズに移しただけ」であり、用語抽出自体も run 間でブレる（`affinage` の訳語が `refinamiento` / `ajuste fino` に分かれるなど）
- **gemma4-26b は安定維持**: 急落なし。run 3 が 96→99 と微改善
- **一般語の混入**: `mathématiques`・`physicien`・`anglais` など専門用語ではない語が抽出される。プロンプトの改善余地あり

---

## 翻訳の trtools への統合

experimental/ 〜 experimental4/ の知見を反映した翻訳・評価ツールを `trtools` パッケージとして実装・整備した。

- `trtools translate`: experimental3 の推奨設定（threshold=10・CoT なし・サマリー圧縮）をベースに、用語注入・スキップ付き空行保持を実装。構造化出力・スライディング履歴といった旧設計は廃止
- `trtools term extract/translate`: 用語抽出・訳語確定を翻訳ループから分離。校正済み TSV を全 run で共有することで run 間の用語ブレを排除
- `trtools eval / agg`: 5項目×20点・3回評価の中央値集計
- `trtools batch`: 翻訳→評価→集約を一括実行。入力ファイルをオプションなし引数で列挙し、ファイル名から topic・言語コードを自動導出。`examples/tr-fr/Makefile` から呼び出す形で本番運用に移行

### experimental5/: trtools translate への移行

**目的**: 用語抽出を `trtools term` として分離・校正済みのため、翻訳を `trtools translate` で実行する。全 run が同一の校正済み用語辞書を共有することで、experimental4 で残存していた run 間の用語ブレ（`affinage` → `refinamiento` / `ajuste fino`）を原理的に排除する。

**解決策**:
- 用語は `examples/terms/finetuning-fr.{json,tsv}` として事前に抽出・校正済みの共有ファイルを使用
- 翻訳は `uv run trtools translate --terms-json ... --terms-tsv ...` で実行
- experimental4 と同一設定（threshold=10・keep=5・CoT なし）

**実験設定**: gemma4-26b・gemma4-e4b × 翻訳3回 × 評価3回

**スコア結果**:

| モデル | run 1 | run 2 | run 3 |
|---|:---:|:---:|:---:|
| gemma4-26b | 95 | 96 | 97 |
| gemma4-e4b | 95 | 95 | 94 |

**主な知見**:
- **gemma4-e4b の急落が解消**: experimental4 の 92点（急落）が消え、94〜95点で安定。共有用語辞書による run 間ブレ排除の効果が確認された
- **gemma4-26b**: 上限が 99→97 に下がったが 95〜97 の範囲で安定維持。急落なし。減点はほぼ `antisèche` の訳語選択（`acordeón` の地域差）のみで構造的欠陥なし
- **gemma4-e4b**: run によって発言者ラベル消失・人称不統一といった軽微な構造的問題が出るが、リソース制約環境向けの割り切りモデルとして許容範囲
- **評価者の検出漏れ**: 発言者消失を 3回中 2回見落とし（93〜94点）。qwen3.6 の検出精度に限界がある

### 評価速度についての所感

翻訳を `--no-think` で最適化した結果、翻訳フェーズよりローカル評価（qwen3.6 × 3evalrun = 72回）がボトルネックになった。以前は翻訳が非効率だったためクラウド（Gemini 2.5 Flash）の評価が相対的に高速だったが、翻訳最適化後はその関係が逆転している。評価の CoT 出力を無効化すれば高速化できるが、減点理由の正確な特定が qwen3.6 の CoT に依存しているため、速度より信頼性を優先してこれ以上の最適化は行わない。

---

## 次のステップ

### TODO: examples/ のエスペラント・ヒンディー語訳を再作成

`examples/evals/` の評価結果より、`onde-eo`（中央値10点）・`onde-hi`（中央値13点）は構造的欠陥レベルで参照訳として使用不可。量子力学・近接場顕微鏡などの専門用語をこれらの言語では正確に扱えなかったと推定される。

**対応方針**: `trtools batch` で `onde-eo.txt`・`onde-hi.txt` を再翻訳し、`examples/evals/` の該当評価ファイルも再実行する。

---

## 将来の検討事項

現在の実験は43行のポッドキャストスクリプトが対象だが、最終目標は**小説1冊の丸ごと翻訳**（数万行・数十万トークン規模）。たった43行でもモデル選定・KV キャッシュ・用語統一・評価方式と課題が山積みであり、小説ではさらに登場人物の一貫性・伏線・文体の維持・章をまたぐ文脈など次元が違う難しさが加わる。一方で、この実験を通じてサマリー圧縮・事前用語抽出・CoT 不使用といった基盤となる設計判断が固まりつつあり、スケールアップ時の問題が見えやすくなっている。そのスケールで生じる課題と検討事項：

- **階層的コンテキスト**: 直近セクションは詳細要約、遠いセクションは粗筋、という粒度付きの要約管理。現在の単一サマリー方式では対応しきれない。
- **RAG**: 翻訳対象の行だけを見ていると前提条件を知らずに誤訳する可能性がある（例：「このシーンで言及された人物は何者か」「この伏線は何章で回収されたか」）。理想は1冊丸ごとコンテキストに入れて長距離参照することだが、ローカルで動くモデルの実用限界は 32K トークン程度であり、設定上は大きくできても巨大コンテキストでは取りこぼしが発生する。単なる要約では長距離参照が失われるため、関連チャンクを動的に検索して渡す RAG が現実的な対策になる可能性がある。
