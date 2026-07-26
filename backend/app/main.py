from fastapi import FastAPI
from app.routers import health
from app.database import Base, engine
from app.models.user import User
from app.routers import health, users, tickets
from app.models.ticket import Ticket
from app.routers import auth

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


@app.get("/")
def home():
    return {
        "message": "Welcome to HospitalAI 🚀",
        "status": "Running Successfully"
    }