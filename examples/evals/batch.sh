#!/bin/bash
# Evaluates the reference translations in examples/ with TypeSafe's Jev (pinned in
# trtools/jev.py), one run per language. The *.json files and SCORES.txt are the previous
# evaluator's record (ollama:qwen3.6, three runs each) and are no longer written.
set -e

TOPICS="finetuning momentum onde transformer"

# Source language -> targets translated from it
declare -A SRC_NAME=([en]="English" [fr]="French")
declare -A TARGETS=([fr]="en es" [en]="de ja zh")

# One file per topic and source, since a record names only its target language.
# trtools jev skips the languages a file already holds.
for topic in $TOPICS; do
    for src in en fr; do
        uv run trtools jev "../$topic-$src.txt" -f "${SRC_NAME[$src]}" \
            --tr-dir .. --langs ${TARGETS[$src]} -o "jev-$topic-$src.jsonl"
    done
done

# --- Aggregation ---
echo -e "\nAggregating ..."
for topic in $TOPICS; do
    for src in en fr; do
        uv run trtools agg --jev --prefix "$topic-$src" "jev-$topic-$src.jsonl"
    done
done > SCORES-jev.txt.tmp
mv SCORES-jev.txt.tmp SCORES-jev.txt
cat SCORES-jev.txt

echo -e "\nPer-language average (mean over topics):"
python3 -c "
import re
from collections import defaultdict

scores = defaultdict(list)
with open('SCORES-jev.txt') as f:
    for line in f:
        m = re.match(r'\w+-\w+-(\w+): (\d+(?:\.\d+)?)', line)
        if m:
            lang, score = m.group(1), float(m.group(2))
            scores[lang].append(score)

lang_names = {'en':'English','de':'German','es':'Spanish','ja':'Japanese','zh':'Chinese'}
for lang, vals in sorted(scores.items(), key=lambda x: -sum(x[1])/len(x[1])):
    avg = sum(vals) / len(vals)
    name = lang_names.get(lang, lang)
    print(f'  {name}: {avg:.2f} ({len(vals)} topics)')
"
