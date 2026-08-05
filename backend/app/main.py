from fastapi import FastAPI
from app.routers import health
from app.database import Base, engine
from app.models.user import User
from app.routers import health, users, tickets, auth, comments, activity, attachments
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.models.activity import Activity
from app.models.attachment import Attachment
from app.routers import dashboard
from app.jobs.scheduler import start_scheduler
from app.routers import reports


app = FastAPI(
    title="HospitalAI",
    description="Hospital IT Help Desk API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(activity.router)
app.include_router(attachments.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to HospitalAI 🚀",
        "status": "Running Successfully"
    }

@app.on_event("startup")
def startup():
    start_scheduler()
