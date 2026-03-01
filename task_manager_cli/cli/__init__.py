"""Compatibility shim for `task_manager_cli.cli`.

Re-export the `main` entrypoint from `lib/cli.py` so existing imports
(`from task_manager_cli.cli import main`) continue to work.
"""
from task_manager_cli.lib.cli import main, cli

__all__ = ["main", "cli"]
