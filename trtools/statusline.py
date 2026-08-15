import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (Progress, ProgressColumn, SpinnerColumn, TextColumn,
                           BarColumn, TaskProgressColumn, TimeElapsedColumn)
from rich.text import Text
from .llm import ConsoleStream


def _fmt_elapsed(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}"


class StatusLine:
    def __init__(self, label=None, start=None, index=None, count=None):
        self.console = Console()
        self.stream = ConsoleStream(self.console)
        self._label = label
        self._start = start
        self._index = index
        self._count = count

    def write(self, text: str) -> None:
        self.stream.write(text)

    def rule(self, text: str) -> None:
        self.console.rule(f"[dim]{text}[/dim]")

    def show_pair(self, orig: str, tr: str) -> None:
        table = Table(show_header=False, expand=True, border_style="green")
        table.add_column()
        table.add_row(orig, end_section=True)
        table.add_row(tr)
        self.console.print(table)

    def show_panel(self, text: str, title: str) -> None:
        self.console.print(Panel(text, title=title, border_style="cyan"))

    def progress(self, total: int, start: int = 0) -> "_ProgressContext":
        return _ProgressContext(self.console, self._label, self._start, total, start,
                                 index=self._index, count=self._count)


class _ProgressContext:
    def __init__(self, console, label, start, total, completed=0, index=None, count=None):
        self._total = total
        self._completed = completed

        class MofNParenColumn(ProgressColumn):
            def render(self, task) -> Text:
                completed = int(task.completed)
                n = int(task.total) if task.total is not None else "?"
                return Text(f"({completed}/{n})", style="progress.download")

        class LangMofNColumn(ProgressColumn):
            def render(self, task) -> Text:
                return Text(f"({index}/{count})", style="progress.download")

        class BatchTimeColumn(ProgressColumn):
            def render(self, task) -> Text:
                return Text(_fmt_elapsed(time.time() - start), style="progress.elapsed")

        columns = [SpinnerColumn()]
        if label:
            columns.append(TextColumn("[bold cyan]{task.description}"))
        if count:
            columns.append(LangMofNColumn())
        if start is not None:
            columns.append(BatchTimeColumn())
        if label or start is not None or count:
            columns.append(TextColumn("|"))
        columns += [BarColumn(), TaskProgressColumn(), MofNParenColumn(), TimeElapsedColumn()]

        self._progress = Progress(*columns, console=console)
        self._label = label
        self._task = None

    def __enter__(self):
        self._progress.__enter__()
        self._task = self._progress.add_task(self._label or "", total=self._total, completed=self._completed)
        return self

    def __exit__(self, *args):
        return self._progress.__exit__(*args)

    def update(self, completed: int) -> None:
        self._progress.update(self._task, completed=completed)
