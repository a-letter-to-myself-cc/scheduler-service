import requests
from celery import shared_task
import os
from django.utils.timezone import now, localtime
from datetime import timedelta

@shared_task
def send_letter_reminders():
    """
    매 분마다 실행되는 루틴 알림 전송 태스크
    """
    now_dt = localtime(now()).replace(second=0, microsecond=0)
    today = now_dt.strftime("%A")
    current_time = now_dt.strftime("%H:%M")

    print(f"✅ 루틴 알림 작업 실행 - {now_dt}")
    print(f"현재 요일: {today}, 시간: {current_time}")

    # 루틴 서비스 API 호출
    ROUTINE_API_URL = os.getenv("ROUTINE_SERVICE_URL", "http://routine_service:8000/api/routines/today/")
    try:
        response = requests.get(ROUTINE_API_URL)
        if response.status_code != 200:
            print(f"❌ 루틴 서비스 응답 실패: {response.status_code}")
            return
        routines = response.json()
        print(f"📋 조회된 루틴 수: {len(routines)}")
    except Exception as e:
        print(f"❌ 루틴 API 요청 실패: {str(e)}")
        return

    # 알림 서비스로 전송
    NOTIFICATION_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8000/notify/")
    for routine in routines:
        try:
            response = requests.post(NOTIFICATION_URL, json={
                "email": routine["email"],
                "username": routine["username"],
                "routine_time": routine["time"]
            })
            print(f"📬 알림 전송 완료 → {routine['username']} ({routine['email']})")
        except Exception as e:
            print(f"❌ 알림 전송 실패: {str(e)}")
        