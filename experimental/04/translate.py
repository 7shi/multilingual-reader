# 対話テキスト翻訳（用語事前抽出方式）
# experimental/03 の構造を踏襲し、翻訳開始前に全文から用語と固有名詞を抽出して
# 訳語を確定する。再編成のたびに「対象範囲に絞った用語リスト」を chat_history に注入する。
# CoT は使用しない（翻訳・要約・抽出・訳生成すべて think=False）。

import argparse
import json
import os
import sys
import time
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema

parser = argparse.ArgumentParser(description="対話テキストを用語事前抽出方式で翻訳")
parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: French, English, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: Spanish, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳モデル")
parser.add_argument("--threshold", type=int, default=10, help="要約生成の間隔（デフォルト: 10）")
parser.add_argument("--keep", type=int, default=5, help="要約後〜再編成までの翻訳ペア数（デフォルト: 5）")
parser.add_argument("--terms", dest="terms_file", default=None,
                    help="用語ファイルのパス（デフォルト: <output_base>-terms.json）")
parser.add_argument("--terms-only", action="store_true",
                    help="用語抽出と訳生成のみ実行して終了（翻訳は行わない）")
args = parser.parse_args()

MODEL = args.model
THRESHOLD = args.threshold
KEEP = args.keep
FROM_LANG = args.from_lang
TO_LANG = args.to_lang

if args.terms_file:
    TERMS_FILE = args.terms_file
else:
    base, _ = os.path.splitext(args.output_file)
    TERMS_FILE = f"{base}-terms.json"


class TermList(BaseModel):
    terms: list[str] = Field(
        description="Proper nouns and domain-specific technical terms in the original source language"
    )


class TermPair(BaseModel):
    original: str = Field(description="The term in the source language")
    translation: str = Field(description="The translated term in the target language")


class Glossary(BaseModel):
    glossary: list[TermPair]


with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

entries = []
for line in lines:
    line = line.strip()
    if not line or ":" not in line:
        continue
    speaker, text = line.split(":", 1)
    entries.append((speaker.strip(), text.strip()))

total = len(entries)


def chunk_range(chunk_index):
    """1-indexed chunk_index → (start_entry, end_entry) いずれも 1-indexed inclusive。"""
    start = (chunk_index - 1) * KEEP + 1
    end = min(chunk_index * KEEP, total)
    return start, end


def num_chunks():
    return (total + KEEP - 1) // KEEP


def print_response_stats(response):
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


def call_with_schema(prompts, schema):
    """1回限りの構造化出力呼び出し（履歴なし）。JSON エラー時は最大3回リトライ。"""
    max_retries = 3
    for attempt in range(max_retries):
        response = generate_with_schema(
            prompts,
            schema=schema,
            model=MODEL,
            include_thoughts=False,
            show_params=False,
        )
        try:
            data = json.loads(response.text)
            print_response_stats(response)
            return data
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                print(f"  JSONデコードエラー（試行{attempt+1}/{max_retries}）: {e}")
                time.sleep(3)
            else:
                raise


def extract_terms(chunk_text):
    """単一チャンクから元言語の用語を抽出する。"""
    prompt = (
        f"Extract proper nouns and domain-specific technical terms from the following "
        f"{FROM_LANG} text. Return them in the original {FROM_LANG} form (do NOT translate).\n\n"
        f"Include:\n"
        f"- Person names, place names, organization names\n"
        f"- Work titles, product names, brand names\n"
        f"- Domain-specific technical terms and jargon\n\n"
        f"Exclude:\n"
        f"- Common everyday words and general vocabulary\n"
        f"- Pronouns, articles, conjunctions, prepositions\n"
        f"- Speaking styles or expressions\n\n"
        f"Output each term in its base form WITHOUT leading articles "
        f"(e.g., output 'affinage', not 'l'affinage' or 'le affinage').\n\n"
        f"Text:\n{chunk_text}"
    )
    data = call_with_schema([prompt], TermList)
    return data.get("terms", [])


def translate_glossary(originals):
    """全用語をまとめて翻訳する。"""
    if not originals:
        return {}
    listing = "\n".join(f"- {t}" for t in originals)
    prompt = (
        f"Translate the following {FROM_LANG} terms into {TO_LANG}. "
        f"Provide a translation for every term. If a term is a proper noun "
        f"(e.g., person name) that should remain unchanged, output it as-is.\n\n"
        f"Terms:\n{listing}"
    )
    data = call_with_schema([prompt], Glossary)
    pairs = data.get("glossary", [])
    mapping = {p["original"]: p["translation"] for p in pairs}
    for orig in originals:
        if orig not in mapping:
            print(f"  WARNING: glossary missing translation for '{orig}', using original.")
            mapping[orig] = orig
    return mapping


def write_terms_file(path, chunk_terms_map, translations):
    """用語ファイルを JSON で出力する。"""
    data = {
        "from": FROM_LANG,
        "to": TO_LANG,
        "chunks": [
            {"index": cidx, "start": chunk_range(cidx)[0], "end": chunk_range(cidx)[1],
             "terms": chunk_terms_map[cidx]}
            for cidx in sorted(chunk_terms_map.keys())
        ],
        "glossary": translations,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_terms_file(path):
    """用語ファイル（JSON）を読み込み、(chunk_terms_map, translations) を返す。"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("from") != FROM_LANG:
        raise ValueError(
            f"用語ファイルの from 言語 ({data.get('from')}) が引数 ({FROM_LANG}) と一致しません: {path}"
        )
    if data.get("to") != TO_LANG:
        raise ValueError(
            f"用語ファイルの to 言語 ({data.get('to')}) が引数 ({TO_LANG}) と一致しません: {path}"
        )

    chunk_terms_map = {c["index"]: c["terms"] for c in data.get("chunks", [])}
    translations = data.get("glossary", {})
    return chunk_terms_map, translations


# Phase 0: 用語抽出と訳生成
if os.path.exists(TERMS_FILE):
    print(f"既存の用語ファイルを読み込み: {TERMS_FILE}")
    chunk_terms_map, term_translations = read_terms_file(TERMS_FILE)
else:
    print(f"用語抽出を開始: {num_chunks()} チャンク (keep={KEEP})")
    chunk_terms_map = {}
    for cidx in range(1, num_chunks() + 1):
        start, end = chunk_range(cidx)
        chunk_text = "\n".join(f"{sp}: {tx}" for sp, tx in entries[start - 1:end])
        print(f"[Extract chunk {cidx}: lines {start}-{end}]")
        chunk_terms_map[cidx] = extract_terms(chunk_text)

    seen = set()
    unique_terms = []
    for cidx in sorted(chunk_terms_map.keys()):
        for t in chunk_terms_map[cidx]:
            if t not in seen:
                seen.add(t)
                unique_terms.append(t)

    print(f"[Translating glossary: {len(unique_terms)} unique terms]")
    term_translations = translate_glossary(unique_terms)

    write_terms_file(TERMS_FILE, chunk_terms_map, term_translations)
    print(f"用語ファイルを保存: {TERMS_FILE}")

if args.terms_only:
    sys.exit(0)


def build_terms_messages(start_entry, end_entry):
    """指定範囲（1-indexed inclusive）に登場する用語のメッセージペアを返す。"""
    chunks_in_range = []
    for cidx in sorted(chunk_terms_map.keys()):
        cstart, cend = chunk_range(cidx)
        if cstart <= end_entry and cend >= start_entry:
            chunks_in_range.append(cidx)

    seen = set()
    relevant = []
    for cidx in chunks_in_range:
        for t in chunk_terms_map[cidx]:
            if t not in seen:
                seen.add(t)
                relevant.append(t)

    if not relevant:
        return []

    listing = "\n".join(f"{t} => {term_translations.get(t, t)}" for t in relevant)
    user_msg = {
        "role": "user",
        "content": (
            f"Glossary for the upcoming {FROM_LANG} → {TO_LANG} translation. "
            f"Use these translations consistently:\n{listing}"
        ),
    }
    assistant_msg = {
        "role": "assistant",
        "content": "Acknowledged. I will use these translations consistently.",
    }
    return [user_msg, assistant_msg]


# Phase 1: 翻訳ループ
system_message = {
    "role": "system",
    "content": (
        f"You are a professional translator. Translate the following {FROM_LANG} "
        f"text to {TO_LANG}. Maintain consistency with previous translations and "
        f"preserve the context and nuance of the original text. Provide only the "
        f"translation without any explanations or commentary."
    ),
}


def call_llm(prompt):
    """chat_history に prompt を追加して LLM を呼び出し、応答も history に追加する。"""
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    response = generate_with_schema(
        chat_history,
        model=MODEL,
        include_thoughts=False,
        show_params=False,
    )
    response_text = response.text.strip()
    print_response_stats(response)

    assistant_message = {"role": "assistant", "content": response_text}
    chat_history.append(assistant_message)

    return response_text, user_message, assistant_message


def summarize_messages():
    """内容サマリーを生成（CoT なし）。用語・固有名詞は事前抽出済みのため含めない。"""
    summary_content = (
        "Please summarize the translation history above in 2-3 sentences (in English). "
        "Focus on topics and narrative context. "
        "If a previous summary exists, integrate the new content with it rather "
        "than starting over."
    )
    return call_llm(summary_content)


translation_messages = []
summary_messages = []
chat_history = [system_message] + build_terms_messages(1, min(THRESHOLD + KEEP, total))
next_compression = None

translations = []
start_time = time.time()

for i, (speaker, text) in enumerate(entries, 1):
    prompt = (
        f"Translate the following {FROM_LANG} line spoken by {speaker} "
        f"into {TO_LANG}.\n{text}"
    )
    print(f"[{i}/{total}] {speaker}")
    translated_text, user_message, assistant_message = call_llm(prompt)

    translation_messages.append(user_message)
    translation_messages.append(assistant_message)

    translations.append((speaker, translated_text))

    if i % THRESHOLD == 0 and i + KEEP <= total:
        print(f"[Generating summary after translation {i}]")
        saved_len = len(chat_history)
        _, sum_req, sum_res = summarize_messages()
        del chat_history[saved_len:]
        summary_messages.append(sum_req)
        summary_messages.append(sum_res)
        next_compression = i + KEEP

    if next_compression is not None and i == next_compression:
        print(f"[Compressing history after translation {i}: keeping {KEEP} pairs]")
        next_start = i + 1
        next_end = min(i + THRESHOLD + KEEP, total)
        terms_msgs = build_terms_messages(next_start, next_end)
        chat_history = (
            [system_message]
            + terms_msgs
            + summary_messages[-2:]
            + translation_messages[-KEEP * 2:]
        )
        next_compression = None

elapsed = time.time() - start_time

with open(args.output_file, "w", encoding="utf-8") as f:
    for speaker, translation in translations:
        f.write(f"{speaker}: {translation}\n")

print(f"\n翻訳完了: {FROM_LANG} → {TO_LANG} ({args.output_file})")
print(f"処理時間: {elapsed:.1f}秒 ({elapsed/60:.1f}分)")
