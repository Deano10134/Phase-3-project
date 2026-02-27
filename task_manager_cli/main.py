"""Entrypoint for the task manager CLI."""
from task_manager_cli.cli.commands import main


def run(argv=None):
    return main(argv=argv)


if __name__ == "__main__":
    run()
