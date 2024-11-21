from rest_framework.routers import DefaultRouter
from apps.groups.api.viewsets.general_views import *
from apps.groups.api.viewsets.group_viewset import ClassGroupViewSet

router = DefaultRouter()

router.register(r'subjects', SubjectViewSet, basename = 'subjects')
router.register(r'departaments', DepartamentViewSet, basename = 'departaments')
router.register(r'periods', PeriodViewSet, basename = 'periods')
router.register(r'school_rooms', SchoolRoomViewSet, basename = 'school_rooms')
router.register(r'class_groups', ClassGroupViewSet, basename = 'class_groups')
router.register(r'schedules', ScheduleViewSet, basename = 'schedule')

urlpatterns = router.urls