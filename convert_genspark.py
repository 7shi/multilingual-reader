# HTMLファイルから対話データを抽出するプル型パーサー
# fr-onde.htmlから話者(Camille/Luc)と発言内容を読み取り、fr-onde.txt形式で出力
from xml7shi import reader

def normalize(text):
    # テキストの正規化: 改行・タブをスペースに変換し、連続スペースを1個にまとめる
    import re
    return re.sub(r'\s+', ' ', text.strip())

# HTMLファイルを読み込み
with open("fr-onde.html", "r", encoding="utf-8") as f:
    html = f.read()

# プル型XMLリーダーでHTMLを解析
xr = reader(html)
while xr.read():
    # divタグで話者を判定
    if xr.tag == "div":
        cls = xr["class"].split()
        if "speaker-color-1" in cls:
            speaker = "Camille"
        elif "speaker-color-2" in cls:
            speaker = "Luc"
    # spanタグの発言内容を出力
    elif xr.tag == "span" and xr["class"] == "content" and xr.read():
        print(speaker + ":", normalize(xr.text))
