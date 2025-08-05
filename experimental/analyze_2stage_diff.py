#!/usr/bin/env python3
# log.jsonlから2段階翻訳の効果を分析するスクリプト

import json
import difflib
import argparse
from typing import List, Dict

def load_jsonl(file_path: str) -> List[Dict]:
    """JSON混在ファイルから{...}部分を抽出して読み込み"""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # "{"から"}"までのJSON部分を抽出
    i = 0
    entry_num = 0
    while i < len(content):
        # "{"を見つける
        start = content.find('{', i)
        if start == -1:
            break
        
        # 対応する"}"を見つける（ネストと文字列を考慮）
        brace_count = 0
        end = start
        in_string = False
        escape_next = False
        
        while end < len(content):
            char = content[end]
            
            if escape_next:
                escape_next = False
            elif char == '\\' and in_string:
                escape_next = True
            elif char == '"' and not escape_next:
                in_string = not in_string
            elif not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        break
            end += 1
        
        if brace_count == 0:  # 正常に閉じた場合
            json_str = content[start:end+1]
            try:
                entry = json.loads(json_str)
                entry_num += 1
                entry['line_num'] = entry_num
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"警告: エントリー{entry_num}でJSONパースエラー: {e}")
            i = end + 1
        else:
            i = start + 1
    
    return entries

def extract_speaker_info(text_before_json: str) -> str:
    """JSONの直前行から話者情報を抽出"""
    lines = text_before_json.strip().split('\n')
    if lines:
        last_line = lines[-1].strip()
        # 「名前:」の形式を探す
        if ':' in last_line:
            speaker = last_line.split(':', 1)[0].strip()
            return speaker
    return ""

def load_jsonl_with_speakers(file_path: str) -> List[Dict]:
    """JSON混在ファイルから{...}部分と話者情報を抽出して読み込み"""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # "{"から"}"までのJSON部分を抽出
    i = 0
    entry_num = 0
    while i < len(content):
        # "{"を見つける
        start = content.find('{', i)
        if start == -1:
            break
        
        # 話者情報を抽出（JSONの直前の行から）
        text_before = content[:start]
        speaker = extract_speaker_info(text_before)
        
        # 対応する"}"を見つける（ネストと文字列を考慮）
        brace_count = 0
        end = start
        in_string = False
        escape_next = False
        
        while end < len(content):
            char = content[end]
            
            if escape_next:
                escape_next = False
            elif char == '\\' and in_string:
                escape_next = True
            elif char == '"' and not escape_next:
                in_string = not in_string
            elif not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        break
            end += 1
        
        if brace_count == 0:  # 正常に閉じた場合
            json_str = content[start:end+1]
            try:
                entry = json.loads(json_str)
                entry_num += 1
                entry['line_num'] = entry_num
                entry['speaker'] = speaker
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"警告: エントリー{entry_num}でJSONパースエラー: {e}")
            i = end + 1
        else:
            i = start + 1
    
    return entries

def create_draft_output(entries: List[Dict], input_file: str) -> str:
    """draft_translationを結合してINPUT-draft.txtの内容を作成"""
    output_lines = []
    
    for entry in entries:
        if 'draft_translation' in entry and 'speaker' in entry:
            speaker = entry['speaker']
            draft = entry['draft_translation'].strip()
            
            if speaker and draft:
                output_lines.append(f"{speaker}: {draft}")
            elif draft:
                output_lines.append(draft)
    
    return '\n'.join(output_lines)

def analyze_differences(entries: List[Dict]) -> Dict:
    """draft_translationとimproved_translationの差異を分析"""
    stats = {
        'total_entries': len(entries),
        'identical_count': 0,
        'modified_count': 0,
        'differences': []
    }
    
    for entry in entries:
        if 'draft_translation' not in entry or 'improved_translation' not in entry:
            continue
            
        draft = entry['draft_translation'].strip()
        final = entry['improved_translation'].strip()
        
        if draft == final:
            stats['identical_count'] += 1
        else:
            stats['modified_count'] += 1
            
            # 文字レベルの差分を計算
            diff = list(difflib.unified_diff(
                draft.splitlines(keepends=True),
                final.splitlines(keepends=True),
                fromfile='draft',
                tofile='final',
                lineterm=''
            ))
            
            stats['differences'].append({
                'line_num': entry.get('line_num', '不明'),
                'draft': draft,
                'final': final,
                'quality_check': entry.get('quality_check', ''),
                'diff': ''.join(diff) if diff else '差分なし'
            })
    
    return stats

def print_summary(stats: Dict, show_details: bool = False, max_examples: int = 10):
    """結果の要約を表示"""
    print("=" * 60)
    print("2段階翻訳の効果分析")
    print("=" * 60)
    
    print(f"総エントリー数: {stats['total_entries']}")
    print(f"変更なし: {stats['identical_count']} ({stats['identical_count']/stats['total_entries']*100:.1f}%)")
    print(f"変更あり: {stats['modified_count']} ({stats['modified_count']/stats['total_entries']*100:.1f}%)")
    
    if not show_details:
        print(f"\n詳細表示するには --details オプションを使用してください")
        return
    
    print("\n" + "=" * 60)
    print("変更された翻訳の詳細")
    print("=" * 60)
    
    for i, diff_entry in enumerate(stats['differences'][:max_examples]):
        print(f"\n--- エントリー {i+1} (行 {diff_entry['line_num']}) ---")
        print(f"初回翻訳: {diff_entry['draft']}")
        print(f"最終翻訳: {diff_entry['final']}")
        
        if diff_entry['quality_check']:
            print(f"品質チェック: {diff_entry['quality_check'][:200]}...")
        
        print("-" * 40)
    
    if len(stats['differences']) > max_examples:
        print(f"\n... 他 {len(stats['differences']) - max_examples} 件の変更あり")

def main():
    parser = argparse.ArgumentParser(description="2段階翻訳の効果を分析")
    parser.add_argument("jsonl_file", help="分析対象のJSONLファイル")
    parser.add_argument("-d", "--details", action="store_true", help="詳細な差分を表示")
    parser.add_argument("-n", "--max-examples", type=int, default=10, help="表示する例の最大数")
    parser.add_argument("--draft-output", action="store_true", help="draft_translationを結合してINPUT-draft.txtを出力")
    
    args = parser.parse_args()
    
    try:
        # 通常の分析処理
        entries = load_jsonl(args.jsonl_file)
        if not entries:
            print("エラー: 有効なエントリーが見つかりませんでした")
            return
        
        stats = analyze_differences(entries)
        print_summary(stats, args.details, args.max_examples)
        
        # draft出力が指定された場合の追加処理
        if args.draft_output:
            print("\n" + "=" * 60)
            print("draft翻訳の出力")
            print("=" * 60)
            
            # 話者情報付きでエントリーを再読み込み
            entries_with_speakers = load_jsonl_with_speakers(args.jsonl_file)
            
            # 出力ファイル名を生成（INPUT.txt → INPUT-draft.txt）
            base_name = args.jsonl_file
            if base_name.endswith('.txt'):
                output_file = base_name[:-4] + '-draft.txt'
            else:
                output_file = base_name + '-draft.txt'
            
            # draft翻訳を結合して出力
            draft_content = create_draft_output(entries_with_speakers, args.jsonl_file)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(draft_content)
            
            print(f"draft翻訳を {output_file} に出力しました ({len(entries_with_speakers)} エントリー)")
        
    except FileNotFoundError:
        print(f"エラー: ファイル '{args.jsonl_file}' が見つかりません")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    main()
