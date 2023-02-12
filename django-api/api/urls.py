from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    TaskDetailAPIView, 
    TaskCreateAPIView,
    TaskUpdateAPIView,
    TaskToggleFocusAPIView,
    TaskToggleDoneAPIView,
    TaskListFocusedAPIView,
    TaskListDoneAPIView,
    TaskListReadinessInboxAPIView,
    TaskListReadinessSometimeAPIView,
    TaskListReadinessAnytimeAPIView,
    TaskListReadinessWaitingAPIView,
    TaskDisableAPIView,
    TaskListAPIView,
    CreateAccountView,
    LogoutView,
)

urlpatterns = [
    path('account/create/', CreateAccountView.as_view(), name='account_create'),
    path('auth/', obtain_auth_token),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('task/<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('task/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_update'),
    path('task/toggle-focus/<int:pk>/', TaskToggleFocusAPIView.as_view(), name='task_toggle_focus'),
    path('task/toggle-done/<int:pk>/', TaskToggleDoneAPIView.as_view(), name='task_toggle_done'),
    path('task/focused/', TaskListFocusedAPIView.as_view(), name='focused_task_list'),
    path('task/done/', TaskListDoneAPIView.as_view(), name='done_task_list'),
    path('task/inbox/', TaskListReadinessInboxAPIView.as_view(), name='inbox_task_list'),
    path('task/sometime/', TaskListReadinessSometimeAPIView.as_view(), name='sometime_task_list'),
    path('task/anytime/', TaskListReadinessAnytimeAPIView.as_view(), name='anytime_task_list'),
    path('task/waiting/', TaskListReadinessWaitingAPIView.as_view(), name='waiting_task_list'),
    path('task/disable/<int:pk>/', TaskDisableAPIView.as_view(), name='task_disable'),
    path('task/', TaskListAPIView.as_view(), name='task_list'),
]