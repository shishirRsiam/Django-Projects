# Generated by Django 5.1.2 on 2024-12-26 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication_App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='resume',
        ),
    ]
