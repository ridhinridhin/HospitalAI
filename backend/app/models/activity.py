from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, UTC

from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

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
        nullable=False
    )

    user_name = Column(String, nullable=False)

    action = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )