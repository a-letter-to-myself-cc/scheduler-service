from django.urls import path, include
from schedule.views import health_check

urlpatterns = [
    path("", include("schedule.urls")), # 내부 API만 씀
    path('health/', health_check),  #헬스체크용
]
