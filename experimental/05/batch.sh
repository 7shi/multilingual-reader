#!/bin/bash
set -e

INPUT="../../examples/finetuning-fr.txt"
TERMS_JSON="../../examples/tr/terms/finetuning-fr.json"
TERMS_TSV="../../examples/tr/terms/finetuning-fr.tsv"
EVALUATOR="ollama:qwen3.6"
EVAL_OPT="--original $INPUT -f French -t Spanish -m $EVALUATOR -w 3"

MODELS=($(cat MODELS.txt))

declare -A MODEL_ID=(
    [gemma4-26b]="ollama:gemma4:26b"
    [gemma4-e4b]="ollama:gemma4:e4b"
)

mkdir -p tr evals

# --- 翻訳（モデル × 翻訳run = 6 ファイル） ---
for model in "${MODELS[@]}"; do
    for trrun in 1 2 3; do
        out="tr/$model-$trrun.txt"
        if [ -f "$out" ]; then
            echo "Skipping $out (already exists)"
            continue
        fi
        echo -e "\nTranslating $out ..."
        uv run trtools translate $INPUT -f French -t Spanish \
          -o "$out" -m ${MODEL_ID[$model]} \
          --threshold 10 --keep 5 --no-think \
          --terms-json "$TERMS_JSON" --terms-tsv "$TERMS_TSV" || true
    done
done

# --- 評価（モデル × 翻訳run × 評価run = 18 ファイル） ---
for model in "${MODELS[@]}"; do
    for trrun in 1 2 3; do
        out="tr/$model-$trrun.txt"
        if [ ! -f "$out" ]; then
            echo "Skipping $model-$trrun evaluation (translation not available)"
            continue
        fi
        for evrun in 1 2 3; do
            eval_out="evals/$model-$trrun-eval-$evrun.json"
            if [ -f "$eval_out" ]; then
                echo "Skipping $eval_out (already exists)"
            else
                echo -e "\nEvaluating $out (eval run $evrun)..."
                uv run trtools eval $EVAL_OPT --translation "$out" -o "$eval_out"
            fi
        done
    done
done

# --- 集約（翻訳 run 単位で集約） ---
: > SCORES.txt
for model in "${MODELS[@]}"; do
    for trrun in 1 2 3; do
        jsons=(evals/$model-$trrun-eval-*.json)
        if [ -e "${jsons[0]}" ]; then
            echo -e "\n=== $model (translation run $trrun) ===" | tee -a SCORES.txt
            uv run trtools agg "${jsons[@]}" | tee -a SCORES.txt
        fi
    done
done
