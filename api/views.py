from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, authentication
from django.shortcuts import get_list_or_404
from tasks.models import Task
from tasks.serializers import TaskSerializer
import requests

# Create your views here.

class TaskDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        authentication.TokenAuthentication,
    ]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

class TaskListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

class TaskCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        authentication.TokenAuthentication,
    ]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

      
class TaskUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['post']
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        authentication.TokenAuthentication,
    ]
    lookup_field = 'pk'
    
    def perform_create(self, serializer):
        data = self.request.data
        serializer.save(data=data)
        return super().perform_update(serializer)
