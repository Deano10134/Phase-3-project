"""Query helpers that return CLI-usable lists/dicts using the ORM."""
from .db import get_session
from .models import User, Project, Task, TimeLog


def list_users():
    session = get_session()
    try:
        users = session.query(User).order_by(User.id).all()
        return [[u.id, u.username, u.email] for u in users]
    finally:
        session.close()


def list_projects():
    session = get_session()
    try:
        projects = session.query(Project).order_by(Project.id).all()
        return [[p.id, p.name, p.description] for p in projects]
    finally:
        session.close()


def list_tasks():
    session = get_session()
    try:
        tasks = session.query(Task).order_by(Task.id).all()
        table = []
        for t in tasks:
            table.append([
                t.id,
                t.title,
                bool(t.completed),
                (t.created_at.isoformat() if t.created_at else None),
                (int(t.age_days) if t.age_days is not None else None),
            ])
        return table
    finally:
        session.close()


def timelogs_for_task(task_id):
    session = get_session()
    try:
        logs = session.query(TimeLog).filter(TimeLog.task_id == task_id).order_by(TimeLog.started_at).all()
        return [[l.id, l.task_id, (l.started_at.isoformat() if l.started_at else None), l.duration_hours, l.duration_minutes] for l in logs]
    finally:
        session.close()
