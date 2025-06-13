from scheduler_service.celery import app
from celery import shared_task
import requests
import os

# 루틴 API URL
ROUTINE_SERVICE_URL = os.getenv("ROUTINE_SERVICE_URL", "http://routine-service:8003/api/routines/today/")

@shared_task(name="schedule.tasks.send_letter_reminders")
def send_letter_reminders():
    print("✅ 루틴 알림 작업 실행됨!")

    try:
        response = requests.get(ROUTINE_SERVICE_URL)
        response.raise_for_status()
        routines = response.json()
    except Exception as e:
        print("❌ 루틴 요청 실패:", e)
        return

    for routine in routines:
        print(f"📬 예약된 루틴 → {routine['username']} | {routine['time']} | {routine['email']}")
        
        # app.send_task 대신 → shared_task를 통해 명시적 등록 없이 처리
        from celery import current_app
        current_app.send_task(
            'notify.send_notification',
            args=[routine['email'], routine['username'], routine['time']],
            queue='notification_queue'
        )
