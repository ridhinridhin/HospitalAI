from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.models.user import User

from app.database import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.schemas.pagination import TicketListResponse

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


@router.get("/", response_model=TicketListResponse)
def get_tickets(
    search: str | None = Query(None),
    status: str | None = Query(None),
    priority: str | None = Query(None),
    department: str | None = Query(None),
    assigned_to: str | None = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_tickets(
        db=db,
        current_user=current_user,
        search=search,
        status=status,
        priority=priority,
        department=department,
        assigned_to=assigned_to,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
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