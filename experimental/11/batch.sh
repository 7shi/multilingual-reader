#!/bin/bash
# Experiment 11: evaluates each target translation with the 50-item scheme, three runs
# under each of three evaluator models, to see whether the score stops depending on the
# run and on which model produced it.
#
# Targets are the translations whose score wobbled most under the current scheme
# (see pick_unstable.py / targets.tsv).
#
# Only the new scheme is run here. The old scheme is measured under qwen3.6 only -- that
# is the reference the production tables are built on -- and those results already exist
# in examples/tr/onde/*/evals/, which agg50.py reads in place. Running the old scheme
# under other evaluators would answer a question this experiment is not asking: model
# dependence is what the new scheme is being tested for.
#
# Thinking is left ON. trtools/batch.py:169 hardcodes no_think=False for the evaluation
# phase, so every accumulated evaluation was produced with it; passing --no-think here
# would measure something the production tables never measured.
#
# Existing result files are left alone, so the script can be re-run.

set -u

cd "$(dirname "$0")"/../..
BASE_DIR="experimental/11"

ORIGINAL="examples/onde-en.txt"
TARGETS="${BASE_DIR}/targets.tsv"
RUNS=3
SPLIT="${SPLIT:-none}"

# Evaluator model -> name used in result filenames
declare -A EVALUATORS
EVALUATORS[ollama:qwen3.6]="qwen3.6"
EVALUATORS[ollama:gemma4:31b]="gemma4-31b"
EVALUATORS[ollama:gpt-oss:120b]="gpt-oss-120b"

EVAL_ORDER=(ollama:qwen3.6 ollama:gemma4:31b ollama:gpt-oss:120b)

# A failure here is a call that came back structurally wrong: valid JSON that does not
# fit the schema, which the retry inside call_json does not catch. How often that happens
# is itself part of what the experiment measures, so failures are recorded rather than
# allowed to stop the batch.
ATTEMPTS=3
FAILURES="${BASE_DIR}/FAILURES.txt"

mkdir -p "${BASE_DIR}/evals"
: > "${FAILURES}"

# try_eval <scheme> <output> <command...>
try_eval() {
    local scheme="$1" out="$2"
    shift 2
    local attempt
    for attempt in $(seq 1 ${ATTEMPTS}); do
        if "$@"; then
            return 0
        fi
        echo "  attempt ${attempt}/${ATTEMPTS} failed for ${out}"
        rm -f "${out}"
    done
    printf '%s\t%s\n' "${scheme}" "${out}" >> "${FAILURES}"
    echo "  GIVING UP on ${out}"
    return 0
}

run_eval() {  # <output> <translation> <lang_name> <evaluator> <label> <run> <index>
    try_eval new "$1" \
        uv run "${BASE_DIR}/eval50.py" \
        --original "${ORIGINAL}" --translation "$2" \
        -m "$4" -f English -t "$3" \
        --split "${SPLIT}" --run "$6" --runs "${RUNS}" \
        --label "$5" --start "${BATCH_START}" \
        --index "$7" --count "${TOTAL}" -o "$1"
}

mapfile -t TARGET_ROWS < <(tail -n +2 "${TARGETS}")
TOTAL=$(( ${#TARGET_ROWS[@]} * ${#EVAL_ORDER[@]} * RUNS ))
INDEX=0
BATCH_START=$(date +%s.%N)

# Evaluator is the outer loop: switching models means reloading them, so each one is
# loaded once and used for every target rather than cycled per translation.
for EVALUATOR in "${EVAL_ORDER[@]}"; do
    EV_NAME="${EVALUATORS[$EVALUATOR]}"
    echo -e "\n########## Evaluator: ${EV_NAME} ##########"

    for ROW in "${TARGET_ROWS[@]}"; do
        IFS=$'\t' read -r TRANSLATOR LANG LANG_NAME RANGE SCORES MEDIAN <<< "${ROW}"
        TR_FILE="examples/tr/onde/${TRANSLATOR}/tr/onde-${LANG}.txt"

        if [ ! -f "${TR_FILE}" ]; then
            echo "Missing translation, skipping: ${TR_FILE}"
            continue
        fi

        STEM="onde-${TRANSLATOR}-${LANG}-${EV_NAME}"
        LABEL="${LANG}: ${LANG_NAME} / ${EV_NAME}"

        for RUN in $(seq 1 ${RUNS}); do
            OUT="${BASE_DIR}/evals/${STEM}-${RUN}.json"
            INDEX=$((INDEX + 1))
            if [ ! -f "${OUT}" ]; then
                echo -e "\n=== [${INDEX}/${TOTAL}] ${TRANSLATOR}/${LANG} ${EV_NAME} run ${RUN} ==="
                run_eval "${OUT}" "${TR_FILE}" "${LANG_NAME}" "${EVALUATOR}" "${LABEL}" "${RUN}" "${INDEX}"
            else
                echo "[${INDEX}/${TOTAL}] exists, skipping: ${OUT}"
            fi
        done
    done
done

echo -e "\n=== Comparison ==="
uv run "${BASE_DIR}/agg50.py" | tee "${BASE_DIR}/SCORES.md"
