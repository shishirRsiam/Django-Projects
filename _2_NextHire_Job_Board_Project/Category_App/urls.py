from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/categories/', CategoryViewSet.as_view(), name='categories'),
]
