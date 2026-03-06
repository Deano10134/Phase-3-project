"""Entrypoint for the task manager CLI."""
from task_manager_cli.lib.cli.main import cli


def run():
    return cli()


if __name__ == "__main__":
    run()
