# 指定ファイルをローカルLLMで英語と日本語に翻訳（1行ずつ処理、文脈付き）

import argparse
parser = argparse.ArgumentParser(description="対話テキストを1:1で翻訳")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳に使用するモデル")
parser.add_argument("-r", "--reasoning-level", type=int, default=2, choices=[0, 1, 2, 3, 4], help="推論レベル: 0=推論なし, 1=標準推論, 2=2段階翻訳, 3=3段階翻訳, 4=分割3段階翻訳")
parser.add_argument("--history", type=int, default=5, help="コンテキストに含める過去の対話履歴数 (デフォルト: 5)")
parser.add_argument("--translated-context", action="store_true", help="履歴コンテキストに翻訳文のみを提供（対訳形式ではなく）")
parser.add_argument("--no-think", action="store_true", help="thinking処理を無効化（Qwen3モデル用）")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm

# Field templates
translation_field = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")
translation_result_field = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
reasoning_field = Field(description=f"Detailed translation reasoning process:\n1. Syntactic analysis of the original {args.from_lang} text (subject, predicate, object, modifiers, etc.)\n2. Contextual interpretation of speaker's intent and emotional tone\n3. Evaluation of translation options for key vocabulary and idiomatic expressions\n4. Consideration of cultural nuances and appropriate register/politeness level\n5. Justification for final translation choices and overall approach")
draft_translation_field = Field(description=f"First draft translation from {args.from_lang} to {args.to_lang}")
quality_assessment_field = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) There are no omissions of information from the original text or additions of information not present in the original, 4) The translation is natural and appropriate. List specific issues found.")
improvement_suggestions_field = Field(description=f"Provide specific suggestions for improving the translation quality")
improved_translation_field = Field(description=f"Based on the quality assessment and improvement suggestions above, provide an improved {args.from_lang} to {args.to_lang} translation that addresses all identified issues")

if args.reasoning_level == 0:
    class Translation(BaseModel):
        translation: str = translation_field
elif args.reasoning_level == 1:
    class Translation(BaseModel):
        reasoning: str = reasoning_field
        translation: str = translation_result_field
elif args.reasoning_level == 2:
    class Translation(BaseModel):
        draft_translation: str = draft_translation_field
        quality_assessment: str = quality_assessment_field
        improvement_suggestions: str = improvement_suggestions_field
        improved_translation: str = improved_translation_field
elif args.reasoning_level == 3:
    class Translation(BaseModel):
        reasoning: str = reasoning_field
        draft_translation: str = draft_translation_field
        quality_assessment: str = quality_assessment_field
        improvement_suggestions: str = improvement_suggestions_field
        improved_translation: str = improved_translation_field
elif args.reasoning_level == 4:
    # 第1段階：推論と初回翻訳
    class FirstStageTranslation(BaseModel):
        reasoning: str = reasoning_field
        draft_translation: str = draft_translation_field
    
    # 第2段階：品質評価と改善翻訳
    class SecondStageTranslation(BaseModel):
        quality_assessment: str = quality_assessment_field
        improvement_suggestions: str = improvement_suggestions_field
        improved_translation: str = improved_translation_field
    
    Translation = FirstStageTranslation  # デフォルトは第1段階

json_descriptions = create_json_descriptions_prompt(Translation)

def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def generate_with_retry(prompts, schema, model, stage_name=""):
    """リトライ機能付きのLLM生成関数"""
    descriptions = create_json_descriptions_prompt(schema)
    for j in range(5):
        if j:
            print(f"Retry{' (' + stage_name + ')' if stage_name else ''}:", j)
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
    
    # 文脈作成（直前のhistory個の翻訳結果）
    context_lines = []
    if context_history and args.history > 0:
        context_lines.append("Previous conversation context:")
        context_lines.append("")
        for ctx in context_history[-args.history:]:
            if args.translated_context:
                # 翻訳文のみを提供
                context_lines.append(f"{ctx['speaker']}: {ctx['translation']}")
            else:
                # 対訳形式で提供（デフォルト）
                context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
                context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
                context_lines.append("")
    
    context = "\n".join(context_lines) if context_lines else "(No context)"
    
    # プロンプト作成（話者情報を含める）
    prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"
    
    # 実際の翻訳実行
    if args.reasoning_level == 4:
        # レベル4：2段階に分割した処理
        # 第1段階：推論と初回翻訳
        first_parsed = generate_with_retry([context, prompt], FirstStageTranslation, args.model, "Stage 1")
        
        # 第2段階：品質評価と改善翻訳
        second_stage_prompt = f"Review and improve this {args.from_lang} to {args.to_lang} translation:\n\nOriginal: {text}\nDraft translation: {first_parsed['draft_translation']}"
        second_parsed = generate_with_retry([context, second_stage_prompt], SecondStageTranslation, args.model, "Stage 2")
        
        # 結果を統合
        parsed = {
            'reasoning': first_parsed['reasoning'],
            'draft_translation': first_parsed['draft_translation'],
            'quality_assessment': second_parsed['quality_assessment'],
            'improvement_suggestions': second_parsed['improvement_suggestions'],
            'improved_translation': second_parsed['improved_translation']
        }
    else:
        # 従来の1回呼び出し処理
        parsed = generate_with_retry([context, prompt], Translation, args.model)
    
    # 文脈履歴に追加
    if args.reasoning_level in [2, 3, 4]:
        translated_text = normalize(parsed['improved_translation'])
    else:
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
