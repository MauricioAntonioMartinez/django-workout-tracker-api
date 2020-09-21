from rest_framework import exceptions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import AuthSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the db
    """
    serializer_class = UserSerializer


class CreateAuthView(ObtainAuthToken):
    """Create a new token for user
    """
    serializer_class = AuthSerializer
    # rendered_classes = api_settings.DEFAULT_RENDERER_CLASSES
