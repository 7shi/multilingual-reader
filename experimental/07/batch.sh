#!/bin/bash
set -e

# Move to the working directory to simplify resolving execution paths
cd "$(dirname "$0")"/../..
BASE_DIR="experimental/07"

mkdir -p "${BASE_DIR}/tr" "${BASE_DIR}/evals"

REVIEWER="ollama:qwen3.6"
EVALUATOR="ollama:qwen3.6"
ORIGINAL_FILE="examples/onde-en.txt"

# Target languages
LANGS=(
    "nl:Dutch"
    "cs:Czech"
)

for LANG_INFO in "${LANGS[@]}"; do
    CODE="${LANG_INFO%%:*}"
    LANG_NAME="${LANG_INFO##*:}"

    TR_BASE="examples/tr/onde/gemma4/tr/onde-${CODE}.txt"
    OUTPUT_FILE="${BASE_DIR}/tr/onde-${CODE}-reviewed.txt"

    echo "=== Reviewing ${LANG_NAME} ==="
    if [ ! -f "${OUTPUT_FILE}" ]; then
        uv run "${BASE_DIR}/review.py" \
            --original "${ORIGINAL_FILE}" \
            --translation "${TR_BASE}" \
            -f English -t "${LANG_NAME}" \
            -o "${OUTPUT_FILE}" \
            -m "${REVIEWER}" \
            --no-think
    else
        echo "Review output already exists, skipping."
    fi

    echo "=== Evaluating ${LANG_NAME} ==="
    for i in 1 2 3; do
        EVAL_FILE="${BASE_DIR}/evals/onde-${CODE}-reviewed-${i}.json"
        if [ ! -f "${EVAL_FILE}" ]; then
            uv run trtools eval \
                --original "${ORIGINAL_FILE}" \
                --translation "${OUTPUT_FILE}" \
                -m "${EVALUATOR}" \
                -f English -t "${LANG_NAME}" \
                -o "${EVAL_FILE}"
        else
            echo "Evaluation ${i} already exists, skipping."
        fi
    done
done

echo "=== Aggregating Scores ==="
uv run trtools agg "${BASE_DIR}"/evals/*.json | tee "${BASE_DIR}"/SCORES.txt