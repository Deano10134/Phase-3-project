"""Entrypoint for the task manager CLI."""
from task_manager_cli.cli.commands import main


def run():
    return main()


if __name__ == "__main__":
    run()
