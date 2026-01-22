from datetime import datetime
import time
from app.database import tasks
from app.whatsapp import send_whatsapp
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

print('Worker started...')
print("NOW:", datetime.now())
print("UTC NOW:", datetime.now(timezone.ist))
now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
print("IST NOW:", now_ist)


while True:
    now = datetime.now()
    reminders = tasks.find({'reminder_time': {'$lte': now}, 'status': 'pending'})
    for r in reminders:
        send_whatsapp(r['user_phone'], r['message'])
        tasks.update_one({'_id': r['_id']}, {'$set': {'status': 'done'}})
    time.sleep(60)
