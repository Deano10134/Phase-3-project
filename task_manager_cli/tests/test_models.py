def test_models_import():
    from task_manager_cli.models import base
    assert hasattr(base, "Base")
