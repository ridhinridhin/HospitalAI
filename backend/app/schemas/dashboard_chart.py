from pydantic import BaseModel


class TrendPoint(BaseModel):
    date: str
    tickets: int


class PriorityChart(BaseModel):
    priority: str
    count: int


class DepartmentChart(BaseModel):
    department: str
    count: int


class EngineerChart(BaseModel):
    engineer: str
    tickets: int


class DashboardSummary(BaseModel):
    total_tickets: int
    open_tickets: int
    resolved_tickets: int
    overdue_tickets: int
    critical_overdue: int
    sla_compliance: float

class ResolutionTime(BaseModel):
    average_hours: float