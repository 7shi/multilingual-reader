#!/bin/bash
set -e

cd "$(dirname "$0")"/../..
BASE_DIR="experimental/10"

TRANSLATOR="ollama:gemma4:26b"
REVIEWER="ollama:qwen3.6"
EVALUATOR="ollama:qwen3.6"
ORIGINAL="examples/onde-en.txt"
LANG_CODE="bg"
LANG_NAME="Bulgarian"
TERMS_DIR="examples/tr/terms"

BATCH_START=$(date +%s.%N)
LABEL="${LANG_CODE}: ${LANG_NAME}"

TR_BASE="${BASE_DIR}/tr/onde-${LANG_CODE}.txt"
TR_REV="${BASE_DIR}/tr/onde-${LANG_CODE}-rev.txt"

# 1. 翻訳
if [ ! -f "${TR_BASE}" ]; then
    echo "=== Translating to ${LANG_NAME} ==="
    uv run trtools --label "${LABEL} (tr)" --start "${BATCH_START}" translate \
        "${ORIGINAL}" -f English -t "${LANG_NAME}" \
        -o "${TR_BASE}" -m "${TRANSLATOR}" --no-think --threshold 20 \
        --terms-json "${TERMS_DIR}/onde-en.json" \
        --terms-tsv  "${TERMS_DIR}/onde-en.tsv"
else
    echo "Translation already exists, skipping."
fi

# 2. 翻訳評価（3回）
echo "=== Evaluating base translation ==="
for i in 1 2 3; do
    EVAL_FILE="${BASE_DIR}/evals/onde-${LANG_CODE}-${i}.json"
    if [ ! -f "${EVAL_FILE}" ]; then
        echo -e "\nEvaluating ${TR_BASE} (run ${i}/3)..."
        uv run trtools --label "${LABEL} (eval1)" --start "${BATCH_START}" eval \
            --original "${ORIGINAL}" --translation "${TR_BASE}" \
            -m "${EVALUATOR}" -f English -t "${LANG_NAME}" \
            --run $i --runs 3 \
            -o "${EVAL_FILE}"
    else
        echo "Eval ${i} already exists, skipping."
    fi
done

echo "=== Base scores ==="
uv run trtools agg "${BASE_DIR}/evals/onde-${LANG_CODE}-"{1,2,3}.json | tee "${BASE_DIR}/SCORES.txt"

# 3. 推敲
if [ ! -f "${TR_REV}" ]; then
    echo "=== Reviewing ${LANG_NAME} ==="
    uv run trtools --label "${LABEL} (rev)" --start "${BATCH_START}" review \
        --original "${ORIGINAL}" --translation "${TR_BASE}" \
        -f en -t "${LANG_CODE}" \
        -o "${TR_REV}" -m "${REVIEWER}" --no-think \
        --terms "${TERMS_DIR}/common.tsv"
else
    echo "Review already exists, skipping."
fi

# 4. 推敲後評価（3回）
echo "=== Evaluating reviewed translation ==="
for i in 1 2 3; do
    EVAL_FILE="${BASE_DIR}/evals/onde-${LANG_CODE}-rev-${i}.json"
    if [ ! -f "${EVAL_FILE}" ]; then
        echo -e "\nEvaluating ${TR_REV} (run ${i}/3)..."
        uv run trtools --label "${LABEL} (eval2)" --start "${BATCH_START}" eval \
            --original "${ORIGINAL}" --translation "${TR_REV}" \
            -m "${EVALUATOR}" -f English -t "${LANG_NAME}" \
            --run $i --runs 3 \
            -o "${EVAL_FILE}"
    else
        echo "Eval ${i} already exists, skipping."
    fi
done

echo "=== Reviewed scores ==="
uv run trtools agg "${BASE_DIR}/evals/onde-${LANG_CODE}-rev-"{1,2,3}.json | tee -a "${BASE_DIR}/SCORES.txt"
