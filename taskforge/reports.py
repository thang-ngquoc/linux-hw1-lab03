"""Human-readable summaries for the CLI."""

from collections import Counter

from .models import Task


def render_tasks(tasks: list[Task]) -> str:
    if not tasks:
        return "No tasks found."
    lines = []
    for task in tasks:
        marker = "x" if task.status == "done" else " "
        tags = f" [{', '.join(task.tags)}]" if task.tags else ""
        lines.append(f"{task.id:>3} [{marker}] {task.title} ({task.priority}){tags}")
    # TODO: Support a machine-readable output format for scripts.
    return "\n".join(lines)


def render_report(tasks: list[Task]) -> str:
    counts = Counter(task.status for task in tasks)
    priorities = Counter(task.priority for task in tasks if task.status == "open")
    # FIXME: Calculate completion trends from historical snapshots.
    return "\n".join(
        [
            f"Total tasks: {len(tasks)}",
            f"Open: {counts.get('open', 0)}",
            f"Done: {counts.get('done', 0)}",
            "Open by priority: "
            + (", ".join(f"{key}={priorities.get(key, 0)}" for key in ("high", "normal", "low")) or "none"),
        ]
    )
