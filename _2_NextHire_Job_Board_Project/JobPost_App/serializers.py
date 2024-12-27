from rest_framework import serializers
from .models import JobPost
from django.contrib.auth.models import User

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ["user", "title", "description", "company", "location", "salary", "type", "deadline"]
        read_only_fields = ["user",]
