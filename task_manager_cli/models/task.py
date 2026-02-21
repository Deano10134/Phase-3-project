"""Task model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from sqlalchemy.ext.hybrid import hybrid_property
from .base import Base
import datetime




class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"

    @hybrid_property
    def age_days(self):
        if not self.created_at:
            return None
        delta = datetime.datetime.utcnow() - self.created_at
        return delta.days

    @age_days.expression
    def age_days(cls):
        # use julianday difference to compute age in days for SQLite-compatible SQL
        return func.julianday(func.datetime('now')) - func.julianday(cls.created_at)
