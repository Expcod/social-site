from django.urls import path
from .views import UserAPIView, UserReletionAPIView, ChatAPIView, MessageAPIView, PostView, LikeView,CommentView,filter_post

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    path('user-reletions/', UserReletionAPIView.as_view(), name='user-reletion-list'),
    path('user-reletions/<int:pk>/', UserReletionAPIView.as_view(), name='user-reletion-detail'),
    path('chats/', ChatAPIView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatAPIView.as_view(), name='chat-detail'),
    path('messages/', MessageAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageAPIView.as_view(), name='message-detail'),
    #post
    path('post', PostView.as_view(), name = 'post-list-create'),
    path('post/<int:id>', PostView.as_view(), name = 'update-delete'),
    #post-filter
    path('search', filter_post),
    #comment
    path('comment/<int:id>', CommentView.as_view()),
    #like
    path('like', LikeView.as_view(), name = 'list'),
    path('like/<int:id>', LikeView.as_view(), name = 'post-delete-put')
]
