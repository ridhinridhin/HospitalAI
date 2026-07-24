from fastapi import FastAPI
from app.routers import health

app = FastAPI(
    title="HospitalAI",
    description="Hospital IT Help Desk API",
    version="1.0.0"
)

app.include_router(health.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to HospitalAI 🚀",
        "status": "Running Successfully"
    }