import os
import shutil
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.attachment import Attachment
from app.models.user import User

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_attachment(
    db: Session,
    ticket_id: int,
    file: UploadFile,
    current_user: User,
):
    unique_name = f"{uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, unique_name)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    attachment = Attachment(
        ticket_id=ticket_id,
        uploaded_by=current_user.id,          # Integer FK
        file_name=file.filename,              # Matches model
        file_path=filepath,                   # Matches model
        file_type=file.content_type or "application/octet-stream",
        file_size=os.path.getsize(filepath),
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment