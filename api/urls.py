from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import TaskListAPIView, TaskDetailAPIView, TaskCreateAPIView, TaskUpdateAPIView, TaskListAPIView

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('task/<int:pk>', TaskDetailAPIView.as_view(), name='task-detail'),
    path('task/create/', TaskCreateAPIView.as_view(), name='create-task'),
    path('task/update/<int:pk>', TaskUpdateAPIView.as_view(), name='task-update'),
    path('task/', TaskListAPIView.as_view(), name='task-list'),
]