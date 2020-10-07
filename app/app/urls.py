from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/exercise/', include('exercise.urls')),
    path('api/workout/', include('workout.urls')),
    path('api/routine/', include('routine.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# this creates the path to access to the media without the need for creating a new server for
# hosting our files
