from django.urls import path
from .views import celery_status

urlpatterns = [
    path('scheduler/status/', celery_status, name='celery_status'),
    path('health/', views.health_check),
]
