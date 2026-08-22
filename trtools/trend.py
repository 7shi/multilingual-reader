# 評価ログから言語ごとの傾向を要約するサブコマンド
# 3回分の評価結果をマージして LLM に渡し、README の「傾向の分析」列に貼れる一文を生成する。
# 中間結果は JSONL に追記するため、中断しても未処理の言語だけを再開できる。

import json
from pathlib import Path
from .aggregate import find_evaluation_groups, load_evaluation_data, calculate_statistics
from .language import LANGUAGES, LANG_NAMES
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .statusline import StatusLine

CRITERIA = [
    "readability",
    "fluency",
    "terminology",
    "contextual_adaptation",
    "information_completeness",
]

# 同期対象の表を識別するヘッダ行（言語ごと）
TABLE_HEADERS = {
    "en": "| Language | Score | Trend Analysis |",
    "ja": "| 言語 | スコア | 傾向の分析 |",
}
TABLE_SEPARATOR = "| --- | ---: | --- |"


def add_parser(subparsers):
    parser = subparsers.add_parser("trend", help="評価ログから言語ごとの傾向を要約")
    parser.add_argument("files", nargs="*", help="評価結果JSONファイル（複数指定可能）")
    parser.add_argument("-m", "--model", default=None,
                        help="要約に使用するモデル（--render-only 時は不要）")
    parser.add_argument("-o", "--output", dest="output_file", default="TRENDS.jsonl",
                        help="中間結果のJSONL（デフォルト: TRENDS.jsonl）")
    parser.add_argument("--sync", default=None,
                        help="生成後に表を書き戻す README.md のパス")
    parser.add_argument("--render-only", action="store_true",
                        help="生成せずJSONLから表の出力・同期のみ行う")
    parser.add_argument("--no-think", action="store_true", help="thinking処理を無効化")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
    parser.add_argument("-l", "--lang", choices=["en", "ja"], default="en",
                        help="要約の出力言語（デフォルト: en）")
    parser.set_defaults(func=run)
    return parser


def _lang_code(base_name):
    """base_name（例: onde-ja、onde-ja-1）から言語コードを取り出す。"""
    parts = base_name.split("-")
    if len(parts) >= 3 and parts[-1].isdigit():
        return parts[-2]
    return parts[-1]


def _is_japanese(text):
    """かな・漢字を含むか。プレーンテキスト出力が英語で返る場合の検出用。"""
    return any(
        "぀" <= ch <= "ヿ" or "一" <= ch <= "鿿"
        for ch in text
    )


def _clean(text):
    """LLM のプレーンテキスト出力を表のセルに入る一行に整える。"""
    s = " ".join(text.split())
    # 全体が引用符で囲まれている場合のみ外す（訳語の引用は保持）
    for lq, rq in (("「", "」"), ('"', '"'), ("'", "'"), ("“", "”")):
        if len(s) > 1 and s.startswith(lq) and s.endswith(rq) and lq not in s[1:-1]:
            s = s[1:-1].strip()
    s = s.rstrip("。.")
    # セル区切りと衝突するためエスケープする
    return s.replace("|", "\\|")


def load_jsonl(path):
    """JSONL を {lang: record} として読み込む。存在しなければ空。"""
    records = {}
    p = Path(path)
    if not p.exists():
        return records
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            records[rec["lang"]] = rec
    return records


def append_jsonl(path, record):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _build_input(data_list):
    """評価ログ3件を Evaluation ブロックのプレーンテキストに変換する。
    criterion 別のスコア・reasoning は要約を混乱させるため渡さず、
    合計スコアと overall_comment のみを渡す。
    """
    blocks = []
    for i, d in enumerate(data_list, 1):
        if not d or "evaluation" not in d:
            continue
        ev = d["evaluation"]
        total = sum(ev[c]["score"] for c in CRITERIA if c in ev)
        comment = ev.get("overall_comment", "")
        blocks.append(f"# Evaluation {i} (Score {total})\n\n{comment}")
    return "\n\n".join(blocks)


def _matches_lang(text, lang):
    """テキストが指定言語（en/ja）で書かれているか。"""
    return _is_japanese(text) if lang == "ja" else not _is_japanese(text)


def render_table(records, lang):
    """JSONL のレコードから Markdown の表を組み立てる。スコア降順・言語コード昇順。"""
    rows = sorted(records.values(), key=lambda r: (-r["score"], r["lang"]))
    lines = [TABLE_HEADERS[lang], TABLE_SEPARATOR]
    for r in rows:
        name = LANGUAGES.get(r["lang"], {}).get(lang, r["lang"])
        lines.append(f"| {name} | {r['score']} | {r['analysis']} |")
    return lines


def sync_readme(path, table_lines):
    """README 内の TABLE_HEADERS のいずれかを持つ表を差し替える。"""
    p = Path(path)
    lines = p.read_text(encoding="utf-8").split("\n")
    result = []
    i = 0
    replaced = False
    while i < len(lines):
        if lines[i].strip() in TABLE_HEADERS.values():
            result.extend(table_lines)
            replaced = True
            i += 1
            # 既存の表本体を読み飛ばす
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
        else:
            result.append(lines[i])
            i += 1
    if not replaced:
        headers = " / ".join(TABLE_HEADERS.values())
        print(f"警告: {path} に対象の表が見つかりませんでした: {headers}")
        return False
    p.write_text("\n".join(result), encoding="utf-8")
    print(f"表を更新しました: {path}")
    return True


def run(args):
    records = load_jsonl(args.output_file)

    if not args.render_only:
        if not args.files:
            print("エラー: 評価JSONファイルを指定してください（--render-only 時は不要）")
            return
        if not args.model:
            print("エラー: -m/--model が必要です")
            return

        groups = find_evaluation_groups(args.files)
        if not groups:
            print("評価ファイルのグループが見つかりませんでした。")
            return

        # 未処理の言語だけを対象にする
        pending = []
        for base_name, runs in sorted(groups.items()):
            code = _lang_code(base_name)
            if code in records:
                continue
            pending.append((base_name, code, runs))

        skipped = len(groups) - len(pending)
        if skipped:
            print(f"{skipped}言語はJSONLに存在するためスキップします。")

        output_lang_name = "Japanese" if args.lang == "ja" else "English"

        if pending:
            client = LLMClient(
                model=args.model,
                think=(not args.no_think),
                retry_wait=args.retry_wait,
            )
            # 言語ごとに1回しか処理しないため、全言語で1本のバーとして表示する
            # 再開時も分母は全言語のままとし、スキップ済みを完了済みとして扱う
            total = len(groups)
            ui = StatusLine(label=pending[0][1], left_count=True)
            with ui.progress(total, start=skipped) as prog:
                for offset, (base_name, code, runs) in enumerate(pending, skipped + 1):
                    prog.update(offset - 1, label=code)
                    data_list = [load_evaluation_data(runs[i]) for i in [1, 2, 3]]
                    _, total_scores = calculate_statistics(data_list)
                    lang_name = LANG_NAMES.get(code, code.capitalize())

                    evaluations = _build_input(data_list)
                    prompts = [
                        f"<evaluations lang=\"{lang_name}\">\n"
                        f"{evaluations}\n"
                        f"</evaluations>",
                        f"The block above contains three independent evaluations of one translation "
                        f"whose target language is {lang_name}. Trust these evaluations as given; "
                        f"do not re-evaluate the translation yourself. Summarize the single most "
                        f"notable characteristic in one short phrase. "
                        f"An issue mentioned in multiple runs is more reliable than one mentioned "
                        f"only once.\n"
                        f"IMPORTANT: The summary must be written in {output_lang_name}, but it "
                        f"describes a translation into {lang_name}. Never confuse the language you "
                        f"write in with the language being evaluated.\n"
                        f"IMPORTANT: State only what the evaluations actually say. Do not add "
                        f"details they do not mention. For example, if they report a mixed-language "
                        f"defect without naming the intruding language, describe it generically "
                        f"rather than guessing which language it was.\n"
                        f"OUTPUT FORMAT: Reply with the summary phrase itself and nothing else. "
                        f"It goes directly into a Markdown table cell, so no labels, no quotation "
                        f"marks around the whole phrase, no bullet points, no line breaks, no "
                        f"trailing period, and no explanation before or after. "
                        f"If defects exist, state the most prominent one concretely. If the "
                        f"translation is sound, state that briefly. "
                        f"Keep it within 40 characters if written in Japanese, or a short phrase of "
                        f"about 8 words or fewer if written in English. "
                        f"Write it in {output_lang_name} — not in {lang_name}.",
                    ]

                    print(f"\nAnalyzing {base_name} ...")
                    for attempt in range(3):
                        p = prompts if attempt == 0 else prompts + [
                            f"The previous reply was not in {output_lang_name}. "
                            f"Reply again with the same summary written in {output_lang_name}, "
                            f"and output nothing but the phrase itself."
                        ]
                        text = client.call(p, file=ui.stream)
                        ui.stream.end()
                        if _matches_lang(text, args.lang):
                            break
                        print(f"{output_lang_name}で返らなかったため再試行します（{attempt + 1}/3）")

                    median = total_scores["median"]
                    record = {
                        "lang": code,
                        "score": int(median) if median is not None else 0,
                        "analysis": _clean(text),
                    }
                    # 1言語ごとに追記して中断に備える
                    append_jsonl(args.output_file, record)
                    records[code] = record
                    prog.update(offset, label=code)

    if not records:
        print(f"{args.output_file} にレコードがありません。")
        return

    table = render_table(records, args.lang)
    print()
    for line in table:
        print(line)

    if args.sync:
        sync_readme(args.sync, table)
