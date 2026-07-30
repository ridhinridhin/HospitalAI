from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.activity import ActivityResponse
from app.services.activity_service import get_ticket_activity
from app.services.ticket_service import get_ticket_by_id

router = APIRouter(
    prefix="/tickets/{ticket_id}/activity",
    tags=["Activity"],
)


@router.get("/", response_model=list[ActivityResponse])
def list_activity(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ensure the user has access to the ticket
    get_ticket_by_id(db, ticket_id, current_user)

    return get_ticket_activity(db, ticket_id)