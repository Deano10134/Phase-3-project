"""User model."""
from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
