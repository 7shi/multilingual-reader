#!/bin/bash
EVALUATOR="ollama:qwen3.6"

declare -A LANG_NAME=(
    [en]="English"  [fr]="French"   [es]="Spanish"
    [de]="German"   [ja]="Japanese" [zh]="Chinese"
    [eo]="Esperanto" [hi]="Hindi"
)

declare -A TARGETS=(
    [finetuning]="en es de ja zh"
    [transformer]="en es de ja zh"
    [onde]="en es de ja zh eo hi"
    [momentum]="en es de ja zh"
)

for topic in finetuning transformer onde momentum; do
    src_file="../$topic-fr.txt"
    for tgt_lang in ${TARGETS[$topic]}; do
        tgt_file="../$topic-$tgt_lang.txt"
        [ -f "$tgt_file" ] || continue
        for run in {1..3}; do
            eval_out="$topic-$tgt_lang-eval-$run.json"
            if [ -f "$eval_out" ]; then
                echo "Skipping $eval_out (already exists)"
                continue
            fi
            echo -e "\nEvaluating $tgt_file (run $run)..."
            uv run tr-eval \
                --original "$src_file" --translation "$tgt_file" \
                -f French -t "${LANG_NAME[$tgt_lang]}" \
                -m "$EVALUATOR" -w 3 \
                -o "$eval_out"
        done
    done
done

# --- 集約 ---
jsons=(*.json)
if [ -e "${jsons[0]}" ]; then
    echo -e "\nAggregating ..."
    uv run tr-agg "${jsons[@]}" | tee SCORES.txt

    echo -e "\n言語別平均値（中央値の平均）:"
    python3 -c "
import re
from collections import defaultdict

scores = defaultdict(list)
with open('SCORES.txt') as f:
    for line in f:
        m = re.match(r'\w+-(\w+)-eval: (\d+)/100点', line)
        if m:
            lang, score = m.group(1), int(m.group(2))
            scores[lang].append(score)

lang_names = {'en':'English','de':'German','es':'Spanish','ja':'Japanese',
              'zh':'Chinese','eo':'Esperanto','hi':'Hindi'}
for lang, vals in sorted(scores.items(), key=lambda x: -sum(x[1])/len(x[1])):
    avg = sum(vals) / len(vals)
    name = lang_names.get(lang, lang)
    print(f'  {name}: {avg:.2f} ({len(vals)}トピック)')
"
else
    echo "No eval files found, skipping aggregation"
fi
