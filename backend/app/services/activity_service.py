from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.user import User


def log_activity(
    db: Session,
    ticket_id: int,
    current_user: User,
    action: str
):
    activity = Activity(
        ticket_id=ticket_id,
        user_id=current_user.id,
        user_name=current_user.name,
        action=action
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_ticket_activity(
    db: Session,
    ticket_id: int
):
    return (
        db.query(Activity)
        .filter(Activity.ticket_id == ticket_id)
        .order_by(Activity.created_at.asc())
        .all()
    )