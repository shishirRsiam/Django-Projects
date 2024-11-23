from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='edit_address'),
    path('logout/', views.logout_view, name='logout'),
    path('reset/password/', views.password_reset, name='change_password'),
    path('reset/password/', views.password_reset, name='password_reset'),
    path('signup/', views.sign_up, name='sign_up'),
]
