#!/usr/bin/env python3
"""
Script to automatically sync the tables in SCORES.md into README.md

Algorithm:
1. Store the tables from SCORES.md in a dict, keyed by header row
2. Scan README.md line by line, matching against the dict whenever a table header is detected
"""


def extract_tables_from_scores(content: str) -> dict[str, list[str]]:
    """
    Extract the tables from SCORES.md and store them in a dict, keyed by header row.

    When a key is duplicated, only the first occurrence is kept.

    Returns:
        {header row: [all rows of the table (header, separator, data rows)]}
    """
    lines = content.split('\n')
    tables = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect a table header row (a line starting with |)
        if line.startswith('|'):
            header_line = line
            table_lines = [header_line]
            i += 1

            # Collect the remaining rows of the table (as long as lines keep starting with |)
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('|'):
                    table_lines.append(next_line)
                    i += 1
                elif next_line == '':
                    # A blank line might mark the end of the table, but keep checking the next line
                    i += 1
                    break
                else:
                    # A non-table line ends the table
                    break

            # Store the table keyed by header row (keep the first occurrence on duplicates)
            if header_line not in tables:
                tables[header_line] = table_lines
        else:
            i += 1

    return tables


def sync_readme_with_scores(readme_content: str, tables_dict: dict[str, list[str]]) -> str:
    """
    Scan the content of README.md and replace any matched table header with the corresponding table from SCORES.md
    """
    lines = readme_content.split('\n')
    result = []
    i = 0
    table_count = 0
    matched_count = 0

    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()

        # Detect a table header row
        if line_stripped.startswith('|'):
            table_count += 1
            header_preview = line_stripped[:60] + '...' if len(line_stripped) > 60 else line_stripped

            if line_stripped in tables_dict:
                # On a match
                matched_count += 1
                print(f"  ✓ Table #{table_count}: matched")
                print(f"    Header: {header_preview}")

                # Get the corresponding table from SCORES.md
                new_table = tables_dict[line_stripped]
                result.extend(new_table)
                i += 1

                # Skip the old table in README.md
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('|'):
                        i += 1
                    elif next_line == '':
                        # Keep and skip the blank line too
                        result.append('')
                        i += 1
                        break
                    else:
                        # A non-table line ends this loop
                        break
            else:
                # No match
                print(f"  × Table #{table_count}: no match (left unchanged)")
                print(f"    Header: {header_preview}")

                # Keep the line as is
                result.append(line)
                i += 1
        else:
            # Keep the line as is
            result.append(line)
            i += 1

    print(f"\n  Total: detected {table_count} table(s), updated {matched_count}")
    return '\n'.join(result)


def main():
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Script to sync the tables in SCORES.md into README.md')
    parser.add_argument('scores_path', type=Path, help='Path to the SCORES.md file')
    args = parser.parse_args()

    # File paths
    scores_path = args.scores_path
    readme_path = Path(__file__).parent / 'README.md'

    # Existence check
    if not scores_path.exists():
        print(f"Error: {scores_path} not found")
        return 1

    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        return 1

    # Read the files
    scores_content = scores_path.read_text(encoding='utf-8')
    readme_content = readme_path.read_text(encoding='utf-8')

    # Extract the tables from SCORES.md
    print("Extracting tables from SCORES.md...")
    tables_dict = extract_tables_from_scores(scores_content)
    print(f"  Detected {len(tables_dict)} table(s)")

    # Update README.md
    print("Updating tables in README.md...")
    updated_content = sync_readme_with_scores(readme_content, tables_dict)

    # Write README.md
    readme_path.write_text(updated_content, encoding='utf-8')
    print("Done!")

    return 0


if __name__ == '__main__':
    exit(main())
