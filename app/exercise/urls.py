from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet

router = DefaultRouter()  # automatic generate urls
router.register('tags', TagViewSet)
router.register('ingredient', IngredientViewSet)

app_name = 'exercise'

urlpatterns = [path('', include(router.urls))]
# all the generated url are registered
