# 原文の要約を事前生成するサブコマンド（trtools translate 用キャッシュ）
#
# 要約は "in English" で出力され、翻訳先言語 (to_lang) に依存しない。
# そのため原文（トピック）ごとに1回だけ生成しておけば、同じトピックの
# すべての to_lang / 複数回の translate 実行で使い回せる。
# 保存先はソースと同じディレクトリの {topic}-summary.jsonl（トピック名は
# 入力ファイル名の "-<言語コード>" を除いた部分）。
# translate はこのファイルを読むだけで自動生成はせず、無ければエラーにする。

import json
from pathlib import Path
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS


def add_parser(subparsers):
    parser = subparsers.add_parser("summary", help="原文の要約を事前生成（trtools translate 用キャッシュ）")
    parser.add_argument("input_files", nargs="+", help="要約対象のテキストファイル（複数指定可）")
    parser.add_argument("-f", "--from", dest="from_lang", required=True,
                        help="原語（例: French, English, Japanese）")
    parser.add_argument("-m", "--model", required=True, help="要約生成モデル")
    parser.add_argument("--threshold", type=int, default=10,
                        help="要約生成の間隔（行数）（translate と揃える。デフォルト: 10）")
    parser.add_argument("--keep", type=int, default=5,
                        help="チェックポイント算出用の保持行数（translate と揃える。デフォルト: 5）")
    parser.add_argument("--no-think", action="store_true",
                        help="thinking 処理を無効化（Qwen3 モデル用）")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"リトライ時の待機時間（秒）（デフォルト: {DEFAULT_RETRY_WAIT_SECONDS}秒）")
    parser.set_defaults(func=run)


def read_content_lines(input_file):
    """空行以外を抽出する（元の行インデックスを保持）。"""
    with open(input_file, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    return [(i, line.rstrip("\n")) for i, line in enumerate(all_lines) if line.strip()]


def topic_summary_path(input_file):
    """入力ファイルのトピック名から要約キャッシュのパスを導出する。
    例: examples/finetuning-fr.txt → examples/finetuning-summary.jsonl"""
    p = Path(input_file)
    topic, _, _ = p.stem.rpartition("-")
    topic = topic or p.stem
    return p.parent / f"{topic}-summary.jsonl"


def summary_checkpoints(total, threshold, keep):
    """要約を生成するチェックポイント（訳し終えた行数）の一覧を返す。"""
    checkpoints = []
    i = threshold
    while i <= total:
        if i + keep < total:
            checkpoints.append(i)
        i += threshold
    return checkpoints


def _read_cache(path):
    summaries = {}
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    summaries[entry["i"]] = entry["summary"]
    return summaries


def load_summaries(input_file, total, threshold, keep):
    """生成済みの要約キャッシュを読み込む。不足があればエラーにする。"""
    checkpoints = summary_checkpoints(total, threshold, keep)
    if not checkpoints:
        return {}

    path = topic_summary_path(input_file)
    summaries = _read_cache(path)
    missing = [i for i in checkpoints if i not in summaries]
    if missing:
        raise FileNotFoundError(
            f"要約キャッシュが不足しています: {path}（不足行: {missing}）\n"
            f"先に `trtools summary {input_file} -f <from_lang> -m <model> "
            f"--threshold {threshold} --keep {keep}` を実行してください。"
        )
    return summaries


def _generate_one(input_file, from_lang, threshold, keep, client):
    content_lines = read_content_lines(input_file)
    total = len(content_lines)
    checkpoints = summary_checkpoints(total, threshold, keep)
    path = topic_summary_path(input_file)

    if not checkpoints:
        print(f"要約は不要です（行数が threshold+keep 以下）: {input_file}")
        return

    summaries = _read_cache(path)
    missing = [i for i in checkpoints if i not in summaries]
    if not missing:
        print(f"要約は既に生成済みです: {path}")
        return

    system_msg = {
        "role": "system",
        "content": (
            f"You are analyzing a {from_lang} text. Summarize the text so far in 2-3 "
            f"sentences (in English). Focus on topics and narrative context. If a "
            f"previous summary exists, integrate the new content with it rather than "
            f"starting over."
        ),
    }
    history = [system_msg]
    prev_end = 0
    with open(path, "a", encoding="utf-8") as out_f:
        for i in checkpoints:
            chunk_text = "\n".join(line for _, line in content_lines[prev_end:i])
            user_msg = {"role": "user", "content": chunk_text}
            history.append(user_msg)
            if i in summaries:
                summary_text = summaries[i]
            else:
                summary_text = client.call(history).strip()
                summaries[i] = summary_text
                out_f.write(json.dumps({"i": i, "summary": summary_text}, ensure_ascii=False) + "\n")
                out_f.flush()
                print(f"要約を生成しました（{i}/{total}行）")
            history.append({"role": "assistant", "content": summary_text})
            prev_end = i

    print(f"要約を保存しました: {path}")


def run(args):
    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    n = len(args.input_files)
    for idx, input_file in enumerate(args.input_files, 1):
        print(f"[{idx}/{n}] {input_file}")
        _generate_one(input_file, args.from_lang, args.threshold, args.keep, client)
