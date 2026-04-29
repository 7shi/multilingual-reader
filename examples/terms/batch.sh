#!/bin/bash
set -e
MODEL="ollama:gemma4:31b"
#MODEL="google:gemma-4-31b-it"
#MODEL="openrouter:google/gemma-4-31b-it:free"
KEEP=5
EXTRA_LANGS=$(sed -n 's/^EXTRA_LANGS\s*=\s*//p' common.mk | sed 's/\S\+/-t &/g')

for topic in finetuning transformer onde momentum; do
    # fr → en, es（直接翻訳）
    fr_file="../$topic-fr.txt"
    [ -f "$fr_file" ] || continue
    echo -e "\n[Extract] $topic (French)..."
    uv run trtools term extract "$fr_file" \
        -f fr -m "$MODEL" --keep $KEEP --no-think \
        -o "$topic-fr.json"
    echo -e "\n[Translate] $topic (French -> English, Spanish)..."
    uv run trtools term translate "$topic-fr.json" \
        -t en -t es \
        -m "$MODEL" --no-think \
        -c common.tsv -o "$topic-fr.tsv"

    # en → de, ja, zh, (EXTRA_LANGS は onde のみ)（英語からの重訳）
    en_file="../$topic-en.txt"
    [ -f "$en_file" ] || continue
    echo -e "\n[Extract] $topic (English)..."
    uv run trtools term extract "$en_file" \
        -f English -m "$MODEL" --keep $KEEP --no-think \
        -o "$topic-en.json"
    en_langs="-t de -t ja -t zh"
    [ "$topic" = "onde" ] && en_langs="$en_langs $EXTRA_LANGS"
    echo -e "\n[Translate] $topic (English -> de/ja/zh...)..."
    uv run trtools term translate "$topic-en.json" \
        $en_langs -m "$MODEL" --no-think \
        -c common.tsv -o "$topic-en.tsv"
done
