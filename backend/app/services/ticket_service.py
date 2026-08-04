from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services.activity_service import log_activity

from app.services.email_service import (
    send_ticket_created_email,
    send_ticket_assigned_email,
    send_ticket_resolved_email
)

from datetime import datetime, UTC, timedelta


def create_ticket(
    db: Session,
    ticket_data: TicketCreate,
    current_user: User
):
    ticket_data_dict = ticket_data.model_dump()

    sla_hours = {
        "Low": 72,
        "Medium": 48,
        "High": 24,
        "Critical": 8
    }

    hours = sla_hours.get(ticket_data.priority, 48)

    sla_due = datetime.now(UTC) + timedelta(hours=hours)

    # Remove user-controlled identity fields
    ticket_data_dict.pop("employee_id", None)
    ticket_data_dict.pop("employee_name", None)

    ticket = Ticket(
        **ticket_data_dict,
        owner_id=current_user.id,
        employee_id=str(current_user.id),
        employee_name=current_user.name,
        sla_due_date=sla_due
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)


    log_activity(
        db,
        ticket.id,
        current_user,
        "Created the ticket"
    )

    owner = (
        db.query(User)
        .filter(User.id == ticket.owner_id)
        .first()

   )

    if owner:
        send_ticket_created_email(
            employee_email=owner.email,
            employee_name=owner.name,
            ticket_title=ticket.title
        )

    #send_ticket_assigned_email(
     #   engineer_email=engineer.email,
     #  engineer_name=engineer.name,
     #  ticket_title=ticket.title,
     #   ticket_description=ticket.description,
     #   priority=ticket.priority,
     #   department=ticket.department,
     #   assigned_by=current_user.name
    #)

    return ticket


def get_all_tickets(db: Session, current_user: User):

    if current_user.role in ["admin", "engineer"]:
        return db.query(Ticket).all()

    return db.query(Ticket).filter(
        Ticket.owner_id == current_user.id
    ).all()


def get_ticket_by_id(
    db: Session,
    ticket_id: int,
    current_user: User
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if current_user.role == "employee":

        if ticket.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return ticket


def update_ticket(
    db: Session,
    ticket_id: int,
    ticket_data: TicketUpdate,
    current_user: User
):
    ticket = get_ticket_by_id(
        db,
        ticket_id,
        current_user
    )

    update_data = ticket_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    log_activity(
        db,
        ticket.id,
        current_user,
        "Updated the ticket"
    )

    # Send email when a ticket is assigned
    if (
        "assigned_to" in update_data
        and ticket.assigned_to
    ):
        engineer = (
            db.query(User)
            .filter(User.name == ticket.assigned_to)
            .first()
        )

        if engineer:
            send_ticket_assigned_email(
                engineer_email=engineer.email,
                engineer_name=engineer.name,
                ticket_title=ticket.title
            )

    # Send email when a ticket is resolved
    if (
        "status" in update_data
        and ticket.status == "Resolved"
    ):
        owner = (
            db.query(User)
            .filter(User.id == ticket.owner_id)
            .first()
        )

        if owner:
            send_ticket_resolved_email(
                employee_email=owner.email,
                employee_name=owner.name,
                ticket_title=ticket.title
            )

    return ticket


def delete_ticket(
    db: Session,
    ticket_id: int,
    current_user: User
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete tickets"
        )

    ticket = get_ticket_by_id(
        db,
        ticket_id,
        current_user
    )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }


def get_overdue_tickets(
    db: Session,
    current_user: User
):
    now = datetime.now(UTC)

    overdue_tickets = (
        db.query(Ticket)
        .filter(
            Ticket.sla_due_date < now,
            Ticket.status != "Resolved"
        )
        .all()
    )

    # Mark tickets as overdue
    for ticket in overdue_tickets:
        if not ticket.is_overdue:
            ticket.is_overdue = True

    db.commit()

    if current_user.role in ["admin", "engineer"]:
        return overdue_tickets

    return [
        ticket
        for ticket in overdue_tickets
        if ticket.owner_id == current_user.id
    ]

def escalate_ticket(
    db: Session,
    ticket_id: int,
    current_user: User
):
    ticket = get_ticket_by_id(
        db,
        ticket_id,
        current_user
    )

    if ticket.status == "Resolved":
        raise HTTPException(
            status_code=400,
            detail="Resolved tickets cannot be escalated"
        )

    if not ticket.is_overdue:
        raise HTTPException(
            status_code=400,
            detail="Only overdue tickets can be escalated"
        )

    ticket.escalation_level += 1
    ticket.escalated_at = datetime.now(UTC)

    db.commit()
    db.refresh(ticket)

    log_activity(
        db,
        ticket.id,
        current_user,
        f"Escalated ticket (Level {ticket.escalation_level})"
    )

    engineer = (
        db.query(User)
        .filter(User.name == ticket.assigned_to)
        .first()
    )

    if engineer:
        send_ticket_assigned_email(
            engineer_email=engineer.email,
            engineer_name=engineer.name,
            ticket_title=ticket.title,
            ticket_description=ticket.description,
            priority=ticket.priority,
            department=ticket.department,
            assigned_by=f"Escalated by {current_user.name}"
        )

    return ticket