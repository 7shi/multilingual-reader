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
import re
import sys
from pathlib import Path


def extract_js_object_content(js_content: str, object_name: str) -> dict:
    """
    Extract the content of a JavaScript object from the JS file.
    
    Args:
        js_content: The full JavaScript file content
        object_name: Name of the object to extract (e.g., 'podcastTexts')
        
    Returns:
        Dictionary with language codes as keys and text content as values
    """
    # Pattern to match the object declaration and its content
    pattern = rf'const\s+{object_name}\s*=\s*\{{([^}}]+(?:\}}[^}}]*)*)\}};'
    
    match = re.search(pattern, js_content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find object '{object_name}' in JavaScript file")
    
    object_content = match.group(1)
    
    # Extract each language section
    languages = {}
    
    # Pattern to match language keys and their template literal content
    lang_pattern = r'(\w+):\s*`([^`]*(?:`[^`]*`[^`]*)*)`'
    
    for lang_match in re.finditer(lang_pattern, object_content, re.DOTALL):
        lang_code = lang_match.group(1)
        lang_text = lang_match.group(2)
        
        # Clean up the text content
        # Remove any escaped backticks and normalize line endings
        lang_text = lang_text.replace('\\`', '`')
        lang_text = lang_text.replace('\\n', '\n')
        
        languages[lang_code] = lang_text.strip()
    
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
            
        # Ensure proper speaker format (Speaker: text)
        if ':' in line and not line.startswith(' '):
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
  %(prog)s podcast-text-data.js -o physics_podcast
    Creates: physics_podcast-fr.txt, physics_podcast-en.txt, physics_podcast-ja.txt
  
  %(prog)s custom-data.js -o quantum_mechanics
    Creates: quantum_mechanics-fr.txt, quantum_mechanics-en.txt, quantum_mechanics-ja.txt
        """
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output filename prefix (e.g., "physics" creates physics-fr.txt, physics-en.txt, physics-ja.txt)'
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
        
        # Extract the podcast texts object
        languages = extract_js_object_content(js_content, 'podcastTexts')
        
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