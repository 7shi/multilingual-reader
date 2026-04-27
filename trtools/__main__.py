import argparse
from trtools import evaluate, aggregate, term

def main():
    parser = argparse.ArgumentParser(
        prog="trtools",
        description="翻訳ツール集",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    evaluate.add_parser(subparsers)
    aggregate.add_parser(subparsers)
    term.add_parser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
