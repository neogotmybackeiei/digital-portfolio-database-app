from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('works.urls')),
]

# Serve media files in all environments. In production, WhiteNoise handles
# the actual file serving via wsgi.py; this route ensures Django can resolve
# and reverse media URLs (e.g. in templates) regardless of DEBUG mode.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
