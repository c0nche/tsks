from enum import Enum
from __future__ import annotations
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import date


class TaskKind(Enum):
    TASK = "task"
    SUBTASK = "subtask"

@dataclass
class Task:
    task_id: str = field(default_factory=lambda: uuid4().hex)
    kind: TaskKind 
    parent: str | None = None
    title: str
    category: str
    desc_md: str = ""
    done: bool = False
    deadline: date | None = None
    
    @property
    def is_task(self):
        return TaskKind.TASK == self.kind 

    @property 
    def is_subtask(self):
        return TaskKind.SUBTASK == self.kind

    def to_dict(self):
        return data = {
            "task_id": self.task_id,
            "kind": self.kind.value,
            "parent": self.parent if self.parent else None,
            "title": self.title,
            "category": self.category,
            "desc_md": self.desc_md,
            "done": self.done,
            "deadline": self.deadline.isoformat() if self.deadline else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            task_id = data["task_id"],
            kind = TaskKind(data["kind"]),
            parent = data.get("parent"),
            title = data["title"],
            category = data["category"],
            desc_md = data.get("desc_md", ""),
            done = data.get("done", False),
            deadline = date.fromisoformat(data["deadline"]) if data.get("deadline") else None
        )


@dataclass
class TreeNode:
    task: Task
    subtasks: list[TreeNode]
