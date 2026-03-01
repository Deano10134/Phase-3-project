def test_models_importable():
    import task_manager_cli.lib.db.models as models

    assert hasattr(models, "Base")
