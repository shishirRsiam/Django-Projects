from .Authentication_App_Import import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/auth/', ),
    path('api/register/', UserRegistrationApiView.as_view(), name='register'),
    path('api/post/', JobPostApiViewSet.as_view(), name='post'),
    path('api/post/apply/<int:id>/', JobApplyApiView.as_view(), name='job_apply'),
    path('api/post/<int:id>/', JobPostApiViewSet.as_view(), name='post_detail'),
    path('api/profile/', UserView.as_view(), name='profile'),
    path('api/update/profile/', UserUpdateView.as_view(), name='update_profile'),
    path('api/auth/', UserView.as_view(), name='auth'),
    path('api/login/', LoginApiView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/accounts/activate/<str:idb64>/<str:token>/', ActivateAccountView.as_view(), name='login'),
]