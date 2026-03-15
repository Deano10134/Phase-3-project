"""Alembic environment, wired to task_manager_cli.lib.db.models.Base.

This uses the project's `get_engine()` when running migrations online so
the same database URL selection logic is respected.
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_target_metadata():
    # import the project's metadata
    from task_manager_cli.lib.db import models

    return models.Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_target_metadata(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Prefer project engine if available
    try:
        from task_manager_cli.lib.db.session import get_engine

        engine = get_engine()
    except Exception:
        engine = None

    if engine is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    else:
        connectable = engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=get_target_metadata())

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
