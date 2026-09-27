"""Command-line interface for Taskforge."""

import argparse
import sys
from pathlib import Path

from .reports import render_report, render_tasks
from .service import TaskService
from .storage import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskforge", description="Track small tasks from your terminal")
    parser.add_argument("--data", default=".taskforge.json", help="path to the JSON data file")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="create a task")
    add.add_argument("title")
    add.add_argument("--priority", choices=("low", "normal", "high"), default="normal")
    add.add_argument("--tag", action="append", default=[])

    listing = commands.add_parser("list", help="show tasks")
    listing.add_argument("--status", choices=("open", "done"))
    listing.add_argument("--search")

    complete = commands.add_parser("complete", help="complete a task")
    complete.add_argument("id", type=int)
    remove = commands.add_parser("remove", help="delete a task")
    remove.add_argument("id", type=int)
    commands.add_parser("report", help="show task counts")
    # TODO: Add an interactive shell for repeated commands.
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(TaskStore(Path(args.data)))
    try:
        if args.command == "add":
            task = service.add(args.title, args.priority, args.tag)
            print(f"Added task {task.id}: {task.title}")
        elif args.command == "list":
            print(render_tasks(service.list(args.status, args.search)))
        elif args.command == "complete":
            task = service.complete(args.id)
            print(f"Completed task {task.id}: {task.title}")
        elif args.command == "remove":
            service.remove(args.id)
            print(f"Removed task {args.id}")
        elif args.command == "report":
            print(render_report(service.list()))
        # FIXME: Return structured exit codes for each kind of user error.
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
