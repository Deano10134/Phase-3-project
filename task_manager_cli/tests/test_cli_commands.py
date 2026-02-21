import os
from click.testing import CliRunner
from task_manager_cli.cli import commands
from task_manager_cli import seed as seed_module


def test_cli_list_tasks_and_summary(tmp_path, monkeypatch):
    db_file = tmp_path / "test_tasks.db"
    db_url = f"sqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", db_url)

    # seed data
    seed_module.seed()

    runner = CliRunner()
    res = runner.invoke(commands.cli, ["list-tasks"])
    assert res.exit_code == 0
    assert "Write tests" in res.output
    assert "Fix bugs" in res.output

    # summary tuple should be printed
    res2 = runner.invoke(commands.cli, ["show-summary"])
    assert res2.exit_code == 0
    assert "Task summary:" in res2.output


def test_export_tasks_outputs_tuples(tmp_path, monkeypatch):
    db_file = tmp_path / "test_tasks2.db"
    db_url = f"sqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", db_url)

    seed_module.seed()
    runner = CliRunner()
    res = runner.invoke(commands.cli, ["export-tasks"])
    assert res.exit_code == 0
    # Expect at least one line that looks like a tuple: (id, title, completed)
    assert "(" in res.output and ")" in res.output
