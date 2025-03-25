
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/form/', include('form.urls')),
    path('api/users/', include('users.urls')),
]
