from core.models import Ingredient, Recipe, Tag
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (IngredientSerializer, RecipeDetailSerializer,
                          RecipeSerializer, TagSerializer)


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


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrive the recipes for the authenticated user
        """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return apropiate serializer class
        """
        # the retrive is adding the /<pk> to the endpoint
        print('ACTION !!!', self.action)
        # depending of the action the serializer may change
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class  # the normal serializer class

    def perform_create(self, serializer):
        """Create a new recipe
        """
        # when saving a new object instance
        serializer.save(user=self.request.user)
