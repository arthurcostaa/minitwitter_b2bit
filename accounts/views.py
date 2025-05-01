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

    @action(
        detail=True, methods=['post', 'delete'], url_path='follow', url_name='follow'
    )
    def follow(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        current_user = self.request.user

        if current_user == user:
            if request.method == 'POST':
                data = {'detail': "You can't follow yourself."}
            elif request.method == 'DELETE':
                data = {'detail': "You can't unfollow yourself."}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            current_user.follow(user)
            data = {'detail': 'User followed successfully.'}
        elif request.method == 'DELETE':
            current_user.unfollow(user)
            data = {'detail': 'User unfollowed successfully.'}
        return Response(data, status=status.HTTP_200_OK)
