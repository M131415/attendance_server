from rest_framework.routers import DefaultRouter

from apps.users.api.viewsets.teacher_viewset import TeacherViewSet
from apps.users.api.viewsets.student_viewset import StudentViewSet


router = DefaultRouter()

router.register(r'teachers', TeacherViewSet, basename="teachers")
router.register(r'students', StudentViewSet, basename="students")


urlpatterns = router.urls
