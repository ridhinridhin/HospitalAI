from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import (
    create_comment,
    get_ticket_comments,
)

router = APIRouter(
    prefix="/tickets/{ticket_id}/comments",
    tags=["Comments"],
)


@router.post("/", response_model=CommentResponse)
def add_comment(
    ticket_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_comment(
        db,
        ticket_id,
        comment,
        current_user,
    )


@router.get("/", response_model=list[CommentResponse])
def list_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_ticket_comments(
        db,
        ticket_id,
        current_user,
    )