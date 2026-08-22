# examples/tr/onde/qwen3.6/

Translation and evaluation of the onde text, covering an extended set of languages.

Target languages: `CORE_LANGS` + `EXTRA_LANGS` defined in [common.mk](../../common.mk)

## Running

`make` runs translation, evaluation, and aggregation in one batch. Translations go to `tr/`, evaluations to `evals*/`, and scores to `SCORES*.txt`.

- Translation model: qwen3.6
- Evaluation model: qwen3.6 (gpt-oss:120b for comparison)
- Settings: threshold=20, keep=5, no CoT, term file injection (`../../terms/*-en.{json,tsv}`)

## Translation quality overview

The quality trend for each language, based on the evaluation results (`SCORES.txt`) and manual content verification (evaluator: `qwen3.6`), is as follows.

Guide: high quality (90+), practical range (80-89), medium quality (60-79), critical defects (below 60)

| Language | Score | Trend Analysis |
| --- | ---: | --- |
| Spanish | 97 | Minor stylistic tweaks could be applied for absolute idiomatic perfection in spoken physics contexts |
| French | 97 | Untranslated English word 'ripple' |
| Portuguese | 97 | Flawless professional-grade execution |
| Italian | 96 | Minor anglicisms retained (perplexing) |
| Romanian | 92 | Minor typos and grammatical slips |
| Dutch | 91 | Minor terminology errors and unidiomatic phrasing |
| Russian | 91 | Minor typos and lexical slips |
| Vietnamese | 91 | Minor unpolished phrasing and code-switching |
| German | 89 | High quality with minor grammatical and terminology issues |
| Persian | 89 | Minor stylistic and transliteration issues |
| Galician | 89 | Portuguese lexical interference and minor phrasing issues |
| Norwegian | 86 | Minor grammatical and typographical errors |
| Chinese | 86 | Minor fluency and terminology issues |
| Serbian | 85 | Minor terminology and typo errors |
| Croatian | 83 | Minor grammatical and terminology errors |
| Hungarian | 83 | Numerous typographical errors and typos |
| Swedish | 80 | Machine translation artifacts and fluency issues |
| Afrikaans | 78 | Pervasive Dutch interference and lexical calques |
| Catalan | 78 | Multiple grammatical errors disrupt natural flow |
| Lithuanian | 77 | Lexical errors and non-idiomatic phrasing |
| Danish | 76 | Mixed-language artifact and minor errors |
| Japanese | 76 | Mixed language artifacts (Chinese and English) |
| Korean | 75 | Inconsistent terminology and untranslated English terms |
| Ukrainian | 73 | Noticeable grammatical errors and awkward phrasing |
| Polish | 72 | Grammatical errors and typos disrupt fluency |
| Albanian | 71 | Noticeable linguistic and grammatical flaws |
| Hebrew | 70 | Prominent typographical and grammatical errors disrupt fluency |
| Czech | 68 | Grammatical errors and unnatural phrasing |
| Belarusian | 66 | High density of errors and typos |
| Latvian | 65 | Pervasive machine-translation artifacts and grammatical errors |
| Turkish | 63 | Recurring mistranslation of "Kader" |
| Slovak | 62 | Grammatical errors and awkward phrasing |
| Greek | 61 | Critical terminology errors and untranslated English words |
| Indonesian | 55 | Critical mixed-language fragment and terminology errors |
| Malay | 55 | Technical terminology errors and mistranslations |
| Estonian | 53 | Frequent errors and poor terminology |
| Bulgarian | 50 | Pervasive MT artifacts and lexical errors |
| Urdu | 50 | Severe lexical errors and foreign text insertion |
| Finnish | 49 | Severe grammatical errors and mixed-language artifacts |
| Slovene | 48 | Pervasive untranslated English fragments and grammatical errors |
| Azerbaijani | 46 | Severe terminology errors and grammatical flaws |
| Armenian | 46 | Significant fluency and accuracy issues |
| Macedonian | 46 | Severe grammatical errors and inaccurate terminology |
| Lao | 45 | Severe physics terminology errors and unnatural phrasing |
| Bengali | 42 | Pervasive typos and structural breaks |
| Mongolian | 42 | Severe lexical and grammatical errors impair readability |
| Telugu | 39 | Severe grammatical and technical terminology errors |
| Kannada | 38 | Pervasive orthographic and grammatical errors |
| Marathi | 38 | Severe linguistic flaws and poor fluency |
| Nepali | 37 | Pervasive typos and flawed terminology |
| Georgian | 36 | Severe lexical mistranslations and grammatical errors |
| Arabic | 33 | Persistent Chinese character intrusion and mixed-language artifacts |
| Icelandic | 33 | P pervasive grammatical and typographical errors with technical mistranslations |
| Interlingua | 32 | Severe mixed-language contamination |
| Malayalam | 32 | Severe orthographic and grammatical defects |
| Sinhala | 32 | Pervasive character corruption and major defects |
| Swahili | 32 | Severe machine-translation artifacts and technical errors |
| Irish | 30 | Severe grammatical errors and incorrect terminology |
| Khmer | 30 | Severe typos and terminology errors |
| Hindi | 29 | Catastrophic typos and scientific mistranslation |
| Welsh | 27 | Pervasive severe machine-translation artifacts |
| Esperanto | 27 | Severe grammatical and lexical failures |
| Thai | 26 | Severe orthographic and linguistic corruption |
| Tagalog | 25 | Severe machine translation artifacts and lexical errors |
| Basque | 23 | Severe lexical, grammatical, and terminological defects |
| Burmese | 19 | Massive text-generation loop |
| Tamil | 18 | Catastrophic orthographic and spelling corruption |

## 過去の実験: gpt-oss:120b による評価との比較

`qwen3.6` による評価（`evals/`）に加え、比較検証用として `gpt-oss:120b` による評価も実施しました。結果は `gpt-oss-120b/` ディレクトリに保存されています（評価 `gpt-oss-120b/evals/`、スコア `gpt-oss-120b/SCORES.txt`）。

| 言語 | qwen3.6 | gpt-oss |
| :--- | :--- | :--- |
| エストニア語 | 53 | 84 |
| セルビア語 | 85 | 79 |
| トルコ語 | 63 | 77 |
| 朝鮮語 | 75 | 74 |
| カンナダ語 | 38 | 73 |
| エスペラント | 27 | 64 |
| テルグ語 | 39 | 62 |
| ヒンディー語 | 29 | 43 |
※ 対象言語は当時の8言語のみ。

これらの評価ログを比較すると、両モデルとも**「翻訳テキストに含まれるエラー（プロンプトの混入、漢字の幻覚、致命的な誤訳など）を正確に検知・指摘する能力」については非常に高く、同等に機能している**ことが分かりました。

しかし、そのエラーに対して**「どのように点数をつけるか（採点基準）」において、両者に極端な違い**があり、結果として「自己評価の方が圧倒的に厳しくなる」という興味深い現象が確認されました。

1. **qwen3.6（自己評価）の傾向：容赦ない減点方式（文法警察）**
   `qwen3.6` は自身が生成した翻訳の「文法エラー、正しくない語形変化、スペルミス、不自然な直訳」を正確に検知した上で、「抜本的な書き直しが必要」「完全に破綻している」と自分自身を容赦なく酷評し、**極めて低いスコア（20〜40点台）**をつけています。

2. **gpt-oss:120b（他者評価）の傾向：意味重視の加点方式（寛容さ）**
   対して `gpt-oss:120b` は、漢字の混入や誤訳といった致命的なエラーを正しくログに列挙して指摘しているにもかかわらず、「全体として科学的な内容は伝わる」と文脈のゲシュタルト性を高く評価し、**比較的高めのスコア（60〜80点台）**を与える傾向がありました。
