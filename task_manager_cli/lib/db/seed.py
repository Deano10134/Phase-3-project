"""Seed helpers (merged).

Provide a simple `seed()` entrypoint that creates tables and inserts
demo data. Uses the `session` helpers available under `lib/db`.
"""
from task_manager_cli.lib.db.session import get_engine, get_session
from task_manager_cli.lib.db.models import Base, User, Project, Task
import datetime


def seed(engine_or_url: str | None = None):
    """Create tables and insert demo data.

    `engine_or_url` may be an SQLAlchemy Engine, a database URL string, or None.
    If None, the package `get_engine()` is used.
    """
    engine = None
    if isinstance(engine_or_url, str):
        engine = get_engine(engine_or_url)
    elif engine_or_url is None:
        engine = get_engine()
    else:
        engine = engine_or_url

    Base.metadata.create_all(engine)
    session = get_session(engine)

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
