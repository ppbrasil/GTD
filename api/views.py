from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, authentication, response
from rest_framework.views import APIView
from django.shortcuts import get_list_or_404, get_object_or_404
from tasks.models import Task
from tasks.serializers import TaskSerializer
from api.authentication import TokenAuthentication

# Create your views here.

class TaskDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all().filter(is_active=True)
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

class TaskListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all().filter(is_active=True)
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

class TaskCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

      
class TaskUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()
        return super().perform_update(serializer)


class TaskDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_active = False
        task.save()
        serializer = TaskSerializer(task)
        return response.Response(serializer.data)

class TaskToggleFocusAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.focus = not task.focus
        task.save()
        serializer = TaskSerializer(task)
        return response.Response(serializer.data)

class TaskToggleDoneAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    authentication_classes = [
        authentication.SessionAuthentication, 
        TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.done = not task.done
        task.save()
        serializer = TaskSerializer(task)
        return response.Response(serializer.data)

class TaskListFocusedAPIView(TaskListAPIView):
    def get_queryset(self):
        return Task.objects.filter(focus=True)

class TaskListDoneAPIView(TaskListAPIView):
    def get_queryset(self):
        return Task.objects.filter(done=True)

class TaskListReadinessInboxAPIView(TaskListAPIView):
    def get_queryset(self):
        return Task.objects.filter(readiness='inbox')

class TaskListReadinessSometimeAPIView(TaskListAPIView):
    def get_queryset(self):
        return Task.objects.filter(readiness='sometime')

class TaskListReadinessAnytimeAPIView(TaskListAPIView):
    def get_queryset(self):
        return Task.objects.filter(readiness='anytime')

class TaskListReadinessWaitingAPIView(TaskListAPIView):
    def get_queryset(self):
        return Task.objects.filter(readiness='waiting')
