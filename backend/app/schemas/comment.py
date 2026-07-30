from datetime import datetime
from pydantic import BaseModel


class CommentCreate(BaseModel):
    message: str


class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    user_name: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True