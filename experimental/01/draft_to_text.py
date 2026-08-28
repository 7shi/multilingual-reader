#!/usr/bin/env python3
# Utility to take a draft.json file and output only the translations as plain text

import argparse
import json
import os
import sys

def load_draft_json(file_path):
    """Load a draft.json file"""
    if not os.path.exists(file_path):
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error: failed to parse JSON file: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: failed to read file: {e}", file=sys.stderr)
        return None

def extract_translations(data):
    """Extract only the translations from the JSON data"""
    translations = []

    if isinstance(data, dict) and 'results' in data:
        results = data['results']

        # List format
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and 'speaker' in item and 'translation' in item:
                    translations.append({
                        'speaker': item['speaker'],
                        'translation': item['translation']
                    })

        # Dict format (for legacy support)
        elif isinstance(results, dict):
            for line_key, item_data in results.items():
                if isinstance(item_data, dict) and 'speaker' in item_data and 'translation' in item_data:
                    translations.append({
                        'speaker': item_data['speaker'],
                        'translation': item_data['translation']
                    })
    
    return translations

def save_translations_to_text(translations, output_path):
    """Save the translations to a text file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in translations:
                f.write(f"{item['speaker']}: {item['translation']}\n")
        return True
    except Exception as e:
        print(f"Error: failed to write output file: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Output only the translations from a draft.json file as plain text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python draft_to_text.py output_draft.json                    # generates output_draft.txt
  python draft_to_text.py output_draft.json -o custom.txt     # generates custom.txt
  python draft_to_text.py output_draft.json --stdout          # print to stdout

Supported formats:
  - New format: {"metadata": {...}, "results": [{"speaker": "...", "translation": "..."}, ...]}
  - Old format: {"metadata": {...}, "results": {"key": {"speaker": "...", "translation": "..."}, ...}}
"""
    )

    parser.add_argument("input_file", help="Input draft.json file")
    parser.add_argument("-o", "--output", help="Output file name (default: change extension to .txt)")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout (no file output)")

    args = parser.parse_args()

    # Load the JSON file
    data = load_draft_json(args.input_file)
    if data is None:
        sys.exit(1)

    # Extract translation data
    translations = extract_translations(data)
    if not translations:
        print("Warning: no translation data found", file=sys.stderr)
        sys.exit(1)

    print(f"Extracted {len(translations)} lines of translation data")

    # Output processing
    if args.stdout:
        # Print to stdout
        for item in translations:
            print(f"{item['speaker']}: {item['translation']}")
    else:
        # File output
        if args.output:
            output_path = args.output
        else:
            # Change extension to .txt
            output_path = args.input_file.replace('.json', '.txt')

        if save_translations_to_text(translations, output_path):
            print(f"Output complete: {output_path}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()