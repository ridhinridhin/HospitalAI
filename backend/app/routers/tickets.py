from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.services.ticket_service import (
    create_ticket as create_ticket_service,
    get_all_tickets,
    get_ticket_by_id,
    update_ticket as update_ticket_service,
    delete_ticket as delete_ticket_service,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return create_ticket_service(db, ticket)

@router.get("/", response_model=list[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return get_all_tickets(db)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return get_ticket_by_id(db, ticket_id)

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
):
    return update_ticket_service(db, ticket_id, ticket_data)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return delete_ticket_service(db, ticket_id)