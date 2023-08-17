from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    false,
    func
)
from .base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    is_staff = Column(
        Boolean,
        nullable=False,
        server_default=false(),
        default=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )

    posts = relationship(
        "Post",
        back_populates="user",
        uselist=True,
    )

    def __str__(self):
        return (f"User(id={self.id},"
                f" username={self.username!r},"
                f" email={self.email!r},"
                f" is_staff={self.is_staff!r})")

    def __repr__(self):
        return str(self)
