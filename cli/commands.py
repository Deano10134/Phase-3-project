import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
try:
    from tabulate import tabulate
except Exception:
    def tabulate(rows, headers=None):
        if headers:
            print(" | ".join(headers))
            print("-" * len(" | ".join(headers)))
        for r in rows:
            print(" | ".join(str(x) for x in r))

from db.models import User, Category, Task, Tag

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///db/task_manager.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def list_users():
    session = Session()
    users = session.query(User).all()
    table = [[u.id, u.username, u.email] for u in users]
    print(tabulate(table, headers=["ID", "Username", "Email"]))
    session.close()

def list_categories():
    session = Session()
    categories = session.query(Category).all()
    table = [[c.id, c.name, c.description or 'N/A'] for c in categories]
    print(tabulate(table, headers=["ID", "Name", "Description"]))
    session.close()

def list_tasks():
    session = Session()
    tasks = session.query(Task).all()
    table = [
        [
            t.id,
            t.title,
            t.status,
            t.user.username if t.user else "N/A",
            "Yes" if getattr(t, "is_overdue", False) else "No"
        ]
        for t in tasks
    ]
    print(tabulate(table, headers=["ID", "Title", "Status", "User", "Overdue"]))
    session.close()

def add_task():
    session = Session()
    title = input("Title: ")
    description = input("Description: ")
    try:
        priority = int(input("Priority (1=Low, 2=Medium, 3=High): "))
    except ValueError:
        priority = 1
    user_id = int(input("User ID: "))
    category_id_input = input("Category ID (optional, press Enter to skip): ")
    category_id = int(category_id_input) if category_id_input else None
    
    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        user_id=user_id,
        category_id=category_id
    )
    session.add(new_task)
    session.commit()
    print(f"Task '{title}' added.")
    session.close()
