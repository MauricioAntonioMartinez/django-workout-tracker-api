import datetime as dt
from collections.abc import Iterable

from core.model.exercise import Exercise
from core.model.workout import Workout,Set,Serie
from core.models import ExpiringTokenAuthentication
from rest_framework import filters, generics, mixins, status, viewsets

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ExerciseSerializer


class Auth(viewsets.ModelViewSet):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExerciseSearch(generics.ListAPIView, viewsets.ViewSet):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    orderin_fields = ['created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ExerciseViewSet(Auth):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()
    body_parts = Exercise._meta.get_field('body_part').choices
    difficulties = Exercise._meta.get_field('difficulty').choices

    @action(methods=['get'], url_path='details', detail=False)
    def get_exercise_details(self, request):
        return Response({"body_parts": self.body_parts,
                         "difficuties": self.difficulties}, status.HTTP_200_OK)

    def get_queryset(self):
        body_part = self.request.query_params.get('body_part')
        difficulty = self.request.query_params.get('difficulty')
        queryset = self.queryset.filter(user=self.request.user)
        if body_part:
            bp = [bd[0] for bd in self.body_parts if bd[1] == body_part][0]
            queryset = queryset.filter(body_part=bp)
        if difficulty:
            df = [df[0] for df in self.difficulties if df[1] == difficulty][0]
            queryset = queryset.filter(difficulty=df)
        return queryset

    # class BaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
    #                   mixins.CreateModelMixin):
    #     authentication_classes = (TokenAuthentication, )
    #     permission_classes = (IsAuthenticated,)

    #     def get_queryset(self):
    #         """Resturn objects for the current authenticated user only
    #         """
    #         assigned_only = bool(
    #             int(self.request.query_params.get('assigned_only', 0)))
    #         # all the params are string therefor converts to an int and the into
    #         # a boolean
    #         queryset = self.queryset
    #         if assigned_only:
    #             queryset = queryset.filter(recipe__isnull=False).distinct()
    #             # not return what is not assigned to a recipe
    #         return queryset.filter(user=self.request.user).order_by('-name')

    #     def perform_create(self, serializer):  # before the serializer is saved
    #         serializer.save(user=self.request.user)

    #     # the mixins adds functionality to the view set

    # class TagViewSet(BaseViewSet):
    #     """Manage tags in the database
    #     """
    #     queryset = Tag.objects.all()
    #     serializer_class = TagSerializer

    # class IngredientViewSet(BaseViewSet):
    #     serializer_class = IngredientSerializer
    #     queryset = Ingredient.objects.all()

    # class RecipeViewSet(viewsets.ModelViewSet):
    #     """Manage recipes in the database
    #     """
    #     serializer_class = RecipeSerializer
    #     queryset = Recipe.objects.all()
    #     authentication_classes = (TokenAuthentication,)
    #     permission_classes = (IsAuthenticated,)

    #     def _params_to_ints(self, qs):
    #         """Convert a list of string IDs to a list of integers
    #         """
    #         return [int(str_id) for str_id in qs.split(',')]

    #     def get_queryset(self):
    #         """Retrive the recipes for the authenticated user
    #         """
    #         tags = self.request.query_params.get('tags')
    #         ingredients = self.request.query_params.get('ingredients')
    #         query_set = self.queryset.filter(user=self.request.user)

    #         if tags:
    #             tags_ids = self._params_to_ints(tags)
    #             query_set = query_set.filter(tags__id__in=tags_ids)
    #             # provides function to filter by a field in the tags
    #         if ingredients:
    #             ingredient_ids = self._params_to_ints(ingredients)
    #             query_set = query_set.filter(ingredients__id__in=ingredient_ids)

    #         return query_set

    #     def get_serializer_class(self):
    #         """Return apropiate serializer class
    #         """
    #         # the retrive is adding the /<pk> to the endpoint
    #         print('ACTION !!!', self.action)
    #         # depending of the action the serializer may change
    #         if self.action == 'retrieve':
    #             return RecipeDetailSerializer

    #         if self.action == 'upload_image':  # the action if created another one
    #             return RecipeImageSerializer  # has the same name as the url path
    #         return self.serializer_class  # the normal serializer class

    #     def perform_create(self, serializer):
    #         """Create a new recipe
    #         """
    #         # when saving a new object instance
    #         serializer.save(user=self.request.user)

    #     @action(methods=['POST'], detail=True, url_path='upload-image')
    #     # this action will be for the specific like /recipes/1
    #     # path name at the end will be /recipes/1/upload-image
    #     def upload_image(self, request, pk=None):
    #         """Upload an image to a recipe
    #         """
    #         recipe = self.get_object()  # this will be you access to the
    #         # object that is access via the id
    #         serializer = self.get_serializer(
    #             recipe,
    #             data=request.data
    #         )

    #         if serializer.is_valid():
    #             serializer.save()  # saves to the database
    #             return Response(
    #                 serializer.data,
    #                 status=status.HTTP_200_OK
    #             )
    #         return Response(
    #             serializer.errors,  # return the errors by the serializer
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
