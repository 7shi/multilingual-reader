#!/bin/bash
set -e

# 作業ディレクトリに移動して実行パスを解決しやすくする
cd "$(dirname "$0")"/../..
BASE_DIR="experimental/08"

mkdir -p "${BASE_DIR}/tr" "${BASE_DIR}/evals" "${BASE_DIR}/tr-fb" "${BASE_DIR}/evals-fb"

REVIEWER="ollama:qwen3.6"
EVALUATOR="ollama:qwen3.6"
ORIGINAL_FILE="examples/onde-en.txt"

# 対象言語
LANGS=(
    "nl:Dutch"
    "cs:Czech"
)

for LANG_INFO in "${LANGS[@]}"; do
    CODE="${LANG_INFO%%:*}"
    LANG_NAME="${LANG_INFO##*:}"

    TR_BASE="examples/tr/onde/gemma4/tr/onde-${CODE}.txt"
    OUTPUT_FILE="${BASE_DIR}/tr/onde-${CODE}-reviewed.txt"

    echo "=== Reviewing ${LANG_NAME} (1-step CoT) ==="
    if [ ! -f "${OUTPUT_FILE}" ]; then
        uv run "${BASE_DIR}/review.py" \
            --original "${ORIGINAL_FILE}" \
            --translation "${TR_BASE}" \
            -f English -t "${LANG_NAME}" \
            -o "${OUTPUT_FILE}" \
            -m "${REVIEWER}"
    else
        echo "Review output already exists, skipping."
    fi

    echo "=== Evaluating ${LANG_NAME} ==="
    for i in 1 2 3; do
        EVAL_FILE="${BASE_DIR}/evals/onde-${CODE}-reviewed-${i}.json"
        if [ ! -f "${EVAL_FILE}" ]; then
            echo -e "\nEvaluating ${OUTPUT_FILE} (run ${i})..."
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

echo ""
echo "=== Applying Fallback ==="
for LANG_INFO in "${LANGS[@]}"; do
    CODE="${LANG_INFO%%:*}"
    LANG_NAME="${LANG_INFO##*:}"

    REVIEWED_FILE="${BASE_DIR}/tr/onde-${CODE}-reviewed.txt"
    TR_BASE="examples/tr/onde/gemma4/tr/onde-${CODE}.txt"
    FB_FILE="${BASE_DIR}/tr-fb/onde-${CODE}-reviewed.txt"

    echo "--- ${LANG_NAME} ---"
    uv run "${BASE_DIR}/apply_fallback.py" \
        --reviewed "${REVIEWED_FILE}" \
        --baseline "${TR_BASE}" \
        -o "${FB_FILE}"

    if [ -f "${FB_FILE}" ]; then
        echo "=== Evaluating ${LANG_NAME} (fallback) ==="
        for i in 1 2 3; do
            EVAL_FILE="${BASE_DIR}/evals-fb/onde-${CODE}-reviewed-${i}.json"
            if [ ! -f "${EVAL_FILE}" ]; then
                echo -e "\nEvaluating ${FB_FILE} (run ${i})..."
                uv run trtools eval \
                    --original "${ORIGINAL_FILE}" \
                    --translation "${FB_FILE}" \
                    -m "${EVALUATOR}" \
                    -f English -t "${LANG_NAME}" \
                    -o "${EVAL_FILE}"
            else
                echo "Evaluation ${i} already exists, skipping."
            fi
        done
    fi
done

echo "=== Aggregating Scores ==="
uv run trtools agg "${BASE_DIR}"/evals/*.json | tee "${BASE_DIR}"/SCORES.txt

FB_EVALS=("${BASE_DIR}"/evals-fb/*.json)
if [ -f "${FB_EVALS[0]}" ]; then
    echo ""
    echo "=== Aggregating Fallback Scores ==="
    uv run trtools agg "${BASE_DIR}"/evals-fb/*.json | tee "${BASE_DIR}"/SCORES-fb.txt
fi
