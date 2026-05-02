#!/bin/bash
# 3段階多モデル翻訳実行スクリプト

if [ "$#" -ne 5 ]; then
    echo "使用法: $0 <入力ファイル> <原語> <翻訳先言語> <出力ファイル> <品質チェックモデル>"
    echo "例: $0 input.txt French Spanish output.txt ollama:qwen2.5:7b"
    exit 1
fi

INPUT_FILE="$1"
FROM_LANG="$2"
TO_LANG="$3"
OUTPUT_FILE="$4"
CHECKER_MODEL="$5"

echo "3段階多モデル翻訳を開始: $FROM_LANG → $TO_LANG"
echo "入力: $INPUT_FILE"
echo "出力: $OUTPUT_FILE"
echo "品質チェックモデル: $CHECKER_MODEL"
echo

# フェーズ1: 初回翻訳
echo "=== フェーズ1: 初回翻訳 ==="
python translate.py phase1 "$INPUT_FILE" -f "$FROM_LANG" -t "$TO_LANG" -o "$OUTPUT_FILE"
if [ $? -ne 0 ]; then
    echo "エラー: フェーズ1が失敗しました"
    exit 1
fi

# 中間ファイル名を生成
BASE_NAME="${OUTPUT_FILE%.*}"
DRAFT_FILE="${BASE_NAME}_draft.json"
CHECK_FILE="${BASE_NAME}_check.json"

echo
# フェーズ2: 品質チェック
echo "=== フェーズ2: 品質チェック (モデル: $CHECKER_MODEL) ==="
python translate.py phase2 -o "$OUTPUT_FILE" --draft-file "$DRAFT_FILE" -c "$CHECKER_MODEL"
if [ $? -ne 0 ]; then
    echo "エラー: フェーズ2が失敗しました"
    exit 1
fi

echo
# フェーズ3: 修正反映
echo "=== フェーズ3: 修正反映 ==="
python translate.py phase3 -o "$OUTPUT_FILE" --draft-file "$DRAFT_FILE" --check-file "$CHECK_FILE"
if [ $? -ne 0 ]; then
    echo "エラー: フェーズ3が失敗しました"
    exit 1
fi

echo
echo "=== 3段階翻訳完了 ==="
echo "最終結果: $OUTPUT_FILE"
echo "中間ファイル:"
echo "  - 初回翻訳: $DRAFT_FILE"
echo "  - 品質チェック: $CHECK_FILE"