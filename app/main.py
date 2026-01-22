from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.database import tasks

app = FastAPI(title="WhatsApp Reminder SaaS")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/create-reminder")
def create_reminder(phone: str, message: str, time: str):
    tasks.insert_one({
        "user_phone": phone,
        "message": message,
        "reminder_time": datetime.fromisoformat(time),
        "status": "pending"
    })
    return {"message": "Reminder created successfully"}