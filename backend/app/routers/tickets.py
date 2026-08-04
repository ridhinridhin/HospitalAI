from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.models.user import User

from app.database import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate

from app.services.ticket_service import (
    create_ticket as create_ticket_service,
    get_all_tickets,
    get_ticket_by_id,
    update_ticket as update_ticket_service,
    delete_ticket as delete_ticket_service,
    get_overdue_tickets,
    escalate_ticket,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_ticket_service(
        db,
        ticket,
        current_user
    )


@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_tickets(
        db,
        current_user
    )


# Must be above /{ticket_id}
@router.get("/overdue", response_model=list[TicketResponse])
def overdue_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_overdue_tickets(
        db,
        current_user
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_ticket_by_id(
        db,
        ticket_id,
        current_user
    )


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_ticket_service(
        db,
        ticket_id,
        ticket_data,
        current_user
    )


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return delete_ticket_service(
        db,
        ticket_id,
        current_user
    )

@router.post(
    "/{ticket_id}/escalate",
    response_model=TicketResponse
)
def escalate(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "engineer"))
):
    return escalate_ticket(
        db,
        ticket_id,
        current_user
    )