from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers
from EmailSent_App import email_sent
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator

from Applications_App.models import *
from Applications_App.views import *
from .response import *

from rest_framework.authtoken.models import Token

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator