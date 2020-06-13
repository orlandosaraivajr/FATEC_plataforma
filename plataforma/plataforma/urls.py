from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from plataforma import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
