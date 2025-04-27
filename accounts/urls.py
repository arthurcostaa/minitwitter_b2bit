from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
