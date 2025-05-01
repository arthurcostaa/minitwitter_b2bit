import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.created_at + datetime.timedelta(hours=1) > datetime.now():
            raise ValidationError(
                "You can't update this post."
                "It's been more than one hour since it was created."
            )
        serializer.save()

    @action(detail=True, methods=['post', 'delete'], url_path='like', url_name='like')
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_user = self.request.user

        if request.method == 'POST':
            current_user.like(post)
            data = {'detail': 'Post liked successfully'}
        elif request.method == 'DELETE':
            current_user.unlike(post)
            data = {'detail': 'Post unliked successfully'}

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='feed', url_name='feed')
    def feed(self, request):
        followed_users = request.user.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
