# 対話テキスト翻訳（ハイブリッドモード）
# experimental/02/translate.py をベースに、以下を固定化：
# - 翻訳本体は CoT なし
# - 要約生成は CoT あり（--no-think で CoT なしに切り替え可）
# - サマリー方式は glossary 固定
# - 要約は履歴に残さず、再編成タイミングで初めて注入
# - 構造化出力（schema）は不使用
#
# サイクル長 = THRESHOLD（要約間隔）。再編成は要約から KEEP 行後。

import argparse
import time
from llm7shi.compat import generate_with_schema

parser = argparse.ArgumentParser(description="対話テキストをハイブリッドモード（翻訳=CoTなし、要約=CoTあり）で翻訳")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: French, English, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: Spanish, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳モデル")
parser.add_argument("--threshold", type=int, default=20, help="要約生成の間隔（デフォルト: 20）")
parser.add_argument("--keep", type=int, default=5, help="要約後〜再編成までの翻訳ペア数（デフォルト: 5）")
parser.add_argument("--no-think", action="store_true", help="要約生成の CoT を無効化（翻訳は常に CoT なし）")
args = parser.parse_args()

MODEL = args.model
THRESHOLD = args.threshold
KEEP = args.keep
THINK_SUMMARY = not args.no_think

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

entries = []
for line in lines:
    line = line.strip()
    if not line or ":" not in line:
        continue
    speaker, text = line.split(":", 1)
    entries.append((speaker.strip(), text.strip()))

system_message = {
    "role": "system",
    "content": (
        f"You are a professional translator. Translate the following {args.from_lang} "
        f"text to {args.to_lang}. Maintain consistency with previous translations and "
        f"preserve the context and nuance of the original text. Provide only the "
        f"translation without any explanations or commentary."
    ),
}


def call_llm(prompt, think):
    """chat_history に prompt を追加して LLM を呼び出し、応答も history に追加する。"""
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    response = generate_with_schema(
        chat_history,
        model=MODEL,
        include_thoughts=think,
        show_params=False,
    )
    response_text = response.text.strip()

    chunk = response.chunks[-1] if response.chunks else None
    if chunk and hasattr(chunk, "prompt_eval_count") and chunk.prompt_eval_count:
        prompt_dur = chunk.prompt_eval_duration / 1e9
        prompt_tps = chunk.prompt_eval_count / prompt_dur
        eval_dur   = chunk.eval_duration / 1e9
        eval_tps   = chunk.eval_count / eval_dur
        total_dur  = chunk.total_duration / 1e9
        print(f"  prompt: {chunk.prompt_eval_count} tokens, {prompt_dur:.2f}s, {prompt_tps:.0f} tps"
              f" | eval: {chunk.eval_count} tokens, {eval_dur:.2f}s, {eval_tps:.0f} tps"
              f" | total: {total_dur:.2f}s")

    assistant_message = {"role": "assistant", "content": response_text}
    chat_history.append(assistant_message)

    return response_text, user_message, assistant_message


def summarize_messages():
    """glossary サマリーを生成（CoT は THINK_SUMMARY で制御）。"""
    summary_content = (
        "Please compress the translation history above into a concise summary "
        "with two parts.\n\n"
        "PART 1 - Proper noun glossary:\n"
        "List original→translated mappings for:\n"
        "- Person names, place names, work/product titles\n"
        "- Domain-specific technical terms with their chosen translations\n"
        "Do NOT include speaking styles, tone, or expression patterns.\n\n"
        "PART 2 - Content summary (English, 2-3 sentences):\n"
        "Summarize what was discussed. Focus on topics and narrative context, "
        "not on how things were phrased.\n\n"
        "If a previous summary exists, integrate the new content with it rather "
        "than starting over."
    )
    return call_llm(summary_content, think=THINK_SUMMARY)


translation_messages = []       # 累積翻訳 (U, A) ペア（削除しない台帳）
summary_messages = []           # 累積サマリー (U, A) ペア
chat_history = [system_message] # LLM に実際に渡すコンテキスト
next_compression = None

translations = []
start_time = time.time()

total = len(entries)
for i, (speaker, text) in enumerate(entries, 1):
    prompt = (
        f"Translate the following {args.from_lang} line spoken by {speaker} "
        f"into {args.to_lang}.\n{text}"
    )
    print(f"[{i}/{total}] {speaker}")
    translated_text, user_message, assistant_message = call_llm(prompt, think=False)

    translation_messages.append(user_message)
    translation_messages.append(assistant_message)

    translations.append((speaker, translated_text))

    # 要約生成（CoT あり）→ 履歴から削除
    # 末尾近くで再編成が翻訳数を超える場合はスキップ
    if i % THRESHOLD == 0 and i + KEEP <= total:
        print(f"[Generating summary after translation {i}]")
        saved_len = len(chat_history)
        _, sum_req, sum_res = summarize_messages()
        del chat_history[saved_len:]
        summary_messages.append(sum_req)
        summary_messages.append(sum_res)
        next_compression = i + KEEP

    # 再編成: [system, 最新サマリー, 直近 KEEP ペア]
    if next_compression is not None and i == next_compression:
        print(f"[Compressing history after translation {i}: keeping {KEEP} pairs]")
        chat_history = [system_message] + summary_messages[-2:] + translation_messages[-KEEP * 2:]
        next_compression = None

elapsed = time.time() - start_time

with open(args.output_file, "w", encoding="utf-8") as f:
    for speaker, translation in translations:
        f.write(f"{speaker}: {translation}\n")

print(f"\n翻訳完了: {args.from_lang} → {args.to_lang} ({args.output_file})")
print(f"処理時間: {elapsed:.1f}秒 ({elapsed/60:.1f}分)")
