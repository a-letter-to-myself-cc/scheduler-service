# from celery import Celery
# from celery.schedules import crontab
# from schedule.tasks import send_letter_reminders
# from celery import shared_task
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler_service.settings')

# app = Celery('scheduler_service')

# # 1. settings.py의 CELERY_* 먼저 읽기
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # 2. ✅ task별 라우팅 설정
# app.conf.task_routes = {
#     'schedule.tasks.send_letter_reminders': {'queue': 'scheduler_queue'},
# }

# # 3. 자동 tasks 로딩
# app.autodiscover_tasks()
# app.conf.timezone = 'Asia/Seoul'
# app.conf.enable_utc = False

# # 4. Celery Beat 주기 등록
# app.conf.beat_schedule = {
#     'send-routine-reminder-every-minute': {
#         'task': 'schedule.tasks.send_letter_reminders',
#         'schedule': crontab(minute='*/1'),
#     },
# }


# scheduler_service/celery.py

from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler_service.settings')

app = Celery('scheduler_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['schedule'])  # ✅ schedule 앱 내부의 tasks.py 자동탐색
app.conf.timezone = 'Asia/Seoul'
app.conf.enable_utc = False

app.conf.beat_schedule = {
    'send-routine-reminder-every-minute': {
        'task': 'schedule.tasks.send_letter_reminders',
        'schedule': crontab(minute='*/1'),
    },
}
