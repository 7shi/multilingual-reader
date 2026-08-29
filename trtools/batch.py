# Batch subcommand that runs translate -> evaluate -> aggregate in one go

import os
import time
from argparse import Namespace
from pathlib import Path
from . import translate, evaluate, aggregate
from .language import LANG_NAMES


def add_parser(subparsers):
    parser = subparsers.add_parser("batch", help="Run translate -> evaluate -> aggregate in one go")
    parser.add_argument("files", nargs="+",
                        help="Input text files (e.g. ../finetuning-fr.txt)")
    parser.add_argument("--langs", nargs="+", required=True,
                        help="List of target language codes (e.g. en es)")
    parser.add_argument("-f", "--from", dest="from_lang", default=None,
                        help="Source language (auto-derived from the filename's language code if omitted)")
    parser.add_argument("-m", "--model", default=None, help="Translation model (not needed with --eval-only)")
    parser.add_argument("--evaluator", default=None, help="Evaluation model (not needed with --tr-only)")
    parser.add_argument("--tr-only", action="store_true", help="Run translation only (skip evaluation and aggregation)")
    parser.add_argument("--eval-only", action="store_true", help="Run evaluation only (skip translation and aggregation)")
    parser.add_argument("--terms-dir", default=None,
                        help="Directory of term files (no term injection if omitted)")
    parser.add_argument("--tr-runs", type=int, default=1, help="Number of translation runs (default: 1)")
    parser.add_argument("--eval-runs", type=int, default=3, help="Number of evaluation runs (default: 3)")
    parser.add_argument("--threshold", type=int, default=10,
                        help="Interval for summary generation (default: 10)")
    parser.add_argument("--keep", type=int, default=5,
                        help="Number of translation pairs to keep after compression (default: 5)")
    parser.add_argument("--no-think", action="store_true", help="Disable CoT")
    parser.add_argument("--no-agg", action="store_true", help="Skip aggregation (do not generate SCORES.txt)")
    parser.add_argument("--tr-dir", default="tr", help="Translation output directory (default: tr)")
    parser.add_argument("--eval-dir", default="evals", help="Evaluation output directory (default: evals)")
    parser.add_argument("-w", "--retry-wait", type=int, default=3,
                        help="Retry wait time in seconds (default: 3)")
    parser.set_defaults(func=run)
    return parser


def _parse_input_file(file_path):
    """Derive (topic, from_code) from a file path.
    e.g. ../finetuning-fr.txt -> ("finetuning", "fr")
    """
    stem = Path(file_path).stem  # e.g. "finetuning-fr"
    topic, from_code = stem.rsplit("-", 1)
    return topic, from_code


def _line_count(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def _tr_path(topic, lang, trrun, tr_runs, tr_dir="tr"):
    """Return the translation output file path. No suffix when tr_runs==1."""
    if tr_runs == 1:
        return f"{tr_dir}/{topic}-{lang}.txt"
    return f"{tr_dir}/{topic}-{lang}-{trrun}.txt"


def _eval_path(topic, lang, trrun, tr_runs, evrun, eval_dir="evals"):
    """Return the evaluation output file path. Omits the trrun part when tr_runs==1."""
    if tr_runs == 1:
        return f"{eval_dir}/{topic}-{lang}-{evrun}.json"
    return f"{eval_dir}/{topic}-{lang}-{trrun}-{evrun}.json"


def run(args):
    if args.tr_only and args.eval_only:
        print("Error: --tr-only and --eval-only cannot be specified together")
        return
    if not args.eval_only and not args.model:
        print("Error: -m/--model is required (specify --eval-only to run evaluation only)")
        return
    if not args.tr_only and not args.evaluator:
        print("Error: --evaluator is required (specify --tr-only to run translation only)")
        return

    terms_dir = Path(args.terms_dir) if args.terms_dir else None

    if not args.eval_only:
        os.makedirs(args.tr_dir, exist_ok=True)
    if not args.tr_only:
        os.makedirs(args.eval_dir, exist_ok=True)

    # Resolve (topic, from_code, from_lang, input_file) for each file
    inputs = []
    for file_path in args.files:
        p = Path(file_path)
        if not p.exists():
            print(f"Skipping {file_path} (not found)")
            continue
        topic, from_code = _parse_input_file(file_path)
        from_lang = args.from_lang or LANG_NAMES.get(from_code, from_code.capitalize())
        inputs.append((topic, from_code, from_lang, p))

    # --- Translation phase ---
    if not args.eval_only:
        tr_total = len(inputs) * len(args.langs) * args.tr_runs
        tr_index = 0
        tr_start = time.time()
        for topic, from_code, from_lang, input_file in inputs:
            terms_json = str(terms_dir / f"{topic}-{from_code}.json") if terms_dir else None
            terms_tsv = str(terms_dir / f"{topic}-{from_code}.tsv") if terms_dir else None

            for lang in args.langs:
                lang_name = LANG_NAMES.get(lang, lang.capitalize())
                for trrun in range(1, args.tr_runs + 1):
                    tr_index += 1
                    out = _tr_path(topic, lang, trrun, args.tr_runs, args.tr_dir)
                    if os.path.exists(out) and _line_count(out) >= _line_count(str(input_file)):
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
                        fix=False,
                        label=lang,
                        start=tr_start,
                        index=tr_index,
                        count=tr_total,
                    )
                    translate.run(tr_args)

    if args.tr_only:
        return

    # --- Evaluation phase ---
    ev_total = len(inputs) * len(args.langs) * args.tr_runs
    ev_index = 0
    ev_start = time.time()
    for topic, from_code, from_lang, input_file in inputs:
        for lang in args.langs:
            lang_name = LANG_NAMES.get(lang, lang.capitalize())
            for trrun in range(1, args.tr_runs + 1):
                ev_index += 1
                tr_file = _tr_path(topic, lang, trrun, args.tr_runs, args.tr_dir)
                if not os.path.exists(tr_file):
                    print(f"Skipping {tr_file} evaluation (translation not available)")
                    continue
                if _line_count(tr_file) != _line_count(input_file):
                    print(f"Skipping {tr_file} evaluation (line count mismatch)")
                    continue
                for evrun in range(1, args.eval_runs + 1):
                    eval_out = _eval_path(topic, lang, trrun, args.tr_runs, evrun, args.eval_dir)
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
                        run=evrun,
                        runs=args.eval_runs,
                        label=lang,
                        start=ev_start,
                        index=ev_index,
                        count=ev_total,
                    )
                    evaluate.run(eval_args)

    if args.eval_only or args.no_agg:
        return

    # --- Aggregation phase ---
    with open("SCORES.txt", "w", encoding="utf-8") as scores_f:
        first = True
        for topic, from_code, from_lang, _ in inputs:
            for lang in args.langs:
                for trrun in range(1, args.tr_runs + 1):
                    jsons = [
                        _eval_path(topic, lang, trrun, args.tr_runs, evrun, args.eval_dir)
                        for evrun in range(1, args.eval_runs + 1)
                        if os.path.exists(_eval_path(topic, lang, trrun, args.tr_runs, evrun, args.eval_dir))
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
                            line = f"{base_name}: {int(total['median'])}"
                            print(line)
                            scores_f.write(line + "\n")
