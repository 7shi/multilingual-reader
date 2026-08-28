import argparse
from trtools import evaluate, aggregate, term, translate, batch, review, trend, summary

def main():
    parser = argparse.ArgumentParser(
        prog="trtools",
        description="Translation tool suite",
    )
    parser.add_argument("--label", default=None, help="Label shown in the progress bar (e.g. 'nl: Dutch (2/10)')")
    parser.add_argument("--start", type=float, default=None, help="Batch start time (Unix timestamp)")

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    evaluate.add_parser(subparsers)
    aggregate.add_parser(subparsers)
    trend.add_parser(subparsers)
    term.add_parser(subparsers)
    summary.add_parser(subparsers)
    translate.add_parser(subparsers)
    review.add_parser(subparsers)
    batch.add_parser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
