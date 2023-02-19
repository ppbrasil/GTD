from django.http import Http404
from rest_framework import generics, permissions, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.db import models

def enable_task_required(func):
    class DecoratedView(generics.UpdateAPIView):
        http_method_names = ['patch']
        queryset = func.queryset
        serializer_class = func.serializer_class
        authentication_classes = func.authentication_classes
        permission_classes = func.permission_classes
        lookup_field = func.lookup_field

        def get_serializer(self, *args, **kwargs):
            kwargs['partial'] = True
            return super().get_serializer(*args, **kwargs)

        def get_queryset(self):
            queryset = super().get_queryset().exclude(is_active=False)
            if isinstance(queryset, models.QuerySet):
                return queryset
            else:
                for task in queryset:
                    if task.is_active == False:
                        queryset.remove(task)
                return queryset

        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            if instance.is_active == False:
                raise Http404
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    DecoratedView.__name__ = func.__name__
    DecoratedView.__doc__ = func.__doc__
    DecoratedView.__module__ = func.__module__
    return DecoratedView
