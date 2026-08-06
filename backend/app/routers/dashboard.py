from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import require_role

from app.schemas.dashboard import TicketStats
from app.services.dashboard_service import get_ticket_statistics

from app.schemas.dashboard import PriorityStats
from app.services.dashboard_service import get_priority_statistics

from app.schemas.dashboard import DepartmentStat
from app.services.dashboard_service import get_department_statistics

from app.schemas.dashboard import EngineerWorkload
from app.services.dashboard_service import get_engineer_workload

from app.schemas.ticket import TicketResponse
from app.services.dashboard_service import get_recent_tickets

from app.schemas.activity import ActivityResponse
from app.services.dashboard_service import get_recent_activities

from app.schemas.dashboard import SLAStats
from app.services.dashboard_service import get_sla_statistics

from app.schemas.dashboard_chart import TrendPoint
from app.services.dashboard_service import get_ticket_trends

from app.schemas.dashboard_chart import PriorityChart
from app.services.dashboard_service import get_priority_chart

from app.schemas.dashboard_chart import DepartmentChart
from app.services.dashboard_service import get_department_chart

from app.schemas.dashboard_chart import EngineerChart
from app.services.dashboard_service import get_engineer_chart

from app.schemas.dashboard_chart import DashboardSummary
from app.services.dashboard_service import get_dashboard_summary

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/ticket-stats",
    response_model=TicketStats
)
def ticket_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_ticket_statistics(db)

@router.get(
    "/priority-stats",
    response_model=PriorityStats
)
def priority_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return get_priority_statistics(db)

@router.get(
    "/department-stats",
    response_model=list[DepartmentStat]
)
def department_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return get_department_statistics(db)

@router.get(
    "/engineer-workload",
    response_model=list[EngineerWorkload]
)
def engineer_workload(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return get_engineer_workload(db)

@router.get(
    "/recent-tickets",
    response_model=list[TicketResponse]
)
def recent_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return get_recent_tickets(db)

@router.get(
    "/recent-activities",
    response_model=list[ActivityResponse]
)
def recent_activities(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return get_recent_activities(db)

@router.get(
    "/sla-stats",
    response_model=SLAStats
)
def sla_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_sla_statistics(db)

@router.get(
    "/trends",
    response_model=list[TrendPoint]
)
def ticket_trends(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_ticket_trends(db)


@router.get(
    "/priority-chart",
    response_model=list[PriorityChart]
)
def priority_chart(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_priority_chart(db)

@router.get(
    "/department-chart",
    response_model=list[DepartmentChart]
)
def department_chart(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_department_chart(db)

@router.get(
    "/engineer-chart",
    response_model=list[EngineerChart]
)
def engineer_chart(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_engineer_chart(db)

@router.get(
    "/summary",
    response_model=DashboardSummary
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "engineer"))
):
    return get_dashboard_summary(db)