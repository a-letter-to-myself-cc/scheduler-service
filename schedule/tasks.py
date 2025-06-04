from celery import Celery
import requests
from celery import shared_task
import os

# @shared_task
# def send_letter_reminders():
    
#     #현재 시간 정보 가져오기
#     from django.utils.timezone import now, localtime
#     from datetime import timedelta

#     now_dt = localtime(now()).replace(second=0, microsecond=0)
#     today = now_dt.strftime("%A") # Monday, Tuesday ...
#     current_day = now_dt.day # 1~31
#     current_time = now_dt.time()

#     # ±1분 오차 허용
#     window_start = (now_dt - timedelta(minutes=1)).time()
#     window_end = (now_dt + timedelta(minutes=1)).time()

#     print("✅ 루틴 알림 작업 실행됨!")
#     print(f"현재 시간: {current_time}")
#     print(f"알림 시간 범위: {window_start} ~ {window_end}")
#     print(f"오늘 요일: {today}, 날짜: {current_day}")

#     # 🟡 루틴 정보 API 호출 (routine-service)
#     ROUTINE_API_URL = os.getenv("ROUTINE_SERVICE_URL", "http://localhost:8303/api/routines/today/")
#     try:
#         response = requests.get(ROUTINE_API_URL)
#         if response.status_code != 200:
#             print("❌ 루틴 서비스 응답 실패:", response.status_code)
#             return
#         routines = response.json()
#     except Exception as e:
#         print("❌ 루틴 API 요청 실패:", e)
#         return

#     # 🔵 notification-service로 task 큐 전달
#     from notify.tasks import send_notification

#     for routine in routines:
#         print(f"📌 루틴 확인 → {routine}")
#         send_notification.delay(
#             routine['user_email'],
#             routine['username'],
#             routine['time']
#         )
        
        
#마이크로서비스 테스트용!!!!!!

# 환경 변수로 설정된 Celery 브로커 주소 사용
NOTIFY_QUEUE_BROKER = os.getenv("CELERY_BROKER_URL", "amqp://localhost")

# 직접 task 인스턴스를 만들지 않고 전역 app 이용
app = Celery('scheduler_service')
app.conf.broker_url = NOTIFY_QUEUE_BROKER

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8005/notify/email/")
ROUTINE_SERVICE_URL = os.getenv("ROUTINE_SERVICE_URL", "http://routine_service:8003/api/routines/today/")

@shared_task
def send_letter_reminders():
    print("✅ 테스트용 루틴 알림 작업 실행됨!")

    try:
        response = requests.get(ROUTINE_SERVICE_URL)
        routines = response.json()
    except Exception as e:
        print("❌ 루틴 요청 실패:", e)
        return

    for routine in routines:
        print(f"📬 예약된 루틴 → {routine['username']} | {routine['time']} | {routine['email']}")
        
        # 🔥 큐로 task 전송: 문자열로 task 경로 지정
        app.send_task(
            'notify.tasks.send_notification',
            args=[routine['email'], routine['username'], routine['time']],
            queue='notification_queue'  # 👈 반드시 지정해줘야 함!
        )
        
def send_notification(routine):
    try:
        response = requests.post(NOTIFICATION_SERVICE_URL, json={
            "email": routine.user.email,
            "username": routine.user.username,
            "time": str(routine.time)
        })
        print(f"📬 이메일 요청 완료 → {routine.user.email}, 응답 코드: {response.status_code}")
    except Exception as e:
        print("❌ 이메일 요청 실패:", e)
        