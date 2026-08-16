# 言語コードと表記の対応表
# 追加・修正はこの LANGUAGES のみを編集する。
# ja は README の表で使用する日本語表記。

LANGUAGES = {
    "af": {"en": "Afrikaans", "ja": "アフリカーンス語"},
    "ar": {"en": "Arabic", "ja": "アラビア語"},
    "az": {"en": "Azerbaijani", "ja": "アゼルバイジャン語"},
    "be": {"en": "Belarusian", "ja": "ベラルーシ語"},
    "bg": {"en": "Bulgarian", "ja": "ブルガリア語"},
    "bn": {"en": "Bengali", "ja": "ベンガル語"},
    "ca": {"en": "Catalan", "ja": "カタルーニャ語"},
    "cs": {"en": "Czech", "ja": "チェコ語"},
    "cy": {"en": "Welsh", "ja": "ウェールズ語"},
    "da": {"en": "Danish", "ja": "デンマーク語"},
    "de": {"en": "German", "ja": "ドイツ語"},
    "el": {"en": "Greek", "ja": "ギリシャ語"},
    "en": {"en": "English", "ja": "英語"},
    "eo": {"en": "Esperanto", "ja": "エスペラント"},
    "es": {"en": "Spanish", "ja": "スペイン語"},
    "et": {"en": "Estonian", "ja": "エストニア語"},
    "eu": {"en": "Basque", "ja": "バスク語"},
    "fa": {"en": "Persian", "ja": "ペルシア語"},
    "fi": {"en": "Finnish", "ja": "フィンランド語"},
    "fr": {"en": "French", "ja": "フランス語"},
    "ga": {"en": "Irish", "ja": "アイルランド語"},
    "gl": {"en": "Galician", "ja": "ガリシア語"},
    "he": {"en": "Hebrew", "ja": "ヘブライ語"},
    "hi": {"en": "Hindi", "ja": "ヒンディー語"},
    "hr": {"en": "Croatian", "ja": "クロアチア語"},
    "hu": {"en": "Hungarian", "ja": "ハンガリー語"},
    "hy": {"en": "Armenian", "ja": "アルメニア語"},
    "ia": {"en": "Interlingua", "ja": "インターリングア"},
    "id": {"en": "Indonesian", "ja": "インドネシア語"},
    "is": {"en": "Icelandic", "ja": "アイスランド語"},
    "it": {"en": "Italian", "ja": "イタリア語"},
    "ja": {"en": "Japanese", "ja": "日本語"},
    "ka": {"en": "Georgian", "ja": "ジョージア語"},
    "km": {"en": "Khmer", "ja": "クメール語"},
    "kn": {"en": "Kannada", "ja": "カンナダ語"},
    "ko": {"en": "Korean", "ja": "朝鮮語"},
    "lo": {"en": "Lao", "ja": "ラーオ語"},
    "lt": {"en": "Lithuanian", "ja": "リトアニア語"},
    "lv": {"en": "Latvian", "ja": "ラトビア語"},
    "mk": {"en": "Macedonian", "ja": "マケドニア語"},
    "ml": {"en": "Malayalam", "ja": "マラヤーラム語"},
    "mn": {"en": "Mongolian", "ja": "モンゴル語"},
    "mr": {"en": "Marathi", "ja": "マラーティー語"},
    "ms": {"en": "Malay", "ja": "マレー語"},
    "my": {"en": "Burmese", "ja": "ビルマ語"},
    "ne": {"en": "Nepali", "ja": "ネパール語"},
    "nl": {"en": "Dutch", "ja": "オランダ語"},
    "no": {"en": "Norwegian", "ja": "ノルウェー語"},
    "pl": {"en": "Polish", "ja": "ポーランド語"},
    "pt": {"en": "Portuguese", "ja": "ポルトガル語"},
    "ro": {"en": "Romanian", "ja": "ルーマニア語"},
    "ru": {"en": "Russian", "ja": "ロシア語"},
    "si": {"en": "Sinhala", "ja": "シンハラ語"},
    "sk": {"en": "Slovak", "ja": "スロバキア語"},
    "sl": {"en": "Slovene", "ja": "スロベニア語"},
    "sq": {"en": "Albanian", "ja": "アルバニア語"},
    "sr": {"en": "Serbian", "ja": "セルビア語"},
    "sv": {"en": "Swedish", "ja": "スウェーデン語"},
    "sw": {"en": "Swahili", "ja": "スワヒリ語"},
    "ta": {"en": "Tamil", "ja": "タミル語"},
    "te": {"en": "Telugu", "ja": "テルグ語"},
    "th": {"en": "Thai", "ja": "タイ語"},
    "tl": {"en": "Tagalog", "ja": "タガログ語"},
    "tr": {"en": "Turkish", "ja": "トルコ語"},
    "uk": {"en": "Ukrainian", "ja": "ウクライナ語"},
    "ur": {"en": "Urdu", "ja": "ウルドゥー語"},
    "vi": {"en": "Vietnamese", "ja": "ベトナム語"},
    "zh": {"en": "Chinese", "ja": "中国語"},
}

LANG_NAMES = {code: names["en"] for code, names in LANGUAGES.items()}


def resolve_lang(lang):
    return LANG_NAMES.get(lang, lang)


def resolve_langs(langs):
    return [resolve_lang(l) for l in langs]
