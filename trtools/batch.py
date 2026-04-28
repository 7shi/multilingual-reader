# 翻訳→評価→集約を一括実行するバッチサブコマンド

import os
from argparse import Namespace
from pathlib import Path
from . import translate, evaluate, aggregate

LANG_NAMES = {
    "en": "English", "es": "Spanish", "de": "German",
    "ja": "Japanese", "zh": "Chinese", "fr": "French",
    "eo": "Esperanto", "hi": "Hindi",
}


def add_parser(subparsers):
    parser = subparsers.add_parser("batch", help="翻訳→評価→集約を一括実行")
    parser.add_argument("files", nargs="+",
                        help="入力テキストファイル（例: ../finetuning-fr.txt）")
    parser.add_argument("--langs", nargs="+", required=True,
                        help="翻訳先言語コードリスト（例: en es）")
    parser.add_argument("-f", "--from", dest="from_lang", default=None,
                        help="原語（省略時はファイル名の言語コードから自動導出）")
    parser.add_argument("-m", "--model", required=True, help="翻訳モデル")
    parser.add_argument("--evaluator", default=None, help="評価モデル（--translate-only 時は不要）")
    parser.add_argument("--translate-only", action="store_true", help="翻訳のみ実行（評価・集約をスキップ）")
    parser.add_argument("--terms-dir", default=None,
                        help="用語ファイルのディレクトリ（省略時は用語注入なし）")
    parser.add_argument("--tr-runs", type=int, default=1, help="翻訳回数（デフォルト: 1）")
    parser.add_argument("--eval-runs", type=int, default=3, help="評価回数（デフォルト: 3）")
    parser.add_argument("--threshold", type=int, default=10,
                        help="要約生成の間隔（デフォルト: 10）")
    parser.add_argument("--keep", type=int, default=5,
                        help="圧縮後に保持する翻訳ペア数（デフォルト: 5）")
    parser.add_argument("--no-think", action="store_true", help="CoT 無効化")
    parser.add_argument("--no-agg", action="store_true", help="集約をスキップ（SCORES.txt を生成しない）")
    parser.add_argument("-w", "--retry-wait", type=int, default=3,
                        help="リトライ待機秒数（デフォルト: 3）")
    parser.set_defaults(func=run)
    return parser


def _parse_input_file(file_path):
    """ファイルパスから (topic, from_code) を導出する。
    例: ../finetuning-fr.txt → ("finetuning", "fr")
    """
    stem = Path(file_path).stem  # 例: "finetuning-fr"
    topic, from_code = stem.rsplit("-", 1)
    return topic, from_code


def _tr_path(topic, lang, trrun, tr_runs):
    """翻訳出力ファイルパスを返す。tr_runs==1 のときはサフィックスなし。"""
    if tr_runs == 1:
        return f"tr/{topic}-{lang}.txt"
    return f"tr/{topic}-{lang}-{trrun}.txt"


def _eval_path(topic, lang, trrun, tr_runs, evrun):
    """評価出力ファイルパスを返す。tr_runs==1 のときは trrun 部分を省略。"""
    if tr_runs == 1:
        return f"evals/{topic}-{lang}-eval-{evrun}.json"
    return f"evals/{topic}-{lang}-{trrun}-eval-{evrun}.json"


def run(args):
    if not args.translate_only and not args.evaluator:
        print("エラー: --evaluator が必要です（翻訳のみ実行する場合は --translate-only を指定）")
        return

    terms_dir = Path(args.terms_dir) if args.terms_dir else None

    os.makedirs("tr", exist_ok=True)
    if not args.translate_only:
        os.makedirs("evals", exist_ok=True)

    # ファイルごとに (topic, from_code, from_lang, input_file) を解決
    inputs = []
    for file_path in args.files:
        p = Path(file_path)
        if not p.exists():
            print(f"Skipping {file_path} (not found)")
            continue
        topic, from_code = _parse_input_file(file_path)
        from_lang = args.from_lang or LANG_NAMES.get(from_code, from_code.capitalize())
        inputs.append((topic, from_code, from_lang, p))

    # --- 翻訳フェーズ ---
    for topic, from_code, from_lang, input_file in inputs:
        terms_json = str(terms_dir / f"{topic}-{from_code}.json") if terms_dir else None
        terms_tsv = str(terms_dir / f"{topic}-{from_code}.tsv") if terms_dir else None
        for lang in args.langs:
            lang_name = LANG_NAMES.get(lang, lang.capitalize())
            for trrun in range(1, args.tr_runs + 1):
                out = _tr_path(topic, lang, trrun, args.tr_runs)
                if os.path.exists(out):
                    print(f"Skipping {out} (already exists)")
                    continue
                print(f"\nTranslating {out} ...")
                tr_args = Namespace(
                    input_file=str(input_file),
                    from_lang=from_lang,
                    to_lang=lang_name,
                    output_file=out,
                    model=args.model,
                    threshold=args.threshold,
                    keep=args.keep,
                    terms_json=terms_json,
                    terms_tsv=terms_tsv,
                    no_think=args.no_think,
                    retry_wait=args.retry_wait,
                )
                try:
                    translate.run(tr_args)
                except Exception as e:
                    print(f"翻訳エラー ({out}): {e}")

    if args.translate_only:
        return

    # --- 評価フェーズ ---
    for topic, from_code, from_lang, input_file in inputs:
        for lang in args.langs:
            lang_name = LANG_NAMES.get(lang, lang.capitalize())
            for trrun in range(1, args.tr_runs + 1):
                tr_file = _tr_path(topic, lang, trrun, args.tr_runs)
                if not os.path.exists(tr_file):
                    print(f"Skipping {tr_file} evaluation (translation not available)")
                    continue
                for evrun in range(1, args.eval_runs + 1):
                    eval_out = _eval_path(topic, lang, trrun, args.tr_runs, evrun)
                    if os.path.exists(eval_out):
                        print(f"Skipping {eval_out} (already exists)")
                        continue
                    print(f"\nEvaluating {tr_file} (eval run {evrun})...")
                    eval_args = Namespace(
                        original=str(input_file),
                        translation=tr_file,
                        model=args.evaluator,
                        from_lang=from_lang,
                        to_lang=lang_name,
                        output_file=eval_out,
                        retry_wait=args.retry_wait,
                        no_think=False,
                    )
                    try:
                        evaluate.run(eval_args)
                    except Exception as e:
                        print(f"評価エラー ({eval_out}): {e}")

    if args.no_agg:
        return

    # --- 集約フェーズ ---
    with open("SCORES.txt", "w", encoding="utf-8") as scores_f:
        first = True
        for topic, from_code, from_lang, _ in inputs:
            for lang in args.langs:
                for trrun in range(1, args.tr_runs + 1):
                    jsons = [
                        _eval_path(topic, lang, trrun, args.tr_runs, evrun)
                        for evrun in range(1, args.eval_runs + 1)
                        if os.path.exists(_eval_path(topic, lang, trrun, args.tr_runs, evrun))
                    ]
                    if not jsons:
                        continue
                    prefix = "" if first else "\n"
                    first = False
                    if args.tr_runs == 1:
                        header = f"{prefix}=== {topic} {from_code.upper()}→{lang.upper()} ==="
                    else:
                        header = f"{prefix}=== {topic} {from_code.upper()}→{lang.upper()} (translation run {trrun}) ==="
                    print(header)
                    scores_f.write(header + "\n")
                    results = aggregate.aggregate_evaluations(jsons)
                    for base_name, result in results.items():
                        total = result["total_scores"]
                        if total["median"] is not None:
                            line = f"{base_name}: {int(total['median'])}/100点"
                            print(line)
                            scores_f.write(line + "\n")
