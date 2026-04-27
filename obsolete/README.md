# Obsolete

仕様が古くなったスクリプトを格納。

## convert_genspark.py

Genspark HTMLファイルから話者別対話データを抽出するスクリプト。

### 使用方法（当時）

```bash
# 基本使用（デフォルトの話者名 A,B）
uv run convert_genspark.py input.html -o output.txt

# 話者名を指定
uv run convert_genspark.py input.html -o output.txt --speaker Camille,Luc
```

### 機能

- Genspark HTMLファイルから話者別対話データを抽出
- `--speaker` オプションで話者名をカンマ区切りで指定可能
- デフォルトでは話者名 A,B を使用
- プル型XMLパーサーによる効率的なHTML解析
- UTF-8エンコーディングで多言語対応

### 新しいデータセット追加時の手順（当時）

Gensparkで生成した場合：

1. Gensparkの出力からDOMの該当箇所をコピーしてHTMLファイルとして保存
2. `convert_genspark.py` を使用して対話データを抽出：

```bash
uv run convert_genspark.py genspark_output.html -o base_dialogue.txt --speaker Camille,Luc
```
