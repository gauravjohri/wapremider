from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import time

from app.database import tasks
from app.whatsapp import send_whatsapp

IST = ZoneInfo("Asia/Kolkata")

print("✅ Worker started...")

while True:
    try:
        # 🔒 Always use UTC for logic
        now_utc = datetime.now(timezone.utc)
        now_ist = now_utc.astimezone(IST)

        print(f"⏰ NOW IST: {now_ist}")

        reminders = tasks.find({"status": "pending"})

        for r in reminders:
            rt = r.get("reminder_time")

            if not rt:
                print("⚠️ Missing reminder_time, skipping:", r["_id"])
                continue

            # 🔑 Normalize reminder_time
            if isinstance(rt, str):
                # string → datetime → UTC
                rt = datetime.fromisoformat(rt).replace(tzinfo=timezone.utc)

            elif rt.tzinfo is None:
                # naive datetime → assume UTC
                rt = rt.replace(tzinfo=timezone.utc)

            # Convert only for display/logging
            rt_ist = rt.astimezone(IST)

            print(
                "CHECK:",
                "REMINDER IST:", rt_ist,
                "| NOW IST:", now_ist
            )

            # ✅ FINAL CORRECT COMPARISON (UTC vs UTC)
            if rt <= now_utc:
                print("📤 SENDING:", r["user_phone"])

                send_whatsapp(r["user_phone"], r["message"])

                tasks.update_one(
                    {"_id": r["_id"]},
                    {"$set": {"status": "done"}}
                )

        time.sleep(30)

    except Exception as e:
        print("❌ WORKER ERROR:", e)
        time.sleep(10)
