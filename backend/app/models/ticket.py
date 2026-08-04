from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, UTC

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    # Ticket Details
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Ticket Owner
    owner_id = Column(Integer, nullable=False, index=True)

    # Employee Information
    employee_id = Column(String, nullable=False, index=True)
    employee_name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    # Ticket Status
    priority = Column(String, default="Medium")
    status = Column(String, default="Open")

    # IT Assignment
    assigned_to = Column(String, nullable=True)

    # SLA Information
    sla_due_date = Column(DateTime, nullable=True)
    is_overdue = Column(Boolean, default=False)
    escalation_level = Column(Integer, default=0)
    escalated_at = Column(DateTime, nullable=True)

    # Time Tracking
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )