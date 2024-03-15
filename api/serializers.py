from rest_framework import serializers
from main.models import User, UserReletion, Chat, Message, Post, PostFiles, Comment, Like

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


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReletion
        fields = ['from_user',]
        depth=1


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReletion
        fields = ['to_user',]
        depth=1

class ChatListSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer(read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'last_message', 'unread_messages', 'users']

class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFiles
        fields = ['file']

class PostSerializer(serializers.ModelSerializer):
    files = PostFileSerializer(many = True, read_only = True)
    class Meta:
        model = Post
        fields = ['id','title', 'body', 'files']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =['author', 'text', 'date']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'status']