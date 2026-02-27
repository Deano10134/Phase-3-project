"""Time log model."""
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class TimeLog(Base):
    __tablename__ = "timelogs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_hours = Column(Float, default=0.0)

    # relationship to Task (not required by the DB schema but useful in ORM)
    task = relationship("Task", back_populates="timelogs")

    def __repr__(self):
        return f"<TimeLog id={self.id} task_id={self.task_id} duration_hours={self.duration_hours}>"

    @hybrid_property
    def duration_minutes(self):
        """Return the duration in whole minutes (Python-side logic).

        Falls back to computing from `duration_hours` column when present.
        """
        if self.duration_hours is None:
            return None
        return int(self.duration_hours * 60)

    @duration_minutes.expression
    def duration_minutes(cls):
        # SQL expression: multiply stored hours by 60
        return func.round(cls.duration_hours * 60)
