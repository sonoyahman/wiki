from django.contrib import admin
from django.urls import path, include
from .views import kensakufunc
from .views import mainkensakufunc
from .views import MainClass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kensaku/', kensakufunc),
    path('mainkensaku/', mainkensakufunc),
    path('main/', MainClass.as_view()),
]