from rest_framework.routers import DefaultRouter

from apps.users.api.viewsets.user_viewset import UserViewSet
from apps.users.api.viewsets.general_viewset import CareerViewSet


router = DefaultRouter()

router.register(r'users', UserViewSet, basename="users")
router.register(r'careers', CareerViewSet, basename="careers")

urlpatterns = router.urls
