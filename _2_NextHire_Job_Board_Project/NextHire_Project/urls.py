from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Authentication_App.urls')),
    path('', include('Category_App.urls')),
]
