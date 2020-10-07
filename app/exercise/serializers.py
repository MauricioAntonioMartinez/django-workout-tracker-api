from core.models import Exercise, Serie, Set, Workout
from rest_framework import serializers


class ExerciseSerializer(serializers.ModelSerializer):
    difficulty_name = serializers.SerializerMethodField(
        method_name='get_difficulty_name')
    body_part_name = serializers.SerializerMethodField(
        method_name='get_body_part_name'
    )

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'difficulty', 'notes',
                  'body_part', 'difficulty_name',  'body_part_name')
        read_only_fields = ('id', 'difficulty_name', 'body_part_name')
        # extra_kwargs = {
        #     'difficulty': {'write_only': True},
        # }

    def get_difficulty_name(self, instance):
        return instance.get_difficulty_display()

    def get_body_part_name(self, instance):
        return instance.get_body_part_display()


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'name')
#         read_only_fields = ('id',)


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name')
#         read_only_fields = ('id',)


# class RecipeSerializer(serializers.ModelSerializer):
#     # ingredients = [1,2,3,4,5,6] => Ingredient[]
#     ingredients = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Ingredient.objects.all()
#     )
#     # list the objects by the primary key specified in the fields
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )

#     class Meta:
#         model = Recipe
#         fields = ('id', 'title', 'time_minutes',
#                   'ingredients', 'link', 'tags', 'price',)
#         read_only_fields = ('id',)


# class RecipeDetailSerializer(RecipeSerializer):
#     """Serialize a recipe detail
#     """
#     # this overrides the fields ingredients to not only accept
#     # ids for a given ingredients or tags,
#     # serialize all the ingredients and tags fields
#     ingredients = IngredientSerializer(many=True, read_only=True)
#     # this thing populates the ingredients
#     tags = TagSerializer(many=True, read_only=True)


# class RecipeImageSerializer(serializers.ModelSerializer):
#     """Serializer to uploading images to recipes
#     """
#     class Meta:
#         model = Recipe
#         fields = ('id', 'image')
#         read_only_fields = ('id',)
