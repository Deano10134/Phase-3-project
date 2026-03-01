"""Consolidated DB models module.

Combines the separate model classes into a single `models.py` module
under `lib/db/` so the simpler layout is available.
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
    func,
    Table,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


# Association table for Task and Tag (many-to-many)
task_tag = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), nullable=True)

    tasks = relationship("Task", back_populates="user")
    categories = relationship("Category", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="categories")
    tasks = relationship("Task", back_populates="category")

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    completed_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    tags = relationship("Tag", secondary=task_tag, back_populates="tasks")

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"

    @hybrid_property
    def age_days(self):
        if not self.created_at:
            return None
        delta = datetime.utcnow() - self.created_at
        return delta.days

    @age_days.expression
    def age_days(cls):
        return func.julianday(func.datetime("now")) - func.julianday(cls.created_at)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(20))

    tasks = relationship("Task", secondary=task_tag, back_populates="tags")

    def __repr__(self):
        return f"<Tag id={self.id} name={self.name}>"


# The following models are not used in seed.py, but I'll leave them for now.
# If they are not needed, they can be removed.


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Project id={self.id} name={self.name}>"


class TimeLog(Base):
    __tablename__ = "timelogs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_hours = Column(Float, default=0.0)

    task = relationship("Task")  # Simplified relationship

    def __repr__(self):
        return f"<TimeLog id={self.id} task_id={self.task_id} duration_hours={self.duration_hours}>"

    @hybrid_property
    def duration_minutes(self):
        if self.duration_hours is None:
            return None
        return int(self.duration_hours * 60)

    @duration_minutes.expression
    def duration_minutes(cls):
        return func.round(cls.duration_hours * 60)


class RecurringTask(Base):
    __tablename__ = "recurring_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    interval = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<RecurringTask id={self.id} title={self.title}>"
