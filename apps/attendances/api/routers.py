from rest_framework.routers import DefaultRouter
from apps.attendances.api.viewsets.enrolloment_viewset import EnrollomentViewSet
from apps.attendances.api.viewsets.attendance_viewset import AttendanceViewSet

router = DefaultRouter()

router.register(r'enrollments', EnrollomentViewSet, basename = 'enrollments')
router.register(r'attendances', AttendanceViewSet, basename = 'attendances')

urlpatterns = router.urls