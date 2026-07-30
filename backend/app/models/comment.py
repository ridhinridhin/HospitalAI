from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, UTC

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user_name = Column(String, nullable=False)

    message = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )