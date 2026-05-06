import argparse
import time
from tqdm import tqdm
from trtools.llm import LLMClient

parser = argparse.ArgumentParser(description="他者評価による翻訳推敲スクリプト")
parser.add_argument("--original", required=True, help="原文テキストファイル")
parser.add_argument("--translation", required=True, help="ベースライン翻訳テキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: Dutch）")
parser.add_argument("-o", "--output", required=True, help="推敲後出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="推敲に使用するモデル")
parser.add_argument("--history", type=int, default=10, help="コンテキスト履歴数")
parser.add_argument("--no-think", action="store_true", help="thinking処理を無効化")
args = parser.parse_args()

with open(args.original, "r", encoding="utf-8") as f:
    orig_lines = f.readlines()
with open(args.translation, "r", encoding="utf-8") as f:
    tr_lines = f.readlines()

if len(orig_lines) != len(tr_lines):
    print("Warning: The number of lines in original and translation files do not match.")

client = LLMClient(model=args.model, think=(not args.no_think))

context_history = []
results = []

for i, (orig_line, tr_line) in enumerate(zip(orig_lines, tr_lines)):
    orig_line = orig_line.strip()
    tr_line = tr_line.strip()
    
    if not orig_line or ":" not in orig_line:
        results.append(tr_line)
        continue
    
    print(f"\n[{i+1}/{len(orig_lines)}]")
    print(f"Original: {orig_line}")
    print(f"Base: {tr_line}")
    
    speaker, text = orig_line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()
    
    if ":" in tr_line:
        tr_speaker, tr_text = tr_line.split(":", 1)
        tr_speaker = tr_speaker.strip()
        tr_text = tr_text.strip()
    else:
        tr_speaker = speaker
        tr_text = tr_line

    chat_history = []
    
    system_msg = {
        "role": "system",
        "content": f"You are an expert {args.to_lang} reviewer. Your task is to review and refine a {args.from_lang} to {args.to_lang} translation."
    }
    chat_history.append(system_msg)
    
    if context_history and args.history > 0:
        context_prompt = "Previous context:\n\n"
        for ctx in context_history[-args.history:]:
            context_prompt += f"Original: {ctx['original']}\nTranslation: {ctx['translation']}\n\n"
        chat_history.append({"role": "user", "content": context_prompt.strip()})
        chat_history.append({"role": "assistant", "content": "Understood. I will use this context for consistency."})

    # Prompt 1: Analysis
    prompt1 = f"Original {args.from_lang} text:\n{text}\n\nBase {args.to_lang} translation:\n{tr_text}\n\nPlease analyze this translation. Point out any literal translations, interference from other languages, unnatural phrasing, or grammar issues. If it's perfect, just say 'No issues'."
    chat_history.append({"role": "user", "content": prompt1})
    
    print("\nAnalysis:")
    # リアルタイムにストリーミング出力されるため、戻り値のprintは不要
    analysis = client.call(chat_history)
    print()
    chat_history.append({"role": "assistant", "content": analysis})

    if "No issues" in analysis or "no issues" in analysis.lower():
        improved_tr = tr_text
        print("\nRefined (Kept base translation):")
        print(improved_tr)
        print()
    else:
        # Prompt 2: Refinement
        prompt2 = f"Now, provide the improved {args.to_lang} translation for the original text based on your analysis. Output ONLY the improved translation text. Do not include the speaker name '{speaker}:', quotes, or any explanations."
        chat_history.append({"role": "user", "content": prompt2})

        print("\nRefined:")
        # リアルタイムにストリーミング出力されるため、戻り値のprintは不要
        improved_tr = client.call(chat_history)
        improved_tr = improved_tr.strip()

        # clean up quotes if the model wrapped it
        if improved_tr.startswith('"') and improved_tr.endswith('"'):
            improved_tr = improved_tr[1:-1].strip()
        print()
    
    results.append(f"{speaker}: {improved_tr}")
    
    context_history.append({
        'original': orig_line,
        'translation': f"{speaker}: {improved_tr}"
    })

with open(args.output, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")
        
print(f"\nReview complete. Saved to {args.output}")
