"""CLI implemented with click."""
import click

from task_manager_cli.database import get_engine, get_session
from task_manager_cli.models.task import Task


@click.group()
def cli():
    """Task Manager CLI"""


@cli.command()
@click.argument("name", required=False)
def noop(name):
    """A no-op command for smoke testing."""
    click.echo(f"noop {name or ''}")


@cli.command("list-tasks")
def list_tasks():
    """Query tasks from the database and print CLI-friendly output."""
    engine = get_engine()
    session = get_session(engine)

    tasks = session.query(Task).order_by(Task.created_at).all()
    if not tasks:
        click.echo("No tasks found.")
        return

    # Build a list of dicts representing tasks (uses dict and list)
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

    # Print as human-friendly lines
    for d in task_dicts:
        click.echo(f"[{d['id']}] {d['title']} - created: {d['created']} - age_days: {d['age_days']}")

    # Also demonstrate tuples: create a tuple summary (total, completed)
    total = len(task_dicts)
    completed = sum(1 for d in task_dicts if d['completed'])
    summary_tuple = (total, completed)
    click.echo(f"Summary (total, completed): {summary_tuple}")

    # And a dict mapping status to a tuple of task ids
    status_map = {
        "completed": tuple(d['id'] for d in task_dicts if d['completed']),
        "pending": tuple(d['id'] for d in task_dicts if not d['completed']),
    }
    click.echo(f"Status map: {status_map}")


@cli.command("show-summary")
def show_summary():
    """Show a tuple summary of tasks: (total, completed)."""
    engine = get_engine()
    session = get_session(engine)
    total = session.query(Task).count()
    completed = session.query(Task).filter(Task.completed.is_(True)).count()
    summary = (total, completed)
    click.echo(f"Task summary: {summary}")


@cli.command("export-tasks")
def export_tasks():
    """Export tasks as a list of tuples (id, title, completed)."""
    engine = get_engine()
    session = get_session(engine)
    tasks = session.query(Task).order_by(Task.id).all()
    tuples = [(t.id, t.title, bool(t.completed)) for t in tasks]
    # Print each tuple on its own line
    for tup in tuples:
        click.echo(str(tup))


def main(argv=None):
    # Use click's programmatic invocation entry so different click versions work
    return cli.main(args=argv)
