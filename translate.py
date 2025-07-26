# 指定ファイルをローカルLLMで英語と日本語に翻訳（1行ずつ処理、文脈付き）

import argparse

DEFAULT_MODEL = "ollama:gemma3n:e4b"

parser = argparse.ArgumentParser(description="対話テキストを1:1で翻訳")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"翻訳に使用するモデル（デフォルト: {DEFAULT_MODEL}）")
parser.add_argument("--test", action="store_true", help="dry-runモード（実際の翻訳は行わない）")
args = parser.parse_args()

import json
import re
from pathlib import Path
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt

class Translation(BaseModel):
    reasoning: str = Field(description="reasoning before translation")
    translation: str = Field(description="translation result")

def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

# fr-onde.txtを読み込み
with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

output_file = args.output_file

json_descriptions = create_json_descriptions_prompt(Translation)

# 翻訳結果を保存するリスト
translated_lines = []
# 文脈保持用
context_history = []

# 1行ずつ翻訳
for i, line in enumerate(lines):
    line = line.strip()
    if line and ":" in line:
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
        
        if args.test:
            # dry-runモード：実際の翻訳は行わず、ダミーデータを使用
            print(f"[TEST] Context:\n{context}")
            print(f"[TEST] Prompt:\n{prompt}")

            translated_text = f"[TEST {args.to_lang.upper()}] {text}"
        else:
            # 実際の翻訳実行
            result = generate_with_schema(
                [context, prompt, json_descriptions],
                schema=Translation,
                model=args.model,
            )
            
            if result and result.text:
                try:
                    parsed = json.loads(result.text.strip())
                    translated_text = normalize(parsed['translation'])
                except json.JSONDecodeError:
                    # JSON解析失敗時は原文を保持
                    translated_text = text
            else:
                # 翻訳失敗時は原文を保持
                translated_text = text

        translated_lines.append(f"{speaker}: {translated_text}")
        
        # 文脈履歴に追加
        context_history.append({
            'speaker': speaker,
            'original': text,
            'translation': translated_text
        })
        
        if not args.test:
            print(f"翻訳完了: {i+1}/{len([l for l in lines if l.strip() and ':' in l])} - {speaker}")
    else:
        # 空行はそのまま保持
        translated_lines.append("")

# 結果を保存
with open(output_file, "w", encoding="utf-8") as f:
    for line in translated_lines:
        f.write(line + "\n")

if args.test:
    print(f"[TEST] 処理完了: {len([l for l in lines if l.strip() and ':' in l])}行をテスト処理")
    print("[TEST] 実際のファイルは生成されませんでした")
else:
    print(f"翻訳完了: {args.from_lang} → {args.to_lang} ({output_file})")
