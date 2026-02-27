def test_models_importable():
    import task_manager_cli.models as models

    assert hasattr(models, "Base")
