"""GTD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import register_user, login_user, logout_user
from tasks.views import list_task, create_task, filtered_list_task, readiness_filter, focus_filter, done_filter
from .views import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('list/', list_task, name='list_task'),
    path('filtered_list/', filtered_list_task, name='filtered_list_task'),
    path('readiness_filter/<str:filter>/', readiness_filter, name='readiness_filter'),
    path('focus_filter/', focus_filter, name='focus_filter'),
    path('done_filter/', done_filter, name='done_filter'),
    path('create_task/', create_task, name='create_task'),
    path('api/', include('api.urls')),
    path('', dashboard, name='dashboard'),
]
