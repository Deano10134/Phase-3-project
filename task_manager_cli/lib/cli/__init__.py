"""CLI package exports.

Imports are lazy to avoid the double-execution RuntimeWarning that occurs
when `task_manager_cli.lib.cli.main` is run via `python -m` (Python loads
the package __init__ before executing the module as __main__, which would
cause eager imports to see the module twice).
"""
from __future__ import annotations
import sys as _sys


def cli(*args, **kwargs):
    # Guard: if main is already loaded as __main__, reuse it directly.
    mod = _sys.modules.get("task_manager_cli.lib.cli.main") or __import__(
        "task_manager_cli.lib.cli.main", fromlist=["cli"]
    )
    return mod.cli(*args, **kwargs)


def main(argv=None):
    mod = _sys.modules.get("task_manager_cli.lib.cli.main") or __import__(
        "task_manager_cli.lib.cli.main", fromlist=["main"]
    )
    return mod.main(argv)


__all__ = ["cli", "main"]
