from datetime import datetime
import time
from app.database import tasks
from app.whatsapp import send_whatsapp

print('Worker started...')
while True:
    now = datetime.now()
    reminders = tasks.find({'reminder_time': {'$lte': now}, 'status': 'pending'})
    for r in reminders:
        send_whatsapp(r['user_phone'], r['message'])
        tasks.update_one({'_id': r['_id']}, {'$set': {'status': 'done'}})
    time.sleep(60)
