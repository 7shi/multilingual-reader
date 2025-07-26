#!/usr/bin/env python3
"""
Script to extract multilingual text data from podcast-text-data.js
and split it into separate text files for each language.

Usage:
    python split_podcast_data.py input_file -o output_prefix

Example:
    python split_podcast_data.py podcast-text-data.js -o quantum_physics
    # Creates: quantum_physics-fr.txt, quantum_physics-en.txt, quantum_physics-ja.txt
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_js_array_content(js_content: str, object_name: str = None) -> dict:
    """
    Extract the content of a JavaScript array from the JS file (supports both old format and new datasets format).
    
    Args:
        js_content: The full JavaScript file content
        object_name: Name of the object to extract (e.g., 'podcastTexts') - for old format
        
    Returns:
        Dictionary with language codes as keys and text content as values
    """
    data = None
    
    # Try new datasets format first - extract first datasets.push([...]) found
    pattern = r'datasets\.push\(\s*(\[.*?\])\s*\);'
    match = re.search(pattern, js_content, re.DOTALL)
    if match:
        json_content = match.group(1)
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON content from datasets format: {e}")
    
    # Try old format if new format failed or wasn't specified
    if data is None and object_name:
        # 先頭から`const podcastTexts =`を検索
        start_pattern = rf'const\s+{object_name}\s*='
        start_match = re.search(start_pattern, js_content)
        if not start_match:
            raise ValueError(f"Could not find object '{object_name}' in JavaScript file")
        
        start_pos = start_match.end()
        
        # 末尾から`;`を検索
        end_match = re.search(r';\s*$', js_content)
        if not end_match:
            raise ValueError("Could not find ending semicolon in JavaScript file")
        
        end_pos = end_match.start()
        
        # その間を取り出してjson.loads
        json_content = js_content[start_pos:end_pos].strip()
        
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON content: {e}")
    
    if data is None:
        raise ValueError("Could not extract data from JavaScript file")
    
    if not isinstance(data, list):
        raise ValueError("Expected JSON array format")
    
    # 最初の行で言語を取得
    if not data:
        raise ValueError("No data found in JSON array")
    
    first_item = data[0]
    if not isinstance(first_item, dict):
        raise ValueError("Expected dictionary format in JSON array")
    
    expected_languages = set(first_item.keys())
    
    # speakerキーを除外してテキスト用の言語を取得
    text_languages = expected_languages - {'speaker'}
    
    # 各言語の行を結合
    languages = {lang: [] for lang in text_languages}
    
    for i, item in enumerate(data):
        if isinstance(item, dict):
            # 言語に変化がないかチェック
            current_languages = set(item.keys())
            if current_languages != expected_languages:
                print(f"警告: 行{i+1}で言語構成が変化しました。期待: {expected_languages}, 実際: {current_languages}", file=sys.stderr)
            
            # 話者情報を取得
            speaker = item.get('speaker', '')
            
            for lang in text_languages:
                if lang in item:
                    text = item[lang]
                    # 話者情報がある場合は「話者: 文章」形式で復元
                    if speaker and text:
                        restored_text = f"{speaker}: {text}"
                    elif text:
                        restored_text = text
                    else:
                        restored_text = ""
                    languages[lang].append(restored_text)
                else:
                    languages[lang].append("")  # 空行で補完
    
    # リストを文字列に変換
    for lang in languages:
        languages[lang] = '\n'.join(languages[lang])
    
    return languages


def clean_text_content(text: str) -> str:
    """
    Clean and format the extracted text content.
    
    Args:
        text: Raw text content from JavaScript
        
    Returns:
        Cleaned text with proper formatting
    """
    # Split into lines and clean each line
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # すべての行を追加（話者: 文章形式はすでに復元済み）
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def write_language_files(languages: dict, output_prefix: str) -> list:
    """
    Write separate text files for each language.
    
    Args:
        languages: Dictionary with language codes and text content
        output_prefix: Prefix for output filenames
        
    Returns:
        List of created filenames
    """
    created_files = []
    
    for lang_code, text_content in languages.items():
        filename = f"{output_prefix}-{lang_code}.txt"
        filepath = Path(filename)
        
        # Clean the text content
        cleaned_text = clean_text_content(text_content)
        
        # Write to file with UTF-8 encoding
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
                f.write('\n')  # Ensure file ends with newline
            
            created_files.append(filename)
            print(f"Created: {filename} ({len(cleaned_text.splitlines())} lines)")
            
        except IOError as e:
            print(f"Error writing file {filename}: {e}", file=sys.stderr)
            continue
    
    return created_files


def main():
    parser = argparse.ArgumentParser(
        description="Extract multilingual text data from podcast-text-data.js",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # New datasets format
  %(prog)s onde.js -o onde_physics
    Creates: onde_physics-fr.txt, onde_physics-en.txt, onde_physics-ja.txt
  
  %(prog)s momentum.js -o momentum_physics
    Creates: momentum_physics-fr.txt, momentum_physics-en.txt, momentum_physics-ja.txt
  
  # Old format
  %(prog)s podcast-text-data.js --object podcastTexts -o physics_podcast
    Creates: physics_podcast-fr.txt, physics_podcast-en.txt, physics_podcast-ja.txt
        """
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output filename prefix (e.g., "physics" creates physics-fr.txt, physics-en.txt, physics-ja.txt)'
    )
    
    
    parser.add_argument(
        '--object',
        default='podcastTexts',
        help='Object name to extract from old format (default: podcastTexts)'
    )
    
    parser.add_argument(
        'input_file',
        help='Input JavaScript file'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Read the JavaScript file
        with open(input_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Extract the podcast texts array (supports both old and new formats)
        languages = extract_js_array_content(js_content, object_name=args.object)
        
        if not languages:
            print("No language data found in the JavaScript file", file=sys.stderr)
            sys.exit(1)
        
        print(f"Found {len(languages)} languages: {', '.join(languages.keys())}")
        
        # Write separate files for each language
        created_files = write_language_files(languages, args.output)
        
        if created_files:
            print(f"\nSuccessfully created {len(created_files)} files:")
            for filename in created_files:
                print(f"  - {filename}")
        else:
            print("No files were created", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()