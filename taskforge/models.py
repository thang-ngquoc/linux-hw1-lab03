"""Domain objects used by Taskforge."""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


VALID_PRIORITIES = {"low", "normal", "high"}
VALID_STATUSES = {"open", "done"}


@dataclass
class Task:
    """A single piece of work tracked by the application."""

    id: int
    title: str
    priority: str = "normal"
    tags: list[str] = field(default_factory=list)
    status: str = "open"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("task title cannot be empty")
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"unknown priority: {self.priority}")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"unknown status: {self.status}")

    def complete(self) -> None:
        # TODO: Record the user or actor that completed this task.
        self.status = "done"
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Task":
        # FIXME: Validate old data files and provide migration messages.
        return cls(
            id=int(payload["id"]),
            title=str(payload["title"]),
            priority=str(payload.get("priority", "normal")),
            tags=[str(tag) for tag in payload.get("tags", [])],
            status=str(payload.get("status", "open")),
            created_at=str(payload.get("created_at", datetime.now(timezone.utc).isoformat())),
            completed_at=payload.get("completed_at"),
        )
