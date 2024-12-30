from rest_framework import serializers
from .models import JobPost, Applied
from django.contrib.auth.models import User

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ('user',)
        
class ApplySerializer(serializers.ModelSerializer):
    job = JobPostSerializer()
    class Meta:
        model = Applied
        fields = '__all__'
        read_only_fields = ('user',)



