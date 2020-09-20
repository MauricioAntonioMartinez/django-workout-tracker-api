from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Create a new user with the email
        """
        email = 'test@test.com'
        password = '1234567'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for the new user normalized
        """
        email = 'aaa@TTTT.COM'
        user = get_user_model().objects.create_user(
            email=email, password='12121212')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating a user with no email
        """
        with self.assertRaises(ValueError):
            # anything should rise an error
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_a_super_user(self):
        user = get_user_model().objects.create_superuser('test@test.com', '123134')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
