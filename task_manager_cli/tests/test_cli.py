def test_cli_import():
    from task_manager_cli.cli import commands
    assert hasattr(commands, "main")
