# Task Manager

A small command-line task manager written in Python. Tasks are stored in a local JSON file, and an optional OpenAI-powered feature can break a complex task down into simple subtasks.

## Features

- Add, list, complete and delete tasks from an interactive menu
- Tasks persist between runs in `tasks.json`
- **Add complex task**: describe a larger goal and the app asks OpenAI (`gpt-4o-mini`) to split it into 3-5 actionable subtasks, each added as its own task

## Requirements

- Python 3.10 or newer (the menu uses `match` statements)
- An OpenAI API key, only needed for the "Add complex task" option

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### OpenAI API key (optional)

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-key-here
```

`.env` is git-ignored. Without a key, options 1 and 3-6 still work; option 2 prints an error.

## Usage

```bash
python main.py
```

```
--- Intelligent Task Manager ---
1. Add Task
2. Add complex task
3. List Tasks
4. Complete Task
5. Delete Task
6. Exit
```

Example list output:

```
[ ] #1: Buy groceries
[✓] #2: Write README
```

Complete and delete operate on the task ID shown in the list.

## Running the tests

```bash
python -m unittest test_task_manager -v
```

The tests use a temporary directory for the JSON file, so your real `tasks.json` is not touched.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Interactive menu and entry point |
| `task_manager.py` | `Task` and `TaskManager` classes, JSON persistence |
| `ai_service.py` | OpenAI client and `create_simple_task` subtask generation |
| `test_task_manager.py` | Unit tests for `Task` and `TaskManager` |
| `requirements.txt` | Pinned Python dependencies |
| `tasks.json` | Task data, created on first save (git-ignored) |

## How it works

- `TaskManager` loads `tasks.json` on startup and rewrites it after every add, complete or delete. A missing file means an empty list.
- IDs increment from the highest existing ID, so after a restart the next ID continues from the last task in the file.
- `create_simple_task` sends the description to OpenAI, parses lines starting with `-` into subtasks, and returns a single `Error: ...` entry if the key is missing, the request fails, or nothing usable comes back.

## Known limitations

- If the highest-numbered task is deleted and the app is restarted, that ID is reused.
- A corrupt `tasks.json` raises an error on startup rather than being recovered.
