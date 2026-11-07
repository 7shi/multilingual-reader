#!/bin/bash
# Build mislabel/tr/: existing gpt-6-sol translations (and the English original)
# copied under another language's code, so the evaluator is told the wrong target.
set -e
cd "$(dirname "$0")"
ROOT=../..
T=$ROOT/examples/tr/onde/gpt-6-sol/tr
mkdir -p mislabel/tr
cp $ROOT/examples/onde-en.txt mislabel/tr/onde-fr.txt  # English labelled French
cp $T/onde-fr.txt mislabel/tr/onde-de.txt              # French labelled German
cp $T/onde-es.txt mislabel/tr/onde-pt.txt              # Spanish labelled Portuguese
cp $T/onde-ja.txt mislabel/tr/onde-zh.txt              # Japanese labelled Chinese
cp $T/onde-hr.txt mislabel/tr/onde-sr.txt              # Croatian labelled Serbian
