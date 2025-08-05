# 指定ファイルをローカルLLMで翻訳（構造化出力なし、通常のクエリによる翻訳）

import argparse
parser = argparse.ArgumentParser(description="対話テキストを1:1で翻訳（構造化出力なし）")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳に使用するモデル")
parser.add_argument("--history", type=int, default=5, help="コンテキストに含める過去の対話履歴数 (デフォルト: 5)")
parser.add_argument("--translated-context", action="store_true", help="履歴コンテキストに翻訳文のみを提供（対訳形式ではなく）")
parser.add_argument("--no-think", action="store_true", help="reasoning処理を無効化（Qwen3モデル用）")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import re
from llm7shi.compat import generate_with_schema
from tqdm import tqdm

def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def generate_with_retry(system_prompt, prompts, model):
    """リトライ機能付きのLLM生成関数"""
    for j in range(5):
        if j:
            print(f"Retry: {j}")
        try:
            result = generate_with_schema(
                prompts,
                system_prompt=system_prompt,
                model=model,
                max_length=4096,
                show_params=False,
                include_thoughts=(not args.no_think),
            )
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
    
    # システムプロンプトの作成
    system_prompt = "Output only the translation without any additional explanation or formatting."
    
    # プロンプト作成（話者情報を含める）
    prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"
    
    # 翻訳実行
    translated_text = generate_with_retry(system_prompt, [context, prompt], args.model)
    translated_text = normalize(translated_text)
    
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
