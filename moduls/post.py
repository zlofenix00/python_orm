from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    func
)
from sqlalchemy.orm import relationship
from .base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=False)
    body = Column(
        Text,
        nullable=False,
        unique=False,
        default="",
        server_default="",
    )

    published_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=False,
    )

    user = relationship(
        "User",
        back_populates="posts",
        uselist=False,
    )

    def __str__(self):
        return (f"Post(id={self.id},"
                f" title={self.title!r},"
                f" body={self.body!r})")

    def __repr__(self):
        return str(self)
