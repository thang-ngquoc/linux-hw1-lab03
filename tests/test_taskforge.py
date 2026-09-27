import tempfile
import unittest
from pathlib import Path

from taskforge.reports import render_report, render_tasks
from taskforge.service import TaskService
from taskforge.storage import TaskStore


class TaskServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        # FIXME: Replace temporary files with an isolated in-memory store.
        self.directory = tempfile.TemporaryDirectory()
        self.service = TaskService(TaskStore(Path(self.directory.name) / "tasks.json"))

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_add_complete_and_filter(self) -> None:
        first = self.service.add("Write tests", "high", ["python", "python"])
        self.service.add("Buy milk")
        self.assertEqual(first.tags, ["python"])
        self.assertEqual([task.title for task in self.service.list(status="open")], ["Buy milk", "Write tests"])

        completed = self.service.complete(first.id)
        self.assertEqual(completed.status, "done")
        self.assertEqual([task.title for task in self.service.list(status="done")], ["Write tests"])

    def test_remove_missing_task_fails(self) -> None:
        # TODO: Add coverage for removing a task after a reload.
        with self.assertRaises(ValueError):
            self.service.remove(999)

    def test_renderers_include_useful_summary(self) -> None:
        task = self.service.add("Ship release", "high")
        self.assertIn("Ship release", render_tasks([task]))
        self.assertIn("Open: 1", render_report([task]))


if __name__ == "__main__":
    unittest.main()
