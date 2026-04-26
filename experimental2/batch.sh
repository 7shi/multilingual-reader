#!/bin/bash
set -e

INPUT="../examples/finetuning-fr.txt"
EVALUATOR="ollama:qwen3.6"
EVAL_OPT="--original $INPUT -f French -t Spanish -m $EVALUATOR -w 3"

MODELS=($(cat MODELS.txt))

declare -A MODEL_ID=(
    [aya-expanse-8b]="ollama:aya-expanse:8b"
    [aya-expanse-32b]="ollama:aya-expanse:32b"
    [command-r7b]="ollama:command-r7b"
    [command-r-35b]="ollama:command-r:35b-08-2024-q4_K_M"
    [gemma2-9b]="ollama:gemma2:9b-instruct-q4_K_M"
    [gemma3-4b]="ollama:gemma3:4b"
    [gemma3-12b]="ollama:gemma3:12b"
    [gemma3-27b]="ollama:gemma3:27b"
    [gemma3n-e4b]="ollama:gemma3n:e4b"
    [gemma4-e2b]="ollama:gemma4:e2b"
    [gemma4-e4b]="ollama:gemma4:e4b"
    [gemma4-26b]="ollama:gemma4:26b"
    [gemma4-31b]="ollama:gemma4:31b"
    [gpt-oss-20b]="ollama:gpt-oss:20b"
    [gpt-oss-120b]="ollama:gpt-oss:120b"
    [llama3.3]="ollama:llama3.3"
    [llama4-scout]="ollama:llama4:scout"
    [mixtral-8x7b]="ollama:mixtral:8x7b"
    [mixtral-8x22b]="ollama:mixtral:8x22b"
    [mistral-small3.2]="ollama:mistral-small3.2"
    [ministral-3-3b]="ollama:ministral-3:3b"
    [ministral-3-8b]="ollama:ministral-3:8b"
    [ministral-3-14b]="ollama:ministral-3:14b"
    [phi4]="ollama:phi4"
    [qwen3-4b]="ollama:qwen3:4b"
    [qwen3-14b]="ollama:qwen3:14b"
    [qwen3-30b]="ollama:qwen3:30b"
    [qwen3-32b]="ollama:qwen3:32b"
    [qwen3.5-4b]="ollama:qwen3.5:4b"
    [qwen3.5-9b]="ollama:qwen3.5:9b"
    [qwen3.5-27b]="ollama:qwen3.5:27b"
    [qwen3.5-35b]="ollama:qwen3.5:35b"
    [qwen3.6-27b]="ollama:qwen3.6:27b"
    [qwen3.6-35b]="ollama:qwen3.6"
)

needs_no_think() {
    case "$1" in
        gemma4-*|qwen3-*|qwen3.*) return 0 ;;
        *) return 1 ;;
    esac
}

mkdir -p tr evals

# --- 翻訳 ---
for model in "${MODELS[@]}"; do
    out="tr/$model.txt"
    if [ -f "$out" ]; then
        echo "Skipping $out (already exists)"
        continue
    fi
    extra=""
    if needs_no_think "$model"; then extra="--no-think"; fi
    echo -e "\nTranslating $out ..."
    uv run translate.py $INPUT -f French -t Spanish \
      -o "$out" -m ${MODEL_ID[$model]} --summary glossary $extra || true
done

# --- 評価 ---
for model in "${MODELS[@]}"; do
    out="tr/$model.txt"
    if [ ! -f "$out" ]; then
        echo "Skipping $model evaluation (translation not available)"
        continue
    fi
    for run in {1..3}; do
        eval_out="evals/$model-eval-$run.json"
        if [ -f "$eval_out" ]; then
            echo "Skipping $eval_out (already exists)"
        else
            echo -e "\nEvaluating $out (run $run)..."
            uv run tr-eval $EVAL_OPT --translation "$out" -o "$eval_out"
        fi
    done
done

# --- 集約 ---
jsons=(evals/*.json)
if [ -e "${jsons[0]}" ]; then
    echo -e "\nAggregating all models ..."
    uv run tr-agg "${jsons[@]}" | tee SCORES.txt
else
    echo "No eval files found, skipping aggregation"
fi
