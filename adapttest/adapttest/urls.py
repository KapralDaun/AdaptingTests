from django.contrib import admin

from testing.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('testing.urls'))
]

handler404 = pageNotFound
