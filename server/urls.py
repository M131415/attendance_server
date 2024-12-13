from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path

urlpatterns = [
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