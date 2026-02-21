"""Recurring task model."""
from sqlalchemy import Column, Integer, String, Text
from .base import Base


class RecurringTask(Base):
    __tablename__ = "recurring_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    interval = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<RecurringTask id={self.id} title={self.title}>"
