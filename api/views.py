from rest_framework.decorators import api_view
from rest_framework.response import Response

from tasks.models import Task
from tasks.serializers import TaskSerializer

# Create your views here.

@api_view(['GET'])
def task_details(request, *args, **kwargs):
    #instance = Task.objects.get(id=id)
    instance = Task.objects.all().order_by('?').first()
    if instance:
        data = TaskSerializer(instance).data
    return Response(data)

