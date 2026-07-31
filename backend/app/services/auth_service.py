from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.hashing import verify_password

from datetime import datetime, timedelta, UTC
import secrets

from app.auth.hashing import hash_password


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def generate_reset_token(
    db: Session,
    email: str
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)

    db.commit()

    return user


def reset_password(
    db: Session,
    token: str,
    new_password: str
):
    user = (
        db.query(User)
        .filter(User.reset_token == token)
        .first()
    )

    if not user:
        return False

    if (
        user.reset_token_expiry is None
        or user.reset_token_expiry < datetime.utcnow()
    ):
        return False

    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()
    db.refresh(user)

    return True
