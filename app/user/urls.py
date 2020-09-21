from django.urls import path

from .views import CreateAuthView, CreateUserView

app_name = 'user'


urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateAuthView.as_view(), name='token'),
]
