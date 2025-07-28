# 指定ファイルをローカルLLMで英語と日本語に翻訳（1行ずつ処理、文脈付き）

DEFAULT_MODEL = "ollama:gemma3n:e4b"

import argparse
parser = argparse.ArgumentParser(description="対話テキストを1:1で翻訳")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"翻訳に使用するモデル（デフォルト: {DEFAULT_MODEL}）")
parser.add_argument("--no-reasoning", action="store_true", help="推論過程を出力しない")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm

if args.no_reasoning:
    class Translation(BaseModel):
        translation: str = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
else:
    class Translation(BaseModel):
        reasoning: str = Field(description=f"Carefully analyze the meaning and context of the original {args.from_lang} text. Consider cultural nuances, idiomatic expressions, and the speaker's intent. Evaluate different possible translation choices and explain your reasoning for selecting the most appropriate words and phrasing for the {args.to_lang} translation.")
        translation: str = Field(description=f"{args.from_lang} to {args.to_lang} translation result")

json_descriptions = create_json_descriptions_prompt(Translation)

def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

context_history = []  # 文脈保持用

# 翻訳対象行を事前にカウント
translation_lines = [line for line in lines if line.strip() and ":" in line.strip()]

# 1行ずつ翻訳
for i, line in enumerate(tqdm(lines, desc="翻訳処理")):
    line = line.strip()
    
    # 話者が分離できなければスキップ
    if ":" not in line:
        continue
    
    print()
    print(line)
    
    # 話者を分離
    speaker, text = line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()
    
    # 文脈作成（直前の5つの翻訳結果）
    context_lines = []
    if context_history:
        context_lines.append("Previous conversation context:")
        context_lines.append("")
        for ctx in context_history[-5:]:
            context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
            context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
            context_lines.append("")
    
    context = "\n".join(context_lines) if context_lines else "(No context)"
    
    # プロンプト作成（話者情報を含める）
    prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"
    
    # 実際の翻訳実行
    for j in range(5):
        if j:
            print("Retry:", j)
        try:
            result = generate_with_schema(
                [context, prompt, json_descriptions],
                schema=Translation,
                model=args.model,
                max_length=4096,
                show_params=False,
            )
            parsed = json.loads(result.text.strip())
            break
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise
    
    # 文脈履歴に追加
    translated_text = normalize(parsed['translation'])
    context_history.append({
        'speaker': speaker,
        'original': text,
        'translation': translated_text
    })
    

# 結果を保存
with open(args.output_file, "w", encoding="utf-8") as f:
    for ctx in context_history:
        f.write(f"{ctx['speaker']}: {ctx['translation']}\n")

print(f"翻訳完了: {args.from_lang} → {args.to_lang} ({args.output_file})")
