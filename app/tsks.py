from textual.app import App
from textual.reactive import reactive
from .services import load, save
from .models import Task

from .screens.TodayScreen import TodayScreen

class Tsks(App):
    tasks = reactive([], init=False)
    
    def on_mount(self) -> None:
        self.tasks = load()
        self.push_screen(TodayScreen())

    def watch_tasks(self, new_tasks):
       save(new_tasks) 

if __name__ == "__main__":
    app = Tsks()
    app.run()
