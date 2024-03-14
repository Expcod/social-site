from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from . import serializers


class MyModelView(ModelViewSet):
    queryset = models.MyModel.objects.all() 
    serializer_class = serializers.MyModelSerializer


    def get_queryset(self):
        queryset = models.MyModel.objects.all()
        return queryset
 
@api_view(['GET'])
def list_data(request):
    return Response([])