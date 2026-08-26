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
| Spanish | 97 | Exceptional quality with minor stylistic nuances |
| French | 97 | Retention of English word 'ripple' |
| Portuguese | 97 | Flawless high-quality work |
| Italian | 96 | Retained English word 'perplexing' |
| Romanian | 92 | High quality with minor typos and slips |
| Dutch | 91 | Minor calques and terminology errors |
| Russian | 91 | Minor typos and stiff phrasing |
| Vietnamese | 91 | Minor code-switching and fluency issues requiring light proofreading |
| German | 89 | Minor grammatical and terminology imperfections |
| Persian | 89 | Minor stylistic calques and transliterations |
| Galician | 89 | Portuguese lexical interference |
| Norwegian | 86 | Minor grammatical errors and awkward technical phrasing |
| Chinese | 86 | Accurate terminology hindered by literal phrasing |
| Serbian | 85 | Minor terminology errors like 'Abov limit' and typo 'divirira' |
| Croatian | 83 | Minor grammatical and terminology errors |
| Hungarian | 83 | Numerous typographical errors |
| Swedish | 80 | Clear signs of machine translation and literal phrasing |
| Afrikaans | 78 | Pervasive Dutch interference and typographical errors |
| Catalan | 78 | Multiple major grammatical errors |
| Lithuanian | 77 | Lexical errors and grammatical imperfections |
| Danish | 76 | Mixed-language artifact ('actually kender, faktum') |
| Japanese | 76 | Critical mixed-language artifacts disrupt fluency |
| Korean | 75 | Untranslated English words and technical inconsistencies |
| Ukrainian | 73 | Notable grammatical errors and awkward phrasing |
| Polish | 72 | Grammatical and typographical errors |
| Albanian | 71 | Grammatical errors and non-idiomatic phrasing |
| Hebrew | 70 | Severe typos and grammar errors |
| Czech | 68 | Grammatical errors and unnatural literal translations |
| Belarusian | 66 | High density of grammatical errors and unnatural phrasing |
| Latvian | 65 | Pervasive MT artifacts and grammatical errors |
| Turkish | 63 | Prominent mistranslations and fluency issues |
| Slovak | 62 | High frequency of grammatical and typographical errors |
| Greek | 61 | Critical terminology errors and unnatural phrasing |
| Indonesian | 55 | Mixed-language Chinese fragment and terminology errors |
| Malay | 55 | Technical terminology errors and unnatural phrasing |
| Estonian | 53 | Frequent terminology errors and typos |
| Bulgarian | 50 | Severe machine-translation artifacts and lexical errors |
| Urdu | 50 | Major lexical errors including Russian intrusion and mistranslations |
| Finnish | 49 | Severe grammatical errors and mixed-language artifacts |
| Slovene | 48 | Pervasive untranslated English fragments and grammatical errors |
| Azerbaijani | 46 | Severe terminology errors and unnatural phrasing |
| Armenian | 46 | Significant fluency and accuracy issues |
| Macedonian | 46 | Severe linguistic and technical inaccuracies |
| Lao | 45 | Severe physics terminology errors and poor fluency |
| Bengali | 42 | Extensive orthographic and mechanical errors |
| Mongolian | 42 | Severe lexical and grammatical errors impair readability |
| Telugu | 39 | Severe terminology inconsistency and pervasive grammatical errors |
| Marathi | 38 | Major linguistic flaws and spelling errors |
| Nepali | 37 | Pervasive typos and poor linguistic quality |
| Georgian | 36 | Severe systemic errors and major defects |
| Arabic | 33 | Intrusion of Chinese characters |
| Icelandic | 33 | Severe grammar errors and pervasive mistranslations |
| Interlingua | 32 | Severe mixed-language contamination and structural defects |
| Malayalam | 32 | Severe orthographic and grammatical defects |
| Sinhala | 32 | Pervasive systematic character corruption and grammatical defects |
| Swahili | 32 | Severe machine translation artifacts and linguistic flaws |
| Irish | 30 | Severe grammatical errors and incorrect scientific terminology |
| Khmer | 30 | Severe typos and terminology errors |
| Hindi | 29 | Severe typographical and systematic errors |
| Welsh | 27 | Severe machine-translation artifacts |
| Esperanto | 27 | Critical structural and lexical failures with mixed languages |
| Kannada | 26 | Severe terminology mistranslation and structural defects |
| Thai | 26 | Pervasive spelling and orthographic errors |
| Tagalog | 25 | Severe machine-translation artifacts and lexical errors |
| Basque | 23 | Severe lexical and grammatical defects |
| Burmese | 19 | Massive text-generation loop causes corruption |
| Tamil | 18 | Severe orthographic corruption and spelling errors |

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
