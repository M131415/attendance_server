from rest_framework.routers import DefaultRouter
from apps.groups.api.viewsets.general_views import *

router = DefaultRouter()

router.register(r'subjects', SubjectViewSet, basename = 'subjects')
router.register(r'departaments', DepartamentViewSet, basename = 'departaments')
router.register(r'periods', PeriodViewSet, basename = 'periods')
router.register(r'school_rooms', SchoolRoomViewSet, basename = 'school_rooms')

urlpatterns = router.urls