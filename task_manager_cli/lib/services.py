from typing import List, Dict, Optional
from task_manager_cli.lib.db.models import Task, User, Category, Tag
from task_manager_cli.lib.db.session import get_engine, get_session

class TaskService:
    def __init__(self, engine=None):
        self.engine = engine or get_engine()

    def list_tasks(self, user_name: str = None, category_name: str = None) -> List[Dict]:
        session = get_session(self.engine)
        try:
            query = session.query(Task)
            if user_name:
                query = query.join(User).filter(User.username == user_name)
            if category_name:
                query = query.join(Category).filter(Category.name == category_name)

            tasks = query.order_by(Task.created_at).all()
            result = []
            for t in tasks:
                result.append({
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": bool(t.completed),
                    "created": t.created_at.isoformat() if t.created_at else None,
                    "age_days": int(t.age_days) if t.age_days is not None else None,
                    "user": t.user.username if t.user else None,
                    "category": t.category.name if t.category else None,
                })
            return result
        finally:
            session.close()

    def get_summary(self) -> tuple:
        session = get_session(self.engine)
        try:
            total = session.query(Task).count()
            completed = session.query(Task).filter(Task.completed.is_(True)).count()
            return (total, completed)
        finally:
            session.close()

    def create_task(self, title: str, description: str = None, user_id: int = None, category_id: int = None) -> Dict:
        if not title or len(title.strip()) < 3:
            raise ValueError("Task title must be at least 3 characters long.")
        
        session = get_session(self.engine)
        try:
            task = Task(
                title=title.strip(),
                description=description,
                user_id=user_id,
                category_id=category_id
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return {
                "id": task.id,
                "title": task.title,
                "completed": bool(task.completed)
            }
        finally:
            session.close()

    def delete_task(self, task_id: int) -> bool:
        session = get_session(self.engine)
        try:
            task = session.query(Task).filter(Task.id == task_id).one_or_none()
            if not task:
                return False
            session.delete(task)
            session.commit()
            return True
        finally:
            session.close()
