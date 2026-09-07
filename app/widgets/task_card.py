from textual.app import ComposeResult
from textual.widgets import Static, Label
from ..services import get_task
from ..models import Task

class TaskCard(Static):
    DEFAULT_CSS = """
    TaskCard {
        layout: vertical;
        width: 30;
        height: auto;
        padding: 1;
        border: solid $panel;
        margin: 1 2;
    }

    TaskCard:focus {
        border: solid $accent;
    }

    #title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    #subtask {
        color: $warning;
        text-style: none;
        margin-top: 1;
    }
    """
    can_focus = True

    def __init__(self, task: Task):
        super().__init__()
        self.task_data = task

    def compose(self) -> ComposeResult:
        yield Label(self.task_data.title, id='title')
        yield Label(self.task_data.category, id='category')
        if self.task_data.parent:
            yield Label("subtask of " + get_task(self.task_data.parent, self.app.tasks).title, id='subtask')
