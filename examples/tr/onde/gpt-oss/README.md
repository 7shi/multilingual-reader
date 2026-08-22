# examples/tr/onde/gpt-oss/

onde テキストを対象とした追加言語を含む翻訳・評価を行います。

対象言語: [common.mk](../../common.mk) で定義された `CORE_LANGS` + `EXTRA_LANGS`

## 実行

`make` で翻訳・評価・集計を一括実行。

- 翻訳モデル: `gpt-oss:120b` (Ollama)
- 評価モデル: `qwen3.6` (Ollama)
- 設定: threshold=20・keep=5・CoT なし・用語ファイル注入（`../../terms/*-en.{json,tsv}`）

**出力先**: 翻訳 `tr/`、評価 `evals/`、スコア `SCORES.txt`

**注意点**: `gpt-oss:120b` は CoT（思考プロセス）の出力を無効にできないため、翻訳に非常に時間がかかります。本ディレクトリでの翻訳実行は、あくまで品質検証を目的としています。

## 翻訳品質の概要

評価結果（`SCORES.txt`）および内容の検証に基づく各言語の品質傾向は以下の通りです。

目安：高品質 (90点以上)、実用範囲 (80〜89点)、中品質 (60〜79点)、致命的な欠陥 (60点未満)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 98 | Minor missing speaker tags |
| French | 97 | Professional quality with occasional missing speaker tags |
| Catalan | 96 | High quality with missing speaker tags |
| Italian | 95 | Inconsistent speaker attribution formatting |
| Japanese | 94 | Inconsistent omission of speaker tags |
| Vietnamese | 93 | Missing speaker labels disrupts flow |
| Portuguese | 90 | Speaker labels dropped; technical accuracy high |
| Swedish | 89 | Missing speaker tags and minor grammatical errors |
| Ukrainian | 88 | Missing speaker tags and literal phrasing |
| Dutch | 86 | Accurate content marred by formatting and fluency issues |
| Arabic | 83 | Minor fluency and formatting issues |
| German | 83 | Frequent omission of speaker attribution tags |
| Turkish | 83 | Minor formatting and phrasing issues |
| Afrikaans | 81 | Missing speaker labels disrupt dialogue format |
| Bulgarian | 80 | Missing speaker attribution and formatting inconsistencies |
| Czech | 80 | Missing speaker tags and minor errors |
| Galician | 80 | Missing speaker labels and gender errors |
| Russian | 79 | Systematic omission of speaker tags |
| Chinese | 79 | Missed speaker attribution tags |
| Indonesian | 78 | Structural formatting errors |
| Danish | 77 | Missing speaker tags and grammatical errors |
| Hungarian | 77 | Structural flaws and grammatical errors |
| Nepali | 77 | Systemic grammatical errors and typos |
| Macedonian | 75 | Lack of proofreading and structural errors |
| Persian | 74 | Missing speaker tags disrupt flow |
| Interlingua | 73 | Inconsistencies between evaluations on quality and errors |
| Slovene | 73 | Significant formatting errors and grammatical fractures |
| Slovak | 71 | Critical omission of speaker labels and minor typos |
| Urdu | 70 | Inconsistent scientific transliteration and terminology |
| Belarusian | 69 | Notable terminology errors and formatting issues |
| Malay | 69 | Significant terminology errors and missing speaker labels |
| Norwegian | 69 | Missing speaker tags and awkward calques |
| Polish | 67 | Missing speaker labels |
| Tagalog | 67 | Significant linguistic and grammatical flaws |
| Greek | 66 | Significant terminology and structural errors |
| Azerbaijani | 65 | Missing speaker tags disrupt dialogue format |
| Hebrew | 65 | Missing speaker labels and grammatical errors |
| Korean | 65 | Missing speaker tags disrupt readability |
| Finnish | 63 | Missing speaker labels and typos |
| Latvian | 61 | Missing speaker labels and grammatical errors |
| Serbian | 61 | Missing speaker tags and formatting issues |
| Marathi | 60 | Pervasive orthographic errors |
| Swahili | 58 | Significant scientific terminology errors |
| Esperanto | 57 | Missing dialogue speaker tags |
| Croatian | 57 | Severe formatting and structural defects |
| Romanian | 56 | Significant structural and formatting defects |
| Malayalam | 54 | Pervasive orthographic and grammatical errors |
| Albanian | 54 | Missing speaker tags and grammatical errors |
| Estonian | 53 | Severe grammatical errors and terminology inaccuracies |
| Welsh | 52 | severe grammatical and terminology flaws |
| Mongolian | 52 | Heavy machine-translation artifacts and terminology errors |
| Bengali | 50 | Severe orthographic and grammatical errors |
| Kannada | 49 | pervasive linguistic and technical defects |
| Lithuanian | 48 | Major structural and terminological defects |
| Basque | 45 | Systematic grammatical errors and missing speaker labels |
| Icelandic | 45 | Grammatical errors and awkward calques |
| Thai | 42 | Pervasive orthographic errors throughout |
| Armenian | 41 | Frequent lexical and critical mistranslations |
| Hindi | 39 | Major typographical and formatting defects |
| Telugu | 39 | Severe mixed-script corruption and pervasive grammatical errors |
| Burmese | 38 | Severe spelling errors |
| Sinhala | 33 | Pervasive orthographic errors and unnatural phrasing |
| Khmer | 32 | Systematic orthographic errors and rigid syntax |
| Georgian | 31 | Severe grammatical and structural errors |
| Tamil | 30 | Severe orthographic and grammatical errors |
| Irish | 29 | Major grammatical and terminology defects |
| Lao | 23 | Critical terminology errors and mixed language |

全体を通して、モデルの規模に反して低リソース言語の翻訳は極めて不安定で、多言語の混入、状況認識の漏出、話者タグの脱落などが頻発しました。

## 過去の実験: OpenRouter との比較

当初は同一の処理をローカル（Ollama）とクラウド API（OpenRouter）の両環境で並行実行し、プロバイダー間の挙動の差異を検証していました。より厳密な検証のため、OpenRouterで生成した翻訳結果に対して、OpenRouterとOllamaの両方で評価を行っています（`openrouter/` 以下の `evals/` と `evals-ollama/`）。

以下の表は、3つの組み合わせによるスコアを示しています（ol: Ollama, or: OpenRouter）。
- **ol-ol**: ローカル翻訳・ローカル評価 (`SCORES.txt` から過去の8言語を抜粋)
- **or-ol**: クラウド翻訳・ローカル評価 (`openrouter/SCORES-ollama.txt`)
- **or-or**: クラウド翻訳・クラウド評価 (`openrouter/SCORES.txt`)

| 言語 | ol-ol | or-ol | or-or |
| :--- | :--- | :--- | :--- |
| トルコ語 | 83 | 89 | 87 |
| 朝鮮語 | 65 | 81 | 80 |
| セルビア語 | 61 | 81 | 53 |
| ヒンディー語 | 39 | 68 | 67 |
| エスペラント | 57 | 30 | 33 |
| テルグ語 | 39 | 31 | 30 |
| エストニア語 | 53 | 24 | 20 |
| カンナダ語 | 49 | 10 | 7 |
※ 対象言語は当時の8言語のみ。

これにより、以下の2つの視点で比較が可能になります。
- **翻訳モデルの実行環境の比較 (ol-ol vs or-ol)**: 評価者を Ollama に固定し、翻訳をどちらで行ったかの違い。各環境での実行は1回のみであるため、スコアの乱高下がプロバイダー間の差なのか、単なるサンプリングの揺らぎなのかは区別できません。しかし、どちらの環境であっても多くの低リソース言語で60点未満のスコアとなり、非実用的であることに変わりはないため、結果的には大差ないと言えます。
- **評価モデルの実行環境の比較 (or-ol vs or-or)**: 翻訳を OpenRouter に固定し、評価をどちらで行ったかの違い。

### エラー検知能力の完全な一致

同一の評価モデル（`qwen3.6`）を用いた場合、**ローカル（Ollama）でもクラウド（OpenRouter）でも、テキストに含まれる「文字化け」「他言語の混入」「プロンプトの漏洩」といったエラーを寸分違わず正確に検知・指摘する能力（読む力）を持っている**ことが証明されました。スコアに生じる数点〜10点程度のブレはプロバイダーの能力差ではなく、推論（サンプリング）ごとのランダムな揺らぎに過ぎません。

なお、セルビア語において `or-ol` (81点) と `or-or` (53点) で大きな評価の乖離が見られました。評価ログを確認したところ、OpenRouter で生成した翻訳テキストの途中に構造上の欠陥（`Cam… ... ... ...` という無意味な断片）が含まれており、Ollama と OpenRouter の両方の評価モデルが**この同じエラーを正確に検知**していました。しかし、Ollama 側の一部の評価プロセスがこのエラーを軽微なものとして無視して高得点（91点）を与えたのに対し、OpenRouter 側の評価プロセスはガイドラインに従い「致命的な構造的欠陥」として厳しく減点（24点、53点など）したため、平均スコアに大きな差が生じました。これも検知能力の差ではなく、評価の厳しさ（ペナルティの重み付け）のランダムな揺らぎによるものです。

### 構造化出力（JSONフォーマット）の安定性の違い

運用上の重要な知見として、構造化出力のバグの出方にプロバイダー間で明確な差が見られました。

- **OpenRouter（クラウド）**: 構造化出力が不安定になることがあり、`reasoning` フィールドに「無意味な内容」が入って出力が破損するケースが複数回発生しました。この場合、JSONの構文としては成立してしまうため、プログラムによるエラー検知が難しく、目視確認と手動での再実行が必要でした。
- **Ollama（ローカル）**: 無意味な内容が出力される破損は発生しませんでしたが、代わりに `overall_comment` フィールドの出力が「無限ループ」に陥る事象が一定割合で発生しました。ただし、こちらはツール側のループ検知機能によって自動的にリトライが行われるため、運用上の手間は抑えられています。

完全な自動化パイプラインを構築する上では、プロバイダーごとのこうした「ハルシネーションの出方のクセ」を考慮したエラーハンドリングが必要不可欠であることが示唆されています。
