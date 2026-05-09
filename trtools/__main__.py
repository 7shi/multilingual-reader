import argparse
from trtools import evaluate, aggregate, term, translate, batch, review

def main():
    parser = argparse.ArgumentParser(
        prog="trtools",
        description="翻訳ツール集",
    )
    parser.add_argument("--label", default=None, help="プログレスバーに表示するラベル（例: 'nl: Dutch (2/10)'）")
    parser.add_argument("--start", type=float, default=None, help="バッチ開始時刻（Unixタイムスタンプ）")

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    evaluate.add_parser(subparsers)
    aggregate.add_parser(subparsers)
    term.add_parser(subparsers)
    translate.add_parser(subparsers)
    review.add_parser(subparsers)
    batch.add_parser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
