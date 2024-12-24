from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from EmailSent_App import email_sent
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator

from Applications_App.models import *
from Applications_App.views import *


from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes