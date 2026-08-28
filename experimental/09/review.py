import argparse
import csv
import io
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, ProgressColumn, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.text import Text
from trtools.language import LANG_NAMES
from trtools.llm import LLMClient

parser = argparse.ArgumentParser(description="Translation revision script using third-party evaluation")
parser.add_argument("--original", required=True, help="Original text file")
parser.add_argument("--translation", required=True, help="Baseline translation text file")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. Dutch)")
parser.add_argument("-o", "--output", required=True, help="Output file name for the revised text")
parser.add_argument("-m", "--model", required=True, help="Model to use for revision")
parser.add_argument("--history", type=int, default=10, help="Number of context history entries")
parser.add_argument("--no-think", action="store_true", help="Disable thinking processing")
parser.add_argument("--lang-index", type=int, default=0, help="Language sequence number (passed from batch.sh)")
parser.add_argument("--lang-total", type=int, default=0, help="Total number of languages (passed from batch.sh)")
parser.add_argument("--batch-start", type=float, default=0.0, help="Batch start time (Unix timestamp)")
parser.add_argument("--terms", help="Terminology translation TSV file (used to convert speaker names)")
args = parser.parse_args()

if args.from_lang not in LANG_NAMES:
    parser.error(f"Unknown language code: {args.from_lang}")
if args.to_lang not in LANG_NAMES:
    parser.error(f"Unknown language code: {args.to_lang}")
from_code = args.from_lang
to_code   = args.to_lang
args.from_lang = LANG_NAMES[args.from_lang]
args.to_lang   = LANG_NAMES[args.to_lang]

with open(args.original, "r", encoding="utf-8") as f:
    orig_lines = f.readlines()
with open(args.translation, "r", encoding="utf-8") as f:
    tr_lines = f.readlines()

if len(orig_lines) != len(tr_lines):
    print("Warning: The number of lines in original and translation files do not match.")

terms_dict = {}
if args.terms:
    with open(args.terms, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    if rows:
        headers = rows[0]
        try:
            from_col = headers.index(args.from_lang)
            to_col = headers.index(args.to_lang)
            for row in rows[1:]:
                if len(row) > max(from_col, to_col) and row[from_col]:
                    terms_dict[row[from_col]] = row[to_col]
        except ValueError as e:
            print(f"Warning: {e} in terms TSV")

client = LLMClient(model=args.model, think=(not args.no_think))
console = Console()


class ConsoleStream:
    """Rich console wrapper passed to generate_with_schema's file= parameter.
    Buffers by line and forwards to console.print()."""

    def __init__(self, console: Console):
        self._console = console
        self._buf = ""

    def write(self, text: str) -> None:
        self._buf += text
        while "\n" in self._buf:
            line, self._buf = self._buf.split("\n", 1)
            self._console.print(line, highlight=False)

    def flush(self) -> None:
        pass  # Ignore per-token flush; remaining content is output in end()

    def end(self) -> None:
        if self._buf.strip():
            self._console.print(self._buf, highlight=False)
            self._buf = ""


stream = ConsoleStream(console)
context_history = []
results = []


def _fmt_elapsed(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}"


class MofNParenColumn(ProgressColumn):
    """Column that displays line progress in (xx/xx) format."""

    def render(self, task) -> Text:
        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        return Text(f"({completed}/{total})", style="progress.download")


class LangMofNColumn(ProgressColumn):
    """Column that displays language progress in (xx/xx) format."""

    def render(self, task) -> Text:
        if not args.lang_total:
            return Text("")
        return Text(f"({args.lang_index}/{args.lang_total})", style="progress.download")


class BatchTimeColumn(ProgressColumn):
    """Column that displays the total batch elapsed time."""

    def render(self, task) -> Text:
        if not args.batch_start:
            return Text(_fmt_elapsed(task.elapsed or 0), style="progress.elapsed")
        return Text(_fmt_elapsed(time.time() - args.batch_start), style="progress.elapsed")


def desc() -> str:
    return f"{to_code}: {args.to_lang}"


with Progress(
    SpinnerColumn(),
    TextColumn("[bold cyan]{task.description}"),
    LangMofNColumn(),
    BatchTimeColumn(),
    TextColumn("|"),
    BarColumn(),
    TaskProgressColumn(),
    MofNParenColumn(),
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task(desc(), total=len(orig_lines))

    for i, (orig_line, tr_line) in enumerate(zip(orig_lines, tr_lines)):
        orig_line = orig_line.strip()
        tr_line = tr_line.strip()

        progress.update(task, completed=i, description=desc())

        if not orig_line or ":" not in orig_line:
            results.append(tr_line)
            continue

        console.rule(f"[dim]{i+1}/{len(orig_lines)}[/dim]")

        table = Table(show_header=False, expand=True, border_style="green")
        table.add_column()
        table.add_row(orig_line, end_section=True)
        table.add_row(tr_line)
        console.print(table)

        speaker, text = orig_line.split(":", 1)
        speaker = speaker.strip()
        text = text.strip()
        translated_speaker = terms_dict.get(speaker, speaker)

        if ":" in tr_line:
            tr_speaker, tr_text = tr_line.split(":", 1)
            tr_text = tr_text.strip()
        else:
            tr_text = tr_line

        chat_history = []
        chat_history.append({
            "role": "system",
            "content": f"You are an expert {args.to_lang} reviewer. Your task is to review and refine a {args.from_lang} to {args.to_lang} translation.",
        })

        if context_history and args.history > 0:
            context_prompt = "Previous context:\n\n"
            for ctx in context_history[-args.history:]:
                context_prompt += f"Original: {ctx['original']}\nTranslation: {ctx['translation']}\n\n"
            chat_history.append({"role": "user", "content": context_prompt.strip()})
            chat_history.append({"role": "assistant", "content": "Understood. I will use this context for consistency."})

        # Prompt 1: Analysis
        prompt1 = (
            f"Original {args.from_lang} text:\n{text}\n\n"
            f"Base {args.to_lang} translation:\n{tr_text}\n\n"
            f"Please analyze this translation. Point out any literal translations, interference from other languages, "
            f"unnatural phrasing, or grammar issues. If it's perfect, just say 'No issues'."
        )
        chat_history.append({"role": "user", "content": prompt1})
        analysis = client.call(chat_history, file=stream)
        stream.end()
        chat_history.append({"role": "assistant", "content": analysis})

        if "No issues" in analysis or "no issues" in analysis.lower():
            improved_tr = tr_text
        else:
            # Prompt 2: Refinement
            prompt2 = (
                f"Now, provide the improved {args.to_lang} translation for the original text based on your analysis. "
                f"Output ONLY the improved translation text. Do not include the speaker name '{speaker}:', quotes, or any explanations."
            )
            chat_history.append({"role": "user", "content": prompt2})

            improved_tr = client.call(chat_history, file=None)
            improved_tr = improved_tr.strip()

            if improved_tr.startswith('"') and improved_tr.endswith('"'):
                improved_tr = improved_tr[1:-1].strip()

        console.print(Panel(f"{translated_speaker}: {improved_tr}", title="Refined", border_style="cyan"))

        results.append(f"{translated_speaker}: {improved_tr}")
        context_history.append({
            "original": orig_line,
            "translation": f"{translated_speaker}: {improved_tr}",
        })

    progress.update(task, completed=len(orig_lines), description=desc())

with open(args.output, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")

console.print(f"\n[bold green]Review complete.[/bold green] Saved to {args.output}")
