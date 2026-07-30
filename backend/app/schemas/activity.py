from datetime import datetime
from pydantic import BaseModel


class ActivityResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    user_name: str
    action: str
    created_at: datetime

    class Config:
        from_attributes = True