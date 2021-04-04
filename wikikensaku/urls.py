from django.contrib import admin
from django.urls import path, include
from .views import mainkensakufunc
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mainkensaku/', mainkensakufunc),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)