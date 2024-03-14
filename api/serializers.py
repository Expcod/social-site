from rest_framework.serializers import ModelSerializer

from main import models


class MyModelSerializer(ModelSerializer):
    class Meta:
        model = models.MyModel
        fields = '__all__'