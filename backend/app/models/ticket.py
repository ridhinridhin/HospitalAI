from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    # Ticket Details
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Employee Information
    employee_id = Column(String, nullable=False, index=True)
    employee_name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    # Ticket Status
    priority = Column(String, default="Medium")
    status = Column(String, default="Open")

    # IT Assignment
    assigned_to = Column(String, nullable=True)

    # Time Tracking
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
)