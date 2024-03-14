from django.urls import path
from .views import UserAPIView, UserReletionAPIView, ChatAPIView, MessageAPIView

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    path('user-reletions/', UserReletionAPIView.as_view(), name='user-reletion-list'),
    path('user-reletions/<int:pk>/', UserReletionAPIView.as_view(), name='user-reletion-detail'),
    path('chats/', ChatAPIView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatAPIView.as_view(), name='chat-detail'),
    path('messages/', MessageAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageAPIView.as_view(), name='message-detail'),
]
