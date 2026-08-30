from rich.panel import Panel
from rich.table import Table
from rich.progress import (ProgressColumn, SpinnerColumn, BarColumn,
                           TaskProgressColumn, TimeElapsedColumn)
from rich.text import Text
from llm7shi.statusline import (StatusLine as _BaseStatusLine, ProgressContext,
                                ElapsedColumn, LabelColumn, MofNColumn, SeparatorColumn)


class MofNParenColumn(MofNColumn):
    """`(m/n)` — llm7shi's column in parentheses.

    Deriving rather than rewriting keeps the `remaining` field working, which is
    what makes llm7shi's retry countdown row count down instead of up.
    """

    def render(self, task) -> Text:
        return Text(f"({super().render(task).plain})", style="progress.download")


class LangMofNColumn(ProgressColumn):
    """`(index/count)` — position in the batch of languages, fixed for this bar."""

    def __init__(self, index, count):
        super().__init__()
        self._index = index
        self._count = count

    def render(self, task) -> Text:
        return Text(f"({self._index}/{self._count})", style="progress.download")


class StatusLine(_BaseStatusLine):
    def __init__(self, label=None, start=None, index=None, count=None, left_count=False):
        super().__init__()
        self._label = label
        self._start = start
        self._index = index
        self._count = count
        # When the progress itself represents the item count, place (m/n) on the left (right after the label)
        self._left_count = left_count

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
        return self.progress_context_class(self, total, start, self._label, self._start)


class _ProgressContext(ProgressContext):
    def columns(self) -> list[ProgressColumn]:
        # The layout differs from llm7shi's throughout — (m/n) is parenthesized and
        # sits right of the percentage unless it *is* the item count, the language
        # counter has no llm7shi counterpart, and the trailing clock is per task —
        # so this builds the whole list rather than editing super()'s.
        ui = self._status_line
        columns = [SpinnerColumn()]
        if self._label:
            columns.append(LabelColumn())
        if ui._count:
            columns.append(LangMofNColumn(ui._index, ui._count))
        elif ui._left_count:
            columns.append(MofNParenColumn())
        if self._started_at is not None:
            columns.append(ElapsedColumn(self._started_at))
        if len(columns) > 1:
            columns.append(SeparatorColumn())
        columns += [BarColumn(), TaskProgressColumn()]
        if not ui._left_count:
            columns.append(MofNParenColumn())
        return columns + [TimeElapsedColumn()]

    def update(self, completed: int, label: str = None) -> None:
        if label is None:
            super().update(completed)
        else:
            self._progress.update(self._task, completed=completed, description=label)


StatusLine.progress_context_class = _ProgressContext
