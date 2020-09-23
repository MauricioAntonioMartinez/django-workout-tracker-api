from core.models import Ingredient, Tag
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import IngredientSerializer, TagSerializer


class BaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Resturn objects for the current authenticated user only
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):  # before the serializer is saved
        serializer.save(user=self.request.user)

    # the mixins adds functionality to the view set


class TagViewSet(BaseViewSet):
    """Manage tags in the database
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
