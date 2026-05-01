# 用語抽出・翻訳サブコマンド（term extract / term translate）

import csv
import json
import os
import sys
from pathlib import Path
from pydantic import BaseModel, Field
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .language import resolve_lang, resolve_langs


class TermList(BaseModel):
    terms: list[str] = Field(
        description="Proper nouns and domain-specific technical terms in the original source language"
    )


class TermPair(BaseModel):
    original: str = Field(description="The term in the source language")
    translation: str = Field(description="The translated term in the target language")


class Glossary(BaseModel):
    glossary: list[TermPair]


# ---------------------------------------------------------------------------
# add_parser
# ---------------------------------------------------------------------------

def add_parser(subparsers):
    term_parser = subparsers.add_parser("term", help="用語の抽出・翻訳")
    term_sub = term_parser.add_subparsers(dest="term_command", metavar="<command>")
    term_sub.required = True
    _add_extract_parser(term_sub)
    _add_translate_parser(term_sub)
    _add_show_parser(term_sub)
    _add_set_parser(term_sub)
    _add_reorder_parser(term_sub)
    _add_merge_parser(term_sub)


def _add_show_parser(subparsers):
    parser = subparsers.add_parser("show", help="TSVの列・行を絞り込んで表示")
    parser.add_argument("input_file", metavar="FILE", help="対象TSVファイル")
    parser.add_argument("-l", "--lang", action="append", metavar="LANG",
                        help="表示する言語列（複数指定可、省略時は全列）")
    parser.add_argument("-k", "--key", action="append", metavar="KEY",
                        help="表示するキー（第1列の値、複数指定可、省略時は全行）")
    parser.set_defaults(func=run_show)


def _add_reorder_parser(subparsers):
    parser = subparsers.add_parser("reorder", help="TSVの列を指定順に並べ替えて出力")
    parser.add_argument("input_file", metavar="FILE", help="対象TSVファイル")
    parser.add_argument("-c", "--col", action="append", required=True, metavar="LANG",
                        help="出力する列名（複数指定、言語名または言語コード）")
    parser.add_argument("-o", "--output", required=True, help="出力TSVファイル")
    parser.set_defaults(func=run_reorder)


def _add_set_parser(subparsers):
    parser = subparsers.add_parser("set", help="TSVの特定セルを更新")
    parser.add_argument("input_file", metavar="FILE", help="対象TSVファイル")
    parser.add_argument("-k", "--key", required=True, help="変更するキー（第1列の値）")
    parser.add_argument("-l", "--lang", required=True, help="変更する言語列名")
    parser.add_argument("-v", "--value", required=True, help="新しい値")
    parser.set_defaults(func=run_set)


def _add_extract_parser(subparsers):
    parser = subparsers.add_parser("extract", help="テキストから用語を抽出してJSONに保存")
    parser.add_argument("input_file", help="翻訳対象のテキストファイル")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="原語（例: French, English, Japanese）")
    parser.add_argument("-m", "--model", required=True, help="使用モデル")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="用語抽出ファイル（JSON）")
    parser.add_argument("--keep", type=int, default=5,
                        help="チャンクサイズ（デフォルト: 5）")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
    parser.add_argument("--no-think", action="store_true",
                        help="thinking処理を無効化（Qwen3モデル用）")
    parser.set_defaults(func=run_extract)


def _add_translate_parser(subparsers):
    parser = subparsers.add_parser("translate", help="用語JSONをTSVに翻訳（穴埋め方式）")
    parser.add_argument("extract_file", help="用語抽出ファイル（JSON）")
    parser.add_argument("-t", "--to", dest="to_langs", action="append", required=True,
                        metavar="LANG", help="翻訳先言語（複数指定可）")
    parser.add_argument("-m", "--model", required=True, help="使用モデル")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="出力TSVファイル")
    parser.add_argument("-c", "--common", dest="common_file", default=None,
                        help="共通語彙TSVファイル（一致する用語はLLMをスキップして採用）")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
    parser.add_argument("--no-think", action="store_true",
                        help="thinking処理を無効化（Qwen3モデル用）")
    parser.set_defaults(func=run_translate)


# ---------------------------------------------------------------------------
# 共通ユーティリティ
# ---------------------------------------------------------------------------

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


def _call_translate(client, from_lang, to_lang, terms):
    listing = "\n".join(f"- {t}" for t in terms)
    prompt = (
        f"Translate the following {from_lang} terms into {to_lang}. "
        f"Provide a translation for every term. If a term is a proper noun "
        f"(e.g., person name) that should remain unchanged, output it as-is.\n\n"
        f"Terms:\n{listing}"
    )
    data = client.call_json([prompt], schema=Glossary)
    pairs = data.get("glossary", [])
    original_set = set(terms)
    mapping = {}
    for p in pairs:
        orig = p["original"]
        if orig not in original_set:
            print(f"  WARNING: unexpected term in glossary response '{orig}', ignoring.")
            continue
        mapping[orig] = p["translation"]
    return mapping


def translate_glossary(client, from_lang, to_lang, originals, max_retries=5):
    if not originals:
        return {}
    mapping = _call_translate(client, from_lang, to_lang, originals)
    missing = [t for t in originals if t not in mapping]
    for attempt in range(max_retries):
        if not missing:
            break
        print(f"  Retrying {len(missing)} missing term(s) (attempt {attempt + 1}/{max_retries})...")
        retry_mapping = _call_translate(client, from_lang, to_lang, missing)
        mapping.update(retry_mapping)
        missing = [t for t in missing if t not in mapping]
    for term in missing:
        print(f"  WARNING: no translation for '{term}' after {max_retries} retries, using empty string.")
        mapping[term] = ""
    return mapping


# ---------------------------------------------------------------------------
# term extract
# ---------------------------------------------------------------------------

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


def run_extract(args):
    args.from_lang = resolve_lang(args.from_lang)
    if os.path.exists(args.output_file):
        print(f"用語抽出ファイルが既に存在します（スキップ）: {args.output_file}")
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

    data = {
        "from": args.from_lang,
        "chunks": [
            {"index": cidx, "start": info["start"], "end": info["end"],
             "terms": info["terms"]}
            for cidx, info in sorted(chunk_terms_map.items())
        ],
    }
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"用語抽出ファイルを保存: {args.output_file}")


# ---------------------------------------------------------------------------
# term translate
# ---------------------------------------------------------------------------

def load_tsv(path):
    """TSVを読み込み (header, rows) を返す。rows は {lang: value} の辞書リスト。"""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        rows = [dict(zip(header, row)) for row in reader]
    return header, rows


def save_tsv(path, header, rows):
    """(header, rows) を TSV に保存する。"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        for row in rows:
            writer.writerow([row.get(col, "") for col in header])


def run_translate(args):
    args.to_langs = resolve_langs(args.to_langs)
    # from.json を読み込み
    with open(args.extract_file, "r", encoding="utf-8") as f:
        extract_data = json.load(f)
    from_lang = extract_data["from"]

    # ユニーク用語リストを順序保持で構築
    seen = set()
    unique_terms = []
    for chunk in extract_data.get("chunks", []):
        for t in chunk["terms"]:
            if t not in seen:
                seen.add(t)
                unique_terms.append(t)

    # TSV を開くか新規作成
    if os.path.exists(args.output_file):
        header, rows = load_tsv(args.output_file)
        # from_lang が一致するか確認
        if header[0] != from_lang:
            print(f"WARNING: TSV の原語列 '{header[0]}' が from.json の '{from_lang}' と異なります。")
        # unique_terms に存在しない行は保持しつつ、新しい用語を末尾に追加
        existing = {row[from_lang]: row for row in rows if from_lang in row}
        rows = []
        for t in unique_terms:
            rows.append(existing.get(t, {from_lang: t}))
    else:
        header = [from_lang]
        rows = [{from_lang: t} for t in unique_terms]

    # 新しい to_lang 列をヘッダに追加
    for to_lang in args.to_langs:
        if to_lang not in header:
            header.append(to_lang)

    # 共通語彙の読み込み: {term: {lang: translation}}
    common = {}
    if args.common_file and os.path.exists(args.common_file):
        common_header, common_rows = load_tsv(args.common_file)
        if from_lang not in common_header:
            print(f"WARNING: 共通語彙に '{from_lang}' 列がありません。スキップします。")
        else:
            for row in common_rows:
                term = row.get(from_lang, "")
                if term:
                    common[term] = row

    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    # 言語ごとに穴埋め
    for to_lang in args.to_langs:
        missing_terms = [row[from_lang] for row in rows if not row.get(to_lang)]
        if not missing_terms:
            print(f"[{to_lang}] 全用語が翻訳済み（スキップ）")
            continue

        # 共通語彙で先に埋める
        from_common = []
        need_llm = []
        for term in missing_terms:
            if term in common and common[term].get(to_lang):
                from_common.append(term)
            else:
                need_llm.append(term)
        if from_common:
            print(f"  共通語彙から採用: {len(from_common)} 件")
            for row in rows:
                if not row.get(to_lang) and row[from_lang] in common:
                    val = common[row[from_lang]].get(to_lang, "")
                    if val:
                        row[to_lang] = val

        if not need_llm:
            save_tsv(args.output_file, header, rows)
            print(f"  保存: {args.output_file}")
            continue

        print(f"[Translating {len(need_llm)} term(s) → {to_lang}]")
        mapping = translate_glossary(client, from_lang, to_lang, need_llm)
        for row in rows:
            if not row.get(to_lang):
                term = row[from_lang]
                if term in mapping:
                    row[to_lang] = mapping[term]
        # 言語ごとに保存（中断しても再開可能）
        save_tsv(args.output_file, header, rows)
        print(f"  保存: {args.output_file}")


# ---------------------------------------------------------------------------
# term show / term set
# ---------------------------------------------------------------------------

def run_show(args):
    if args.lang:
        args.lang = resolve_langs(args.lang)
    header, rows = load_tsv(args.input_file)
    key_col = header[0]

    if args.lang:
        cols = [key_col]
        for lang in args.lang:
            if lang not in header:
                print(f"警告: '{lang}' 列が見つかりません", file=sys.stderr)
            else:
                cols.append(lang)
    else:
        cols = header

    if args.key:
        key_set = set(args.key)
        rows = [r for r in rows if r.get(key_col) in key_set]

    writer = csv.writer(sys.stdout, delimiter="\t")
    writer.writerow(cols)
    for row in rows:
        writer.writerow([row.get(c, "") for c in cols])


def run_set(args):
    args.lang = resolve_lang(args.lang)
    header, rows = load_tsv(args.input_file)
    key_col = header[0]

    if args.lang not in header:
        print(f"エラー: '{args.lang}' 列が見つかりません", file=sys.stderr)
        sys.exit(1)

    updated = False
    for row in rows:
        if row.get(key_col) == args.key:
            row[args.lang] = args.value
            updated = True
            break

    if not updated:
        print(f"エラー: キー '{args.key}' が見つかりません", file=sys.stderr)
        sys.exit(1)

    save_tsv(args.input_file, header, rows)
    print(f"更新しました: {args.key!r} [{args.lang}] = {args.value!r}")


def _add_merge_parser(subparsers):
    parser = subparsers.add_parser("merge", help="複数TSVを列結合（後ファイルがセル単位で上書き）")
    parser.add_argument("input_files", metavar="FILE", nargs="+", help="入力TSVファイル（複数）")
    parser.add_argument("-o", "--output", required=True, help="出力TSVファイル")
    parser.set_defaults(func=run_merge)


def run_merge(args):
    header = []
    rows = {}  # key -> {col: value}
    key_order = []

    for path in args.input_files:
        file_header, file_rows = load_tsv(path)
        if not file_header:
            continue
        key_col = file_header[0]
        for col in file_header:
            if col not in header:
                header.append(col)
        for row in file_rows:
            key = row.get(key_col, "")
            if key not in rows:
                rows[key] = {}
                key_order.append(key)
            for col, val in row.items():
                if val:
                    rows[key][col] = val

    merged_rows = [rows[k] for k in key_order]
    save_tsv(args.output, header, merged_rows)
    print(f"保存: {args.output} ({len(merged_rows)} 行, {len(header)} 列)")


def run_reorder(args):
    args.col = resolve_langs(args.col)
    header, rows = load_tsv(args.input_file)
    for col in args.col:
        if col not in header:
            print(f"警告: '{col}' 列が入力ファイルに存在しません（空列として追加）", file=sys.stderr)
    save_tsv(args.output, args.col, rows)
    print(f"保存: {args.output}")
