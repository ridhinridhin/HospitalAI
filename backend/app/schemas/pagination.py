from pydantic import BaseModel

from app.schemas.ticket import TicketResponse


class TicketListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    pages: int
    items: list[TicketResponse]