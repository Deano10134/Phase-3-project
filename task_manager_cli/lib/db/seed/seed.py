"""Seed script to populate initial data (demo)."""
from task_manager_cli.database import get_engine, get_session
from task_manager_cli.models.base import Base
from task_manager_cli.models.user import User
from task_manager_cli.models.project import Project
from task_manager_cli.models.task import Task
import datetime
import os


def seed(engine_or_url: str | None = None):
    """Create tables and insert demo data.

    `engine_or_url` may be an SQLAlchemy Engine, a database URL string, or None.
    If None, the package `get_engine()` is used (which reads settings or env).
    """
    # Resolve engine
    engine = None
    if isinstance(engine_or_url, str):
        engine = get_engine(engine_or_url)
    elif engine_or_url is None:
        engine = get_engine()
    else:
        # assume it's an Engine-like object
        engine = engine_or_url

    Base.metadata.create_all(engine)
    session = get_session(engine)

    # create sample data
    u = User(username="alice", email="alice@example.com")
    p = Project(name="Demo Project", description="A sample project")
    t1 = Task(title="Write tests", description="Add tests for CLI", completed=False, created_at=datetime.datetime.utcnow())
    t2 = Task(title="Fix bugs", description="Fix reported issues", completed=True, created_at=datetime.datetime.utcnow())

    session.add(u)
    session.add(p)
    session.add_all([t1, t2])
    session.commit()


if __name__ == "__main__":
    seed()
