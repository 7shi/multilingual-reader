# Subcommand that checks each translation is in its target language, appending one JSONL
# record per language to langcheck.jsonl.
#
# Jev's five-criterion scoring does not notice a wrong language: French scored as German
# came out higher than as French (experimental/15/README.md section 2). This check is kept
# apart from the scoring request, so SCHEME_ID and every score on disk stay as they are.
# experimental/15/PORT.md is the design; its sections 3.5 and 3.6 are why it has this shape.
#
# Three stages, the first that decides wins:
#   copy     -- most lines are the original's, verbatim; no model.
#   fasttext -- fastText's lid.176 over the whole text, locally. Its top language decides
#               when it is the target, or a language outside the target's group with
#               P >= FT_SURE. It is sure where Jev was not (correct German, Chinese and
#               Spanish at 0.96 and above) and is the better judge of English.
#   jev      -- only what fastText leaves open: a target whose group has other members
#               (Serbian and Croatian; fastText splits them with Serbo-Croatian and
#               Bosnian), or a top language outside the group at low probability (collapsed
#               texts). Jev picks from the languages actually in question; Jev alone, with
#               a catch-all `Other`, sent correct German to `Other` (PORT.md 3.5).

import contextlib
import hashlib
import json
import os
import re
import time
from pathlib import Path

from llm7shi.usage import Usage, append_usage, print_today_totals

from .jev import DEFAULT_ATTEMPTS, DEFAULT_MODEL, DEFAULT_TIMEOUT
from .language import LANGUAGES
from .llm import init_usage_path
from .statusline import StatusLine

# lid.176.ftz from https://dl.fbaipublicfiles.com/fasttext/supervised-models/; its digest
# is part of the scheme, so lid.176.bin or another release cannot be mixed in silently.
LID_ENV = "TRTOOLS_LID_MODEL"
# The project root's .cache/ (gitignored), not the user's home.
LID_DEFAULT = Path(__file__).resolve().parents[1] / ".cache/lid.176.ftz"
LID_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"

# Languages fastText cannot be trusted to tell apart, by lid.176 code. Codes outside the
# corpus (sh, bs, nb, nn) are labels fastText gives to the corpus's languages.
GROUPS = [("hr", "sr", "sh", "bs"), ("ms", "id"), ("da", "no", "nb", "nn")]
# Names for lid.176 codes the corpus does not have, so they can be offered to Jev and
# reported. A code with no name here is reported as the code and not offered.
LID_NAMES = {
    "la": "Latin", "sh": "Serbo-Croatian", "bs": "Bosnian", "nb": "Norwegian Bokmål",
    "nn": "Norwegian Nynorsk", "ast": "Asturian", "nds": "Low German", "ie": "Interlingue",
    "io": "Ido", "oc": "Occitan", "lb": "Luxembourgish", "fy": "Western Frisian",
    "jv": "Javanese", "su": "Sundanese", "war": "Waray", "ceb": "Cebuano", "kw": "Cornish",
    "qu": "Quechua", "pms": "Piedmontese", "jbo": "Lojban", "yi": "Yiddish",
}
FT_SURE = 0.5
FT_TOP_N = 3

INSTRUCTIONS = "Which language is `text` written in?"
OPTION = "The text is written in {}."
OTHER = "Other"
OTHER_DESC = "The text is written in a language not listed here, or in no language."
# Jev's P(target): below JEV_LOW is wrong, below JEV_OK is for a person to read. Within a
# group, correct texts came out at 0.54 and above, Croatian labelled Serbian at 0.02.
JEV_LOW = 0.3
JEV_OK = 0.5

# Share of the translation's non-empty lines that may equal a line of the original.
COPY_SHARE = 0.5
# A leading speaker label, as the corpus writes it ("Camille: ...").
LABEL = re.compile(r"^[^:：]{1,40}[:：]\s*")
# Lines this long or longer are read one by one for the share of English (recorded only).
LINE_CHARS = 30


def lid_path(arg=None):
    return Path(arg or os.environ.get(LID_ENV) or LID_DEFAULT)


def file_digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def langcheck_id(lid_digest):
    """`langcheck@<8 hex>` over everything that determines a verdict."""
    parts = [lid_digest, repr(FT_SURE), repr(FT_TOP_N), INSTRUCTIONS, OPTION, OTHER,
             OTHER_DESC, repr(JEV_LOW), repr(JEV_OK), repr(COPY_SHARE), LABEL.pattern]
    parts += [",".join(g) for g in GROUPS]
    parts += [f"{k}={v}" for k, v in sorted(LID_NAMES.items())]
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return f"langcheck@{digest[:8]}"


def add_parser(subparsers):
    parser = subparsers.add_parser(
        "langcheck", help="Check that each translation is in its target language "
                          "(fastText, then TypeSafe Jev where it is unsure), writing one "
                          "JSONL record per language")
    parser.add_argument("original", help="Original text file")
    parser.add_argument("--langs", nargs="+", required=True,
                        help="Target language codes to check")
    parser.add_argument("-f", "--from", dest="from_lang", default="English",
                        help="Source language (default: English)")
    parser.add_argument("--tr-dir", default="tr",
                        help="Directory holding the translations (default: tr)")
    parser.add_argument("-o", "--output", dest="output_file", default="langcheck.jsonl",
                        help="JSONL file to append to (default: langcheck.jsonl)")
    parser.add_argument("--lid-model",
                        help=f"fastText lid.176 model (default: ${LID_ENV}, "
                             f"else {LID_DEFAULT})")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        help=f"TypeSafe model version (default: {DEFAULT_MODEL})")
    parser.add_argument("--attempts", type=int, default=DEFAULT_ATTEMPTS,
                        help=f"Attempts per language (default: {DEFAULT_ATTEMPTS})")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help=f"Per-request timeout in seconds (default: {DEFAULT_TIMEOUT:g})")
    parser.add_argument("--force", action="store_true",
                        help="Re-check every language, discarding the existing file")
    parser.set_defaults(func=run)
    return parser


def read_records(path):
    records = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{n}: {e}")
    return records


def read_done(path, scheme, model):
    """Language codes already in the JSONL; a line from another scheme or model stops the run."""
    done = {}
    if not path.is_file():
        return done
    for record in read_records(path):
        if record.get("scheme") != scheme:
            raise SystemExit(f"{path}: {record.get('lang')} checked on "
                             f"{record.get('scheme')!r}, this run is {scheme!r}; "
                             f"--force re-checks the file")
        # Records decided before Jev carry no model.
        if record.get("model") not in (None, model):
            raise SystemExit(f"{path}: {record.get('lang')} checked by "
                             f"{record.get('model')!r}, this run is {model!r}")
        done[record["lang"]] = record
    return done


def content_lines(text):
    """Non-empty lines with the speaker label stripped."""
    lines = (LABEL.sub("", line).strip() for line in text.splitlines())
    return [line for line in lines if line]


def copy_share(original_text, translated_text):
    """Share of the translation's content lines that are verbatim lines of the original."""
    original = set(content_lines(original_text))
    lines = content_lines(translated_text)
    if not lines:
        return 0.0
    return sum(line in original for line in lines) / len(lines)


def group_of(code):
    for group in GROUPS:
        if code in group:
            return group
    return (code,)


def lid_name(code):
    if code in LANGUAGES:
        return LANGUAGES[code]["en"]
    return LID_NAMES.get(code)


class Lid:
    def __init__(self, path):
        import fasttext
        if not path.is_file():
            raise SystemExit(f"no fastText model at {path}; download {LID_URL} there, "
                             f"or point --lid-model or ${LID_ENV} at it")
        self.model = fasttext.load_model(str(path))

    def predict(self, text, k):
        labels, probs = self.model.predict(text, k=k)
        return {l.removeprefix("__label__"): round(float(p), 4)
                for l, p in zip(labels, probs)}

    def read(self, text, lang):
        """(top languages of the whole text, P(target), share of long lines in English)"""
        lines = content_lines(text)
        whole = self.predict(" ".join(lines), k=176)
        long = [line for line in lines if len(line) >= LINE_CHARS]
        english = sum(next(iter(self.predict(line, k=1))) == "en" for line in long)
        return (dict(list(whole.items())[:FT_TOP_N]), whole.get(lang, 0.0),
                round(english / len(long), 4) if long else None)


def jev_options(lang, top, source):
    """(option names, target first; whether to add `Other`)

    Within a group (fastText's top language is a member) the question is only which
    member: no source language and no `Other`, which was what took correct texts
    (PORT.md 3.5). Otherwise fastText's top languages, the source and `Other` are added,
    so the language fastText suspects is on the list by name.
    """
    group = group_of(lang)
    # Within the group only the corpus's own languages: Serbo-Croatian or Bosnian beside
    # Serbian and Croatian would split a correct text's probability, and was never tried.
    codes = [c for c in group if c in LANGUAGES]
    in_group = next(iter(top)) in group
    if not in_group:
        codes += [c for c in top if c not in group]
    names = [LANGUAGES[lang]["en"]] + [lid_name(c) for c in codes if lid_name(c)]
    if not in_group:
        names.append(source)
    return list(dict.fromkeys(names)), not in_group


def ask_jev(client, model, text, names, with_other):
    from typesafe_sdk import Choice
    criteria = {name: OPTION.format(name) for name in names}
    if with_other:
        criteria[OTHER] = OTHER_DESC
    response = client.system_one({"text": text},
                                 {"language": Choice(instructions=INSTRUCTIONS,
                                                     criteria=criteria)},
                                 model=model)
    if response.model != model:
        raise SystemExit(f"requested {model} but {response.model} answered; "
                         f"the run is abandoned rather than mixing versions")
    answer = response.choices.get("language")
    if answer is None:
        raise ValueError("no answer for language")
    probabilities = {k: round(float(v), 4) for k, v in answer.probabilities.items()}
    if set(probabilities) != set(criteria):
        raise ValueError(f"unexpected options: {sorted(probabilities)}")
    usage = Usage()
    if response.usage:
        usage = Usage(raw={"input_tokens": response.usage.input_tokens,
                           "output_tokens": response.usage.output_tokens})
    return probabilities, usage


def fasttext_verdict(lang, top):
    """'ok', 'wrong' or None (for Jev) from fastText's top languages.

    A target whose group has other members goes to Jev even when fastText names the
    target: fastText's choice within a group is no evidence either way.
    """
    code, p = next(iter(top.items()))
    group = group_of(lang)
    if code in group:
        return "ok" if len(group) == 1 else None
    return "wrong" if p >= FT_SURE else None


def jev_verdict(p_target):
    if p_target < JEV_LOW:
        return "wrong"
    if p_target < JEV_OK:
        return "review"
    return "ok"


def run(args):
    original = Path(args.original)
    original_text = original.read_text(encoding="utf-8").rstrip()
    out_path = Path(args.output_file)
    tr_dir = Path(args.tr_dir)
    path = lid_path(args.lid_model)
    lid = Lid(path)
    scheme = langcheck_id(file_digest(path))

    if args.force and out_path.is_file():
        out_path.unlink()
    done = read_done(out_path, scheme, args.model)

    pending = []
    for lang in args.langs:
        if lang in done:
            continue
        if lang not in LANGUAGES:
            raise SystemExit(f"no language name for {lang!r}")
        tr_file = tr_dir / f"{original.stem.rsplit('-', 1)[0]}-{lang}.txt"
        if not tr_file.is_file():
            raise SystemExit(f"no translation at {tr_file}")
        pending.append((lang, tr_file))

    print(f"{out_path}: {len(done)} of {len(args.langs)} languages already checked, "
          f"{len(pending)} to go, on {scheme}.")
    if not pending:
        report(out_path)
        return

    usage_path = None
    client = None
    total_usage = Usage()
    asked = 0
    run_start = time.monotonic()
    try:
        ui = StatusLine(label=pending[0][0], left_count=True)
        with contextlib.ExitStack() as stack, \
                ui.progress(len(args.langs), start=len(done)) as prog:
            for offset, (lang, tr_file) in enumerate(pending, len(done) + 1):
                prog.update(offset - 1, label=lang)
                started = time.monotonic()
                text = tr_file.read_text(encoding="utf-8").rstrip()
                share = round(copy_share(original_text, text), 4)
                top, p_lid, english = lid.read(text, lang)
                record = {"lang": lang, "scheme": scheme, "copy_share": share,
                          "fasttext": {"top": top, "p_target": p_lid},
                          "english_lines": english}
                verdict = fasttext_verdict(lang, top)
                if share >= COPY_SHARE:
                    record.update(verdict="wrong", stage="copy",
                                  detected=args.from_lang)
                elif verdict is not None:
                    code = next(iter(top))
                    record.update(verdict=verdict, stage="fasttext",
                                  detected=lid_name(code) or code)
                else:
                    if client is None:
                        from typesafe_sdk import TypeSafeClient
                        client = stack.enter_context(TypeSafeClient(timeout=args.timeout))
                        usage_path = init_usage_path(args.model, save_usage=True)
                    names, with_other = jev_options(lang, top, args.from_lang)
                    for attempt in range(1, args.attempts + 1):
                        try:
                            probabilities, usage = ask_jev(client, args.model, text,
                                                           names, with_other)
                            break
                        except SystemExit:
                            raise
                        except Exception as e:
                            ui.write(f"  attempt {attempt}/{args.attempts} failed "
                                     f"for {lang}: {e}\n")
                    else:
                        raise SystemExit(f"GIVING UP on {lang} after {args.attempts} attempts")
                    total_usage = total_usage + usage
                    asked += 1
                    p_target = probabilities[names[0]]
                    record.update(verdict=jev_verdict(p_target), stage="jev",
                                  detected=max(probabilities, key=probabilities.get),
                                  model=args.model, p_target=p_target,
                                  probabilities=probabilities, usage=usage.to_dict())
                record["seconds"] = round(time.monotonic() - started, 2)
                with out_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                if record["verdict"] != "ok":
                    ui.write(f"  {lang}: {record['verdict']} ({record['stage']}, "
                             f"detected {record['detected']})\n")
                prog.update(offset, label=lang)
    finally:
        if asked:
            append_usage(total_usage, args.model, usage_path)

    elapsed = time.monotonic() - run_start
    print(f"\n{len(pending)} languages in {elapsed:.1f}s, {asked} asked of Jev"
          + (f", {total_usage}" if asked else "") + "\n")
    report(out_path)
    if asked:
        print_today_totals(usage_path, models=[args.model])


def report(path):
    """One line per language that did not pass."""
    flagged = [r for r in read_records(path) if r["verdict"] != "ok"]
    if not flagged:
        print(f"{path}: every language ok")
        return
    for r in flagged:
        p = f", Jev P(target) {r['p_target']:.2f}" if "p_target" in r else ""
        print(f"{path}: {r['lang']} {r['verdict']} ({r['stage']}, "
              f"detected {r['detected']}{p})")
