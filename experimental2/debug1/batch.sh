#!/bin/bash
set -e

INPUT="../../examples/finetuning-fr.txt"
EVALUATOR="ollama:qwen3.6"
EVAL_OPT="--original $INPUT -f French -t Spanish -m $EVALUATOR -w 3"

MODELS=(gemma3-27b gpt-oss-120b gemma4-31b-nt gemma4-31b qwen3.6-35b-nt qwen3.6-35b)
declare -A MODEL_ID=(
    [gemma3-27b]="ollama:gemma3:27b"
    [gpt-oss-120b]="ollama:gpt-oss:120b"
    [gemma4-31b-nt]="ollama:gemma4:31b --no-think"
    [gemma4-31b]="ollama:gemma4:31b"
    [qwen3.6-35b-nt]="ollama:qwen3.6 --no-think"
    [qwen3.6-35b]="ollama:qwen3.6"
)

VARIANTS=(none none-schema glossary glossary-schema)
declare -A VARIANT_OPTS=(
    [none]=""
    [none-schema]="--schema"
    [glossary]="--summary glossary"
    [glossary-schema]="--summary glossary --schema"
)

# --- 翻訳（モデルごとにまとめて実行）---
for model in "${MODELS[@]}"; do
    mkdir -p "$model"
    for variant in "${VARIANTS[@]}"; do
        out="$model/$variant.txt"
        if [ -f "$out" ]; then
            echo "Skipping $out (already exists)"
        else
            echo -e "\nTranslating $out ..."
            uv run ../translate.py $INPUT -f French -t Spanish \
              -o "$out" -m ${MODEL_ID[$model]} ${VARIANT_OPTS[$variant]} || true
        fi
    done
done

# --- 評価（評価者モデルをまとめて実行）---
for model in "${MODELS[@]}"; do
    for variant in "${VARIANTS[@]}"; do
        out="$model/$variant.txt"
        if [ ! -f "$out" ]; then
            echo "Skipping $model/$variant evaluation (translation not available)"
            continue
        fi
        for run in {1..3}; do
            eval_out="$model/$variant-eval-$run.json"
            if [ -f "$eval_out" ]; then
                echo "Skipping $eval_out (already exists)"
            else
                echo -e "\nEvaluating $out (run $run)..."
                uv run tr-eval $EVAL_OPT --translation "$out" -o "$eval_out"
            fi
        done
    done
done

# --- 集約 ---
tmpdir=$(mktemp -d)
for model in "${MODELS[@]}"; do
    for f in "$model"/*-eval-*.json; do
        [ -f "$f" ] || continue
        ln -sf "$(pwd)/$f" "$tmpdir/${f//\//-}"
    done
done
jsons=("$tmpdir"/*.json)
if [ -e "${jsons[0]}" ]; then
    echo -e "\nAggregating all models ..."
    uv run tr-agg "${jsons[@]}" | tee SCORES.txt
else
    echo "No eval files found, skipping aggregation"
fi
rm -rf "$tmpdir"
