from django.contrib.auth.models import User
from .models import UserProfile


from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers

from EmailSent_App import email_sent

from django.contrib.auth import authenticate, login, logout



from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny