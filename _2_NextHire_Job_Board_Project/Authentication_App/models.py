from django.contrib.auth.models import User
from django.db import models
from Category_App.models import Category

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Category)
    resume = models.CharField(max_length=400, null=1)
    bio = models.CharField(max_length=400, null=1)

    ROLE_CHOICES = [
        ('Job Seeker', 'Job Seeker'),
        ('Employer', 'Employer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    