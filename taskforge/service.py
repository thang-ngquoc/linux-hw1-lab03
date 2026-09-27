"""Application operations for creating and querying tasks."""

from .models import Task, VALID_PRIORITIES
from .storage import TaskStore


class TaskService:
    def __init__(self, store: TaskStore) -> None:
        self.store = store

    def add(self, title: str, priority: str = "normal", tags: list[str] | None = None) -> Task:
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}")
        tasks = self.store.load()
        next_id = max((task.id for task in tasks), default=0) + 1
        task = Task(next_id, title.strip(), priority, sorted(set(tags or [])))
        tasks.append(task)
        self.store.save(tasks)
        # TODO: Emit an event when integrations are added.
        return task

    def complete(self, task_id: int) -> Task:
        tasks = self.store.load()
        task = self._find(tasks, task_id)
        if task.status == "done":
            raise ValueError(f"task {task_id} is already complete")
        task.complete()
        self.store.save(tasks)
        return task

    def list(self, status: str | None = None, query: str | None = None) -> list[Task]:
        tasks = self.store.load()
        if status:
            tasks = [task for task in tasks if task.status == status]
        if query:
            needle = query.casefold()
            tasks = [task for task in tasks if needle in task.title.casefold()]
        # FIXME: Add sorting by due date when due dates become part of Task.
        return sorted(tasks, key=lambda task: (task.status == "done", -task.id))

    def remove(self, task_id: int) -> None:
        tasks = self.store.load()
        remaining = [task for task in tasks if task.id != task_id]
        if len(remaining) == len(tasks):
            raise ValueError(f"task {task_id} was not found")
        self.store.save(remaining)
        # TODO: Add a recycle bin instead of deleting immediately.

    @staticmethod
    def _find(tasks: list[Task], task_id: int) -> Task:
        for task in tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"task {task_id} was not found")
