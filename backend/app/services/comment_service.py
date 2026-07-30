from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.comment import Comment
from app.models.user import User
from app.services.ticket_service import get_ticket_by_id

from app.schemas.comment import CommentCreate
from app.services.activity_service import log_activity

from app.models.ticket import Ticket
from app.services.email_service import send_comment_notification

def create_comment(
    db: Session,
    ticket_id: int,
    comment_data: CommentCreate,
    current_user: User
):
    # Ensure the user has access to the ticket
    get_ticket_by_id(db, ticket_id, current_user)

    comment = Comment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        user_name=current_user.name,
        message=comment_data.message,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    log_activity(
        db,
        ticket_id,
        current_user,
        "Added a comment"
    )

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )
    if ticket:
        owner = (
            db.query(User)
            .filter(User.id == ticket.owner_id)
            .first()
        )
        
        # Don't email yourself when commenting
        if owner and owner.id != current_user.id:
            send_comment_notification(
                employee_email=owner.email,
                employee_name=owner.name,
                ticket_title=ticket.title,
                comment=comment.message
            )
    
    return comment


def get_ticket_comments(
    db: Session,
    ticket_id: int,
    current_user: User
):
    # Ensure the user has access to the ticket
    get_ticket_by_id(db, ticket_id, current_user)

    return (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.created_at.asc())
        .all()
    )