from typing import List, Dict, Optional
from datetime import datetime

class Task:
    def __init__(self, title: str, description: str = None, priority: int = 1, completed: bool = False, 
                 created_at: datetime = None, due_date: datetime = None, completed_at: datetime = None, 
                 user_id: int = None, category_id: int = None, id: int = None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.utcnow()
        self.due_date = due_date
        self.completed_at = completed_at
        self.user_id = user_id
        self.category_id = category_id

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"

    @property
    def age_days(self):
        if not self.created_at:
            return None
        delta = datetime.utcnow() - self.created_at
        return delta.days

class User:
    def __init__(self, username: str, email: str = None, id: int = None):
        self.id = id
        self.username = username
        self.email = email
        self.tasks: List[Task] = []

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

class Category:
    def __init__(self, name: str, description: str = None, user_id: int = None, id: int = None):
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.tasks: List[Task] = []

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"

class Tag:
    def __init__(self, name: str, color: str = None, id: int = None):
        self.id = id
        self.name = name
        self.color = color
        self.tasks: List[Task] = []

    def __repr__(self):
        return f"<Tag id={self.id} name={self.name}>"
