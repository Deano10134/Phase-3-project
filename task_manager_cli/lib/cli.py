"""Consolidated CLI implementation.

This file merges the previous `commands.py` and `services.py` logic
into a single module for the `lib` layout.
"""
import click
from typing import List, Dict, Optional

from task_manager_cli.lib.db.session import get_engine, get_session
from task_manager_cli.lib.db.models import Task


@click.group()
def cli():
    """Task Manager CLI"""


@cli.command()
@click.argument("name", required=False)
def noop(name):
    """A no-op command for smoke testing."""
    click.echo(f"noop {name or ''}")


@cli.command("list-tasks")
def list_tasks_cmd():
    """Query tasks from the database and print CLI-friendly output."""
    engine = get_engine()
    session = get_session(engine)

    tasks = session.query(Task).order_by(Task.created_at).all()
    if not tasks:
        click.echo("No tasks found.")
        return

    task_dicts = []
    for t in tasks:
        age = getattr(t, "age_days", None)
        created = t.created_at.isoformat() if t.created_at else "-"
        task_dict = {
            "id": t.id,
            "title": t.title,
            "created": created,
            "age_days": int(age) if age is not None else None,
            "completed": bool(getattr(t, "completed", False)),
        }
        task_dicts.append(task_dict)

    for d in task_dicts:
        click.echo(f"[{d['id']}] {d['title']} - created: {d['created']} - age_days: {d['age_days']}")


@cli.command("show-summary")
def show_summary_cmd():
    """Show a tuple summary of tasks: (total, completed)."""
    engine = get_engine()
    session = get_session(engine)
    total = session.query(Task).count()
    completed = session.query(Task).filter(Task.completed.is_(True)).count()
    summary = (total, completed)
    click.echo(f"Task summary: {summary}")


@cli.command("export-tasks")
def export_tasks_cmd():
    """Export tasks as a list of tuples (id, title, completed)."""
    engine = get_engine()
    session = get_session(engine)
    tasks = session.query(Task).order_by(Task.id).all()
    tuples = [(t.id, t.title, bool(t.completed)) for t in tasks]
    for tup in tuples:
        click.echo(str(tup))


def main(argv=None):
    return cli.main(args=argv)


# --- Service helpers (previously in services.py) ---


def list_tasks(engine=None) -> List[Dict]:
    engine = engine or get_engine()
    session = get_session(engine)
    try:
        tasks = session.query(Task).order_by(Task.created_at).all()
        result = []
        for t in tasks:
            result.append(
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": bool(t.completed),
                    "created": t.created_at.isoformat() if t.created_at else None,
                    "age_days": int(t.age_days) if t.age_days is not None else None,
                }
            )
        return result
    finally:
        session.close()


def get_task(task_id: int, engine=None) -> Optional[Task]:
    engine = engine or get_engine()
    session = get_session(engine)
    try:
        return session.query(Task).filter(Task.id == task_id).one_or_none()
    finally:
        session.close()


def create_task(title: str, description: Optional[str] = None, engine=None) -> Dict:
    engine = engine or get_engine()
    session = get_session(engine)
    try:
        task = Task(title=title.strip(), description=(description or None))
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": bool(task.completed),
            "created": task.created_at.isoformat() if task.created_at else None,
        }
    finally:
        session.close()


def complete_task(task_id: int, engine=None) -> bool:
    engine = engine or get_engine()
    session = get_session(engine)
    try:
        task = session.query(Task).filter(Task.id == task_id).one_or_none()
        if task is None:
            return False
        task.completed = True
        session.add(task)
        session.commit()
        return True
    finally:
        session.close()


def delete_task(task_id: int, engine=None) -> bool:
    engine = engine or get_engine()
    session = get_session(engine)
    try:
        task = session.query(Task).filter(Task.id == task_id).one_or_none()
        if task is None:
            return False
        session.delete(task)
        session.commit()
        return True
    finally:
        session.close()
