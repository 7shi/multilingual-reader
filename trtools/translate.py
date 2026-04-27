# 行単位翻訳サブコマンド（用語注入・サマリー圧縮方式）
# experimental4/translate.py をベースに話者分離を廃止し、空行を保持したまま1行ずつ翻訳する。
# 用語抽出は trtools term extract/translate で事前に実施し、JSON と TSV を読み込んで注入する。

import csv
import json
import time
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS


def add_parser(subparsers):
    parser = subparsers.add_parser("translate", help="テキストを行単位で翻訳（空行保持）")
    parser.add_argument("input_file", help="翻訳対象のテキストファイル")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="原語（例: French, English, Japanese）")
    parser.add_argument("-t", "--to", dest="to_lang", required=True,
                        help="翻訳先言語（例: Spanish, Japanese）")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="出力ファイル名")
    parser.add_argument("-m", "--model", required=True, help="翻訳モデル")
    parser.add_argument("--threshold", type=int, default=10,
                        help="要約生成の間隔（行数）（デフォルト: 10）")
    parser.add_argument("--keep", type=int, default=5,
                        help="圧縮後に保持する翻訳ペア数（デフォルト: 5）")
    parser.add_argument("--terms-json", default=None,
                        help="trtools term extract の出力 JSON ファイル")
    parser.add_argument("--terms-tsv", default=None,
                        help="trtools term translate の出力 TSV ファイル")
    parser.add_argument("--no-think", action="store_true",
                        help="thinking 処理を無効化（Qwen3 モデル用）")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
    parser.set_defaults(func=run)


def _load_terms(terms_json, terms_tsv, from_lang, to_lang):
    """JSON と TSV から chunk_data と glossary を構築する。"""
    with open(terms_json, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    if json_data.get("from") != from_lang:
        print(f"WARNING: 用語JSONの原語 '{json_data.get('from')}' が指定言語 '{from_lang}' と異なります。")

    chunk_data = json_data.get("chunks", [])

    glossary = {}
    with open(terms_tsv, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        if from_lang not in header:
            print(f"WARNING: TSV に '{from_lang}' 列がありません。用語注入をスキップします。")
            return chunk_data, glossary
        if to_lang not in header:
            print(f"WARNING: TSV に '{to_lang}' 列がありません。用語注入をスキップします。")
            return chunk_data, glossary
        from_idx = header.index(from_lang)
        to_idx = header.index(to_lang)
        for row in reader:
            if len(row) > max(from_idx, to_idx):
                term = row[from_idx]
                translation = row[to_idx]
                if term and translation:
                    glossary[term] = translation

    return chunk_data, glossary


def _build_terms_messages(start_line, end_line, chunk_data, glossary, from_lang, to_lang):
    """指定行範囲（1-indexed inclusive）に登場する用語のメッセージペアを返す。"""
    seen = set()
    relevant = []
    for chunk in chunk_data:
        cstart, cend = chunk["start"], chunk["end"]
        if cstart <= end_line and cend >= start_line:
            for t in chunk["terms"]:
                if t not in seen and t in glossary:
                    seen.add(t)
                    relevant.append(t)

    if not relevant:
        return []

    listing = "\n".join(f"{t} => {glossary[t]}" for t in relevant)
    user_msg = {
        "role": "user",
        "content": (
            f"Glossary for the upcoming {from_lang} → {to_lang} translation. "
            f"Use these translations consistently:\n{listing}"
        ),
    }
    assistant_msg = {
        "role": "assistant",
        "content": "Acknowledged. I will use these translations consistently.",
    }
    return [user_msg, assistant_msg]


def run(args):
    from_lang = args.from_lang
    to_lang = args.to_lang
    threshold = args.threshold
    keep = args.keep

    with open(args.input_file, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # 空行以外を翻訳対象として抽出（元の行インデックスを保持）
    content_lines = [(i, line.rstrip("\n")) for i, line in enumerate(all_lines) if line.strip()]
    total = len(content_lines)

    chunk_data = []
    glossary = {}
    if args.terms_json and args.terms_tsv:
        chunk_data, glossary = _load_terms(args.terms_json, args.terms_tsv, from_lang, to_lang)

    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    system_message = {
        "role": "system",
        "content": (
            f"You are a professional translator. Translate the following {from_lang} "
            f"text to {to_lang}. Maintain consistency with previous translations and "
            f"preserve the context and nuance of the original text. Provide only the "
            f"translation without any explanations or commentary."
        ),
    }

    initial_end = min(threshold + keep, total)
    chat_history = (
        [system_message]
        + _build_terms_messages(1, initial_end, chunk_data, glossary, from_lang, to_lang)
    )

    translation_messages = []
    summary_messages = []
    next_compression = None
    results = {}

    def call_llm(prompt):
        user_msg = {"role": "user", "content": prompt}
        chat_history.append(user_msg)
        translated = client.call(chat_history)
        asst_msg = {"role": "assistant", "content": translated}
        chat_history.append(asst_msg)
        return translated, user_msg, asst_msg

    start_time = time.time()

    for i, (orig_idx, line) in enumerate(content_lines, 1):
        print(f"[{i}/{total}] ", end="", flush=True)
        prompt = f"Translate the following {from_lang} line into {to_lang}.\n{line}"
        translated, user_msg, asst_msg = call_llm(prompt)
        translation_messages.extend([user_msg, asst_msg])
        results[orig_idx] = translated

        if i % threshold == 0 and i + keep < total:
            saved_len = len(chat_history)
            print("[summary] ", end="", flush=True)
            summary_prompt = (
                "Please summarize the translation history above in 2-3 sentences (in English). "
                "Focus on topics and narrative context. "
                "If a previous summary exists, integrate the new content with it rather "
                "than starting over."
            )
            _, sum_req, sum_res = call_llm(summary_prompt)
            del chat_history[saved_len:]
            summary_messages.extend([sum_req, sum_res])
            next_compression = i + keep

        if next_compression is not None and i == next_compression:
            next_start = i + 1
            next_end = min(i + threshold + keep, total)
            terms_msgs = _build_terms_messages(
                next_start, next_end, chunk_data, glossary, from_lang, to_lang
            )
            chat_history = (
                [system_message]
                + terms_msgs
                + summary_messages[-2:]
                + translation_messages[-keep * 2:]
            )
            next_compression = None

    elapsed = time.time() - start_time

    with open(args.output_file, "w", encoding="utf-8") as f:
        for i, line in enumerate(all_lines):
            if line.strip():
                f.write(results[i] + "\n")
            else:
                f.write(line)

    print(f"\n翻訳完了: {from_lang} → {to_lang} ({args.output_file})")
    print(f"処理時間: {elapsed:.1f}秒 ({elapsed/60:.1f}分)")
