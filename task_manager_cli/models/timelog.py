"""Time log model."""
from sqlalchemy import Column, Integer, DateTime, Float
from .base import Base
import datetime


class TimeLog(Base):
    __tablename__ = "timelogs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    duration_hours = Column(Float, default=0.0)

    def __repr__(self):
        return f"<TimeLog id={self.id} task_id={self.task_id}>"
