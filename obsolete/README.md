# Obsolete

仕様が古くなったスクリプトを格納。

## translate.py / translate.md

`trtools translate` サブコマンドに置き換えられた旧翻訳スクリプト。話者分離・推論レベル別構造化出力・スライディング方式履歴管理を実装していたが、以下の理由で廃止：

- 推論レベルを上げても翻訳品質は改善しない（実験結果より）
- スライディング方式の履歴管理では用語ブレと KV キャッシュ無効の問題が発生
- 話者分離は汎用性を損なう

`translate.md` は開発記録（多段階翻訳・多モデル協調の試行の経緯）。

新しい実装は `trtools/translate.py`（`uv run trtools translate`）を参照。

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
