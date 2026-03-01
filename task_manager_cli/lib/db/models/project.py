"""Project model."""
from sqlalchemy import Column, Integer, String, Text
from .base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Project id={self.id} name={self.name}>"
