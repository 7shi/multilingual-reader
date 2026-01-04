# 翻訳評価スクリプト（SCORE.md基準）

import argparse
import json
import time
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt

# デフォルトの待機時間（秒）
DEFAULT_RETRY_WAIT_SECONDS = 3

parser = argparse.ArgumentParser(description="翻訳品質を5項目基準で評価")
parser.add_argument("--original", required=True, help="原文ファイル")
parser.add_argument("--translation", required=True, help="翻訳文ファイル")
parser.add_argument("-m", "--model", required=True, help="評価に使用するモデル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", help="評価結果をJSONで保存するファイル名")
parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                    help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
args = parser.parse_args()

# ファイルから内容を読み込み
with open(args.original, "r", encoding="utf-8") as f:
    original_text = f.read().rstrip()

with open(args.translation, "r", encoding="utf-8") as f:
    translated_text = f.read().rstrip()

class ReasoningAndScore(BaseModel):
    reasoning: str = Field(description="Detailed reasoning and consideration for scoring this evaluation criterion")
    score: int = Field(ge=0, le=20, description="Score out of 20 points")

# 評価項目の定義（SCORE.md基準）
class TranslationEvaluation(BaseModel):
    readability: ReasoningAndScore = Field(
        description="Readability and Comprehensibility (20 points): Evaluate whether target language readers can easily understand the content, whether complex concepts are explained clearly, and whether the sentence structure is logical and easy to follow"
    )
    
    fluency: ReasoningAndScore = Field(
        description="Fluency and Naturalness (20 points): Evaluate whether the translated text sounds natural and smooth to native speakers of the target language, whether there are unnatural expressions or awkward grammar, and whether vocabulary choices are appropriate and contemporary"
    )
    
    terminology: ReasoningAndScore = Field(
        description="Technical Terminology Appropriateness (20 points): Evaluate whether technical terms are appropriately handled according to the reader's understanding level, whether explanations or paraphrases are provided when necessary, and whether term selection is consistent"
    )
    
    contextual_adaptation: ReasoningAndScore = Field(
        description="Contextual Adaptation (20 points): Evaluate whether the original text's intent and purpose are effectively conveyed, whether expressions consider the target readers' cultural background, and whether expressions are improved or optimized as needed"
    )
    
    information_completeness: ReasoningAndScore = Field(
        description="Information Completeness (20 points): Evaluate whether important information from the original text is conveyed without omission, whether appropriate supplements are provided to aid reader understanding, and whether redundancy is eliminated while keeping the content concise and clear"
    )
    
    overall_comment: str = Field(
        description="Overall comprehensive evaluation comment about the translation quality as a whole"
    )

# 評価プロンプトの作成
evaluation_prompt = f"""Please evaluate this translation from {args.from_lang} to {args.to_lang}.

Score each evaluation criterion from 0-20 points and provide specific reasoning and comments."""

print("翻訳評価を実行中...")
print()

# プロンプト構成を修正
schema = TranslationEvaluation
prompts = [
    f"<original>\n{original_text}\n</original>",
    f"<translation>\n{translated_text}\n</translation>",
    evaluation_prompt,
    create_json_descriptions_prompt(schema)
]

# LLMによる評価実行（リトライ付き）
max_retries = 3
for attempt in range(max_retries):
    try:
        result = generate_with_schema(
            prompts,
            schema=schema,
            model=args.model,
            max_length=8192,
            show_params=False,
        )
        evaluation_result = json.loads(result.text)
        break  # 成功したらループを抜ける
    except json.JSONDecodeError as e:
        if attempt < max_retries - 1:
            print(f"JSONデコードエラー（試行{attempt + 1}/{max_retries}）: {e}")
            for i in range(args.retry_wait, -1, -1):
                print(f"\rリトライ待ち... {i}s ", end="", flush=True)
                time.sleep(1)
            print()
        else:
            print(f"JSONデコードに{max_retries}回失敗しました。")
            raise

# 結果表示
print("=== 翻訳評価結果 ===")
print(f"1. 読みやすさと理解しやすさ: {evaluation_result['readability']['score']:2d}/20点")
print(f"2. 流暢さと自然さ          : {evaluation_result['fluency']['score']:2d}/20点")
print(f"3. 専門用語の適切性        : {evaluation_result['terminology']['score']:2d}/20点")
print(f"4. 文脈適応性              : {evaluation_result['contextual_adaptation']['score']:2d}/20点")
print(f"5. 情報の完全性            : {evaluation_result['information_completeness']['score']:2d}/20点")

# 総合得点を計算
total_score = (evaluation_result['readability']['score'] + 
               evaluation_result['fluency']['score'] + 
               evaluation_result['terminology']['score'] + 
               evaluation_result['contextual_adaptation']['score'] + 
               evaluation_result['information_completeness']['score'])
print(f"総合得点: {total_score}/100点")

# JSON出力（オプション）
if args.output_file:
    output_data = {
        "original_file": args.original,
        "translation_file": args.translation,
        #"original_text": original_text,
        #"translated_text": translated_text,
        "source_language": args.from_lang,
        "target_language": args.to_lang,
        "model_used": args.model,
        "evaluation": evaluation_result,
        "total_score": total_score
    }
    
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n評価結果をJSONで保存しました: {args.output_file}")
