# Generated by Django 5.1.2 on 2024-11-15 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug_url',
            field=models.SlugField(max_length=250, null=1, unique=True),
        ),
    ]
