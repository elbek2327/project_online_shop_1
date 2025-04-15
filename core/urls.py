

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('shop/', include('shop.urls'), name='shop'),
                  path('users/', include('users.urls'), name='users'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)