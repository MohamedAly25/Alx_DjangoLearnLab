from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User
from posts.models import Post
from posts.serializers import PostSerializer
from notifications.models import Notification

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user_to_follow == request.user:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.following.filter(id=user_id).exists():
        return Response({'error': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.following.add(user_to_follow)
    Notification.objects.create(
        recipient=user_to_follow,
        actor=request.user,
        verb='followed you',
        target=user_to_follow
    )
    return Response({'message': f'Now following {user_to_follow.username}'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.following.filter(id=user_id).exists():
        return Response({'error': 'Not following this user'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.following.remove(user_to_unfollow)
    return Response({'message': f'Unfollowed {user_to_unfollow.username}'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
