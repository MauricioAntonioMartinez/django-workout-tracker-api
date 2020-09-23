from core.models import Ingredient, Tag
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import IngredientSerializer, TagSerializer


# the mixins adds functionality to the view set
class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """Resturn objects for the current authenticated user only
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag
        """
        serializer.save(user=self.request.user)
        # this allow us to modify the serializer before is performed


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                        mixins.CreateModelMixin):

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
