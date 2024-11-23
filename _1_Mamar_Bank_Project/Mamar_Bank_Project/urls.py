from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Accounts.urls')),
    path('', include('Transactions.urls')),
    path('', include('Core.urls')),
]
