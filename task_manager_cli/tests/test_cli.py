def test_cli_smoke():
    from task_manager_cli.cli import main

    # main should be callable
    assert callable(main)
