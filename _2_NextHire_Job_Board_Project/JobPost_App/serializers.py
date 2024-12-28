from rest_framework import serializers
from .models import JobPost
from django.contrib.auth.models import User

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ('user',)