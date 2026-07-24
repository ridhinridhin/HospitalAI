from fastapi import FastAPI

app = FastAPI(
    title="HospitalAI",
    description="Hospital IT Help Desk API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to HospitalAI 🚀",
        "status": "Running Successfully"
    }