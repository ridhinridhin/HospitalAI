from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(
    db: Session,
    ticket_data: TicketCreate,
    current_user: User
):
    ticket_data_dict = ticket_data.model_dump()

    # Remove user-controlled identity fields
    ticket_data_dict.pop("employee_id", None)
    ticket_data_dict.pop("employee_name", None)

    ticket = Ticket(
        **ticket_data_dict,
        owner_id=current_user.id,
        employee_id=str(current_user.id),
        employee_name=current_user.name
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

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