
from rest_framework.routers import DefaultRouter

from .views import RoutineViewSet

router = DefaultRouter()

router.register('', RoutineViewSet)

app_name = 'routine'


urlpatterns = router.urls
