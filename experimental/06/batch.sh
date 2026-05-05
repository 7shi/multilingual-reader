#!/bin/bash
set -e

# 作業ディレクトリに移動して実行パスを解決しやすくする
cd "$(dirname "$0")"/../..
BASE_DIR="experimental/06"

mkdir -p "${BASE_DIR}/tr" "${BASE_DIR}/evals"

TRANSLATOR="ollama:gemma4:26b"
EVALUATOR="ollama:qwen3.6"
INPUT_FILE="examples/onde-en.txt"

# 対象言語
LANGS=(
    "nl:Dutch"
    "cs:Czech"
)

for LANG_INFO in "${LANGS[@]}"; do
    CODE="${LANG_INFO%%:*}"
    LANG_NAME="${LANG_INFO##*:}"

    DRAFT_FILE="${BASE_DIR}/tr/onde-${CODE}-draft.txt"
    OUTPUT_FILE="${BASE_DIR}/tr/onde-${CODE}-final.txt"

    echo "=== Translating to ${LANG_NAME} (2-stage) ==="
    if [ ! -f "${OUTPUT_FILE}" ]; then
        uv run "${BASE_DIR}/translate.py" "${INPUT_FILE}" \
            -f English -t "${LANG_NAME}" \
            -o "${OUTPUT_FILE}" \
            -d "${DRAFT_FILE}" \
            -m "${TRANSLATOR}" \
            --no-think
    else
        echo "Translation already exists, skipping."
    fi

    echo "=== Evaluating ${LANG_NAME} (Draft) ==="
    for i in 1 2 3; do
        EVAL_FILE="${BASE_DIR}/evals/onde-${CODE}-draft-${i}.json"
        if [ ! -f "${EVAL_FILE}" ]; then
            uv run trtools eval \
                --original "${INPUT_FILE}" \
                --translation "${DRAFT_FILE}" \
                -m "${EVALUATOR}" \
                -f English -t "${LANG_NAME}" \
                -o "${EVAL_FILE}"
        else
            echo "Evaluation Draft ${i} already exists, skipping."
        fi
    done

    echo "=== Evaluating ${LANG_NAME} (Final) ==="
    for i in 1 2 3; do
        EVAL_FILE="${BASE_DIR}/evals/onde-${CODE}-final-${i}.json"
        if [ ! -f "${EVAL_FILE}" ]; then
            uv run trtools eval \
                --original "${INPUT_FILE}" \
                --translation "${OUTPUT_FILE}" \
                -m "${EVALUATOR}" \
                -f English -t "${LANG_NAME}" \
                -o "${EVAL_FILE}"
        else
            echo "Evaluation Final ${i} already exists, skipping."
        fi
    done
done

echo "=== Aggregating Scores ==="
uv run trtools agg "${BASE_DIR}"/evals/*.json | tee "${BASE_DIR}"/SCORES.txt