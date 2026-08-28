import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Script to fall back empty output lines to the base translation")
parser.add_argument("--reviewed", required=True, help="Revised text file")
parser.add_argument("--baseline", required=True, help="Baseline translation text file")
parser.add_argument("-o", "--output", required=True, help="Output file name")
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

    # Detect lines where the content after "Speaker: " is empty
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
    print("No fallback needed. No output file will be created.")
    sys.exit(0)

print(f"\nFalling back {len(fallback_indices)} line(s): {fallback_indices}")

os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
with open(args.output, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line)

print(f"Saved to: {args.output}")
