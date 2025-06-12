from django.urls import path
from .views import celery_status
from .views import *


urlpatterns = [
    #단순 상태 확인용
    path('scheduler/status/', celery_status, name='celery_status'),
]
