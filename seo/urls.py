from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projects import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('frontend.urls')),
    path('projects/', include('projects.urls')),
    path('api/accounts/', include('accounts.urls')),

    path('activities/', include('activities.urls')),
    path('api/clients/', include('clients.urls')), 
    path('api/projects/', include('projects.urls')),  
    path("api/run-rank-check/", views.run_rank_check),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)