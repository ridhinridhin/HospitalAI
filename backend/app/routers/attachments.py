from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.attachment import AttachmentResponse
from app.services.attachment_service import upload_attachment

router = APIRouter(
    prefix="/tickets/{ticket_id}/attachments",
    tags=["Attachments"],
)


@router.post("/", response_model=AttachmentResponse)
def upload_file(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_attachment(
        db,
        ticket_id,
        file,
        current_user,
    )