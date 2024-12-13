from rest_framework.routers import DefaultRouter
from apps.groups.api.viewsets.general_views import *
from apps.groups.api.viewsets.course_viewset import CourseViewSet
from apps.groups.api.viewsets.group_viewset import GroupViewSet

router = DefaultRouter()

router.register(r'subjects', SubjectViewSet, basename = 'subjects')
router.register(r'departments', DepartamentViewSet, basename = 'departments')
router.register(r'periods', PeriodViewSet, basename = 'periods')
router.register(r'school_rooms', SchoolRoomViewSet, basename = 'school_rooms')
router.register(r'groups', GroupViewSet, basename = 'groups')
router.register(r'schedules', ScheduleViewSet, basename = 'schedules')
router.register(r'courses', CourseViewSet, basename = 'courses')

urlpatterns = router.urls