#!/usr/bin/env python3
# draft.jsonを指定してテキスト形式で翻訳のみを出力するユーティリティ

import argparse
import json
import os
import sys

def load_draft_json(file_path):
    """draft.jsonファイルを読み込み"""
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません: {file_path}", file=sys.stderr)
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"エラー: JSONファイルの解析に失敗しました: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"エラー: ファイル読み込みに失敗しました: {e}", file=sys.stderr)
        return None

def extract_translations(data):
    """JSONデータから翻訳のみを抽出"""
    translations = []
    
    if isinstance(data, dict) and 'results' in data:
        results = data['results']
        
        # リスト形式の場合
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and 'speaker' in item and 'translation' in item:
                    translations.append({
                        'speaker': item['speaker'],
                        'translation': item['translation']
                    })
        
        # 辞書形式の場合（旧形式対応）
        elif isinstance(results, dict):
            for line_key, item_data in results.items():
                if isinstance(item_data, dict) and 'speaker' in item_data and 'translation' in item_data:
                    translations.append({
                        'speaker': item_data['speaker'],
                        'translation': item_data['translation']
                    })
    
    return translations

def save_translations_to_text(translations, output_path):
    """翻訳をテキストファイルに保存"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in translations:
                f.write(f"{item['speaker']}: {item['translation']}\n")
        return True
    except Exception as e:
        print(f"エラー: ファイル出力に失敗しました: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="draft.jsonファイルから翻訳のみをテキスト形式で出力",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python draft_to_text.py output_draft.json                    # output_draft.txt を生成
  python draft_to_text.py output_draft.json -o custom.txt     # custom.txt を生成
  python draft_to_text.py output_draft.json --stdout          # 標準出力に表示

対応形式:
  - 新形式: {"metadata": {...}, "results": [{"speaker": "...", "translation": "..."}, ...]}
  - 旧形式: {"metadata": {...}, "results": {"key": {"speaker": "...", "translation": "..."}, ...}}
"""
    )
    
    parser.add_argument("input_file", help="入力するdraft.jsonファイル")
    parser.add_argument("-o", "--output", help="出力ファイル名（デフォルト: 拡張子を.txtに変更）")
    parser.add_argument("--stdout", action="store_true", help="標準出力に表示（ファイル出力しない）")
    
    args = parser.parse_args()
    
    # JSONファイル読み込み
    data = load_draft_json(args.input_file)
    if data is None:
        sys.exit(1)
    
    # 翻訳データ抽出
    translations = extract_translations(data)
    if not translations:
        print("警告: 翻訳データが見つかりませんでした", file=sys.stderr)
        sys.exit(1)
    
    print(f"翻訳データを{len(translations)}行抽出しました")
    
    # 出力処理
    if args.stdout:
        # 標準出力に表示
        for item in translations:
            print(f"{item['speaker']}: {item['translation']}")
    else:
        # ファイル出力
        if args.output:
            output_path = args.output
        else:
            # 拡張子を.txtに変更
            output_path = args.input_file.replace('.json', '.txt')
        
        if save_translations_to_text(translations, output_path):
            print(f"出力完了: {output_path}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()