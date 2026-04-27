#!/bin/bash
set -e
EVALUATOR="ollama:qwen3.6"

declare -A LANG_NAME=(
    [en]="English"  [fr]="French"   [es]="Spanish"
    [de]="German"   [ja]="Japanese" [zh]="Chinese"
    [eo]="Esperanto" [hi]="Hindi"
)

# 英語から重訳する言語
declare -A EN_TARGETS=(
    [finetuning]="de ja zh"
    [transformer]="de ja zh"
    [onde]="de ja zh eo hi"
    [momentum]="de ja zh"
)

for topic in finetuning transformer onde momentum; do
    # FR → EN, ES の評価（フランス語が原文）
    fr_file="../$topic-fr.txt"
    [ -f "$fr_file" ] || continue
    for tgt_lang in en es; do
        tgt_file="../$topic-$tgt_lang.txt"
        [ -f "$tgt_file" ] || continue
        for run in {1..3}; do
            eval_out="$topic-fr-$tgt_lang-$run.json"
            if [ -f "$eval_out" ]; then
                echo "Skipping $eval_out (already exists)"
                continue
            fi
            echo -e "\nEvaluating $tgt_file (run $run)..."
            uv run trtools eval \
                --original "$fr_file" --translation "$tgt_file" \
                -f French -t "${LANG_NAME[$tgt_lang]}" \
                -m "$EVALUATOR" -w 3 \
                -o "$eval_out"
        done
    done

    # EN → DE, JA, ZH, (EO, HI は onde のみ) の評価（英語が原文）
    en_file="../$topic-en.txt"
    [ -f "$en_file" ] || continue
    for tgt_lang in ${EN_TARGETS[$topic]}; do
        tgt_file="../$topic-$tgt_lang.txt"
        [ -f "$tgt_file" ] || continue
        for run in {1..3}; do
            eval_out="$topic-en-$tgt_lang-$run.json"
            if [ -f "$eval_out" ]; then
                echo "Skipping $eval_out (already exists)"
                continue
            fi
            echo -e "\nEvaluating $tgt_file (run $run)..."
            uv run trtools eval \
                --original "$en_file" --translation "$tgt_file" \
                -f English -t "${LANG_NAME[$tgt_lang]}" \
                -m "$EVALUATOR" -w 3 \
                -o "$eval_out"
        done
    done
done

# --- 集約 ---
jsons=(*.json)
if [ -e "${jsons[0]}" ]; then
    echo -e "\nAggregating ..."
    uv run trtools agg "${jsons[@]}" | tee SCORES.txt

    echo -e "\n言語別平均値（中央値の平均）:"
    python3 -c "
import re
from collections import defaultdict

scores = defaultdict(list)
with open('SCORES.txt') as f:
    for line in f:
        m = re.match(r'\w+-\w+-(\w+): (\d+)/100点', line)
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
