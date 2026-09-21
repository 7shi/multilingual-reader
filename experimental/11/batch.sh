#!/bin/bash
# Experiment 11: runs the three reference evaluators (qwen3.6, gemma4:31b, gpt-oss:120b)
# across all three variants (evals, evals-nt, evals-ne), then aggregates the results.
#
# The per-target/per-run work is eval50.py's: this script only supplies the fixed set of
# evaluators and variants that make up the reference comparison. Any other evaluator
# (e.g. a commercial model) can be added the same way, by invoking eval50.py directly with
# its own -m/-s -- see README.md.
#
# Existing result files are left alone, so the script can be re-run; a failed call stops
# the whole run (see eval50.evaluate_target), so a missing output file is a failure, not
# something recorded separately.

set -eu

cd "$(dirname "$0")"/../..
BASE_DIR="experimental/11"
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
# evidence costs.
declare -A VARIANTS
VARIANTS[evals]=""
VARIANTS[evals-nt]="--no-think --no-evidence"
VARIANTS[evals-ne]="--no-evidence"

VARIANT_ORDER=(evals evals-nt evals-ne)

for VARIANT in "${VARIANT_ORDER[@]}"; do
    echo -e "\n########## Variant: ${VARIANT} ##########"

    # Evaluator is the outer loop: switching models means reloading them, so each one is
    # loaded once and used for every target rather than cycled per translation.
    for EVALUATOR in "${EVAL_ORDER[@]}"; do
        EV_NAME="${EVALUATORS[$EVALUATOR]}"
        echo -e "\n########## Evaluator: ${EV_NAME} ##########"

        uv run "${BASE_DIR}/eval50.py" -m "${EVALUATOR}" -s "${EV_NAME}" \
            --split "${SPLIT}" ${VARIANTS[$VARIANT]}
    done
done

echo -e "\n=== Comparison ==="
uv run "${BASE_DIR}/agg50.py" | tee "${BASE_DIR}/SCORES.md"
