"""JSON persistence for Taskforge."""

import json
from pathlib import Path
from typing import Any

from .models import Task


class TaskStore:
    """Load and save tasks in a small human-readable JSON document."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        if not self.path.read_text(encoding="utf-8").strip():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid task file: {self.path}") from exc
        if not isinstance(raw, list):
            raise ValueError("task file must contain a JSON list")
        # FIXME: Keep a backup before reading a file with an unfamiliar schema.
        return [Task.from_dict(item) for item in raw]

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload: list[dict[str, Any]] = [task.to_dict() for task in tasks]
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.path)
        # TODO: Add file locking for simultaneous CLI processes.
