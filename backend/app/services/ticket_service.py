from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(db: Session, ticket_data: TicketCreate):
    ticket = Ticket(**ticket_data.model_dump())

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket_by_id(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


def update_ticket(db: Session, ticket_id: int, ticket_data: TicketUpdate):
    ticket = get_ticket_by_id(db, ticket_id)

    update_data = ticket_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket


def delete_ticket(db: Session, ticket_id: int):
    ticket = get_ticket_by_id(db, ticket_id)

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}