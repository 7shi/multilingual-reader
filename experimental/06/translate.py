import argparse
import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm

parser = argparse.ArgumentParser(description="2段階翻訳スクリプト（行単位・下訳保存対応）")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="最終出力ファイル名")
parser.add_argument("-d", "--draft", dest="draft_file", required=True, help="下訳出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳に使用するモデル")
parser.add_argument("--history", type=int, default=5, help="コンテキストに含める過去の対話履歴数 (デフォルト: 5)")
parser.add_argument("--no-think", action="store_true", help="thinking処理を無効化（Qwen3モデル用）")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

draft_translation_field = Field(description=f"First draft translation from {args.from_lang} to {args.to_lang}")
quality_assessment_field = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) There are no omissions of information from the original text or additions of information not present in the original, 4) The translation is natural and appropriate. List specific issues found.")
improvement_suggestions_field = Field(description=f"Provide specific suggestions for improving the translation quality")
improved_translation_field = Field(description=f"Based on the quality assessment and improvement suggestions above, provide an improved {args.from_lang} to {args.to_lang} translation that addresses all identified issues")

class Translation(BaseModel):
    draft_translation: str = draft_translation_field
    quality_assessment: str = quality_assessment_field
    improvement_suggestions: str = improvement_suggestions_field
    improved_translation: str = improved_translation_field

def normalize(text):
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def generate_with_retry(prompts, schema, model):
    descriptions = create_json_descriptions_prompt(schema)
    for j in range(5):
        if j:
            print(f"Retry:", j)
        try:
            result = generate_with_schema(
                prompts + [descriptions],
                schema=schema,
                model=model,
                max_length=8192*2,
                show_params=False,
                include_thoughts=(not args.no_think),
            )
            return json.loads(result.text.strip())
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise

context_history = []

for i, line in enumerate(tqdm(lines, desc="翻訳処理")):
    line = line.strip()
    
    if ":" not in line:
        continue
    
    print()
    print(line)
    
    speaker, text = line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()
    
    context_lines = []
    if context_history and args.history > 0:
        context_lines.append("Previous conversation context:")
        context_lines.append("")
        for ctx in context_history[-args.history:]:
            context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
            context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
            context_lines.append("")
    
    context = "\n".join(context_lines) if context_lines else "(No context)"
    
    prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"
    
    parsed = generate_with_retry([context, prompt], Translation, args.model)
    
    draft_text = normalize(parsed['draft_translation'])
    translated_text = normalize(parsed['improved_translation'])
    
    context_history.append({
        'speaker': speaker,
        'original': text,
        'draft': draft_text,
        'translation': translated_text
    })

with open(args.output_file, "w", encoding="utf-8") as f:
    for ctx in context_history:
        f.write(f"{ctx['speaker']}: {ctx['translation']}\n")

with open(args.draft_file, "w", encoding="utf-8") as f:
    for ctx in context_history:
        f.write(f"{ctx['speaker']}: {ctx['draft']}\n")

print(f"翻訳完了: {args.from_lang} → {args.to_lang}")
print(f"下訳出力: {args.draft_file}")
print(f"最終出力: {args.output_file}")