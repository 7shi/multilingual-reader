#!/bin/bash
# 3-phase multi-model translation execution script

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <input file> <source language> <target language> <output file> <quality check model>"
    echo "Example: $0 input.txt French Spanish output.txt ollama:qwen2.5:7b"
    exit 1
fi

INPUT_FILE="$1"
FROM_LANG="$2"
TO_LANG="$3"
OUTPUT_FILE="$4"
CHECKER_MODEL="$5"

echo "Starting 3-phase multi-model translation: $FROM_LANG → $TO_LANG"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Quality check model: $CHECKER_MODEL"
echo

# Phase 1: Initial translation
echo "=== Phase 1: Initial translation ==="
python translate.py phase1 "$INPUT_FILE" -f "$FROM_LANG" -t "$TO_LANG" -o "$OUTPUT_FILE"
if [ $? -ne 0 ]; then
    echo "Error: Phase 1 failed"
    exit 1
fi

# Generate intermediate file names
BASE_NAME="${OUTPUT_FILE%.*}"
DRAFT_FILE="${BASE_NAME}_draft.json"
CHECK_FILE="${BASE_NAME}_check.json"

echo
# Phase 2: Quality check
echo "=== Phase 2: Quality check (model: $CHECKER_MODEL) ==="
python translate.py phase2 -o "$OUTPUT_FILE" --draft-file "$DRAFT_FILE" -c "$CHECKER_MODEL"
if [ $? -ne 0 ]; then
    echo "Error: Phase 2 failed"
    exit 1
fi

echo
# Phase 3: Apply corrections
echo "=== Phase 3: Apply corrections ==="
python translate.py phase3 -o "$OUTPUT_FILE" --draft-file "$DRAFT_FILE" --check-file "$CHECK_FILE"
if [ $? -ne 0 ]; then
    echo "Error: Phase 3 failed"
    exit 1
fi

echo
echo "=== 3-phase translation complete ==="
echo "Final result: $OUTPUT_FILE"
echo "Intermediate files:"
echo "  - Initial translation: $DRAFT_FILE"
echo "  - Quality check: $CHECK_FILE"
