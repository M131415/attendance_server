from rest_framework.routers import DefaultRouter
from apps.groups.api.viewsets.general_views import *

router = DefaultRouter()

router.register(r'subjects', SubjectViewSet, basename = 'subjects')

urlpatterns = router.urls