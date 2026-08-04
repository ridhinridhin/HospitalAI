from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.ticket import Ticket


def check_overdue_tickets():
    db: Session = SessionLocal()

    try:
        now = datetime.now(UTC)

        overdue_tickets = (
            db.query(Ticket)
            .filter(
                Ticket.sla_due_date < now,
                Ticket.status != "Resolved",
                Ticket.is_overdue == False
            )
            .all()
        )

        for ticket in overdue_tickets:
            ticket.is_overdue = True

            print(
                f"[SLA] Ticket #{ticket.id} marked as overdue."
            )

        db.commit()

    finally:
        db.close()