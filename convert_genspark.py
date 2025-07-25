# HTMLファイルから対話データを抽出するプル型パーサー
# 指定ファイルから話者別に発言内容を読み取り、変換して出力

import argparse

parser = argparse.ArgumentParser(description="フランス語対話テキストを英語と日本語に翻訳")
parser.add_argument("input_file", help="入力ファイル")
parser.add_argument("-o", "--output", required=True, help="出力ファイル")
parser.add_argument("--speaker", default="A,B", help="話者名をカンマ区切りで指定 (例: Camille,Luc)")
args = parser.parse_args()

from xml7shi import reader

def normalize(text):
    # テキストの正規化: 改行・タブをスペースに変換し、連続スペースを1個にまとめる
    import re
    return re.sub(r'\s+', ' ', text.strip())

# 話者名を解析
speakers = args.speaker.split(",")
if len(speakers) != 2:
    raise ValueError("話者は2人必要です (例: --speaker Camille,Luc)")
speaker1, speaker2 = speakers

# HTMLファイルを読み込み
with open(args.input_file, "r", encoding="utf-8") as f:
    html = f.read()

# 出力ファイルを開く
with open(args.output, "w", encoding="utf-8") as f:
    # プル型XMLリーダーでHTMLを解析
    xr = reader(html)
    while xr.read():
        # divタグで話者を判定
        if xr.tag == "div":
            cls = xr["class"].split()
            if "speaker-color-1" in cls:
                speaker = speaker1
            elif "speaker-color-2" in cls:
                speaker = speaker2
        # spanタグの発言内容を出力
        elif xr.tag == "span" and xr["class"] == "content" and xr.read():
            print(speaker + ":", normalize(xr.text), file=f)
