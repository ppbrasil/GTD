from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, authentication, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from tasks.models import Task, SimpleTag, Person, Place, Area, Project
from tasks.serializers import TaskSerializer, SimpleTagSerializer, PersonSerializer, PlaceSerializer, AreaSerializer, ProjectSerializer, TaskTreeSerializer
from accounts.serializers import AccountCreationSerializer, AccountDetailsSerializer, LoginSerializer
from api.authentication import TokenAuthentication
from api.permissions import IsObjectOwner

import logging

logger = logging.getLogger(__name__)

# Create your views here.

class CreateAccountView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = AccountCreationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.validated_data
            return Response(AccountDetailsSerializer(user, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    http_method_names = ['post']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsObjectOwner]

    def post(self, request, format=None):
        token = request.auth
        token.delete()
        return Response(status=status.HTTP_200_OK)

class TaskCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class TaskDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all().filter(is_active=True)
    serializer_class = TaskSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    lookup_field = 'pk'
    permission_classes = [
        permissions.IsAuthenticated,
        IsObjectOwner,
    ]

class TaskUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    queryset = Task.objects.all().filter(is_active=True)
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = 'pk'

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

class TaskDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.is_active == False:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user != task.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.is_active = False
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

class TaskToggleFocusAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsObjectOwner]
    queryset = Task.objects.all().filter(is_active=True)
    lookup_field = 'pk'
    serializer_class = TaskSerializer

    def patch(self, request, pk):
        instance = self.get_object()
        instance.focus = not instance.focus
        instance.save()
        return Response(status=status.HTTP_200_OK)

class TaskToggleDoneAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsObjectOwner]
    queryset = Task.objects.all().filter(is_active=True)
    lookup_field = 'pk'
    serializer_class = TaskSerializer

    def patch(self, request, pk):
        instance = self.get_object()
        instance.done = not instance.done
        instance.save()
        return Response(status=status.HTTP_200_OK)

class TaskListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = TaskSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            is_active=True,
            user=user,
            )

class TaskListReadinessInboxAPIView(TaskListAPIView):
    def get_queryset(self):
        return super().get_queryset().filter(readiness='inbox')

class TaskListReadinessSometimeAPIView(TaskListAPIView):
    def get_queryset(self):
        return super().get_queryset().filter(readiness='sometime')

class TaskListReadinessAnytimeAPIView(TaskListAPIView):
    def get_queryset(self):
        return super().get_queryset().filter(readiness='anytime')

class TaskListReadinessWaitingAPIView(TaskListAPIView):
    def get_queryset(self):
        return super().get_queryset().filter(readiness='waiting')

class TaskListFocusedAPIView(TaskListAPIView):
    def get_queryset(self):
        return super().get_queryset().filter(focus=True)

class TaskListDoneAPIView(TaskListAPIView):
    def get_queryset(self):
        return super().get_queryset().filter(done=True)

class SimpleTagCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = SimpleTagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class SimpleTagDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = SimpleTag.objects.all().filter(is_active=True)
    serializer_class = SimpleTagSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get(self, request, pk):
        try:
            tag = SimpleTag.objects.get(pk=pk)
            if tag.is_active == False or request.user != tag.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = SimpleTagSerializer(tag)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)    
    
class SimpleTagUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    queryset = SimpleTag.objects.all().filter(is_active=True)
    serializer_class = SimpleTagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = 'pk'

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

class SimpleTagListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = SimpleTagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SimpleTag.objects.filter(
            user=self.request.user,
            is_active=True
        )

class SimpleTagDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def patch(self, request, pk):
        tag = get_object_or_404(SimpleTag, pk=pk)
        if tag.is_active == False or request.user != tag.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        tag.is_active = False
        tag.save()
        serializer = SimpleTagSerializer(tag)
        return Response(serializer.data)
    
class PersonCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = PersonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class PersonDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Person.objects.all().filter(is_active=True)
    serializer_class = PersonSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
            if person.is_active == False or request.user != person.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = SimpleTagSerializer(person)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        
class PersonUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    queryset = Person.objects.all().filter(is_active=True)
    serializer_class = PersonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = 'pk'

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

class PersonListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = PersonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Person.objects.filter(
            user=self.request.user,
            is_active=True
        )

class PersonDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def patch(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        if person.is_active == False or request.user != person.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        person.is_active = False
        person.save()
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    
class PlaceCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class PlaceDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Place.objects.all().filter(is_active=True)
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get(self, request, pk):
        try:
            place = Place.objects.get(pk=pk)
            if place.is_active == False or request.user != place.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = PlaceSerializer(place)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        
class PlaceUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        return Place.objects.filter(user=self.request.user, is_active=True)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

class PlaceListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Place.objects.filter(
            user=self.request.user,
            is_active=True
        )
    
class PlaceDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def patch(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        if place.is_active == False or request.user != place.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        place.is_active = False
        place.save()
        serializer = PlaceSerializer(place)
        return Response(serializer.data)
    
class AreaCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = AreaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class AreaDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Area.objects.all().filter(is_active=True)
    serializer_class = AreaSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get(self, request, pk):
        try:
            area = Area.objects.get(pk=pk)
            if area.is_active == False or request.user != area.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = AreaSerializer(area)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        
class AreaUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    serializer_class = AreaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        return Area.objects.filter(user=self.request.user, is_active=True)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

class AreaListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = AreaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Area.objects.filter(
            user=self.request.user,
            is_active=True
        )
    
class AreaDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def patch(self, request, pk):
        area = get_object_or_404(Area, pk=pk)
        if area.is_active == False or request.user != area.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        area.is_active = False
        area.save()
        serializer = AreaSerializer(area)
        return Response(serializer.data)
    
class ProjectCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class ProjectDetailAPIView(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = Project.objects.all().filter(is_active=True)
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            if project.is_active == False or request.user != project.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)  
        
class ProjectUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user, is_active=True)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

class ProjectListAPIView(generics.ListAPIView):
    http_method_names = ['get']
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            user=self.request.user,
            is_active=True
        )
    
class ProjectDisableAPIView(APIView):
    http_method_names = ['patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def patch(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.is_active == False or request.user != project.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        project.is_active = False
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

'''
Views to handle the tree mapping
'''

class TaskTreeView(APIView):
    def get(self, request):
        areas = Area.objects.filter(is_active=True)
        serializer = TaskTreeSerializer(areas, many=True)
        return Response(serializer.data)
