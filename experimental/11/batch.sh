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
# Three variants of the new scheme are run: "evals" with thinking on (matching what
# trtools/batch.py:169 hardcodes for the production evaluation phase), "evals-nt" with
# --no-think, to see how much thinking buys in score stability and how much it costs in
# time, and "evals-ne" with evidence off and thinking left on. Each output file records
# its own "duration_seconds", "no_think" and "no_evidence" fields, so the comparison does
# not depend on file mtimes.
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

# Variant (directory name) -> extra eval50.py args
#
# evals-nt also passes --no-evidence: without thinking to hold the rationale, models were
# padding every item with an unrequested overall_comment-like field instead of the requested
# evidence, bloating the answer enough to hit --max-length. Dropping the per-item evidence
# field removes that pressure; the run-level overall_comment is unaffected.
#
# evals-ne drops evidence but keeps thinking, which is the cell evals-nt is missing: since
# evals-nt changes both at once, nothing there separates what thinking is worth from what
# evidence costs. It also tests whether writing evidence takes effort away from the verdict
# itself -- the evidence in evals/ frequently cites line numbers that are simply wrong,
# which is unsurprising given that the model is handed the texts without any line numbers
# in them, but the question is whether producing it also moves the verdict.
declare -A VARIANTS
VARIANTS[evals]=""
VARIANTS[evals-nt]="--no-think --no-evidence"
VARIANTS[evals-ne]="--no-evidence"

VARIANT_ORDER=(evals evals-nt evals-ne)

# A failure here is a call that came back structurally wrong: valid JSON that does not
# fit the schema, which the retry inside call_json does not catch. How often that happens
# is itself part of what the experiment measures, so failures are recorded rather than
# allowed to stop the batch.
ATTEMPTS=3

# try_eval <scheme> <failures_file> <output> <command...>
try_eval() {
    local scheme="$1" failures="$2" out="$3"
    shift 3
    local attempt
    for attempt in $(seq 1 ${ATTEMPTS}); do
        if "$@"; then
            return 0
        fi
        echo "  attempt ${attempt}/${ATTEMPTS} failed for ${out}"
        rm -f "${out}"
    done
    printf '%s\t%s\n' "${scheme}" "${out}" >> "${failures}"
    echo "  GIVING UP on ${out}"
    return 0
}

run_eval() {  # <failures_file> <output> <translation> <lang_name> <evaluator> <label> <run> <index> <extra_args...>
    local failures="$1" out="$2" translation="$3" lang_name="$4" evaluator="$5" label="$6" run="$7" index="$8"
    shift 8
    local attempt_start
    attempt_start=$(date +%s.%N)
    try_eval new "${failures}" "${out}" \
        uv run "${BASE_DIR}/eval50.py" \
        --original "${ORIGINAL}" --translation "${translation}" \
        -m "${evaluator}" -f English -t "${lang_name}" \
        --split "${SPLIT}" --run "${run}" --runs "${RUNS}" \
        --label "${label}" --start "${BATCH_START}" \
        --attempt-start "${attempt_start}" \
        --index "${index}" --count "${TOTAL}" -o "${out}" "$@"
}

mapfile -t TARGET_ROWS < <(tail -n +2 "${TARGETS}")
TOTAL=$(( ${#TARGET_ROWS[@]} * ${#EVAL_ORDER[@]} * RUNS * ${#VARIANT_ORDER[@]} ))
INDEX=0
BATCH_START=$(date +%s.%N)

for VARIANT in "${VARIANT_ORDER[@]}"; do
    EVAL_DIR="${BASE_DIR}/${VARIANT}"
    FAILURES="${BASE_DIR}/FAILURES-${VARIANT}.txt"
    mkdir -p "${EVAL_DIR}"
    : > "${FAILURES}"

    echo -e "\n########## Variant: ${VARIANT} ##########"

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
            LABEL="${LANG}: ${LANG_NAME} / ${EV_NAME} / ${VARIANT}"

            for RUN in $(seq 1 ${RUNS}); do
                OUT="${EVAL_DIR}/${STEM}-${RUN}.json"
                INDEX=$((INDEX + 1))
                if [ ! -f "${OUT}" ]; then
                    echo -e "\n=== [${INDEX}/${TOTAL}] ${TRANSLATOR}/${LANG} ${EV_NAME} ${VARIANT} run ${RUN} ==="
                    run_eval "${FAILURES}" "${OUT}" "${TR_FILE}" "${LANG_NAME}" "${EVALUATOR}" "${LABEL}" "${RUN}" "${INDEX}" ${VARIANTS[$VARIANT]}
                else
                    echo "[${INDEX}/${TOTAL}] exists, skipping: ${OUT}"
                fi
            done
        done
    done
done

echo -e "\n=== Comparison ==="
uv run "${BASE_DIR}/agg50.py" | tee "${BASE_DIR}/SCORES.md"
