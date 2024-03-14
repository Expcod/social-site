from rest_framework import serializers
from main.models import User, UserReletion, Chat, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']

class UserReletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReletion
        fields = ['from_user', 'to_user']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
