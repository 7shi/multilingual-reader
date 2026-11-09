# Translation with PLaMo 3 Translate, one request per language for the whole text.
#
# trtools translate cannot drive this model: its chat template skips system messages and
# reads every user/assistant pair as a source/translation example, so the injected
# instructions, glossary and summary would be translated or taken as history. The options
# go in chat-template variables instead, through llm7shi's Client.plamo3translate().
# The glossary is the target language's whole column of the term TSV, since the whole
# text goes in one request anyway.

from llm7shi import Client

from .whole import add_common_arguments, translate_each

# The model's language codes where they differ from the corpus's (model card, Supported
# Languages). The output file keeps the corpus's code.
MODEL_CODES = {"zh": "zh-hans"}

# The output of PLaMo 3 Translate may be distributed only when marked as such
# (PLaMo Community License, Article 5).
LICENSE_NOTE = ("Outputs of PLaMo 3 Translate, under the PLaMo Community License: "
                "https://plamo.preferredai.jp/info/plamo-community-license-en")


def add_parser(subparsers):
    parser = subparsers.add_parser(
        "plamo", help="Translate a whole text with PLaMo 3 Translate (one request per language)")
    add_common_arguments(parser)
    parser.add_argument("-m", "--model", default="llama.cpp:",
                        help="Model with vendor prefix (default: llama.cpp:, see OPENAI_BASE_URL)")
    parser.set_defaults(func=run)
    return parser


def run(args):
    def make_client(from_code, lang, glossary, max_length, stream):
        return Client.plamo3translate(
            MODEL_CODES.get(lang, lang),
            model=args.model,
            source_lang=from_code,
            glossary=glossary or None,
            file=stream,
            show_params=False,
            keep_history=False,
            # temperature 0 makes a retry repeat the same output; a stop is reported instead
            retries=1,
            max_length=max_length,
        )

    print(LICENSE_NOTE)
    translate_each(args, make_client)
