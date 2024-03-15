from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import User, UserReletion, Chat, Message, PostFiles, Post, Comment, Like
from .serializers import UserSerializer, UserReletionSerializer, ChatSerializer, MessageSerializer,PostFileSerializer,PostSerializer,FollowerSerializer,FollowingSerializer,LikeSerializer,CommentSerializer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes
from django.db.models import Q
from rest_framework.decorators import api_view


class UserAPIView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if username:
            users = User.objects.filter(username__icontains=username)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserReletionAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        following = UserReletion.objects.filter(from_user=user)
        follower = UserReletion.objects.filter(to_user=user)
        following_ser = FollowingSerializer(following, many=True)
        follower_ser = FollowerSerializer(follower, many=True)
        data = {
            'following':following_ser.data,
            'follower':follower_ser.data,
        }
        return Response(data)
    
    def post(self, request):
        serializer = UserReletionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        relation = UserReletion.objects.get(pk=pk)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChatAPIView(APIView):
    def get(self, request, pk):
        chat = Chat.objects.get(pk=pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        chat = Chat.objects.get(pk=pk)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageAPIView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostView(APIView):
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def get(self, request, *args, **kwarg):
        posts = Post.objects.filter(author = request.user)
        posts_ser = PostSerializer(posts, many = True)
        return Response(posts_ser.data)
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, *args, **kwargs):

        author = request.user
        title = request.data['title']
        body = request.data['body']
        files = []
        for i in range(1,11):
            data = f'file{i}'
            if data in request.FILES:
                files.append(request.FILES[data])
        post = Post.objects.create(
            author = author,
            title = title,
            body = body,
        )
        for i in files:
                PostFiles.objects.create(
                    post = post,
                    file = i
                )
        post_ser = PostSerializer(post)
        return Response(post_ser.data)
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, id, *args, **kwargs):
        post = Post.objects.filter(author = request.user).get(id = id)
        if request.data['title']:
            post.title = request.data['title']
        if request.data['body']:
            post.title = request.data['body']
        post.save()
        post_ser = PostSerializer(post)
        return Response(post_ser.data)
    

    def delete(self, request, id, *args, **kwargs):
        post = Post.objects.filter(author = request.user).get(id = id)
        post.delete()
        return Response({'success':'post has been deleted'})

class CommentView(APIView):
    def get(self, request, id, *args, **kwargs): #id => post_id
        post = Post.objects.get(id = id)
        comments = Comment.objects.filter(post = post).order_by('-date')
        comments_ser = CommentSerializer(comments, many = True)
        return Response(comments_ser.data)
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, id, *args, **kwargs): #id => post_id
        post = Post.objects.get(id = id)
        text = request.data['text']
        if request.data.get('reply'):
            reply = Comment.objects.get(id = request['reply_id'])
            comment = Comment.objects.create(
                author = request.user,
                post = post,
                text = text,
                reply = reply
            )
        else:
            comment = Comment.objects.create(
                author = request.user,
                post = post,
                text = text,
            )
        comment_ser = CommentSerializer(comment)
        return Response({'success':'created', 'comment':comment_ser.data})
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, id, *args, **kwargs): # id => comment_id
        try:
            comment = Comment.objects.filter(author = request.user).get(id = id)
            comment.text = request.data['text']
            comment.save()
            comment_ser = CommentSerializer(comment)
            return Response({'succes': 'change has been saved', 'comment': comment_ser.data})
        except:
            return Response({'fatal': f'no comment with id {id}'})
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def delete(self, request, id, *args, **kwargs):
        comment = Comment.objects.filter(author = request.user).get(id = id)
        comment.delete()
        return Response({'success':'comment has been deleted'})



class LikeView(APIView):
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def get(self, request, *args, **kwargs):
        reactions = Like.objects.filter(author = request.user).order_by('status')
        reactions_ser = LikeSerializer(reactions, many = True)
        return Response({'all reactions you gave' : reactions_ser.data})
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id = id)
            status = request.data['status']
            if status.lower() == 'true':
                reaction = True
            elif status.lower() == 'false':
                reaction = False
            else: 
                return Response({"error": "you didn't give a boolean for the status"})
            data = Like.objects.create(
                author = request.user,
                post = post,
                status = reaction,
            )
            like_ser = LikeSerializer(data)
            return Response({'success': 'created emotion', 'emotion':like_ser.data})
        except:
            return Response({'fatal': f'no post with id {id}'})
    

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id = id)
            emotion = Like.objects.filter(author = request.user).get(post = post)
            status = request.data['status']
            if status.lower() == 'true':
                reaction = True
            elif status.lower() == 'false':
                reaction = False
            emotion.status = reaction
            emotion.save()
            emotion_ser = LikeSerializer(emotion)
            return Response({'success':'change has been saved', 'updated_to': emotion_ser.data})
        except:
            return Response({'fatal': f'no post with id {id}'})
    
    
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def delete(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id = id)
            emotion = Like.objects.filter(author = request.user).get(post = post)
            emotion.delete()
            return Response({'success':'emotion has been deleted'})
        except:
            return Response({'fatal': f'no post with id {id}'})

#filter posts
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def filter_post(request):
    search = request.data['search']
    posts = Post.objects.filter(author = request.user).filter(Q(title__icontains = search) | Q(body__icontains = search))
    posts_ser = PostSerializer(posts, many = True)
    return Response (posts_ser.data)

