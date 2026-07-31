from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.database import get_db
from app.schemas.user import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user
from app.auth.jwt_handler import create_access_token

from app.schemas.user import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.services.auth_service import (
    generate_reset_token,
    reset_password
)

from app.services.email_service import (
    send_password_reset_email
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = generate_reset_token(
        db,
        request.email
    )

    # Always return the same response
    if user:
        reset_link = (
            f"http://localhost:5173/reset-password?token={user.reset_token}"
        )

        send_password_reset_email(
            user.email,
            user.name,
            reset_link
        )

    return {
        "message": "If the email exists, a password reset link has been sent."
    }


@router.post("/reset-password")
def reset_password_endpoint(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    success = reset_password(
        db,
        request.token,
        request.new_password
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    return {
        "message": "Password reset successfully"
    }