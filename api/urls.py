from django.urls import path
from .views import task_details

urlpatterns = [
    path('', task_details),
]
