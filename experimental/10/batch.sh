#!/bin/bash
set -e

cd "$(dirname "$0")"/../..
BASE_DIR="experimental/10"

TRANSLATOR="ollama:gemma4:26b"
REVIEWER="ollama:qwen3.6"
EVALUATOR="ollama:qwen3.6"
ORIGINAL="examples/onde-en.txt"
TERMS_DIR="examples/tr/terms"

declare -A LANG_NAMES
LANG_NAMES[bg]="Bulgarian"
LANG_NAMES[eu]="Basque"
LANG_NAMES[et]="Estonian"
LANG_NAMES[sl]="Slovene"
LANG_NAMES[hu]="Hungarian"

LANGS=(bg eu et sl hu)
LANG_TOTAL=${#LANGS[@]}

mkdir -p "${BASE_DIR}/tr" "${BASE_DIR}/evals" "${BASE_DIR}/tr-rev" "${BASE_DIR}/evals-rev"

BATCH_START=$(date +%s.%N)

# 1. Translation
for i in "${!LANGS[@]}"; do
    LANG_CODE="${LANGS[$i]}"
    LANG_INDEX=$((i + 1))
    LANG_NAME="${LANG_NAMES[$LANG_CODE]}"
    LABEL="${LANG_CODE}: ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL})"
    TR_FILE="${BASE_DIR}/tr/onde-${LANG_CODE}.txt"

    if [ ! -f "${TR_FILE}" ]; then
        echo "=== Translating to ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL}) ==="
        uv run trtools --label "${LABEL} (tr)" --start "${BATCH_START}" translate \
            "${ORIGINAL}" -f English -t "${LANG_NAME}" \
            -o "${TR_FILE}" -m "${TRANSLATOR}" --no-think --threshold 20 \
            --terms-json "${TERMS_DIR}/onde-en.json" \
            --terms-tsv  "${TERMS_DIR}/onde-en.tsv"
    else
        echo "Translation already exists, skipping: ${TR_FILE}"
    fi
done

# 2. Translation evaluation (3 runs)
for i in "${!LANGS[@]}"; do
    LANG_CODE="${LANGS[$i]}"
    LANG_INDEX=$((i + 1))
    LANG_NAME="${LANG_NAMES[$LANG_CODE]}"
    LABEL="${LANG_CODE}: ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL})"
    TR_FILE="${BASE_DIR}/tr/onde-${LANG_CODE}.txt"

    echo "=== Evaluating base translation: ${LANG_NAME} ==="
    for j in 1 2 3; do
        EVAL_FILE="${BASE_DIR}/evals/onde-${LANG_CODE}-${j}.json"
        if [ ! -f "${EVAL_FILE}" ]; then
            echo -e "\nEvaluating ${TR_FILE} (run ${j}/3)..."
            uv run trtools --label "${LABEL} (eval1)" --start "${BATCH_START}" eval \
                --original "${ORIGINAL}" --translation "${TR_FILE}" \
                -m "${EVALUATOR}" -f English -t "${LANG_NAME}" \
                --run $j --runs 3 \
                -o "${EVAL_FILE}"
        else
            echo "Eval ${j} already exists, skipping."
        fi
    done
done

# 3. Review
for i in "${!LANGS[@]}"; do
    LANG_CODE="${LANGS[$i]}"
    LANG_INDEX=$((i + 1))
    LANG_NAME="${LANG_NAMES[$LANG_CODE]}"
    LABEL="${LANG_CODE}: ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL})"
    TR_FILE="${BASE_DIR}/tr/onde-${LANG_CODE}.txt"
    TR_REV_FILE="${BASE_DIR}/tr-rev/onde-${LANG_CODE}.txt"

    if [ ! -f "${TR_REV_FILE}" ]; then
        echo "=== Reviewing ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL}) ==="
        uv run trtools --label "${LABEL} (rev)" --start "${BATCH_START}" review \
            --original "${ORIGINAL}" --translation "${TR_FILE}" \
            -f en -t "${LANG_CODE}" \
            -o "${TR_REV_FILE}" -m "${REVIEWER}" --no-think \
            --terms "${TERMS_DIR}/common.tsv"
    else
        echo "Review already exists, skipping: ${TR_REV_FILE}"
    fi
done

# 4. Post-review evaluation (3 runs)
for i in "${!LANGS[@]}"; do
    LANG_CODE="${LANGS[$i]}"
    LANG_INDEX=$((i + 1))
    LANG_NAME="${LANG_NAMES[$LANG_CODE]}"
    LABEL="${LANG_CODE}: ${LANG_NAME} (${LANG_INDEX}/${LANG_TOTAL})"
    TR_REV_FILE="${BASE_DIR}/tr-rev/onde-${LANG_CODE}.txt"

    echo "=== Evaluating reviewed translation: ${LANG_NAME} ==="
    for j in 1 2 3; do
        EVAL_REV_FILE="${BASE_DIR}/evals-rev/onde-${LANG_CODE}-${j}.json"
        if [ ! -f "${EVAL_REV_FILE}" ]; then
            echo -e "\nEvaluating ${TR_REV_FILE} (run ${j}/3)..."
            uv run trtools --label "${LABEL} (eval2)" --start "${BATCH_START}" eval \
                --original "${ORIGINAL}" --translation "${TR_REV_FILE}" \
                -m "${EVALUATOR}" -f English -t "${LANG_NAME}" \
                --run $j --runs 3 \
                -o "${EVAL_REV_FILE}"
        else
            echo "Eval-rev ${j} already exists, skipping."
        fi
    done
done

echo "=== Base scores ==="
uv run trtools agg "${BASE_DIR}/evals"/onde-*.json | tee    "${BASE_DIR}/SCORES.txt"

echo "=== Reviewed scores ==="
uv run trtools agg "${BASE_DIR}/evals-rev"/onde-*.json | tee -a "${BASE_DIR}/SCORES.txt"
