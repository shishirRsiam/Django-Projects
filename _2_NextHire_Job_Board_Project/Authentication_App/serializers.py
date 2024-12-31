from rest_framework import serializers
from . import models
from Category_App.serializers import CategorySerializer

from django.contrib.auth.models import User

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserSerializer(serializers.ModelSerializer):
    skill = CategorySerializer(many=True)
    user = SimpleUserSerializer()
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        read_only_fields = ['user']
