from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search.urls')),  # Homepage only
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('interaction/', include('interaction.urls')),
]

# Media files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)