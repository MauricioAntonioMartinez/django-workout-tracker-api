from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SerieViewSet, SetViewSet, WorkoutViewSet

router = DefaultRouter()

router.register('set', SetViewSet)
router.register('serie', SerieViewSet)
router.register('', WorkoutViewSet)

app_name = 'workout'

urlpatterns = router.urls
