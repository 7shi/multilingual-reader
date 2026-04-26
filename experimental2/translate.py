# 対話テキスト翻訳（サマリー圧縮方式）
# experimental/translate.py（スライディング）の入出力互換を保ちつつ、
# experimental/translate-json.py のサマリー圧縮アーキテクチャを踏襲する。
# chat_history を system + summary + 直近 KEEP ペア の固定構造に維持することで
# KV キャッシュを有効化する。

import argparse
import json
import time
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema

parser = argparse.ArgumentParser(description="対話テキストをサマリー圧縮方式で翻訳")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: French, English, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: Spanish, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳モデル")
parser.add_argument("--threshold", type=int, default=15, help="圧縮発動までのメッセージペア数（デフォルト: 15）")
parser.add_argument("--keep", type=int, default=5, help="圧縮後に保持する直近ペア数（デフォルト: 5）")
parser.add_argument("--summary", choices=["glossary"], default=None,
                    help="サマリー方式: glossary=固有名詞+内容要約。未指定で単純削除（最速）")
parser.add_argument("--no-think", action="store_true", help="thinking処理を無効化（Qwen3モデル用）")
parser.add_argument("--schema", action="store_true", help="構造化出力（JSONスキーマ）を有効化")
parser.add_argument("--no-summary-history", action="store_true",
                    help="サマリーを chat_history に残さない（圧縮時のみ注入）")
args = parser.parse_args()

MODEL = args.model
THRESHOLD = args.threshold
KEEP = args.keep
SUMMARY_TYPE = args.summary
THINK = not args.no_think
SUMMARY_IN_HISTORY = not args.no_summary_history


class Translation(BaseModel):
    translation: str = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")

SCHEMA = Translation if args.schema else None

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 話者分離可能な行のみを翻訳対象とする
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


def call_llm(prompt, schema=None):
    """chat_history に prompt を追加して LLM を呼び出し、応答も history に追加する。"""
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    response = generate_with_schema(
        chat_history,
        schema=schema,
        model=MODEL,
        include_thoughts=THINK,
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


def summarize_messages(summary_type):
    """サマリー生成。chat_history への追加は call_llm が行う。"""
    if summary_type == "glossary":
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
    else:
        raise ValueError(f"Unknown summary type: {summary_type}")

    return call_llm(summary_content)


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
    raw, user_message, assistant_message = call_llm(prompt, schema=SCHEMA)
    translated_text = json.loads(raw)["translation"] if SCHEMA is not None else raw

    translation_messages.append(user_message)
    translation_messages.append(assistant_message)

    translations.append((speaker, translated_text))

    # サマリー生成予約: 翻訳 10, 20, 30, ... 完了後
    if i % (THRESHOLD - KEEP) == 0:
        next_compression = i + KEEP if i + KEEP <= len(entries) else None

        if SUMMARY_TYPE is not None and next_compression is not None:
            print(f"[Generating summary after translation {i}]")
            saved_len = len(chat_history)
            _, sum_req, sum_res = summarize_messages(SUMMARY_TYPE)
            if not SUMMARY_IN_HISTORY:
                del chat_history[saved_len:]
            summary_messages.append(sum_req)
            summary_messages.append(sum_res)

    # 圧縮: 翻訳 15, 25, 35, ... 完了後
    if next_compression is not None and i == next_compression:
        print(f"[Compressing history after translation {i}: keeping {KEEP} pairs]")
        if SUMMARY_TYPE is None:
            chat_history = [system_message] + translation_messages[-KEEP * 2:]
        else:
            chat_history = [system_message] + summary_messages[-2:] + translation_messages[-KEEP * 2:]

elapsed = time.time() - start_time

with open(args.output_file, "w", encoding="utf-8") as f:
    for speaker, translation in translations:
        f.write(f"{speaker}: {translation}\n")

print(f"\n翻訳完了: {args.from_lang} → {args.to_lang} ({args.output_file})")
print(f"処理時間: {elapsed:.1f}秒 ({elapsed/60:.1f}分)")
