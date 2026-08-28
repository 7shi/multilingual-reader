#!/usr/bin/env python3
# Script to analyze the effect of 2-stage translation from log.jsonl

import json
import difflib
import argparse
from typing import List, Dict

def load_jsonl(file_path: str) -> List[Dict]:
    """Extract and load the {...} portions from a file with mixed JSON content"""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the JSON portions from "{" to "}"
    i = 0
    entry_num = 0
    while i < len(content):
        # Find "{"
        start = content.find('{', i)
        if start == -1:
            break

        # Find the matching "}" (accounting for nesting and strings)
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
        
        if brace_count == 0:  # Closed successfully
            json_str = content[start:end+1]
            try:
                entry = json.loads(json_str)
                entry_num += 1
                entry['line_num'] = entry_num
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Warning: JSON parse error at entry {entry_num}: {e}")
            i = end + 1
        else:
            i = start + 1
    
    return entries

def extract_speaker_info(text_before_json: str) -> str:
    """Extract speaker info from the line immediately before the JSON"""
    lines = text_before_json.strip().split('\n')
    if lines:
        last_line = lines[-1].strip()
        # Look for a "name:" format
        if ':' in last_line:
            speaker = last_line.split(':', 1)[0].strip()
            return speaker
    return ""

def load_jsonl_with_speakers(file_path: str) -> List[Dict]:
    """Extract and load the {...} portions and speaker info from a file with mixed JSON content"""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the JSON portions from "{" to "}"
    i = 0
    entry_num = 0
    while i < len(content):
        # Find "{"
        start = content.find('{', i)
        if start == -1:
            break

        # Extract speaker info (from the line immediately before the JSON)
        text_before = content[:start]
        speaker = extract_speaker_info(text_before)

        # Find the matching "}" (accounting for nesting and strings)
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
        
        if brace_count == 0:  # Closed successfully
            json_str = content[start:end+1]
            try:
                entry = json.loads(json_str)
                entry_num += 1
                entry['line_num'] = entry_num
                entry['speaker'] = speaker
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Warning: JSON parse error at entry {entry_num}: {e}")
            i = end + 1
        else:
            i = start + 1
    
    return entries

def create_draft_output(entries: List[Dict], input_file: str) -> str:
    """Join draft_translation entries to build the content of INPUT-draft.txt"""
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
    """Analyze the differences between draft_translation and improved_translation"""
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
            
            # Compute a character-level diff
            diff = list(difflib.unified_diff(
                draft.splitlines(keepends=True),
                final.splitlines(keepends=True),
                fromfile='draft',
                tofile='final',
                lineterm=''
            ))
            
            stats['differences'].append({
                'line_num': entry.get('line_num', 'unknown'),
                'draft': draft,
                'final': final,
                'quality_check': entry.get('quality_check', ''),
                'diff': ''.join(diff) if diff else 'no differences'
            })
    
    return stats

def print_summary(stats: Dict, show_details: bool = False, max_examples: int = 10):
    """Display a summary of the results"""
    print("=" * 60)
    print("2-Stage Translation Effect Analysis")
    print("=" * 60)

    print(f"Total entries: {stats['total_entries']}")
    print(f"Unchanged: {stats['identical_count']} ({stats['identical_count']/stats['total_entries']*100:.1f}%)")
    print(f"Changed: {stats['modified_count']} ({stats['modified_count']/stats['total_entries']*100:.1f}%)")

    if not show_details:
        print(f"\nUse the --details option to show details")
        return

    print("\n" + "=" * 60)
    print("Details of changed translations")
    print("=" * 60)

    for i, diff_entry in enumerate(stats['differences'][:max_examples]):
        print(f"\n--- Entry {i+1} (line {diff_entry['line_num']}) ---")
        print(f"Initial translation: {diff_entry['draft']}")
        print(f"Final translation: {diff_entry['final']}")

        if diff_entry['quality_check']:
            print(f"Quality check: {diff_entry['quality_check'][:200]}...")

        print("-" * 40)

    if len(stats['differences']) > max_examples:
        print(f"\n... {len(stats['differences']) - max_examples} more changed entries")

def main():
    parser = argparse.ArgumentParser(description="Analyze the effect of 2-stage translation")
    parser.add_argument("jsonl_file", help="JSONL file to analyze")
    parser.add_argument("-d", "--details", action="store_true", help="Show detailed differences")
    parser.add_argument("-n", "--max-examples", type=int, default=10, help="Maximum number of examples to show")
    parser.add_argument("--draft-output", action="store_true", help="Join draft_translation entries and output INPUT-draft.txt")

    args = parser.parse_args()

    try:
        # Regular analysis processing
        entries = load_jsonl(args.jsonl_file)
        if not entries:
            print("Error: no valid entries found")
            return

        stats = analyze_differences(entries)
        print_summary(stats, args.details, args.max_examples)

        # Additional processing when draft output is requested
        if args.draft_output:
            print("\n" + "=" * 60)
            print("Draft translation output")
            print("=" * 60)

            # Reload entries with speaker info
            entries_with_speakers = load_jsonl_with_speakers(args.jsonl_file)

            # Generate the output file name (INPUT.txt -> INPUT-draft.txt)
            base_name = args.jsonl_file
            if base_name.endswith('.txt'):
                output_file = base_name[:-4] + '-draft.txt'
            else:
                output_file = base_name + '-draft.txt'

            # Join draft translations and write output
            draft_content = create_draft_output(entries_with_speakers, args.jsonl_file)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            print(f"Wrote draft translations to {output_file} ({len(entries_with_speakers)} entries)")

    except FileNotFoundError:
        print(f"Error: file '{args.jsonl_file}' not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
