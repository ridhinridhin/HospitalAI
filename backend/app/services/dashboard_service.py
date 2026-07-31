from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from sqlalchemy import func

from app.models.activity import Activity

def get_ticket_statistics(db: Session):
    return {
        "total": db.query(Ticket).count(),
        "open": db.query(Ticket).filter(Ticket.status == "Open").count(),
        "in_progress": db.query(Ticket).filter(Ticket.status == "In Progress").count(),
        "resolved": db.query(Ticket).filter(Ticket.status == "Resolved").count(),
        "closed": db.query(Ticket).filter(Ticket.status == "Closed").count(),
    }


def get_priority_statistics(db: Session):
    return {
        "low": db.query(Ticket).filter(Ticket.priority == "Low").count(),
        "medium": db.query(Ticket).filter(Ticket.priority == "Medium").count(),
        "high": db.query(Ticket).filter(Ticket.priority == "High").count(),
    }

def get_department_statistics(db: Session):
    results = (
        db.query(
            Ticket.department,
            func.count(Ticket.id)
        )
        .group_by(Ticket.department)
        .all()
    )

    return [
        {
            "department": department,
            "count": count
        }
        for department, count in results
    ]

def get_engineer_workload(db: Session):
    results = (
        db.query(
            Ticket.assigned_to,
            func.count(Ticket.id)
        )
        .filter(Ticket.assigned_to.isnot(None))
        .group_by(Ticket.assigned_to)
        .all()
    )

    return [
        {
            "engineer": engineer,
            "tickets": count
        }
        for engineer, count in results
    ]


def get_recent_tickets(
    db: Session,
    limit: int = 5
):
    return (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .limit(limit)
        .all()
    )

def get_recent_activities(
    db: Session,
    limit: int = 10
):
    return (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .limit(limit)
        .all()
    )