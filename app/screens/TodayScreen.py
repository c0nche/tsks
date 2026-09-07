from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer
from textual.containers import VerticalScroll, Horizontal
from textual.events import Resize

from ..widgets.task_card import TaskCard
from ..services import get_today_todo, complete_task
from ..models import Task


class TodayScreen(Screen):
    BINDINGS = [
        ("h", "focus_left", "focus left"),
        ("k", "focus_up", "focus up"),
        ("j", "focus_down", "focus down"),
        ("l", "focus_right", "focus right"),
        ("enter", "complete_focused", "complete task")
    ]

    CARD_WIDTH = 32

    def __init__(self):
        super().__init__()
        self.cards = []
        self.focus_id = 0
        self.cols = 1

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="grid")
        yield Footer()
    
    def on_mount(self):
        self.refresh_grid()

    def on_resize(self, event: Resize):
        self.refresh_grid()

    def refresh_grid(self):
        today_tasks = get_today_todo(self.app.tasks)
        grid = self.query_one("#grid", VerticalScroll)
        grid.remove_children()
        
        self.cards = []
        self.cols = max(1, self.size.width // self.CARD_WIDTH)
        if not today_tasks:
            self.focus_id = -1
            return
        
        row = Horizontal()
        grid.mount(row)
        counter = self.cols
        for task in today_tasks:
            if counter == 0:
                counter = self.cols
                row = Horizontal()
                grid.mount(row)
            counter -= 1
            card = TaskCard(task)
            self.cards.append(card)
            row.mount(card)
        if self.focus_id >= len(self.cards) and self.cards:
            self.focus_id -= 1
        self.cards[self.focus_id].focus()

    def action_focus_left(self):
        if self.focus_id % self.cols != 0:
            self.focus_id -= 1
            self.cards[self.focus_id].focus()

    def action_focus_down(self):
        if self.focus_id + self.cols < len(self.cards):
            self.focus_id += self.cols
            self.cards[self.focus_id].focus()

    def action_focus_up(self):
        if self.focus_id >= self.cols:
            self.focus_id -= self.cols
            self.cards[self.focus_id].focus()

    def action_focus_right(self):
        if self.focus_id + 1 < len(self.cards) and (self.focus_id + 1) % self.cols != 0:
            self.focus_id += 1
            self.cards[self.focus_id].focus()

    def action_complete_focused(self):
        if not self.cards or self.focus_id >= len(self.cards):
            return

        card = self.cards[self.focus_id]
        new_tasks = complete_task(card.task_data.task_id, self.app.tasks)
        self.app.tasks = new_tasks
        self.app.mutate_reactive(type(self.app).tasks)
        self.refresh_grid()

