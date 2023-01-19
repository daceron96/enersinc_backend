from rest_framework.routers import DefaultRouter
from .api import PersonViewSet

router = DefaultRouter()

router.register(r'person', PersonViewSet, basename='persons')

urlpatterns = router.urls
