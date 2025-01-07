from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path

# To documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion de la API",
      default_version='v0.1',
      description="Endpoints que se pueden utilizar para la API de Asistencia",
      contact=openapi.Contact(email="l19520555@chilpancingo.tecnm.mx"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('users/',include('apps.users.api.routers')),
    path('courses/',include('apps.groups.api.routers')),
    path('attendances/',include('apps.attendances.api.routers')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]