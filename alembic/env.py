import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# make package importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
try:
    fileConfig(config.config_file_name)
except Exception:
    pass

from task_manager_cli.models.base import Base

target_metadata = Base.metadata


def get_url():
    # attempt to read url from package settings
    try:
        import importlib.resources as resources

        content = resources.read_text("task_manager_cli.config", "settings.toml")
        try:
            import tomli

            cfg = tomli.loads(content)
            url = cfg.get("database", {}).get("url")
            if url:
                return url
        except Exception:
            pass
    except Exception:
        pass
    return os.environ.get("DATABASE_URL", "sqlite:///task_manager.db")


def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # use engine from config but override url with settings if present
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    from sqlalchemy import create_engine
    engine = create_engine(get_url(), poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
