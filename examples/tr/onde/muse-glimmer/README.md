# examples/tr/onde/muse-glimmer/

onde テキストを対象とした追加言語を含む翻訳・評価を行います。

対象言語: [common.mk](../../common.mk) で定義された `CORE_LANGS` + `EXTRA_LANGS`

## 実行

`make` で翻訳・評価・集計を一括実行。翻訳は `tr/`、評価は `evals/`、スコアは `SCORES.txt` に出力。

- 翻訳モデル: muse-glimmer
- 評価モデル: qwen3.6
- 設定: threshold=20・keep=5・CoT なし・用語ファイル注入（`../../terms/*-en.{json,tsv}`）

## 翻訳品質の概要

`make` 実行後、評価結果（`SCORES.txt`）および内容の検証に基づく各言語の品質傾向をここに追記する。

目安：高品質 (90点以上)、実用範囲 (80〜89点)、中品質 (60〜79点)、致命的な欠陥 (60点未満)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Portuguese | 96 | Minor grammar and filler word issues |
| Spanish | 95 | Minor lexical and idiomatic improvements needed |
| Italian | 95 | Minor terminology conventions and minor stylistic adjustments |
| Vietnamese | 93 | Excellent accuracy and natural flow |
| Japanese | 92 | Excellent quality with minor phrasing adjustments needed |
| Chinese | 91 | Minor literal phrasing affecting fluency |
| Catalan | 89 | Lexical mistranslations ('rosseca', 'ressecca') |
| Macedonian | 89 | Minor calques and stiff phrasing |
| Dutch | 89 | Minor stylistic and phrasing issues |
| Polish | 89 | Minor grammatical and fluency issues |
| Bulgarian | 86 | Literal conversational fillers disrupt fluency |
| Persian | 86 | Noticeable fluency issues and mixed-language defects |
| French | 85 | Grammatical errors and inconsistent register |
| Turkish | 85 | Minor fluency issues from literal calques |
| Danish | 84 | Minor grammatical errors and terminology issues |
| Galician | 82 | Notable lexical and morphological errors requiring proofreading |
| Korean | 82 | Non-standard terminology and code-switching detract from fluency |
| Urdu | 82 | Minor issues with terminology consistency and naturalness |
| Afrikaans | 80 | Untranslated English terms and typos |
| Lithuanian | 79 | Technical errors and unnatural phrasing |
| Arabic | 78 | Grammatical errors and duplicate line glitches hinder fluency |
| Slovak | 78 | Grammatical errors and lack of fluency |
| Ukrainian | 78 | Grammatical inconsistencies and literal calques |
| Malay | 76 | Terminology precision issues and Anglicisms |
| Romanian | 76 | Grammatical inconsistencies and lack of polish |
| Croatian | 75 | Recurring grammatical errors and mistranslations |
| German | 74 | Noticeable grammatical inaccuracies |
| Swedish | 74 | Noticeable grammatical awkwardness and duplication errors |
| Armenian | 73 | Calques and lack of natural flow |
| Serbian | 72 | Persistent grammatical errors and terminology mistranslations |
| Czech | 71 | Grammatical errors and awkward calques |
| Hungarian | 71 | Severe fluency issues and typos |
| Slovene | 71 | Grammatical errors and unnatural phrasing |
| Indonesian | 67 | Repetition of dialogue lines and terminology errors |
| Hebrew | 65 | Severe linguistic and terminology errors |
| Estonian | 64 | Numerous typos and technical errors |
| Azerbaijani | 63 | Literal calques and stiff syntax |
| Norwegian | 63 | Grammatical errors, unidiomatic math phrasing, and duplication artifacts |
| Basque | 62 | Mixed language errors and duplication artifacts |
| Swahili | 62 | Significant literal translation artifacts and terminology errors |
| Mongolian | 60 | Pervasive fluency issues and literal phrasing |
| Belarusian | 59 | Multiple machine-translation artifacts and errors |
| Georgian | 57 | Mixed-language artifact and key mistranslations |
| Finnish | 56 | Pervasive grammatical errors and unnatural phrasing |
| Latvian | 53 | Pervasive grammatical and terminology errors |
| Icelandic | 51 | Grammar and terminology errors |
| Welsh | 50 | Pervasive lexical and grammatical errors |
| Tagalog | 50 | Severe machine-translation artifacts and unnatural phrasing |
| Russian | 48 | Grammatical errors and repetition artifacts |
| Greek | 45 | Critical physics terminology errors and unnatural phrasing |
| Irish | 43 | Pervasive grammatical errors and unnatural phrasing |
| Albanian | 43 | Severe grammatical and syntactic defects |
| Telugu | 42 | Severe grammar and terminology flaws |
| Bengali | 41 | Severe orthographical and grammatical errors |
| Thai | 39 | Severe typographical and orthographic corruption |
| Hindi | 38 | Pervasive typographical and formatting errors |
| Esperanto | 36 | Critical terminology errors and grammatical defects |
| Marathi | 35 | Pervasive grammatical errors and unnatural syntax |
| Malayalam | 34 | Pervasive grammatical errors and unnatural syntax |
| Nepali | 34 | Severe machine-translation artifacts and broken syntax |
| Lao | 32 | Severe errors in technical terminology and fluency |
| Kannada | 29 | Severe technical and linguistic defects |
| Interlingua | 27 | Severe linguistic and structural flaws including code artifacts |
| Khmer | 24 | Severe corruption and unintelligibility |
| Sinhala | 23 | Severe grammatical and linguistic errors |
| Tamil | 21 | Pervasive repetitive loops and broken syntax |
| Burmese | 12 | Severe character corruption and structural breakdown |
