#!/bin/bash
set -e

# 作業ディレクトリに移動して実行パスを解決しやすくする
cd "$(dirname "$0")"/../..
BASE_DIR="experimental/09"

mkdir -p "${BASE_DIR}/tr" "${BASE_DIR}/evals"

REVIEWER="ollama:qwen3.6"
EVALUATOR="ollama:qwen3.6"
ORIGINAL_FILE="examples/onde-en.txt"

# 言語ごとの最高得点翻訳をTSVに保存
TSV_FILE="${BASE_DIR}/best.tsv"
uv run "${BASE_DIR}/find_best.py" > "${TSV_FILE}"
echo "Generated: ${TSV_FILE}"

LANG_TOTAL=$(wc -l < "${TSV_FILE}")
LANG_INDEX=0

while IFS=$'\t' read -r CODE _SCORE TR_BASE LANG_NAME; do
    LANG_INDEX=$((LANG_INDEX + 1))
    OUTPUT_FILE="${BASE_DIR}/tr/onde-${CODE}.txt"

    echo "=== Reviewing ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL}) from ${TR_BASE} ==="
    if [ ! -f "${OUTPUT_FILE}" ]; then
        uv run "${BASE_DIR}/review.py" \
            --original "${ORIGINAL_FILE}" \
            --translation "${TR_BASE}" \
            -f en -t "${CODE}" \
            -o "${OUTPUT_FILE}" \
            -m "${REVIEWER}" \
            --no-think \
            --lang-index "${LANG_INDEX}" \
            --lang-total "${LANG_TOTAL}" \
            --terms "examples/tr/terms/common.tsv"
    else
        echo "Review output already exists, skipping."
    fi

    echo "=== Evaluating ${LANG_NAME} (${CODE}) ==="
    for i in 1 2 3; do
        EVAL_FILE="${BASE_DIR}/evals/onde-${CODE}-${i}.json"
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
done < "${TSV_FILE}"

echo "=== Aggregating Scores ==="
uv run trtools agg "${BASE_DIR}"/evals/*.json | tee "${BASE_DIR}"/SCORES.txt
