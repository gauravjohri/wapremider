from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.database import tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WhatsApp Reminder SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (DEV ONLY)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()
    
def log():
    with open("wapreminder-worker.log", "r", encoding="utf-8") as f:
        return f.read()
    
def normalize_phone(phone: str) -> str:
    phone = phone.strip()              # remove spaces
    phone = phone.replace(" ", "")     # remove internal spaces

    if not phone.startswith("+"):
        phone = "+" + phone

    return phone

@app.post("/create-reminder")
def create_reminder(phone: str, message: str, time: str):
    phone = normalize_phone(phone)
    tasks.insert_one({
        "user_phone": phone,
        "message": message,
        "reminder_time": datetime.fromisoformat(time),
        "status": "pending"
    })
    return {"message": "Reminder created successfully"}