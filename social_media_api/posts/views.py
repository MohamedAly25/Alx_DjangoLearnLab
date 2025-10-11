from rest_framework import viewsets, permissions, status, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create notification
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post
            )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
        return Response({'message': 'Post liked'})
    else:
        return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({'message': 'Post unliked'})
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Like.DoesNotExist:
        return Response({'error': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)


class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
