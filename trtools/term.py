# 用語抽出・翻訳サブコマンド
# experimental4/translate.py の Phase 0（用語抽出と訳生成）を独立コマンド化

import json
import os
from pydantic import BaseModel, Field
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS


class TermList(BaseModel):
    terms: list[str] = Field(
        description="Proper nouns and domain-specific technical terms in the original source language"
    )


class TermPair(BaseModel):
    original: str = Field(description="The term in the source language")
    translation: str = Field(description="The translated term in the target language")


class Glossary(BaseModel):
    glossary: list[TermPair]


def add_parser(subparsers):
    parser = subparsers.add_parser("term", help="テキストから用語を抽出し訳語を生成してJSONに保存")
    parser.add_argument("input_file", help="翻訳対象のテキストファイル")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="原語（例: French, English, Japanese）")
    parser.add_argument("-t", "--to", dest="to_lang", required=True,
                        help="翻訳先言語（例: Spanish, Japanese）")
    parser.add_argument("-m", "--model", required=True, help="使用モデル")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="出力用語ファイル（JSON）")
    parser.add_argument("--keep", type=int, default=5,
                        help="チャンクサイズ（デフォルト: 5）")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
    parser.add_argument("--no-think", action="store_true",
                        help="thinking処理を無効化（Qwen3モデル用）")
    parser.set_defaults(func=run)
    return parser


def load_entries(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    entries = []
    for line in lines:
        line = line.strip()
        if not line or ":" not in line:
            continue
        speaker, text = line.split(":", 1)
        entries.append((speaker.strip(), text.strip()))
    return entries


def chunk_ranges(total, keep):
    """全チャンクの (chunk_index, start, end) を返す（1-indexed inclusive）。"""
    num = (total + keep - 1) // keep
    for cidx in range(1, num + 1):
        start = (cidx - 1) * keep + 1
        end = min(cidx * keep, total)
        yield cidx, start, end


def extract_terms(client, from_lang, chunk_text):
    prompt = (
        f"Extract proper nouns and domain-specific technical terms from the following "
        f"{from_lang} text. Return them in the original {from_lang} form (do NOT translate).\n\n"
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
    data = client.call_json([prompt], schema=TermList)
    return data.get("terms", [])


def translate_glossary(client, from_lang, to_lang, originals):
    if not originals:
        return {}
    listing = "\n".join(f"- {t}" for t in originals)
    prompt = (
        f"Translate the following {from_lang} terms into {to_lang}. "
        f"Provide a translation for every term. If a term is a proper noun "
        f"(e.g., person name) that should remain unchanged, output it as-is.\n\n"
        f"Terms:\n{listing}"
    )
    data = client.call_json([prompt], schema=Glossary)
    pairs = data.get("glossary", [])
    mapping = {p["original"]: p["translation"] for p in pairs}
    for orig in originals:
        if orig not in mapping:
            print(f"  WARNING: glossary missing translation for '{orig}', using original.")
            mapping[orig] = orig
    return mapping


def write_terms_file(path, from_lang, to_lang, chunk_terms_map, translations):
    data = {
        "from": from_lang,
        "to": to_lang,
        "chunks": [
            {"index": cidx, "start": info["start"], "end": info["end"],
             "terms": info["terms"]}
            for cidx, info in sorted(chunk_terms_map.items())
        ],
        "glossary": translations,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run(args):
    if os.path.exists(args.output_file):
        print(f"出力ファイルが既に存在します: {args.output_file}")
        return

    entries = load_entries(args.input_file)
    total = len(entries)

    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    chunks = list(chunk_ranges(total, args.keep))
    print(f"用語抽出を開始: {len(chunks)} チャンク (keep={args.keep})")

    chunk_terms_map = {}
    for cidx, start, end in chunks:
        chunk_text = "\n".join(f"{sp}: {tx}" for sp, tx in entries[start - 1:end])
        print(f"[Extract chunk {cidx}: lines {start}-{end}]")
        terms = extract_terms(client, args.from_lang, chunk_text)
        chunk_terms_map[cidx] = {"start": start, "end": end, "terms": terms}

    seen = set()
    unique_terms = []
    for cidx in sorted(chunk_terms_map.keys()):
        for t in chunk_terms_map[cidx]["terms"]:
            if t not in seen:
                seen.add(t)
                unique_terms.append(t)

    print(f"[Translating glossary: {len(unique_terms)} unique terms]")
    translations = translate_glossary(client, args.from_lang, args.to_lang, unique_terms)

    write_terms_file(args.output_file, args.from_lang, args.to_lang, chunk_terms_map, translations)
    print(f"用語ファイルを保存: {args.output_file}")
