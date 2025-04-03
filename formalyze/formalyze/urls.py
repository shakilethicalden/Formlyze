
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Formalyze",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/form/', include('form.urls')),
    path('api/users/', include('users.urls')),
    path("api/", include('google_login.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
