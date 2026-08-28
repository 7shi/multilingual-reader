import csv
from .language import LANG_NAMES
from .llm import LLMClient
from .statusline import StatusLine


def add_parser(subparsers):
    parser = subparsers.add_parser("review", help="Polish a translation via third-party review")
    parser.add_argument("--original", required=True, help="Original text file")
    parser.add_argument("--translation", required=True, help="Baseline translation text file")
    parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language code (e.g. en)")
    parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language code (e.g. nl)")
    parser.add_argument("-o", "--output", required=True, help="Output filename after polishing")
    parser.add_argument("-m", "--model", required=True, help="Model used for polishing")
    parser.add_argument("--history", type=int, default=10, help="Number of context history entries (default: 10)")
    parser.add_argument("--no-think", action="store_true", help="Disable thinking")
    parser.add_argument("--terms", help="Term translation TSV file (used to convert speaker names)")
    parser.set_defaults(func=run)


def run(args):
    ui = StatusLine(label=args.label, start=args.start)

    if args.from_lang not in LANG_NAMES:
        ui.write(f"Unknown language code: {args.from_lang}\n")
        return
    if args.to_lang not in LANG_NAMES:
        ui.write(f"Unknown language code: {args.to_lang}\n")
        return
    from_lang = LANG_NAMES[args.from_lang]
    to_lang = LANG_NAMES[args.to_lang]

    with open(args.original, "r", encoding="utf-8") as f:
        orig_lines = f.readlines()
    with open(args.translation, "r", encoding="utf-8") as f:
        tr_lines = f.readlines()

    if len(orig_lines) != len(tr_lines):
        ui.write("Warning: The number of lines in original and translation files do not match.\n")

    terms_dict = {}
    if args.terms:
        with open(args.terms, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f, delimiter="\t"))
        if rows:
            headers = rows[0]
            try:
                from_col = headers.index(from_lang)
                to_col = headers.index(to_lang)
                for row in rows[1:]:
                    if len(row) > max(from_col, to_col) and row[from_col]:
                        terms_dict[row[from_col]] = row[to_col]
            except ValueError as e:
                ui.write(f"Warning: {e} in terms TSV\n")

    client = LLMClient(model=args.model, think=(not args.no_think))
    context_history = []
    results = []

    with ui.progress(len(orig_lines)) as prog:
        for i, (orig_line, tr_line) in enumerate(zip(orig_lines, tr_lines)):
            orig_line = orig_line.strip()
            tr_line = tr_line.strip()

            prog.update(i)

            if not orig_line or ":" not in orig_line:
                results.append(tr_line)
                continue

            ui.rule(f"{i+1}/{len(orig_lines)}")
            ui.show_pair(orig_line, tr_line)

            speaker, text = orig_line.split(":", 1)
            speaker = speaker.strip()
            text = text.strip()
            translated_speaker = terms_dict.get(speaker, speaker)

            if ":" in tr_line:
                _, tr_text = tr_line.split(":", 1)
                tr_text = tr_text.strip()
            else:
                tr_text = tr_line

            chat_history = [
                {
                    "role": "system",
                    "content": f"You are an expert {to_lang} reviewer. Your task is to review and refine a {from_lang} to {to_lang} translation.",
                }
            ]

            if context_history and args.history > 0:
                context_prompt = "Previous context:\n\n"
                for ctx in context_history[-args.history:]:
                    context_prompt += f"Original: {ctx['original']}\nTranslation: {ctx['translation']}\n\n"
                chat_history.append({"role": "user", "content": context_prompt.strip()})
                chat_history.append({"role": "assistant", "content": "Understood. I will use this context for consistency."})

            prompt1 = (
                f"Original {from_lang} text:\n{text}\n\n"
                f"Base {to_lang} translation:\n{tr_text}\n\n"
                f"Please analyze this translation. Point out any literal translations, interference from other languages, "
                f"unnatural phrasing, or grammar issues. If it's perfect, just say 'No issues'."
            )
            chat_history.append({"role": "user", "content": prompt1})
            analysis = client.call(chat_history, file=ui.stream)
            ui.stream.end()
            chat_history.append({"role": "assistant", "content": analysis})

            if "No issues" in analysis or "no issues" in analysis.lower():
                improved_tr = tr_text
            else:
                prompt2 = (
                    f"Now, provide the improved {to_lang} translation for the original text based on your analysis. "
                    f"Output ONLY the improved translation text. Do not include the speaker name '{speaker}:', quotes, or any explanations."
                )
                chat_history.append({"role": "user", "content": prompt2})
                improved_tr = client.call(chat_history, file=None)
                improved_tr = improved_tr.strip()
                if improved_tr.startswith('"') and improved_tr.endswith('"'):
                    improved_tr = improved_tr[1:-1].strip()

            ui.show_panel(f"{translated_speaker}: {improved_tr}", title="Refined")

            results.append(f"{translated_speaker}: {improved_tr}")
            context_history.append({
                "original": orig_line,
                "translation": f"{translated_speaker}: {improved_tr}",
            })

        prog.update(len(orig_lines))

    with open(args.output, "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")

    ui.write(f"\n[bold green]Review complete.[/bold green] Saved to {args.output}\n")
