from datetime import datetime
import time
from app.database import tasks
from app.whatsapp import send_whatsapp
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

print('Worker started...')
print("NOW:", datetime.now())
IST = ZoneInfo("Asia/Kolkata")



while True:
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc.astimezone(ZoneInfo("Asia/Kolkata"))
    print("NOW:", now_ist)
    reminders = tasks.find({'reminder_time': {'$lte': now_ist}, 'status': 'pending'})
    for r in reminders:
        send_whatsapp(r['user_phone'], r['message'])
        tasks.update_one({'_id': r['_id']}, {'$set': {'status': 'done'}})
    time.sleep(60)
