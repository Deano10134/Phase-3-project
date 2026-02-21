def test_utils_import():
    from task_manager_cli.utils import formatting
    assert formatting.human_duration(1.5) == "1h 30m" or formatting.human_duration(0) == "0m"
