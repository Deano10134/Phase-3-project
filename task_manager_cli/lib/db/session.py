"""Simple SQLAlchemy session factory.

This reads `config/settings.toml` if present (using `tomli`) to obtain
`database.url`. `tomli` is imported only when needed.
"""
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(url: Optional[str] = None):
    if url is None:
        # prefer explicit environment variable when present (useful for tests)
        url = os.environ.get("DATABASE_URL")
        if not url:
            try:
                import importlib.resources as resources

                # read settings file from package resources
                content = resources.read_text("task_manager_cli.config", "settings.toml")
                try:
                    import tomli

                    cfg = tomli.loads(content)
                    url = cfg.get("database", {}).get("url")
                except Exception:
                    url = None
            except Exception:
                url = None

    if not url:
        url = "sqlite:///task_manager.db"

    return create_engine(url, echo=False, future=True)


def get_session(engine=None):
    if engine is None:
        engine = get_engine()
    Session = sessionmaker(bind=engine, future=True)
    return Session()
