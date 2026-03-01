"""Compatibility shim exposing ORM models at `task_manager_cli.models`.

Re-exports `Base` (and other model names) from `lib/db/models.py` so
imports like `import task_manager_cli.models as models` work unchanged.
"""
from task_manager_cli.lib.db.models import Base, User, Project, Task, TimeLog, RecurringTask

__all__ = ["Base", "User", "Project", "Task", "TimeLog", "RecurringTask"]
