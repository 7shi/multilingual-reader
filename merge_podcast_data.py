#!/usr/bin/env python3
"""
スクリプトで複数言語のテキストファイルを読み込み、
行ごとの対訳形式でJavaScript形式に統合する。

使用方法:
    python merge_podcast_data.py -o output.js file1-fr.txt file2-en.txt file3-ja.txt
    python merge_podcast_data.py -o output.js --prefix quantum_physics

例:
    python merge_podcast_data.py -o podcast-text-data.js quantum_physics-fr.txt quantum_physics-en.txt quantum_physics-ja.txt
    python merge_podcast_data.py -o podcast-text-data.js --prefix quantum_physics
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


def detect_language_from_filename(filename: str) -> Optional[str]:
    """
    ファイル名から言語コードを検出する。
    
    Args:
        filename: ファイル名
        
    Returns:
        言語コード（fr, en, ja）またはNone
    """
    filename_lower = filename.lower()
    if filename_lower.endswith('-fr.txt'):
        return 'fr'
    elif filename_lower.endswith('-en.txt'):
        return 'en'
    elif filename_lower.endswith('-ja.txt'):
        return 'ja'
    return None


def read_text_file(filepath: Path) -> List[str]:
    """
    テキストファイルを読み込んで行のリストを返す。
    
    Args:
        filepath: テキストファイルのパス
        
    Returns:
        行のリスト（空行を含む）
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 改行文字を除去
        return [line.rstrip('\n\r') for line in lines]
        
    except IOError as e:
        print(f"ファイル読み込みエラー {filepath}: {e}", file=sys.stderr)
        return []


def merge_language_files(language_files: Dict[str, Path]) -> List[Dict[str, str]]:
    """
    複数言語のファイルを行ごとの対訳形式でマージする。
    
    Args:
        language_files: 言語コードをキー、ファイルパスを値とする辞書
        
    Returns:
        行ごとの対訳データのリスト
    """
    # 各言語のテキストを読み込み
    texts = {}
    max_lines = 0
    
    for lang_code, filepath in language_files.items():
        lines = read_text_file(filepath)
        texts[lang_code] = lines
        max_lines = max(max_lines, len(lines))
        print(f"読み込み完了: {filepath} ({len(lines)}行)")
    
    # 行ごとの対訳データを作成
    merged_data = []
    
    for i in range(max_lines):
        line_data = {}
        
        for lang_code in ['fr', 'en', 'ja']:  # 順序を固定
            if lang_code in texts and i < len(texts[lang_code]):
                line_data[lang_code] = texts[lang_code][i]
            else:
                line_data[lang_code] = ""  # 足りない行は空文字
        
        merged_data.append(line_data)
    
    return merged_data


def generate_javascript_output(merged_data: List[Dict[str, str]]) -> str:
    """
    マージされたデータからJavaScript形式の文字列を生成する（datasets配列形式、nameフィールドなし）。
    
    Args:
        merged_data: 行ごとの対訳データ
        
    Returns:
        JavaScript形式の文字列
    """
    # JSONとして整形（インデント付き）
    json_str = json.dumps(merged_data, ensure_ascii=False, indent=0)
    
    # 新形式（datasets配列、nameフィールドなし）
    js_output = f"""// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {{
    var datasets = [];
}}

// Add dataset to datasets array
datasets.push({json_str});"""
    
    return js_output


def main():
    parser = argparse.ArgumentParser(
        description="複数言語のテキストファイルを行ごとの対訳形式でJavaScript形式に統合",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s -o onde.js file1-fr.txt file2-en.txt file3-ja.txt
    指定されたファイルを直接読み込んでデータセットとして出力

  %(prog)s -o momentum.js --prefix quantum_physics
    quantum_physics-fr.txt, quantum_physics-en.txt, quantum_physics-ja.txt を自動検索してデータセットとして出力
        """
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='出力JavaScriptファイル名'
    )
    
    parser.add_argument(
        '--prefix',
        help='ファイル名のプレフィックス（例: quantum_physics）'
    )
    
    
    parser.add_argument(
        'files',
        nargs='*',
        help='入力テキストファイル（言語コードを含むファイル名）'
    )
    
    args = parser.parse_args()
    
    # ファイルリストの決定
    language_files = {}
    
    if args.prefix:
        # プレフィックスから自動的にファイル名を生成
        for lang_code in ['fr', 'en', 'ja']:
            filepath = Path(f"{args.prefix}-{lang_code}.txt")
            if filepath.exists():
                language_files[lang_code] = filepath
            else:
                print(f"警告: ファイルが見つかりません: {filepath}", file=sys.stderr)
    
    if args.files:
        # 直接指定されたファイルから言語コードを検出
        for filename in args.files:
            filepath = Path(filename)
            if not filepath.exists():
                print(f"エラー: ファイルが見つかりません: {filepath}", file=sys.stderr)
                continue
            
            lang_code = detect_language_from_filename(filepath.name)
            if lang_code:
                language_files[lang_code] = filepath
            else:
                print(f"警告: 言語コードを検出できません: {filepath}", file=sys.stderr)
    
    if not language_files:
        print("エラー: 処理する言語ファイルが見つかりません", file=sys.stderr)
        sys.exit(1)
    
    print(f"検出された言語ファイル: {', '.join(f'{k}={v}' for k, v in language_files.items())}")
    
    # ファイルをマージ
    merged_data = merge_language_files(language_files)
    
    if not merged_data:
        print("エラー: マージするデータがありません", file=sys.stderr)
        sys.exit(1)
    
    # JavaScript形式で出力
    js_output = generate_javascript_output(merged_data)
    
    try:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_output)
        
        print(f"統合完了: {output_path} ({len(merged_data)}行)")
        print(f"含まれる言語: {', '.join(language_files.keys())}")
        
    except IOError as e:
        print(f"出力ファイル書き込みエラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
