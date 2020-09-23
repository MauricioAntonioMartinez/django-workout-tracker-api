from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Tag
from exercise.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APIClient

TAGS_URL = reverse('exercise:tag-list')


class PublicTagsApiTest(TestCase):
    """Test the public available tags API
    """

    def setUp(self):
        self.client = APIClient()

    def def_login_required(self):
        """Test that login is required for retriving tags
        """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivedTagsApiTest(TestCase):
    """Test the authorized user tags API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            '1234123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """Test retriving tags
        """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        # we are now serializing all the tags
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are 
        """
        user2 = get_user_model().objects.create_user(
            'other@other.com',
            '12312312'
        )
        Tag.objects.create(user=user2, name='Fruit')
        tag = Tag.objects.create(user=self.user, name='Other')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successfull(self):
        """Test creating a new tag
        """
        payload = {
            "name": "test tag"
        }
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag
        """
        payload = {
            "name": ""
        }
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
