"""Top-level CLI adapter that delegates to task_manager_cli entrypoint."""

from task_manager_cli.main import run

__all__ = ["run"]
