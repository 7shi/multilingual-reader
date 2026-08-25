# 行単位翻訳サブコマンド（用語注入・サマリー圧縮方式）
# experimental4/translate.py をベースに話者分離を廃止し、空行を保持したまま1行ずつ翻訳する。
# 用語抽出は trtools term extract/translate で事前に実施し、JSON と TSV を読み込んで注入する。

import csv
import json
import os
import time
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .statusline import StatusLine
from .summary import load_summaries

LINE_RETRY_COUNT = 3


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


def _load_terms(terms_json, terms_tsv, from_lang, to_lang, write=None):
    """JSON と TSV から chunk_data と glossary を構築する。"""
    if write is None:
        write = lambda text: print(text, end="")

    with open(terms_json, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    if json_data.get("from") != from_lang:
        write(f"WARNING: 用語JSONの原語 '{json_data.get('from')}' が指定言語 '{from_lang}' と異なります。\n")

    chunk_data = json_data.get("chunks", [])

    glossary = {}
    with open(terms_tsv, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        if from_lang not in header:
            write(f"WARNING: TSV に '{from_lang}' 列がありません。用語注入をスキップします。\n")
            return chunk_data, glossary
        if to_lang not in header:
            write(f"WARNING: TSV に '{to_lang}' 列がありません。用語注入をスキップします。\n")
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


def _build_summary_messages(summary_text):
    """要約テキストをコンテキスト注入用のメッセージペアに変換する。"""
    if not summary_text:
        return []
    user_msg = {
        "role": "user",
        "content": f"Context summary of the source text so far:\n{summary_text}",
    }
    assistant_msg = {
        "role": "assistant",
        "content": "Understood, I will keep this context in mind.",
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

    ui = StatusLine(
        label=getattr(args, 'label', None),
        start=getattr(args, 'start', None),
        index=getattr(args, 'index', None),
        count=getattr(args, 'count', None),
    )

    # 出力ファイルの既存内容から再開位置を求める
    existing_lines = []
    if os.path.exists(args.output_file):
        with open(args.output_file, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()
    resume_count = sum(1 for orig_idx, _ in content_lines if orig_idx < len(existing_lines))
    translated_text = {
        orig_idx: existing_lines[orig_idx].rstrip("\n")
        for orig_idx, _ in content_lines[:resume_count]
    }

    if total > 0 and resume_count >= total:
        ui.write(f"既に翻訳済みです: {args.output_file}\n")
        return

    # 要約は trtools summary で事前生成しておく必要がある（未生成ならエラー）
    summaries = load_summaries(args.input_file, total, threshold, keep)

    chunk_data = []
    glossary = {}
    if args.terms_json and args.terms_tsv:
        chunk_data, glossary = _load_terms(args.terms_json, args.terms_tsv, from_lang, to_lang, ui.write)

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

    def build_chat_history(position):
        """position（訳し終えた行数）時点の chat_history を組み立てる。
        新規開始（position == 0）でも再開でも同じ手順で構築する。"""
        seed_start = position + 1
        seed_end = min(position + threshold + keep, total)
        terms_msgs = _build_terms_messages(seed_start, seed_end, chunk_data, glossary, from_lang, to_lang)
        checkpoint = max((i for i in summaries if i <= position), default=None)
        summary_msgs = _build_summary_messages(summaries.get(checkpoint))
        translation_messages = []
        for orig_idx, line in content_lines[max(0, position - keep):position]:
            translated = translated_text[orig_idx]
            translation_messages.append({
                "role": "user",
                "content": f"Translate the following {from_lang} line into {to_lang}.\n{line}",
            })
            translation_messages.append({"role": "assistant", "content": translated})
        return (
            [system_message] + terms_msgs + summary_msgs
            + translation_messages[-keep * 2:]
        ), translation_messages

    chat_history, translation_messages = build_chat_history(resume_count)

    def translate_line(prompt):
        for attempt in range(1, LINE_RETRY_COUNT + 1):
            user_msg = {"role": "user", "content": prompt}
            chat_history.append(user_msg)
            translated = client.call(chat_history, file=ui.stream)
            ui.stream.end()
            stripped = translated.strip()
            if stripped and "\n" not in stripped:
                asst_msg = {"role": "assistant", "content": stripped}
                chat_history.append(asst_msg)
                return stripped, user_msg, asst_msg
            chat_history.pop()
            if attempt < LINE_RETRY_COUNT:
                ui.write(f"WARNING: 翻訳結果が不正です（試行{attempt}/{LINE_RETRY_COUNT}）。再試行します。\n")
                time.sleep(args.retry_wait)
            else:
                raise RuntimeError(f"翻訳結果が不正です（{LINE_RETRY_COUNT}回失敗）: {prompt!r}")

    start_time = time.time()
    next_compression = None
    next_write_idx = len(existing_lines)

    out_f = open(args.output_file, "a" if resume_count else "w", encoding="utf-8")
    try:
        with ui.progress(total, start=resume_count) as prog:
            for k in range(resume_count, total):
                i = k + 1
                orig_idx, line = content_lines[k]
                prompt = f"Translate the following {from_lang} line into {to_lang}.\n{line}"
                translated, user_msg, asst_msg = translate_line(prompt)
                translation_messages.extend([user_msg, asst_msg])
                translated_text[orig_idx] = translated
                prog.update(i)

                out_f.writelines(all_lines[next_write_idx:orig_idx])
                out_f.write(translated + "\n")
                out_f.flush()
                next_write_idx = orig_idx + 1

                if i % threshold == 0 and i + keep < total and i in summaries:
                    next_compression = i + keep

                if next_compression is not None and i == next_compression:
                    chat_history, translation_messages = build_chat_history(i)
                    next_compression = None

        out_f.writelines(all_lines[next_write_idx:])
    finally:
        out_f.close()

    elapsed = time.time() - start_time

    ui.write(f"\n翻訳完了: {from_lang} → {to_lang} ({args.output_file})\n")
    ui.write(f"処理時間: {elapsed:.1f}秒 ({elapsed/60:.1f}分)\n")
