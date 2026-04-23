import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

django_app = get_wsgi_application()

# Wrap the Django WSGI app with WhiteNoise so that media files stored in
# MEDIA_ROOT (/app/media on the persistent volume) are served at /media/
# in production without requiring DEBUG=True.
from django.conf import settings
application = WhiteNoise(django_app, root=settings.STATIC_ROOT)
application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)

