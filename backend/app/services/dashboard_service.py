from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from sqlalchemy import func

from app.models.activity import Activity


from datetime import datetime, timedelta

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

def get_sla_statistics(db: Session):
    total_tickets = db.query(Ticket).count()

    open_tickets = (
        db.query(Ticket)
        .filter(Ticket.status != "Resolved")
        .count()
    )

    resolved_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Resolved")
        .count()
    )

    overdue_tickets = (
        db.query(Ticket)
        .filter(Ticket.is_overdue == True)
        .count()
    )

    critical_overdue = (
        db.query(Ticket)
        .filter(
            Ticket.is_overdue == True,
            Ticket.priority == "Critical"
        )
        .count()
    )

    sla_compliance = (
        100.0
        if total_tickets == 0
        else round(
            ((total_tickets - overdue_tickets) / total_tickets) * 100,
            2
        )
    )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "overdue_tickets": overdue_tickets,
        "critical_overdue": critical_overdue,
        "sla_compliance": sla_compliance,
    }

def get_sla_statistics(db: Session):
    total_tickets = db.query(Ticket).count()

    open_tickets = (
        db.query(Ticket)
        .filter(
            Ticket.status.in_(["Open", "In Progress"])
        )
        .count()
    )

    resolved_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Resolved")
        .count()
    )

    overdue_tickets = (
        db.query(Ticket)
        .filter(Ticket.is_overdue == True)
        .count()
    )

    critical_overdue = (
        db.query(Ticket)
        .filter(
            Ticket.is_overdue == True,
            Ticket.priority == "Critical"
        )
        .count()
    )

    sla_compliance = (
        100.0
        if total_tickets == 0
        else round(
            ((total_tickets - overdue_tickets) / total_tickets) * 100,
            2
        )
    )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "overdue_tickets": overdue_tickets,
        "critical_overdue": critical_overdue,
        "sla_compliance": sla_compliance,
    }

def get_ticket_trends(db: Session, days: int = 7):
    results = (
        db.query(
            func.date(Ticket.created_at).label("date"),
            func.count(Ticket.id).label("tickets")
        )
        .group_by(func.date(Ticket.created_at))
        .order_by(func.date(Ticket.created_at))
        .all()
    )

    return [
        {
            "date": str(date),
            "tickets": tickets
        }
        for date, tickets in results
    ]

def get_priority_chart(db: Session):
    results = (
        db.query(
            Ticket.priority,
            func.count(Ticket.id)
        )
        .group_by(Ticket.priority)
        .all()
    )

    return [
        {
            "priority": priority,
            "count": count
        }
        for priority, count in results
    ]

def get_department_chart(db: Session):
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


def get_engineer_chart(db: Session):
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

def get_dashboard_summary(db: Session):
    total_tickets = db.query(Ticket).count()

    open_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Open")
        .count()
    )

    resolved_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Resolved")
        .count()
    )

    overdue_tickets = (
        db.query(Ticket)
        .filter(Ticket.is_overdue == True)
        .count()
    )

    critical_overdue = (
        db.query(Ticket)
        .filter(
            Ticket.is_overdue == True,
            Ticket.priority == "Critical"
        )
        .count()
    )

    if total_tickets == 0:
        sla_compliance = 100.0
    else:
        sla_compliance = round(
            ((total_tickets - overdue_tickets) / total_tickets) * 100,
            2
        )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "overdue_tickets": overdue_tickets,
        "critical_overdue": critical_overdue,
        "sla_compliance": sla_compliance
    }

def get_average_resolution_time(db: Session):
    resolved = (
        db.query(Ticket)
        .filter(Ticket.status == "Resolved")
        .all()
    )

    if not resolved:
        return {
            "average_hours": 0
        }

    total_hours = 0

    for ticket in resolved:
        hours = (
            ticket.updated_at - ticket.created_at
        ).total_seconds() / 3600

        total_hours += hours

    average = round(
        total_hours / len(resolved),
        2
    )

    return {
        "average_hours": average
    }