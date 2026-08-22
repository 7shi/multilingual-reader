# examples/tr/onde/qwen3.8/

onde テキストを対象とした追加言語を含む翻訳・評価を行います。

対象言語: [common.mk](../../common.mk) で定義された `CORE_LANGS` + `EXTRA_LANGS`

## 実行

`make` で翻訳・評価・集計を一括実行。翻訳は `tr/`、評価は `evals/`、スコアは `SCORES.txt` に出力。

- 翻訳モデル: qwen3.8
- 評価モデル: qwen3.6
- 設定: threshold=20・keep=5・CoT なし・用語ファイル注入（`../../terms/*-en.{json,tsv}`）

## 翻訳品質の概要

`make` 実行後、評価結果（`SCORES.txt`）および内容の検証に基づく各言語の品質傾向をここに追記する。

目安：高品質 (90点以上)、実用範囲 (80〜89点)、中品質 (60〜79点)、致命的な欠陥 (60点未満)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Portuguese | 98 | Exemplary scientific and conversational quality |
| French | 97 | Professional-grade scientific accuracy with natural podcast tone |
| Italian | 95 | Minor terminology refinement needed for 'psi quadro' |
| Chinese | 95 | Publication-ready quality with minor stylistic tweaks suggested |
| Spanish | 92 | Minor grammatical inconsistencies and oversights |
| German | 91 | Minor lexical and terminology issues |
| Catalan | 90 | Minor grammatical errors and calques |
| Vietnamese | 90 | Minor grammatical and typographical slips |
| Romanian | 89 | Minor grammatical and terminology flaws |
| Turkish | 88 | Minor fluency and typographical errors |
| Ukrainian | 86 | Linguistic unpolish and unnatural phrasing |
| Russian | 85 | Mixed-language glitch and awkward phrasing |
| Swedish | 85 | Minor grammatical errors and literal phrasing |
| Danish | 83 | Grammatical errors and typos |
| Arabic | 77 | Fluency and terminology issues despite scientific accuracy |
| Macedonian | 77 | Technical accuracy hampered by typos and poor fluency |
| Dutch | 77 | Untranslated English word 'easily' and terminology errors |
| Polish | 77 | Grammatical errors and literal calques |
| Galician | 75 | Lexical inaccuracies and Portuguese interference |
| Norwegian | 71 | Systematic typos and incorrect math notation |
| Afrikaans | 68 | Noticeable lexical errors and unnatural phrasing |
| Lithuanian | 67 | Persistent grammatical errors and non-standard terminology |
| Serbian | 65 | Frequent grammatical errors and terminology mistakes |
| Czech | 60 | Mixed-language intrusion and literal calques |
| Indonesian | 60 | Chinese character insertion and terminology errors |
| Croatian | 59 | Frequent typos and technical inaccuracies |
| Urdu | 59 | Major lexical errors and unnatural phrasing |
| Bulgarian | 58 | Pervasive grammatical errors and terminology mistakes |
| Hindi | 57 | Pervasive literalism and terminology errors |
| Japanese | 56 | Severe mixed-language artifacts and unnatural phrasing |
| Hungarian | 55 | Significant technical terminology errors and unnatural phrasing |
| Marathi | 54 | Persistent grammatical errors and unnatural phrasing |
| Interlingua | 53 | Severe mixing of non-Interlingua languages and terms |
| Nepali | 52 | Severe artifacts including Chinese characters and semantic errors |
| Albanian | 52 | Severe lexical and grammatical errors |
| Persian | 50 | Mixed Chinese character insertion |
| Slovak | 50 | Frequent grammatical errors and unnatural calques |
| Slovene | 50 | Severe linguistic and technical defects |
| Bengali | 42 | Significant mistranslations and unnatural phrasing |
| Malay | 42 | Severe structural and dialogue management failures |
| Belarusian | 37 | Severe grammatical errors and terminology inaccuracies |
| Estonian | 33 | Severe terminology errors and grammatical defects |
| Tagalog | 33 | Severe mistranslation and hallucination of physics terms |
| Azerbaijani | 32 | Severe linguistic and semantic errors |
| Hebrew | 32 | Severe semantic and lexical errors |
| Georgian | 32 | Pervasive machine artifacts and severe errors |
| Greek | 31 | Severe mixed-language fragments and terminology errors |
| Esperanto | 31 | Pervasive major defects |
| Latvian | 31 | Severe grammatical and terminological errors |
| Tamil | 30 | Severe structural defects and mixed scripts |
| Korean | 29 | Severe truncation and mixed-language fragments |
| Thai | 28 | Abrupt mid-sentence cutoff and technical errors |
| Armenian | 27 | Catastrophic semantic and structural failure |
| Welsh | 26 | Fundamentally broken with severe lexical and grammatical defects |
| Basque | 26 | Massive repetition glitch |
| Khmer | 26 | Severe machine translation artifacts and gibberish |
| Kannada | 26 | Severe lexical defects and mixed scripts |
| Swahili | 26 | Severe lexical and technical errors |
| Telugu | 26 | Pervasive scientific inaccuracies and severe linguistic defects |
| Mongolian | 23 | Severe structural defects and meta-commentary intrusion |
| Malayalam | 22 | Severe lexical errors and structural breakdowns |
| Burmese | 22 | Severe lexical and grammatical errors |
| Icelandic | 21 | Pervasive severe mistranslations of core physics terminology |
| Lao | 21 | Severe machine translation artifacts |
| Sinhala | 20 | Severe terminology mismatches and broken syntax |
| Irish | 9 | Severe truncation and critical structural failure |
| Finnish | 0 | Severely truncated and structurally broken translation |
