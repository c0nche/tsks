import json
from .models import Task, TreeNode
from datetime import datetime, date
from platformdirs import user_data_dir
from pathlib import Path

DATA_FILE = Path(user_data_dir("Tsks", ensure_exists=True)) / "tasks.json"

def get_task(task_id: str, tasks: list[Task]) -> Task:
    for task in tasks:
        if task.task_id == task_id:
            return task
    raise ValueError(f'Task {task_id} is not found')

def get_subtasks(task_id: str, tasks: list[Task]) -> list[Task]:
    return [task for task in tasks if task.parent == task_id]

def get_today_todo(tasks: list[Task]) -> list[Task]:
    return [task for task in tasks 
            if task.is_subtask and not task.done and
            (task.deadline is None or task.deadline <= date.today())]

def build_tree(tid: str, tasks: list[Task]) -> TreeNode:
    node = TreeNode(get_task(tid))
    for sub in get_subtasks(tid, tasks):
        node.subtasks.append(build_tree(sub.task_id))
    return node

def get_task_tree(subtask_id: str, tasks: list[Task]) -> TreeNode:
    def get_main_task(tid: str) -> str:
        t = get_task(tid, tasks)
        if t.parent == None:
            return t.task_id
        return get_main_task(t.parent)
    main_task = get_main_task(subtask_id)
    return build_tree(main_task, tasks)

def get_task_forest(tasks: list[Task]) -> list[TreeNode]:
    forest = []
    for task in tasks:
        if task.parent == None:
            forest.append(build_tree(task.task_id, tasks))
    return forest

def update_parent(task_id: str, tasks: list[Task]) -> list[Task]:
    for sub in get_subtasks(task_id, tasks):
        if not sub.done:
            return tasks[:]
    return complete_task(task_id, tasks)

def complete_task(task_id: str, tasks: list[Task]) -> list[Task]:
    task = get_task(task_id, tasks)
    if task.is_task:
        if any(not sub.done for sub in get_subtasks(task_id, tasks)):
            return tasks[:]
    task.done = True;
    task.completed_at = date.today()
    if task.parent is not None:
        return update_parent(task.parent, tasks)
    return tasks[:]

def delete_task(task_id: str, tasks: list[Task]) -> list[Task]:
    to_del = set()
    def collect(tid):
        to_del.add(tid)
        for sub in get_subtasks(tid, tasks):
            collect(sub.task_id)
    collect(task_id)
    return [t for t in tasks if t.task_id not in to_del]

def add_task(new_task: Task, tasks: list[Task]) -> list[Task]:
    return tasks + [new_task]

def save(tasks: list[Task]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2, ensure_ascii=False)

def load() -> list[Task]:
    if not DATA_FILE.exists():
        return []
    else:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return[Task.from_dict(item) for item in data]
