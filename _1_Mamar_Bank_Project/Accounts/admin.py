from django.contrib import admin
from . import models
admin.site.register(models.UserAddress)
admin.site.register(models.UserBankAccount)

