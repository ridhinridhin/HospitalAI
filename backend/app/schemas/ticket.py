from datetime import datetime
from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str
    department: str
    priority: str = "Medium"


class TicketResponse(TicketCreate):
    id: int
    employee_id: str
    employee_name: str
    status: str
    assigned_to: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    assigned_to: str | None = None

