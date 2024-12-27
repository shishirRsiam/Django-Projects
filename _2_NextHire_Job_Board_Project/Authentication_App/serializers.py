from rest_framework import serializers
from . import models

from django.contrib.auth.models import User

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    class Meta:
        model = models.UserProfile
        fields = '__all__'
