import contextlib
import io
import json
import os
import tempfile
import unittest

from task_manager import Task, TaskManager


class TaskTests(unittest.TestCase):
    def test_defaults_to_not_completed(self):
        task = Task(1, "Write tests")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Write tests")
        self.assertFalse(task.completed)

    def test_str_pending(self):
        self.assertEqual(str(Task(1, "Write tests")), "[ ] #1: Write tests")

    def test_str_completed(self):
        self.assertEqual(str(Task(2, "Ship", True)), "[✓] #2: Ship")


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = os.path.join(self._tmp.name, "tasks.json")
        self._original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.path
        self.addCleanup(setattr, TaskManager, "FILENAME", self._original_filename)

    def _write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f)

    def _read(self):
        with open(self.path) as f:
            return json.load(f)

    def _run(self, func, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            func(*args)
        return buf.getvalue()

    # --- loading ---
    def test_starts_empty_when_file_missing(self):
        manager = TaskManager()
        self.assertEqual(manager._tasks, [])
        self.assertEqual(manager._next_id, 1)

    def test_loads_existing_tasks_and_continues_ids(self):
        self._write([
            {"id": 1, "description": "a", "completed": False},
            {"id": 5, "description": "b", "completed": True},
        ])
        manager = TaskManager()
        self.assertEqual([t.id for t in manager._tasks], [1, 5])
        self.assertTrue(manager._tasks[1].completed)
        self.assertEqual(manager._next_id, 6)

    def test_empty_file_list_resets_next_id(self):
        self._write([])
        manager = TaskManager()
        self.assertEqual(manager._tasks, [])
        self.assertEqual(manager._next_id, 1)

    def test_corrupt_file_raises(self):
        with open(self.path, "w") as f:
            f.write("not json")
        with self.assertRaises(json.JSONDecodeError):
            TaskManager()

    # --- add ---
    def test_add_task_assigns_incrementing_ids_and_persists(self):
        manager = TaskManager()
        out = self._run(manager.add_task, "first")
        self._run(manager.add_task, "second")
        self.assertIn("Task added: first", out)
        self.assertEqual(
            self._read(),
            [
                {"id": 1, "description": "first", "completed": False},
                {"id": 2, "description": "second", "completed": False},
            ],
        )

    def test_added_tasks_survive_reload(self):
        manager = TaskManager()
        self._run(manager.add_task, "persist me")
        reloaded = TaskManager()
        self.assertEqual(len(reloaded._tasks), 1)
        self.assertEqual(reloaded._tasks[0].description, "persist me")
        self.assertEqual(reloaded._next_id, 2)

    # --- list ---
    def test_list_tasks_empty(self):
        manager = TaskManager()
        self.assertEqual(self._run(manager.list_tasks).strip(), "No tasks pending.")

    def test_list_tasks_prints_each_task(self):
        manager = TaskManager()
        self._run(manager.add_task, "one")
        self._run(manager.add_task, "two")
        lines = self._run(manager.list_tasks).splitlines()
        self.assertEqual(lines, ["[ ] #1: one", "[ ] #2: two"])

    # --- complete ---
    def test_complete_task_marks_and_persists(self):
        manager = TaskManager()
        self._run(manager.add_task, "do it")
        out = self._run(manager.complete_task, 1)
        self.assertIn("Task completed: [✓] #1: do it", out)
        self.assertTrue(manager._tasks[0].completed)
        self.assertTrue(self._read()[0]["completed"])

    def test_complete_unknown_task(self):
        manager = TaskManager()
        out = self._run(manager.complete_task, 99)
        self.assertEqual(out.strip(), "Task not found #99.")

    # --- delete ---
    def test_delete_task_removes_and_persists(self):
        manager = TaskManager()
        self._run(manager.add_task, "keep")
        self._run(manager.add_task, "drop")
        out = self._run(manager.delete_task, 2)
        self.assertIn("Task deleted: [ ] #2: drop", out)
        self.assertEqual([t.id for t in manager._tasks], [1])
        self.assertEqual([t["id"] for t in self._read()], [1])

    def test_delete_unknown_task(self):
        manager = TaskManager()
        out = self._run(manager.delete_task, 7)
        self.assertEqual(out.strip(), "Task not found #7.")

    def test_ids_not_reused_within_session_after_delete(self):
        manager = TaskManager()
        self._run(manager.add_task, "a")
        self._run(manager.add_task, "b")
        self._run(manager.delete_task, 2)
        self._run(manager.add_task, "c")
        self.assertEqual([t.id for t in manager._tasks], [1, 3])


if __name__ == "__main__":
    unittest.main()
