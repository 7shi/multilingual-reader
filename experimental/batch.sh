set -e

EVALUATOR="google:gemini-2.5-flash"
EVAL_DIR="gemini-2.5-flash"
RETRY_WAIT=90

EVAL_CMD="uv run evaluate_translation.py --original ../examples/finetuning-fr.txt -f French -t Spanish -m $EVALUATOR -w $RETRY_WAIT"

process_translation() {
    local command=$1
    local output=$2
    local model=$3
    
    if [ -f "$output" ]; then
        echo "Skipping translation $output (already exists)"
    else
        echo -e "\nTranslating $output ..."
        time $command -o $output -m $model
    fi
    
    # 評価を3回実行
    for eval_run in {1..3}; do
        local eval_output="$EVAL_DIR/${output%.txt}-${eval_run}.json"
        if [ -f "$eval_output" ]; then
            : #echo "Skipping evaluation $eval_output (already exists)"
        else
            if [ -f "$output" ]; then
                echo -e "\nEvaluating $output (run $eval_run)..."
                $EVAL_CMD --translation $output -o $eval_output
            fi
        fi
    done
}

CMD="uv run translate.py -f French -t Spanish ../examples/finetuning-fr.txt"
CMD4="uv run translate4.py -f French -t Spanish ../examples/finetuning-fr.txt"
CMD5="uv run translate5.py -f French -t Spanish ../examples/finetuning-fr.txt"
CMD6="uv run translate6.py -f French -t Spanish ../examples/finetuning-fr.txt"

mkdir -p tr-cmp tr-0 tr-1 tr-2 tr4 tr5 tr6 $EVAL_DIR/{tr-cmp,tr-0,tr-1,tr-2,tr4,tr5,tr6}
#process_translation "$CMD -r 0" tr-cmp/gpt-oss-20b-0.txt ollama:hf.co/unsloth/gpt-oss-20b-GGUF

for m in gemma3:4b gemma3n:e4b gemma2:9b gemma3:12b gemma3:27b phi4 command-r7b command-r:35b aya-expanse:8b aya-expanse:32b qwen3:4b qwen3:14b qwen3:30b qwen3:32b llama3.3 llama4:scout gpt-oss:20b gpt-oss:120b mistral-small3.2 mixtral:8x7b mixtral:8x22b ministral-3:3b ministral-3:8b ministral-3:14b; do
    echo "======== $m ========"
    m2=${m/:/-}
    if [[ "$m" == "gemma2:9b" ]]; then
        model_name="ollama:${m}-instruct-q4_K_M"
    elif [[ "$m" == "command-r:35b" ]]; then
        model_name="ollama:command-r:35b-08-2024-q4_K_M"
    else
        model_name="ollama:$m"
    fi
    for i in {0..4}; do
        process_translation "$CMD -r $i" tr-cmp/$m2-$i.txt $model_name
    done
    process_translation "$CMD -r 0 --history 05" tr-0/$m2-0-05.txt $model_name
    process_translation "$CMD -r 0 --history 10" tr-0/$m2-0-10.txt $model_name
    process_translation "$CMD -r 0 --history 20" tr-0/$m2-0-20-a.txt $model_name
    process_translation "$CMD -r 0 --history 20" tr-0/$m2-0-20-b.txt $model_name
    for h in 05 10 20; do
        process_translation "$CMD -r 1 --history $h" tr-1/$m2-1-$h.txt $model_name
        process_translation "$CMD -r 2 --history $h" tr-2/$m2-2-$h.txt $model_name
        process_translation "$CMD4 --history $h" tr4/$m2-tr4-$h.txt $model_name
        process_translation "$CMD5 --history $h" tr5/$m2-tr5-$h.txt $model_name
        process_translation "$CMD6 --history $h" tr6/$m2-tr6-$h.txt $model_name
    done
done

echo "======== qwen3:4b ========"
for h in 05 10 15 20 25; do
    for i in 0 1 2; do
        process_translation "$CMD -r $i --history $h" tr-$i/qwen3-4b-$i-$h.txt ollama:qwen3:4b
        process_translation "$CMD -r $i --history $h --translated-context" tr-$i/qwen3-4b-$i-t-${h}.txt ollama:qwen3:4b
        process_translation "$CMD -r $i --no-think --history $h" tr-$i/qwen3-4b-$i-nt-$h.txt ollama:qwen3:4b
        process_translation "$CMD -r $i --no-think --history $h --translated-context" tr-$i/qwen3-4b-$i-nt-t-${h}.txt ollama:qwen3:4b
    done
done

for m in qwen3:4b qwen3:14b qwen3:30b qwen3:32b; do
    echo "======== $m (nt) ========"
    m2=${m/:/-}
    for i in {0..4}; do
        process_translation "$CMD -r $i --no-think" tr-cmp/$m2-$i-nt.txt ollama:$m
    done
    process_translation "$CMD -r 0 --history 05 --no-think" tr-0/$m2-0-nt-05.txt $model_name
    process_translation "$CMD -r 0 --history 10 --no-think" tr-0/$m2-0-nt-10.txt $model_name
    process_translation "$CMD -r 0 --history 20 --no-think" tr-0/$m2-0-nt-20-a.txt ollama:$m
    process_translation "$CMD -r 0 --history 20 --no-think" tr-0/$m2-0-nt-20-b.txt ollama:$m
    for h in 05 10 20; do
        process_translation "$CMD -r 1 --history $h --no-think" tr-1/$m2-1-nt-$h.txt $model_name
        process_translation "$CMD -r 2 --history $h --no-think" tr-2/$m2-2-nt-$h.txt $model_name
        process_translation "$CMD4 --history $h --no-think" tr4/$m2-tr4-nt-$h.txt ollama:$m
        process_translation "$CMD5 --history $h --no-think" tr5/$m2-tr5-nt-$h.txt ollama:$m
        process_translation "$CMD6 --history $h --no-think" tr6/$m2-tr6-nt-$h.txt ollama:$m
    done
done

(cd $EVAL_DIR && uv run ../aggregate_evaluations.py tr{-cmp,-0,-1,-2,4,5,6}/*.json) > $EVAL_DIR/SCORES.txt
uv run generate_scores_md.py $EVAL_DIR/SCORES.txt
uv run sync_scores.py $EVAL_DIR/SCORES.md
