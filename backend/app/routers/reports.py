from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import require_role

from app.services.report_service import (
    get_all_tickets,
    export_tickets_to_excel
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/tickets")
def get_ticket_report(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_all_tickets(db)


@router.get("/tickets/excel")
def export_excel(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    file_name = export_tickets_to_excel(db)

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )