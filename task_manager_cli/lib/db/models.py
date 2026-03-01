"""Consolidated DB models module.

Combines the separate model classes into a single `models.py` module
under `lib/db/` so the simpler layout is available.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Project id={self.id} name={self.name}>"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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
        return func.julianday(func.datetime('now')) - func.julianday(cls.created_at)

    timelogs = relationship("TimeLog", back_populates="task")


class TimeLog(Base):
    __tablename__ = "timelogs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_hours = Column(Float, default=0.0)

    task = relationship("Task", back_populates="timelogs")

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
