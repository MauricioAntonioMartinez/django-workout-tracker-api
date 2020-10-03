from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExerciseSearch, ExerciseViewSet

router = DefaultRouter()  # automatic generate urls
router.register('exercise', ExerciseViewSet)
router.register('', ExerciseSearch)

#app_name = 'exercises'

urlpatterns = router.urls
# # all the generated url are registered
