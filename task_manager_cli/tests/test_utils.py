def test_utils_importable():
    import task_manager_cli.utils as utils

    assert hasattr(utils, "simple_priority_sort") or hasattr(utils, "human_duration")
