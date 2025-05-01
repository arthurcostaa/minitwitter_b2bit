from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser
from .permissions import IsOwnerOrReadOnly
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], url_path='follow', url_name='follow')
    def follow(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        current_user = self.request.user

        if current_user == user:
            return Response(
                {'detail': "You can't follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_user.follow(user)

        return Response(
            {'detail': 'User followed successfully.'}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['delete'], url_path='unfollow', url_name='unfollow')
    def unfollow(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        current_user = self.request.user

        if current_user == user:
            return Response(
                {'detail': "You can't unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_user.unfollow(user)

        return Response(
            {'detail': 'User unfollowed successfully.'}, status=status.HTTP_200_OK
        )
