#!/bin/bash
set -e
MODEL="ollama:gemma4:31b"
#MODEL="google:gemma-4-31b-it"
#MODEL="openrouter:google/gemma-4-31b-it:free"
KEEP=5
ADDITIONAL_LANGUAGES="-t Esperanto -t Hindi -t Telugu -t Kannada -t Turkish -t Estonian -t Serbian"

for topic in finetuning transformer onde momentum; do
    # FR → EN, ES（直接翻訳）
    fr_file="../$topic-fr.txt"
    [ -f "$fr_file" ] || continue
    echo -e "\n[Extract] $topic (French)..."
    uv run trtools term extract "$fr_file" \
        -f French -m "$MODEL" --keep $KEEP --no-think \
        -o "$topic-fr.json"
    echo -e "\n[Translate] $topic (French -> English, Spanish)..."
    uv run trtools term translate "$topic-fr.json" \
        -t English -t Spanish \
        -m "$MODEL" --no-think \
        -c common.tsv -o "$topic-fr.tsv"

    # EN → DE, JA, ZH, (EO, HI は onde のみ)（英語からの重訳）
    en_file="../$topic-en.txt"
    [ -f "$en_file" ] || continue
    echo -e "\n[Extract] $topic (English)..."
    uv run trtools term extract "$en_file" \
        -f English -m "$MODEL" --keep $KEEP --no-think \
        -o "$topic-en.json"
    en_langs="-t German -t Japanese -t Chinese"
    [ "$topic" = "onde" ] && en_langs="$en_langs $ADDITIONAL_LANGUAGES"
    echo -e "\n[Translate] $topic (English -> DE/JA/ZH...)..."
    uv run trtools term translate "$topic-en.json" \
        $en_langs -m "$MODEL" --no-think \
        -c common.tsv -o "$topic-en.tsv"
done
