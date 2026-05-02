# 指定ファイルをローカルLLMで翻訳（自由記述式推論テスト）

import argparse
parser = argparse.ArgumentParser(description="対話テキストを1:1で翻訳（自由記述式推論テスト）")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳に使用するモデル")
parser.add_argument("--history", type=int, default=5, help="コンテキストに含める過去の対話履歴数 (デフォルト: 5)")
parser.add_argument("--no-think", action="store_true", help="reasoning処理を無効化（Qwen3モデル用）")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import re
from llm7shi.compat import generate_with_schema
from llm7shi import bold
from tqdm import tqdm

def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()


def generate_with_retry(system_prompt, prompts, model):
    """リトライ機能付きのLLM生成関数"""
    multiplier = 2  # 倍数の初期値
    for j in range(5):
        if j:
            print(f"Retry: {j}")
        try:
            result = generate_with_schema(
                prompts,
                system_prompt=system_prompt,
                model=model,
                max_length=8192*multiplier,
                show_params=False,
                include_thoughts=(not args.no_think),
            )
            if result.max_length is not None:
                multiplier += 1
            elif not result.repetition:
                return result.text.strip()
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise

context_history = []  # 文脈保持用

# 翻訳対象行を事前に抽出
translation_lines = [l for line in lines if (l := line.strip()) and ":" in l]

# 1行ずつ翻訳
for line in tqdm(translation_lines, desc="翻訳処理"):
    print("\n\n" + bold(f"[{args.from_lang}]"), line + "\n")
    
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
            # 対訳形式で提供
            context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
            context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
            context_lines.append("")
    
    context = "\n".join(context_lines) if context_lines else "(No context)"
    
    # システムプロンプトとユーザープロンプトの作成（常に推論モード）
    system_prompt = f"""You are a professional translator. Please translate {args.from_lang} to {args.to_lang}.

First, provide detailed translation reasoning covering:
1. Syntactic analysis of the original {args.from_lang} text (subject, predicate, object, modifiers, etc.)
2. Contextual interpretation of speaker's intent and emotional tone
3. Evaluation of {args.to_lang} translation options for key vocabulary and idiomatic expressions
4. Consideration of cultural nuances and appropriate register/politeness level
5. Justification for final {args.to_lang} translation choices and overall approach

Then provide your final translation on the last line."""
    prompt = f"Analyze and translate the following {args.from_lang} text into {args.to_lang}:\n{line}"
    
    # 翻訳実行
    output_text = generate_with_retry(system_prompt, [context, prompt], args.model)
    
    # 翻訳結果を抽出（常に推論モードなので抽出処理を実行）
    print("\n" + bold(f"[{args.to_lang}]"), end=" ")
    extraction_system_prompt = "Output only the requested translation text."
    extraction_prompt = f"Extract only the final {args.to_lang} translation from the following text. Look for the actual translation result, not the reasoning or analysis sections. Output only the {args.to_lang} translation without any explanations, alternatives, or formatting in any language. If the entire translation is wrapped in quotation marks, remove only the outer quotation marks:\n\n{output_text}"
    
    # 抽出実行
    translated_text = generate_with_retry(extraction_system_prompt, [extraction_prompt], args.model)
    translated_text = normalize(translated_text).removeprefix(speaker + ":").strip()
    print()
    
    # 文脈履歴に追加
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
