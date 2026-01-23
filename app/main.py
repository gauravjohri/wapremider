from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.database import tasks
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
OUT_LOG_FILE = Path("/root/worker.out.log")
ERR_LOG_FILE = Path("/root/worker.err.log")


app = FastAPI(title="WhatsApp Reminder SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (DEV ONLY)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_and_log_main_error(raw_text: str):
    main_error = None

    for line in raw_text.splitlines():
        if "ImportError" in line or "Traceback" in line:
            main_error = line.strip()

    if not main_error:
        main_error = "No Python error found"

    ERR_LOG_FILE.write_text(main_error, encoding="utf-8")
    return main_error

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.get("/log", response_class=HTMLResponse)    
def log():
    if ERR_LOG_FILE.exists():
        return extract_and_log_main_error(ERR_LOG_FILE.read_text(encoding="utf-8"))
    return "Log file not found"

@app.get("/log2", response_class=HTMLResponse)    
def log():
    if OUT_LOG_FILE.exists():
        return OUT_LOG_FILE.read_text(encoding="utf-8")
    return "Log file not found"
    
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