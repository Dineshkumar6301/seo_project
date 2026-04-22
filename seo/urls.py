from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('frontend.urls')),          # UI
    path('projects/', include('projects.urls')),
    path('api/accounts/', include('accounts.urls')),  # API

    path('activities/', include('activities.urls')),  # UI + API
    path('api/clients/', include('clients.urls')),  # API
    path('api/projects/', include('projects.urls')),  # API
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
