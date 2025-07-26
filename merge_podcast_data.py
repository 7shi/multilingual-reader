#!/usr/bin/env python3
"""
スクリプトで複数言語のテキストファイルを読み込み、
行ごとの対訳形式でJavaScript形式に統合する。

使用方法:
    python merge_podcast_data.py -o output.js file1-fr.txt file2-en.txt file3-ja.txt

例:
    python merge_podcast_data.py -o podcast-text-data.js quantum_physics-fr.txt quantum_physics-en.txt quantum_physics-ja.txt
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()


def detect_language_from_filename(filename: str) -> Optional[str]:
    """
    ファイル名から言語コードを検出する（拡張子を取り除いてから処理）。
    
    Args:
        filename: ファイル名
        
    Returns:
        言語コード（fr, en, ja等）またはNone
    """
    # 拡張子を取り除く
    name_without_ext = Path(filename).stem
    
    # 最後のハイフン以降を言語コードとして取得
    if '-' in name_without_ext:
        lang_code = name_without_ext.split('-')[-1].lower()
        return lang_code
    
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


def extract_speaker_and_text(text: str) -> tuple[Optional[str], str]:
    """
    テキストから話者名を抽出する。
    
    Args:
        text: 元のテキスト
        
    Returns:
        (話者名, 話者名を除いた本文)のタプル
    """
    # normalize処理を適用
    text = normalize(text)
    
    if ':' in text:
        parts = text.split(':', 1)
        if len(parts) == 2:
            speaker = normalize(parts[0])
            content = normalize(parts[1])
            return speaker, content
    
    return None, text


def merge_language_files(language_files: List[tuple[str, Path]]) -> List[Dict[str, str]]:
    """
    複数言語のファイルを行ごとの対訳形式でマージする。
    
    Args:
        language_files: (言語コード, ファイルパス)のタプルのリスト（指定順序を保持）
        
    Returns:
        行ごとの対訳データのリスト（speaker + 指定された言語順）
    """
    # 各言語のテキストを読み込み（順序を保持）
    texts = []
    lang_codes = []
    max_lines = 0
    
    for lang_code, filepath in language_files:
        lines = read_text_file(filepath)
        texts.append(lines)
        lang_codes.append(lang_code)
        max_lines = max(max_lines, len(lines))
        print(f"読み込み完了: {filepath} ({len(lines)}行)")
    
    # 行ごとの対訳データを作成
    merged_data = []
    
    for i in range(max_lines):
        speaker = None
        
        # 話者情報を抽出（最初のファイルから優先的に取得）
        for j, lines in enumerate(texts):
            if i < len(lines):
                text = lines[i]
                extracted_speaker, _ = extract_speaker_and_text(text)
                if extracted_speaker and not speaker:
                    speaker = extracted_speaker
        
        # line_dataを作成（speakerを最初に配置）
        line_data = {}
        if speaker:
            line_data["speaker"] = speaker
        else:
            line_data["speaker"] = ""
        
        # 各言語のテキストを指定順序で追加
        for j, lang_code in enumerate(lang_codes):
            if i < len(texts[j]):
                text = texts[j][i]
                _, content = extract_speaker_and_text(text)
                line_data[lang_code] = content
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
    json_str = json_str.replace("[\n{", "[{").replace("},\n{", "},{").replace("}\n]", "}]")
    
    # 新形式（datasets配列、nameフィールドなし）
    js_output = f"""// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {{
    var datasets = [];
}}

// Add dataset to datasets array
datasets.push(
{json_str}
);
"""
    
    return js_output


def main():
    parser = argparse.ArgumentParser(
        description="複数言語のテキストファイルを行ごとの対訳形式でJavaScript形式に統合",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s -o onde.js file1-fr.txt file2-en.txt file3-ja.txt
    指定されたファイルを直接読み込んでデータセットとして出力

        """
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='出力JavaScriptファイル名'
    )
    
    
    
    parser.add_argument(
        'files',
        nargs='*',
        help='入力テキストファイル（言語コードを含むファイル名）'
    )
    
    args = parser.parse_args()
    
    # ファイルリストの決定（指定順序を保持）
    language_files = []
    
    if not args.files:
        print("エラー: ファイルを指定してください", file=sys.stderr)
        sys.exit(1)
    
    # 直接指定されたファイルから言語コードを検出（順序を保持）
    for filename in args.files:
        filepath = Path(filename)
        if not filepath.exists():
            print(f"エラー: ファイルが見つかりません: {filepath}", file=sys.stderr)
            continue
        
        lang_code = detect_language_from_filename(filepath.name)
        if lang_code:
            language_files.append((lang_code, filepath))
        else:
            print(f"警告: 言語コードを検出できません: {filepath}", file=sys.stderr)
    
    if not language_files:
        print("エラー: 処理する言語ファイルが見つかりません", file=sys.stderr)
        sys.exit(1)
    
    print(f"検出された言語ファイル: {', '.join(f'{k}={v}' for k, v in language_files)}")
    
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
        print(f"含まれる言語: {', '.join(lang_code for lang_code, _ in language_files)}")
        
    except IOError as e:
        print(f"出力ファイル書き込みエラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
