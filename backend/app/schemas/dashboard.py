from pydantic import BaseModel

class EngineerWorkload(BaseModel):
    engineer: str
    tickets: int

class PriorityStats(BaseModel):
    low: int
    medium: int
    high: int

class TicketStats(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    closed: int

class DepartmentStat(BaseModel):
    department: str
    count: int