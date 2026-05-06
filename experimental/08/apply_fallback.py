import argparse
import os
import sys

parser = argparse.ArgumentParser(description="空出力行をベース訳でフォールバックするスクリプト")
parser.add_argument("--reviewed", required=True, help="推敲後テキストファイル")
parser.add_argument("--baseline", required=True, help="ベースライン翻訳テキストファイル")
parser.add_argument("-o", "--output", required=True, help="出力ファイル名")
args = parser.parse_args()

with open(args.reviewed, "r", encoding="utf-8") as f:
    reviewed_lines = f.readlines()
with open(args.baseline, "r", encoding="utf-8") as f:
    baseline_lines = f.readlines()

if len(reviewed_lines) != len(baseline_lines):
    print(f"Warning: Line count mismatch (reviewed={len(reviewed_lines)}, baseline={len(baseline_lines)}).")

results = []
fallback_indices = []

for i, (rev_line, base_line) in enumerate(zip(reviewed_lines, baseline_lines)):
    rev_content = rev_line.rstrip("\n")
    base_content = base_line.rstrip("\n")

    # "Speaker: " の後が空の行を検出
    is_empty = False
    if ":" in rev_content:
        _, after_colon = rev_content.split(":", 1)
        if not after_colon.strip():
            is_empty = True
    elif not rev_content.strip():
        is_empty = True

    if is_empty:
        results.append(base_content + "\n")
        fallback_indices.append(i + 1)
        print(f"  Line {i+1}: [empty] -> {base_content}")
    else:
        results.append(rev_line)

if not fallback_indices:
    print("フォールバック不要。出力ファイルは作成しません。")
    sys.exit(0)

print(f"\n{len(fallback_indices)}行をフォールバック: {fallback_indices}")

os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
with open(args.output, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line)

print(f"保存先: {args.output}")
