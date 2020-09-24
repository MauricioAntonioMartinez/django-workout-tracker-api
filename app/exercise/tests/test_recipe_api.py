from core.models import Ingredient, Recipe, Tag
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from exercise.serializers import RecipeDetailSerializer, RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse('exercise:recipe-list')

# /api/recipe/recipes
# /api/recipe/recipes/1/


def detail_url(recipe_id):
    """Return recipe detail URL
    """
    return reverse('exercise:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    """Create and return a sample recipe
    """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)  # create or update existing
    # fields in a dictionary
    return Recipe.objects.create(user=user, **defaults)


def sample_tag(user, name='Main Tag'):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Some Ingredient'):
    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API tests
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            '123123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Test retriving list of recipes
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retriving recipes for user
        """
        user2 = get_user_model().objects.create_user(
            'sadf@sadfa.com',
            'asdfasdf'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail
        """
        recipe = sample_recipe(user=self.user)
        # adding a tag to the current recipe
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def rest_create_basic_recipe(self):
        """Test creating recipe
        """
        payload = {
            "title": "Salad",
            "time_minutes": 10,
            "price": 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        is_equal = all([self.assertEqual(payload[k], getattr(recipe, k))
                        for k in payload.keys()])
        self.assertTrue(is_equal)

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags
        """
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')
        payload = {
            'title': 'Avocado line',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 50,
            'price': 20.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()  # retreive all the tags not the ids
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)  # useful to check list,querysets
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """Test create a recipe with ingredients
        """
        ing1 = sample_ingredient(user=self.user, name='Salt')
        ing2 = sample_ingredient(user=self.user, name='Tomato')

        payload = {
            'title': 'Salad',
            'time_minutes': 10,
            'price': 10.00,
            'ingredients': [ing1.id, ing2.id]
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)

        self.assertIn(ing1, ingredients)
        self.assertIn(ing2, ingredients)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Curry')

        payload = {
            'title': 'Chicken',
            'tags': [new_tag.id]
        }
        self.client.patch(detail_url(recipe.id), payload)
        recipe.refresh_from_db()  # fetches again

        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """Teste updating a recipe with put
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            "title": "Spaghetti Carbonara",
            'time_minutes': 25,
            'price': 5.00
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        self.assertEqual(recipe.tags.count(), 0)
