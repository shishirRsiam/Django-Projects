# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationApiView, LoginApiView

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', UserRegistrationApiView.as_view(), name='register'),
    path('api/login/', LoginApiView.as_view(), name='login'),
]
 